import logging

import aiohttp_jinja2
from aiohttp.client_exceptions import ClientConnectionError, ClientConnectorError, ClientResponseError
from aiohttp.web import HTTPFound, RouteTableDef, json_response
from sdc.crypto.encrypter import encrypt
from structlog import wrap_logger
from aiohttp_session import get_session

from . import (
    BAD_CODE_MSG, BAD_RESPONSE_MSG, INVALID_CODE_MSG, NOT_AUTHORIZED_MSG, VERSION, ADDRESS_CHECK_MSG)
from .case import get_case, post_case_event
from .sample import get_sample_attributes
from .exceptions import InactiveCaseError, InvalidIACError
from .eq import EqPayloadConstructor
from .flash import flash
from .exceptions import InvalidEqPayLoad


logger = wrap_logger(logging.getLogger("respondent-home"))
routes = RouteTableDef()


@routes.view('/info', use_prefix=False)
class Info:

    async def get(self, request):
        info = {
            "name": 'respondent-home-ui',
            "version": VERSION,
        }
        if 'check' in request.query:
            info["ready"] = await request.app.check_services()
        return json_response(info)


@routes.view('/')
class Index:

    def __init__(self):
        self.iac = None
        self.request = None
        self._sample_unit_id = None

    @property
    def client_ip(self):
        if not hasattr(self, '_client_ip'):
            self._client_ip = self.request.headers.get("X-Forwarded-For")
        return self._client_ip

    @property
    def iac_url(self):
        return f"{self.request.app['IAC_URL']}/iacs/{self.iac}"

    @staticmethod
    def join_iac(data, expected_length=12):
        combined = "".join([v.lower() for v in data.values()][:3])
        if len(combined) < expected_length:
            raise TypeError
        return combined

    @staticmethod
    def validate_case(case_json):
        if not case_json.get("active", False):
            raise InactiveCaseError

    def redirect(self):
        raise HTTPFound(self.request.app.router['Index:get'].url_for())

    async def get_iac_details(self):
        logger.debug(f"Making GET request to {self.iac_url}", iac=self.iac, client_ip=self.client_ip)
        try:
            async with self.request.app.http_session_pool.get(self.iac_url, auth=self.request.app["IAC_AUTH"]) as resp:
                logger.debug("Received response from IAC", iac=self.iac, status_code=resp.status)

                try:
                    resp.raise_for_status()
                except ClientResponseError as ex:
                    if resp.status == 404:
                        raise InvalidIACError
                    elif resp.status in (401, 403):
                        logger.info("Unauthorized access to IAC service attempted", client_ip=self.client_ip)
                        flash(self.request, NOT_AUTHORIZED_MSG)
                        return self.redirect()
                    elif 400 <= resp.status < 500:
                        logger.warn(
                            "Client error when accessing IAC service",
                            client_ip=self.client_ip,
                            status=resp.status,
                        )
                        flash(self.request, BAD_RESPONSE_MSG)
                        return self.redirect()
                    else:
                        logger.error("Error in response", url=resp.url, status_code=resp.status)
                        raise ex
                else:
                    return await resp.json()
        except (ClientConnectionError, ClientConnectorError) as ex:
            logger.error("Client failed to connect to iac service", client_ip=self.client_ip)
            raise ex

    @aiohttp_jinja2.template('index.html')
    async def get(self, _):
        return {}

    @aiohttp_jinja2.template('index.html')
    async def post(self, request):
        """
        Forward to Address confirmation
        :param request:
        :return: address confirmation view
        """

        self.request = request
        data = await self.request.post()

        try:
            self.iac = self.join_iac(data)
        except TypeError:
            logger.warn("Attempt to use a malformed access code", client_ip=self.client_ip)
            flash(self.request, BAD_CODE_MSG)
            return self.redirect()

        try:
            iac_json = await self.get_iac_details()
        except InvalidIACError:
            logger.info("Attempt to use an invalid access code", client_ip=self.client_ip)
            flash(self.request, INVALID_CODE_MSG)
            return aiohttp_jinja2.render_template("index.html", self.request, {}, status=202)

        # TODO: case is active, will need to look at for UACs handed out in field but not associated with address
        self.validate_case(iac_json)

        try:
            case_id = iac_json["caseId"]
        except KeyError:
            logger.error('caseId missing from IAC response', client_ip=self.client_ip)
            flash(self.request, BAD_RESPONSE_MSG)
            return {}

        case = await get_case(case_id, self.request.app)

        try:
            self._sample_unit_id = case["sampleUnitId"]
        except KeyError:
            raise InvalidEqPayLoad(f"No sample unit id for case {self._case_id}")

        sample_attr = await get_sample_attributes(self._sample_unit_id, self.request.app)

        try:
            attributes = sample_attr["attributes"]
        except KeyError:
            raise InvalidEqPayLoad(f"Could not retrieve attributes for case {self._case_id}")

        logger.debug("Address Conformation displayed", client_ip=self.client_ip)
        session = await get_session(request)
        session["attributes"] = attributes
        session["case"] = case
        session["iac"] = self.iac
        return aiohttp_jinja2.render_template("address-confirmation.html", self.request, attributes)


@routes.view('/address-confirmation')
class AddressConfirmation:

    def __init__(self):
        self.request = None

    @property
    def client_ip(self):
        if not hasattr(self, '_client_ip'):
            self._client_ip = self.request.headers.get("X-Forwarded-For")
        return self._client_ip

    @aiohttp_jinja2.template('address-confirmation.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        self.request = request
        session = await get_session(request)

        data = await self.request.post()

        try:
            attributes = session["attributes"]
            case = session["case"]
            iac = session["iac"]
        except KeyError:
            return aiohttp_jinja2.render_template("index.html", self.request, {}, status=401)

        try:
            address_confirmation = data["address-check-answer"]
        except KeyError:
            logger.warn("Address confirmation error", client_ip=self.client_ip)
            flash(self.request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'Yes':
            # Correct address flow
            app = self.request.app

            eq_payload = await EqPayloadConstructor(case, attributes, app, iac).build()

            token = encrypt(eq_payload, key_store=self.request.app['key_store'], key_purpose="authentication")

            description = f"Census Instrument launched for case {case['id']}"
            await post_case_event(case['id'], 'EQ_LAUNCH', description, self.request.app)

            logger.info('Redirecting to eQ', client_ip=self.client_ip)
            raise HTTPFound(f"{self.request.app['EQ_URL']}/session?token={token}")

        elif address_confirmation == 'No':
            # TODO: Form to enter address and deal with incorrect address
            pass
        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self.client_ip)
            flash(self.request, ADDRESS_CHECK_MSG)
            return attributes


@routes.view('/cookies-privacy')
class CookiesPrivacy:
    @aiohttp_jinja2.template('cookies-privacy.html')
    async def get(self, _):
        return {}


@routes.view('/contact-us')
class ContactUs:
    @aiohttp_jinja2.template('contact-us.html')
    async def get(self, _):
        return {}
