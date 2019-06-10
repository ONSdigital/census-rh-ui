import logging

import aiohttp_jinja2
from aiohttp.client_exceptions import ClientConnectionError, ClientConnectorError, ClientResponseError
from aiohttp.web import HTTPFound, RouteTableDef, json_response
from sdc.crypto.encrypter import encrypt
from structlog import wrap_logger
from aiohttp_session import get_session

from . import (
    BAD_CODE_MSG, BAD_RESPONSE_MSG, INVALID_CODE_MSG, NOT_AUTHORIZED_MSG, VERSION, ADDRESS_CHECK_MSG, ADDRESS_EDIT_MSG,
    SESSION_TIMEOUT_MSG, WEBCHAT_MISSING_NAME_MSG, WEBCHAT_MISSING_EMAIL_MSG, WEBCHAT_MISSING_LANGUAGE_MSG, WEBCHAT_MISSING_QUERY_MSG)
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

    def check_session(self):
        if self._request.cookies.get('RH_SESSION') is None:
            logger.warn("Session timed out", client_ip=self._client_ip)
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['Index:get'].url_for())

    async def call_questionnaire(self, case, attributes, app):
        eq_payload = await EqPayloadConstructor(case, attributes, app).build()

        token = encrypt(eq_payload, key_store=app['key_store'], key_purpose="authentication")

        #    description = f"Census Instrument launched for case {case['id']}"
        #    await post_case_event(case['id'], 'EQ_LAUNCH', description, app)

        logger.debug('Redirecting to eQ', client_ip=self._client_ip)
        raise HTTPFound(f"{app['EQ_URL']}/session?token={token}")


@routes.view('/')
class Index(View):

    def __init__(self):
        self._iac = None
        self._sample_unit_id = None
        super().__init__()

    @property
    def _rhsvc_url(self):
        return f"{self._request.app['RHSVC_URL']}/uacs/{self._iac}"

    @staticmethod
    def join_iac(data, expected_length=16):
        combined = "".join([v.lower() for v in data.values()][:4])
        if len(combined) < expected_length:
            raise TypeError
        return combined

    @staticmethod
    def validate_case(case_json):
        if not case_json.get("active", False):
            raise InactiveCaseError
        if not case_json.get("caseStatus", None) == "OK":
            raise InvalidEqPayLoad("caseStatus is not OK")

    def redirect(self):
        raise HTTPFound(self._request.app.router['Index:get'].url_for())

    async def get_iac_details(self):
        logger.debug(f"Making GET request to {self._rhsvc_url}", client_ip=self._client_ip)
        try:
            async with self._request.app.http_session_pool.get(self._rhsvc_url,
                                                               auth=self._request.app["RHSVC_AUTH"]) as resp:
                logger.debug("Received response from RH service", status_code=resp.status)

                try:
                    resp.raise_for_status()
                except ClientResponseError as ex:
                    if resp.status == 404:
                        raise InvalidIACError
                    elif resp.status in (401, 403):
                        logger.warn("Unauthorized access to RH service attempted", client_ip=self._client_ip)
                        flash(self._request, NOT_AUTHORIZED_MSG)
                        return self.redirect()
                    elif 400 <= resp.status < 500:
                        logger.warn(
                            "Client error when accessing RH service",
                            client_ip=self._client_ip,
                            status=resp.status,
                        )
                        flash(self._request, BAD_RESPONSE_MSG)
                        return self.redirect()
                    else:
                        logger.error("Error in response", url=resp.url, status_code=resp.status)
                        raise ex
                else:
                    return await resp.json()
        except (ClientConnectionError, ClientConnectorError) as ex:
            logger.error("Client failed to connect to RH service", client_ip=self._client_ip)
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
        self._request = request
        data = await self._request.post()

        try:
            self._iac = self.join_iac(data)
        except TypeError:
            logger.warn("Attempt to use a malformed access code", client_ip=self._client_ip)
            flash(self._request, BAD_CODE_MSG)
            return self.redirect()

        try:
            uac_json = await self.get_iac_details()
        except InvalidIACError:
            logger.warn("Attempt to use an invalid access code", client_ip=self._client_ip)
            flash(self._request, INVALID_CODE_MSG)
            return aiohttp_jinja2.render_template("index.html", self._request, {}, status=202)

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


@routes.view('/address-confirmation')
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


@routes.view('/address-edit')
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

@routes.view('/webchat/chat')
class WebChatWindow:
    @aiohttp_jinja2.template('webchat-window.html')
    async def get(self, _):
        return {}

@routes.view('/webchat')
class WebChat(View):

    @staticmethod
    def validate_form(data):

        form_return = []

        if data.get('screen_name') == '':
            form_return.append('name-missing')

        if data.get('email') == '':
            form_return.append('email-missing')

        if not(data.get('language')):
            form_return.append('language-missing')

        if not(data.get('query')):
            form_return.append('query-missing')

        return form_return

    def redirect(self, data):
        raise HTTPFound(self._request.app.router['WebChat:post'].url_for(), body=data)

    @aiohttp_jinja2.template('webchat-form.html')
    async def get(self, _):
        return {}

    @aiohttp_jinja2.template('webchat-form.html')
    async def post(self, request):

        data = await request.post()
        self._request = request

        try:
            form_return = self.validate_form(data)

            if form_return != []:
                raise TypeError(form_return)

        except TypeError:
            logger.warn("Form submission error", client_ip=self._client_ip)
            if any("name-missing" in s for s in form_return):
                flash(self._request, WEBCHAT_MISSING_NAME_MSG)
            if any("email-missing" in s for s in form_return):
                flash(self._request, WEBCHAT_MISSING_EMAIL_MSG)
            if any("language-missing" in s for s in form_return):
                flash(self._request, WEBCHAT_MISSING_LANGUAGE_MSG)
            if any("query-missing" in s for s in form_return):
                flash(self._request, WEBCHAT_MISSING_QUERY_MSG)
            return self.redirect(data)

        response = aiohttp_jinja2.render_template("webchat-window.html", self._request, data)
        response.headers['Content-Language'] = 'en'

        return response
