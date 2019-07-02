import logging

import aiohttp_jinja2
from aiohttp.client_exceptions import ClientConnectionError, ClientConnectorError, ClientResponseError
from aiohttp.web import HTTPFound, RouteTableDef, json_response
from sdc.crypto.encrypter import encrypt
from structlog import wrap_logger
from aiohttp_session import get_session

from . import (
    BAD_CODE_MSG, INVALID_CODE_MSG, VERSION, ADDRESS_CHECK_MSG, ADDRESS_EDIT_MSG, SESSION_TIMEOUT_MSG)
from .exceptions import InactiveCaseError
from .eq import EqPayloadConstructor
from .flash import flash
from .exceptions import InvalidEqPayLoad
from collections import namedtuple

logger = wrap_logger(logging.getLogger("respondent-home"))
Request = namedtuple("Request", ["method", "url", "auth", "json", "func"])
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


class View:
    """
    Common base class for views
    """

    def __init__(self):
        self._request = None
        self._client_ip = None

    @property
    def client_ip(self):
        if not hasattr(self, '_client_ip'):
            self._client_ip = self._request.headers.get("X-Forwarded-For")
        return self._client_ip

    @property
    def _rhsvc_url_surveylaunched(self):
        return f"{self._request.app['RHSVC_URL']}/surveyLaunched"

    @staticmethod
    def _handle_response(response):
        try:
            response.raise_for_status()
        except ClientResponseError as ex:
            if not ex.status == 404:
                logger.error("Error in response", url=response.url, status_code=response.status)
            raise ex
        else:
            logger.debug("Successfully connected to service", url=str(response.url))

    def check_session(self):
        if self._request.cookies.get('RH_SESSION') is None:
            logger.warn("Session timed out", client_ip=self._client_ip)
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['Index:get'].url_for())

    def redirect(self):
        raise HTTPFound(self._request.app.router['Index:get'].url_for())

    async def _make_request(self, request: Request):
        method, url, auth, json, func = request
        logger.debug(f"Making {method} request to {url} and handling with {func.__name__}")
        try:
            async with self._request.app.http_session_pool.request(method, url, auth=auth, json=json) as resp:
                func(resp)
                # Not all end points return JSON with content type header set.
                # Turn off content type header checking setting parameter to none, empty return body will return none.
                return await resp.json(content_type=None)
        except (ClientConnectionError, ClientConnectorError) as ex:
            logger.error("Client failed to connect", url=url, client_ip=self._client_ip)
            raise ex

    async def call_questionnaire(self, case, attributes, app):
        eq_payload = await EqPayloadConstructor(case, attributes, app).build()

        token = encrypt(eq_payload, key_store=app['key_store'], key_purpose="authentication")

        await self.get_surveylaunched(case)

        logger.debug('Redirecting to eQ', client_ip=self._client_ip)
        raise HTTPFound(f"{app['EQ_URL']}/session?token={token}")

    async def get_surveylaunched(self, case):

        json = {'questionnaireId': case['questionnaireId'], 'caseId': case['caseId']}
        return await self._make_request(
            Request("POST", self._rhsvc_url_surveylaunched, self._request.app["RHSVC_AUTH"],
                    json, self._handle_response))


@routes.view('/start/')
class Index(View):

    def __init__(self):
        self._uac = None
        self._sample_unit_id = None
        super().__init__()

    @property
    def _rhsvc_url(self):
        return f"{self._request.app['RHSVC_URL']}/uacs/{self._uac}"

    @staticmethod
    def join_uac(data, expected_length=16):
        combined = "".join([v.lower() for v in data.values()][:4])
        if len(combined) < expected_length:
            raise TypeError
        return combined

    @staticmethod
    def validate_case(case_json):
        if not case_json.get("active", False):
            raise InactiveCaseError
        if not case_json.get("caseStatus", None) == "OK":
            raise InvalidEqPayLoad("CaseStatus is not OK")

    async def get_uac_details(self):
        logger.debug(f"Making GET request to {self._rhsvc_url}", client_ip=self._client_ip)
        return await self._make_request(
            Request("GET", self._rhsvc_url, self._request.app["RHSVC_AUTH"], None, self._handle_response))

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
        self._request = request
        data = await self._request.post()

        try:
            self._uac = self.join_uac(data)
        except TypeError:
            logger.warn("Attempt to use a malformed access code", client_ip=self._client_ip)
            flash(self._request, BAD_CODE_MSG)
            return self.redirect()

        try:
            uac_json = await self.get_uac_details()
        except ClientResponseError as ex:
            if ex.status == 404:
                logger.warn("Attempt to use an invalid access code", client_ip=self._client_ip)
                flash(self._request, INVALID_CODE_MSG)
                return aiohttp_jinja2.render_template("index.html", self._request, {}, status=202)
            else:
                raise ex

        # TODO: case is active, will need to look at for UACs handed out in field but not associated with address
        self.validate_case(uac_json)

        try:
            attributes = uac_json["address"]
        except KeyError:
            raise InvalidEqPayLoad("Could not retrieve address details")

        # SOMEHOW NEED TO MAP ADDRESS DETAILS TO ATTRIBUTES SO CAN BE DISPLAYED

        logger.debug("Address Confirmation displayed", client_ip=self._client_ip)
        session = await get_session(request)
        session["attributes"] = attributes
        session["case"] = uac_json

        return aiohttp_jinja2.render_template("address-confirmation.html", self._request, attributes)


@routes.view('/start/address-confirmation')
class AddressConfirmation(View):

    @aiohttp_jinja2.template('address-confirmation.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        data = await request.post()
        self._request = request

        self.check_session()
        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['Index:get'].url_for())

        try:
            address_confirmation = data["address-check-answer"]
        except KeyError:
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'Yes':
            # Correct address flow
            await self.call_questionnaire(case, attributes, request.app)

        elif address_confirmation == 'No':
            return aiohttp_jinja2.render_template("address-edit.html", request, attributes)

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@routes.view('/start/address-edit')
class AddressEdit(View):

    def get_address_details(self, data: dict, attributes: dict):
        """
        Replace any changed address details in attributes to be sent to EQ
        :param data: Changed address details
        :param attributes: attributes to be sent
        :return: attributes with changed address
        """

        if not data["address-line-1"].strip():
            raise InvalidEqPayLoad(f"Mandatory address field not present{self._client_ip}")
        else:
            attributes["addressLine1"] = data["address-line-1"].strip()
            attributes["addressLine2"] = data["address-line-2"].strip()
            attributes["addressLine3"] = data["address-line-3"].strip()
            attributes["townName"] = data["town_name"].strip()
            attributes["postcode"] = data["postcode"].strip()

        return attributes

    @aiohttp_jinja2.template('address-edit.html')
    async def post(self, request):
        """
        Address Edit flow. Edited address details.
        """
        data = await request.post()
        self._request = request

        self.check_session()
        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['Index:get'].url_for())

        try:
            attributes = self.get_address_details(data, attributes)
        except InvalidEqPayLoad:
            logger.info("Error editing address, mandatory field required by EQ", client_ip=self._client_ip)
            flash(request, ADDRESS_EDIT_MSG)
            return attributes

        await self.call_questionnaire(case, attributes, request.app)


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


@routes.view('/onlinehelp')
class OnlineHelp:
    @aiohttp_jinja2.template('onlinehelp.html')
    async def get(self, _):
        return {}


@routes.view('/request-code/enter-mobile')
class RequestCodeEnterMobile(View):
    @aiohttp_jinja2.template('mobile-enter-number.html')
    async def get(self, _):
        return {}


@routes.view('/request-code/confirm-mobile')
class RequestCodeConfirmMobile(View):
    @aiohttp_jinja2.template('mobile-confirm-number.html')
    async def post(self, request):

        data = await request.post()
        self._request = request

        self.check_session()
        session = await get_session(request)
        try:
            attributes = session["attributes"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['Index:get'].url_for())

        try:
            mobile_confirmation = data["mobile-confirmation"]
        except KeyError:
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if mobile_confirmation == 'Yes':
            # await self.call_questionnaire(case, attributes, request.app)
            raise HTTPFound(self._request.app.router['RequestCodeCodeSent:post'].url_for())

        elif mobile_confirmation == 'No':
            return aiohttp_jinja2.render_template("address-edit.html", request, attributes)

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@routes.view('/request-code/code-sent')
class RequestCodeCodeSent(View):
    @aiohttp_jinja2.template('mobile-code-sent.html')
    async def post(self, _):
        return {}
