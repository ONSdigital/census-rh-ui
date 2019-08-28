import logging

import aiohttp_jinja2
import re
import ast
from aiohttp.client_exceptions import ClientConnectionError, ClientConnectorError, ClientResponseError, ClientError
from aiohttp.web import HTTPFound, RouteTableDef, json_response
from sdc.crypto.encrypter import encrypt
from structlog import wrap_logger
from aiohttp_session import get_session
from datetime import datetime, timezone

from . import (
    BAD_CODE_MSG, INVALID_CODE_MSG, VERSION, ADDRESS_CHECK_MSG, ADDRESS_EDIT_MSG,
    SESSION_TIMEOUT_MSG, WEBCHAT_MISSING_NAME_MSG, WEBCHAT_MISSING_COUNTRY_MSG,
    WEBCHAT_MISSING_QUERY_MSG, MOBILE_ENTER_MSG, MOBILE_CHECK_MSG, POSTCODE_INVALID_MSG,
    ADDRESS_SELECT_CHECK_MSG, START_LANGUAGE_OPTION_MSG,
    BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY, ADDRESS_CHECK_MSG_CY, ADDRESS_EDIT_MSG_CY,
    SESSION_TIMEOUT_MSG_CY, WEBCHAT_MISSING_NAME_MSG_CY, WEBCHAT_MISSING_COUNTRY_MSG_CY,
    WEBCHAT_MISSING_QUERY_MSG_CY, MOBILE_ENTER_MSG_CY, MOBILE_CHECK_MSG_CY, POSTCODE_INVALID_MSG_CY,
    ADDRESS_SELECT_CHECK_MSG_CY, START_LANGUAGE_OPTION_MSG_CY)
from .exceptions import InactiveCaseError
from .eq import EqPayloadConstructor
from .flash import flash
from .exceptions import InvalidEqPayLoad
from .security import remember, check_permission
from collections import namedtuple

logger = wrap_logger(logging.getLogger("respondent-home"))
Request = namedtuple("Request", ["method", "url", "auth", "json", "func", "response"])
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

    @property
    def _webchat_service_url(self):
        return self._request.app['WEBCHAT_SVC_URL']

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

    async def _make_request(self, request: Request):
        method, url, auth, json, func, response = request
        logger.debug(f"Making {method} request to {url} and handling with {func.__name__}")
        try:
            async with self._request.app.http_session_pool.request(method, url, auth=auth, json=json, ssl=False) as resp:
                func(resp)
                if response == "json":
                    return await resp.json()
                else:
                    return None
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
                    json, self._handle_response, None))


class Start(View):

    def __init__(self):
        self._uac = None
        self._sample_unit_id = None
        super().__init__()

    @property
    def _rhsvc_url(self):
        return f"{self._request.app['RHSVC_URL']}/uacs/{self._uac}"

    @staticmethod
    def join_uac(data, expected_length=16):
        if data.get('uac'):
            combined = data.get('uac').lower().replace(" ", "")
        else:
            combined = ''

        uac_validation_pattern = re.compile(r'^[a-z0-9]{16}$')

        if (len(combined) < expected_length) or not (uac_validation_pattern.fullmatch(combined)):
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
            Request("GET", self._rhsvc_url, self._request.app["RHSVC_AUTH"], None, self._handle_response, "json"))

    @property
    def _rhsvc_modify_address(self):
        return f"{self._request.app['RHSVC_URL']}/cases/"

    async def put_modify_address(self, case, address):
        json = {
            "caseId": case['caseId'],
            "uprn": case['address']['uprn'],
            "addressLine1": address['addressLine1'],
            "addressLine2": address['addressLine2'],
            "addressLine3": address['addressLine3'],
            "townName": address['townName'],
            "postcode": address['postcode']
            }
        return await self._make_request(
            Request("PUT", self._rhsvc_modify_address + case['caseId'] + '/address', self._request.app["RHSVC_AUTH"],
                    json, self._handle_response, None))

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
            attributes["townName"] = data["address-town"].strip()
            attributes["postcode"] = data["address-postcode"].strip()

        return attributes


@routes.view('/start/')
class IndexEN(Start):

    @aiohttp_jinja2.template('index.html')
    async def get(self, _):
        return {'display_region': 'en'}

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
            raise HTTPFound(self._request.app.router['IndexEN:get'].url_for())

        try:
            uac_json = await self.get_uac_details()
        except ClientResponseError as ex:
            if ex.status == 404:
                logger.warn("Attempt to use an invalid access code", client_ip=self._client_ip)
                flash(self._request, INVALID_CODE_MSG)
                return aiohttp_jinja2.render_template("index.html", self._request,
                                                      {'display_region': 'en'}, status=401)
            else:
                raise ex

        await remember(uac_json["caseId"], request)

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

        raise HTTPFound(self._request.app.router['AddressConfirmationEN:get'].url_for())


@routes.view('/dechrau/')
class IndexCY(Start):

    @aiohttp_jinja2.template('index.html')
    async def get(self, _):
        return {'display_region': 'cy', 'locale': 'cy'}

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
            flash(self._request, BAD_CODE_MSG_CY)
            raise HTTPFound(self._request.app.router['IndexCY:get'].url_for())

        try:
            uac_json = await self.get_uac_details()
        except ClientResponseError as ex:
            if ex.status == 404:
                logger.warn("Attempt to use an invalid access code", client_ip=self._client_ip)
                flash(self._request, INVALID_CODE_MSG_CY)
                return aiohttp_jinja2.render_template("index.html", self._request, {'display_region': 'cy',
                                                                                    'locale': 'cy'}, status=401)
            else:
                raise ex

        await remember(uac_json["caseId"], request)

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
        session["attributes"]["display_region"] = 'cy'
        session["attributes"]["locale"] = 'cy'

        raise HTTPFound(self._request.app.router['AddressConfirmationCY:get'].url_for())


@routes.view('/ni/start/')
class IndexNI(Start):

    @aiohttp_jinja2.template('index.html')
    async def get(self, _):
        return {'display_region': 'ni'}

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
            raise HTTPFound(self._request.app.router['IndexNI:get'].url_for())

        try:
            uac_json = await self.get_uac_details()
        except ClientResponseError as ex:
            if ex.status == 404:
                logger.warn("Attempt to use an invalid access code", client_ip=self._client_ip)
                flash(self._request, INVALID_CODE_MSG)
                return aiohttp_jinja2.render_template("index.html", self._request, {'display_region': 'ni'}, status=401)
            else:
                raise ex

        await remember(uac_json["caseId"], request)

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
        session["attributes"]["display_region"] = 'ni'

        raise HTTPFound(self._request.app.router['AddressConfirmationNI:get'].url_for())


@routes.view('/start/address-confirmation')
class AddressConfirmationEN(Start):

    @aiohttp_jinja2.template('address-confirmation.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexEN:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('address-confirmation.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        await check_permission(request)
        self._request = request
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexEN:get'].url_for())

        try:
            address_confirmation = data["address-check-answer"]
        except KeyError:
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'Yes':
            if case['region'] == 'N':
                raise HTTPFound(self._request.app.router['StartLanguageOptionsEN:get'].url_for())
            else:
                attributes['language'] = 'en'
                await self.call_questionnaire(case, attributes, request.app)

        elif address_confirmation == 'No':
            raise HTTPFound(self._request.app.router['AddressEditEN:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@routes.view('/dechrau/address-confirmation')
class AddressConfirmationCY(Start):

    @aiohttp_jinja2.template('address-confirmation.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(self._request.app.router['IndexCY:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('address-confirmation.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        await check_permission(request)
        self._request = request
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(self._request.app.router['IndexCY:get'].url_for())

        try:
            address_confirmation = data["address-check-answer"]
        except KeyError:
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes

        if address_confirmation == 'Yes':
            if case['region'] == 'N':
                raise HTTPFound(self._request.app.router['StartLanguageOptionsCY:get'].url_for())
            else:
                attributes['language'] = 'cy'
                await self.call_questionnaire(case, attributes, request.app)

        elif address_confirmation == 'No':
            raise HTTPFound(self._request.app.router['AddressEditCY:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes


@routes.view('/ni/start/address-confirmation')
class AddressConfirmationNI(Start):

    @aiohttp_jinja2.template('address-confirmation.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexNI:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('address-confirmation.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        await check_permission(request)
        self._request = request
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexNI:get'].url_for())

        try:
            address_confirmation = data["address-check-answer"]
        except KeyError:
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'Yes':
            if case['region'] == 'N':
                raise HTTPFound(self._request.app.router['StartLanguageOptionsNI:get'].url_for())
            else:
                attributes['language'] = 'en'
                await self.call_questionnaire(case, attributes, request.app)

        elif address_confirmation == 'No':
            raise HTTPFound(self._request.app.router['AddressEditNI:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@routes.view('/start/address-edit')
class AddressEditEN(Start):

    @aiohttp_jinja2.template('address-edit.html')
    async def get(self, request):
        """
        Address Edit get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexEN:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('address-edit.html')
    async def post(self, request):
        """
        Address Edit flow. Edited address details.
        """
        await check_permission(request)
        data = await request.post()
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexEN:get'].url_for())

        try:
            attributes = Start.get_address_details(self, data, attributes)
        except InvalidEqPayLoad:
            logger.info("Error editing address, mandatory field required by EQ", client_ip=self._client_ip)
            flash(request, ADDRESS_EDIT_MSG)
            return attributes

        try:
            logger.info("Raising address modification call", client_ip=self._client_ip)
            await self.put_modify_address(session["case"], attributes)
        except ClientResponseError as ex:
            logger.error("Error raising address modification call", client_ip=self._client_ip)
            raise ex

        if case['region'] == 'N':
            raise HTTPFound(self._request.app.router['StartLanguageOptionsNI:get'].url_for())
        else:
            attributes['language'] = 'en'
            await self.call_questionnaire(case, attributes, request.app)


@routes.view('/dechrau/address-edit')
class AddressEditCY(Start):

    @aiohttp_jinja2.template('address-edit.html')
    async def get(self, request):
        """
        Address Edit get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(self._request.app.router['IndexCY:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('address-edit.html')
    async def post(self, request):
        """
        Address Edit flow. Edited address details.
        """
        await check_permission(request)
        data = await request.post()
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(self._request.app.router['IndexCY:get'].url_for())

        try:
            attributes = Start.get_address_details(self, data, attributes)
        except InvalidEqPayLoad:
            logger.info("Error editing address, mandatory field required by EQ", client_ip=self._client_ip)
            flash(request, ADDRESS_EDIT_MSG_CY)
            return attributes

        try:
            logger.info("Raising address modification call", client_ip=self._client_ip)
            await self.put_modify_address(session["case"], attributes)
        except ClientResponseError as ex:
            logger.error("Error raising address modification call", client_ip=self._client_ip)
            raise ex

        if case['region'] == 'N':
            raise HTTPFound(self._request.app.router['StartLanguageOptionsCY:get'].url_for())
        else:
            attributes['language'] = 'cy'
            await self.call_questionnaire(case, attributes, request.app)


@routes.view('/ni/start/address-edit')
class AddressEditNI(Start):

    @aiohttp_jinja2.template('address-edit.html')
    async def get(self, request):
        """
        Address Edit get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexNI:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('address-edit.html')
    async def post(self, request):
        """
        Address Edit flow. Edited address details.
        """
        await check_permission(request)
        data = await request.post()
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexNI:get'].url_for())

        try:
            attributes = Start.get_address_details(self, data, attributes)
        except InvalidEqPayLoad:
            logger.info("Error editing address, mandatory field required by EQ", client_ip=self._client_ip)
            flash(request, ADDRESS_EDIT_MSG)
            return attributes

        try:
            logger.info("Raising address modification call", client_ip=self._client_ip)
            await self.put_modify_address(session["case"], attributes)
        except ClientResponseError as ex:
            logger.error("Error raising address modification call", client_ip=self._client_ip)
            raise ex

        if case['region'] == 'N':
            raise HTTPFound(self._request.app.router['StartLanguageOptionsNI:get'].url_for())
        else:
            attributes['language'] = 'en'
            await self.call_questionnaire(case, attributes, request.app)


@routes.view('/start/language-options')
class StartLanguageOptionsEN(Start):

    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexEN:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def post(self, request):
        await check_permission(request)
        self._request = request
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexEN:get'].url_for())

        try:
            language_option = data["language-option"]
        except KeyError:
            logger.warn("NI language option error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        if language_option == 'Yes':
            attributes['language'] = 'en'
            await self.call_questionnaire(case, attributes, request.app)

        elif language_option == 'No':
            raise HTTPFound(self._request.app.router['StartSelectLanguageEN:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Language selection error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes


@routes.view('/dechrau/language-options')
class StartLanguageOptionsCY(Start):

    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(self._request.app.router['IndexCY:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def post(self, request):
        await check_permission(request)
        self._request = request
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(self._request.app.router['IndexCY:get'].url_for())

        try:
            language_option = data["language-option"]
        except KeyError:
            logger.warn("NI language option error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG_CY)
            return attributes

        if language_option == 'Yes':
            attributes['language'] = 'en'
            await self.call_questionnaire(case, attributes, request.app)

        elif language_option == 'No':
            raise HTTPFound(self._request.app.router['StartSelectLanguageCY:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Language selection error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG_CY)
            return attributes


@routes.view('/ni/start/language-options')
class StartLanguageOptionsNI(Start):

    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexNI:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def post(self, request):
        await check_permission(request)
        self._request = request
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexNI:get'].url_for())

        try:
            language_option = data["language-option"]
        except KeyError:
            logger.warn("NI language option error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        if language_option == 'Yes':
            attributes['language'] = 'en'
            await self.call_questionnaire(case, attributes, request.app)

        elif language_option == 'No':
            raise HTTPFound(self._request.app.router['StartSelectLanguageNI:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Language selection error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes


@routes.view('/start/select-language')
class StartSelectLanguageEN(Start):

    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexEN:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def post(self, request):
        await check_permission(request)
        self._request = request
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexEN:get'].url_for())

        try:
            language_option = data["language-option"]
        except KeyError:
            logger.warn("NI language option error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        if language_option == 'gaeilge':
            attributes['language'] = 'ga'

        elif language_option == 'ulster-scotch':
            attributes['language'] = 'ul'

        elif language_option == 'english':
            attributes['language'] = 'en'

        else:
            # catch all just in case, should never get here
            logger.warn("Language selection error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        await self.call_questionnaire(case, attributes, request.app)


@routes.view('/dechrau/select-language')
class StartSelectLanguageCY(Start):

    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(self._request.app.router['IndexCY:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def post(self, request):
        await check_permission(request)
        self._request = request
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(self._request.app.router['IndexCY:get'].url_for())

        try:
            language_option = data["language-option"]
        except KeyError:
            logger.warn("NI language option error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG_CY)
            return attributes

        if language_option == 'gaeilge':
            attributes['language'] = 'ga'

        elif language_option == 'ulster-scotch':
            attributes['language'] = 'ul'

        elif language_option == 'english':
            attributes['language'] = 'en'

        else:
            # catch all just in case, should never get here
            logger.warn("Language selection error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG_CY)
            return attributes

        await self.call_questionnaire(case, attributes, request.app)


@routes.view('/ni/start/select-language')
class StartSelectLanguageNI(Start):

    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        await check_permission(request)
        self._request = request

        session = await get_session(request)
        try:
            attributes = session["attributes"]
        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexNI:get'].url_for())

        return attributes

    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def post(self, request):
        await check_permission(request)
        self._request = request
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session["attributes"]
            case = session["case"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['IndexNI:get'].url_for())

        try:
            language_option = data["language-option"]
        except KeyError:
            logger.warn("NI language option error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        if language_option == 'gaeilge':
            attributes['language'] = 'ga'

        elif language_option == 'ulster-scotch':
            attributes['language'] = 'ul'

        elif language_option == 'english':
            attributes['language'] = 'en'

        else:
            # catch all just in case, should never get here
            logger.warn("Language selection error", client_ip=self._client_ip)
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        await self.call_questionnaire(case, attributes, request.app)


@routes.view('/start/timeout')
class UACTimeout(View):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, _):
        return {}


class WebChat(View):
    @staticmethod
    def get_now():
        return datetime.utcnow()

    @staticmethod
    def check_open():

        year = WebChat.get_now().year
        month = WebChat.get_now().month
        day = WebChat.get_now().day
        weekday = WebChat.get_now().weekday()
        hour = WebChat.get_now().hour

        census_weekend_open = 8
        census_weekend_close = 16
        saturday_open = 8
        saturday_close = 13
        weekday_open = 8
        weekday_close = 19

        timezone_offset = 0

        if WebChat.get_now() < datetime(2019, 10, 27):
            logger.info("Before switch to GMT - adjusting time", client_ip='')
            timezone_offset = 1

        if year == 2019 and month == 10 and (day == 12 or day == 13):
            if hour < (census_weekend_open - timezone_offset) or hour >= (census_weekend_close - timezone_offset):
                return False
        elif weekday == 5:  # Saturday
            if hour < (saturday_open - timezone_offset) or hour >= (saturday_close - timezone_offset):
                return False
        elif weekday == 6:  # Sunday
            return False
        else:
            if hour < (weekday_open - timezone_offset) or hour >= (weekday_close - timezone_offset):
                return False

        return True

    def validate_form(self, data, display_region):

        form_valid = True

        if not data.get('screen_name'):
            if display_region == 'cy':
                flash(self._request, WEBCHAT_MISSING_NAME_MSG_CY)
            else:
                flash(self._request, WEBCHAT_MISSING_NAME_MSG)
            form_valid = False

        if not(data.get('country')):
            if display_region == 'cy':
                flash(self._request, WEBCHAT_MISSING_COUNTRY_MSG_CY)
            else:
                flash(self._request, WEBCHAT_MISSING_COUNTRY_MSG)
            form_valid = False

        if not(data.get('query')):
            if display_region == 'cy':
                flash(self._request, WEBCHAT_MISSING_QUERY_MSG_CY)
            else:
                flash(self._request, WEBCHAT_MISSING_QUERY_MSG)
            form_valid = False

        return form_valid

    async def get_webchat_closed(self):
        querystring = '?im_name=OOH&im_subject=ONS&im_countchars=1&info_email=EMAIL&info_country=COUNTRY&info_query=QUERY&info_language=LANGUAGEID'  # NOQA
        return await self._make_request(
            Request("GET", self._webchat_service_url + querystring, None,
                    None, self._handle_response, None))


@routes.view('/webchat/chat')
class WebChatWindowEN(WebChat):
    @aiohttp_jinja2.template('webchat-window.html')
    async def get(self, _):
        return {'display_region': 'en'}


@routes.view('/cy/webchat/chat')
class WebChatWindowCY(WebChat):
    @aiohttp_jinja2.template('webchat-window.html')
    async def get(self, _):
        return {'display_region': 'cy', 'locale': 'cy'}


@routes.view('/ni/webchat/chat')
class WebChatWindowNI(WebChat):
    @aiohttp_jinja2.template('webchat-window.html')
    async def get(self, _):
        return {'display_region': 'ni'}


@routes.view('/webchat')
class WebChatEN(WebChat):
    @aiohttp_jinja2.template('webchat-form.html')
    async def get(self, request):

        self._request = request
        logger.info("Date/time check", client_ip=self._client_ip)
        if WebChat.check_open():
            return {'display_region': 'en'}
        else:
            try:
                await self.get_webchat_closed()
            except ClientError:
                logger.error("Failed to send WebChat Closed", client_ip=self._client_ip)

            logger.info("WebChat Closed", client_ip=self._client_ip)
            return {'webchat_status': 'closed', 'display_region': 'en'}

    @aiohttp_jinja2.template('webchat-form.html')
    async def post(self, request):

        data = await request.post()
        self._request = request

        form_valid = self.validate_form(data, 'en')

        if not form_valid:
            logger.info("Form submission error", client_ip=self._client_ip)
            return {'form_value_screen_name': data.get('screen_name'),
                    'form_value_country': data.get('country'),
                    'form_value_query': data.get('query'),
                    'display_region': 'en'}

        context = {'screen_name': data.get('screen_name'),
                   'language': 'english',
                   'country': data.get('country'),
                   'query': data.get('query'),
                   'display_region': 'en',
                   'webchat_url': f"{self._request.app['WEBCHAT_SVC_URL']}"}

        logger.info("Date/time check", client_ip=self._client_ip)
        if WebChat.check_open():
            return aiohttp_jinja2.render_template("webchat-window.html", self._request, context)
        else:
            try:
                await self.get_webchat_closed()
            except ClientError:
                logger.error("Failed to send WebChat Closed", client_ip=self._client_ip)

            logger.info("WebChat Closed", client_ip=self._client_ip)
            return {'webchat_status': 'closed', 'display_region': 'en'}


@routes.view('/cy/webchat')
class WebChatCY(WebChat):
    @aiohttp_jinja2.template('webchat-form.html')
    async def get(self, request):

        self._request = request
        logger.info("Date/time check", client_ip=self._client_ip)
        if WebChat.check_open():
            return {'display_region': 'cy', 'locale': 'cy'}
        else:
            try:
                await self.get_webchat_closed()
            except ClientError:
                logger.error("Failed to send WebChat Closed", client_ip=self._client_ip)

            logger.info("WebChat Closed", client_ip=self._client_ip)
            return {'webchat_status': 'closed', 'display_region': 'cy', 'locale': 'cy'}

    @aiohttp_jinja2.template('webchat-form.html')
    async def post(self, request):

        data = await request.post()
        self._request = request

        form_valid = self.validate_form(data, 'cy')

        if not form_valid:
            logger.info("Form submission error", client_ip=self._client_ip)
            return {'form_value_screen_name': data.get('screen_name'),
                    'form_value_country': data.get('country'),
                    'form_value_query': data.get('query'),
                    'display_region': 'cy',
                    'locale': 'cy'}

        context = {'screen_name': data.get('screen_name'),
                   'language': 'welsh',
                   'country': data.get('country'),
                   'query': data.get('query'),
                   'display_region': 'cy',
                   'locale': 'cy',
                   'webchat_url': f"{self._request.app['WEBCHAT_SVC_URL']}"}

        logger.info("Date/time check", client_ip=self._client_ip)
        if WebChat.check_open():
            return aiohttp_jinja2.render_template("webchat-window.html", self._request, context)
        else:
            try:
                await self.get_webchat_closed()
            except ClientError:
                logger.error("Failed to send WebChat Closed", client_ip=self._client_ip)

            logger.info("WebChat Closed", client_ip=self._client_ip)
            return {'webchat_status': 'closed', 'display_region': 'cy', 'locale': 'cy'}


@routes.view('/ni/webchat')
class WebChatNI(WebChat):
    @aiohttp_jinja2.template('webchat-form.html')
    async def get(self, request):

        self._request = request
        logger.info("Date/time check", client_ip=self._client_ip)
        if WebChat.check_open():
            return {'display_region': 'ni'}
        else:
            try:
                await self.get_webchat_closed()
            except ClientError:
                logger.error("Failed to send WebChat Closed", client_ip=self._client_ip)

            logger.info("WebChat Closed", client_ip=self._client_ip)
            return {'webchat_status': 'closed', 'display_region': 'ni'}

    @aiohttp_jinja2.template('webchat-form.html')
    async def post(self, request):

        data = await request.post()
        self._request = request

        form_valid = self.validate_form(data, 'ni')

        if not form_valid:
            logger.info("Form submission error", client_ip=self._client_ip)
            return {'form_value_screen_name': data.get('screen_name'),
                    'form_value_country': data.get('country'),
                    'form_value_query': data.get('query'),
                    'display_region': 'ni'}

        context = {'screen_name': data.get('screen_name'),
                   'language': 'english',
                   'country': data.get('country'),
                   'query': data.get('query'),
                   'display_region': 'ni',
                   'webchat_url': f"{self._request.app['WEBCHAT_SVC_URL']}"}

        logger.info("Date/time check", client_ip=self._client_ip)
        if WebChat.check_open():
            return aiohttp_jinja2.render_template("webchat-window.html", self._request, context)
        else:
            try:
                await self.get_webchat_closed()
            except ClientError:
                logger.error("Failed to send WebChat Closed", client_ip=self._client_ip)

            logger.info("WebChat Closed", client_ip=self._client_ip)
            return {'webchat_status': 'closed', 'display_region': 'ni'}


class RequestCodeCommon(View):

    def request_code_check_session(self, fulfillment_type, display_region):
        if self._request.cookies.get('RH_SESSION') is None:
            logger.warn("Session timed out", client_ip=self._client_ip)
            raise HTTPFound(self._request.app.router['RequestCodeTimeout' + fulfillment_type + display_region + ':get'].url_for())  # NOQA

    async def get_check_attributes(self, request, fulfillment_type, display_region):
        self._request = request

        self.request_code_check_session(fulfillment_type, display_region)
        session = await get_session(request)
        try:
            attributes = session["attributes"]

        except KeyError:
            raise HTTPFound(self._request.app.router['RequestCodeTimeout' + fulfillment_type + display_region + ':get'].url_for())  # NOQA

        return attributes

    async def get_postcode_return(self, postcode, fulfillment_type, display_region):
        postcode_return = await self.get_ai_postcode(postcode)

        address_options = []

        for singleAddress in postcode_return['response']['addresses']:
            address_options.append(
                {"value": {"uprn": singleAddress['uprn'], "address": singleAddress['formattedAddress']},
                 "label": {"text": singleAddress['formattedAddress']},
                 "id": singleAddress['uprn']})

        address_content = {'postcode': postcode,
                           'addresses': address_options,
                           'display_region': display_region,
                           'fulfillment_type': fulfillment_type,
                           'total_matches': postcode_return['response']['total']}

        return address_content

    postcode_validation_pattern = re.compile(r'^((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|BX|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}))|BFPO[ ]?\d{1,4}$')  # NOQA
    mobile_validation_pattern = re.compile(r'^(\+44\s?7(\d ?){3}|\(?07(\d ?){3}\)?)\s?(\d ?){3}\s?(\d ?){3}$')

    async def get_postcode(self, request, data, fulfillment_type, display_region, locale):
        if RequestCodeCommon.postcode_validation_pattern.fullmatch(data["request-postcode"].upper()):

            logger.info("Valid postcode", client_ip=self._client_ip)

            attributes = {}
            attributes["postcode"] = data["request-postcode"].upper()
            attributes["display_region"] = display_region.lower()
            attributes["locale"] = locale
            attributes["fulfillment_type"] = fulfillment_type

            session = await get_session(request)
            session["attributes"] = attributes

            raise HTTPFound(self._request.app.router['RequestCodeSelectAddress' + fulfillment_type
                                                     + display_region + ':get'].url_for())

        else:
            logger.warn("Attempt to use an invalid postcode", client_ip=self._client_ip)
            if display_region == 'CY':
                flash(self._request, POSTCODE_INVALID_MSG_CY)
            else:
                flash(self._request, POSTCODE_INVALID_MSG)
            raise HTTPFound(self._request.app.router['RequestCodeEnterAddress' + fulfillment_type
                                                     + display_region + ':get'].url_for())

    async def post_enter_mobile(self, attributes, data, request):

        if RequestCodeCommon.mobile_validation_pattern.fullmatch(data['request-mobile-number']):

            attributes["mobile_number"] = data["request-mobile-number"]
            session = await get_session(request)
            session["attributes"] = attributes

            raise HTTPFound(self._request.app.router['RequestCodeConfirmMobile' + attributes["fulfillment_type"]
                                                     + attributes["display_region"].upper() + ':get'].url_for())

        else:
            logger.warn("Attempt to use an invalid mobile number", client_ip=self._client_ip)
            if attributes['display_region'] == 'cy':
                flash(self._request, MOBILE_ENTER_MSG_CY)
            else:
                flash(self._request, MOBILE_ENTER_MSG)
            raise HTTPFound(self._request.app.router['RequestCodeEnterMobile' + attributes["fulfillment_type"]
                                                     + attributes["display_region"].upper() + ':post'].url_for())

    @property
    def _ai_url_postcode(self):
        return f"{self._request.app['ADDRESS_INDEX_SVC_URL']}/addresses/postcode/"

    @property
    def _rhsvc_get_cases_by_uprn(self):
        return f"{self._request.app['RHSVC_URL']}/cases/uprn/"

    @property
    def _rhsvc_get_fulfilments(self):
        return f"{self._request.app['RHSVC_URL']}/fulfilments"

    @property
    def _rhsvc_request_fulfilment(self):
        return f"{self._request.app['RHSVC_URL']}/cases/"

    async def get_ai_postcode(self, postcode):
        return await self._make_request(
            Request("GET", self._ai_url_postcode + postcode, None,
                    None, self._handle_response, "json"))

    async def get_cases_by_uprn(self, uprn):
        return await self._make_request(
            Request("GET", self._rhsvc_get_cases_by_uprn + uprn, None,
                    None, self._handle_response, "json"))

    async def get_fulfilment(self, case_type, region, delivery_channel):
        querystring = '?caseType=' + case_type + '&region=' + region + '&deliveryChannel=' + delivery_channel  # NOQA
        return await self._make_request(
            Request("GET", self._rhsvc_get_fulfilments + querystring, None,
                    None, self._handle_response, "json"))

    async def request_fulfilment(self, case_id, tel_no, fulfilment_code):
        json = {'caseId': case_id, 'telNo': tel_no, 'fulfilmentCode': fulfilment_code,
                'dateTime': datetime.now(timezone.utc).isoformat()}
        return await self._make_request(
            Request("POST", self._rhsvc_request_fulfilment + case_id + '/fulfilments/sms',
                    self._request.app["RHSVC_AUTH"],
                    json, self._handle_response, None))


@routes.view('/request-access-code')
class RequestCodeHouseholdEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-household.html')
    async def get(self, _):
        return {'display_region': 'en'}


@routes.view('/cy/request-access-code')
class RequestCodeHouseholdCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-household.html')
    async def get(self, _):
        return {'display_region': 'cy', 'locale': 'cy'}


@routes.view('/ni/request-access-code')
class RequestCodeHouseholdNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-household.html')
    async def get(self, _):
        return {'display_region': 'ni'}


@routes.view('/request-access-code/enter-address')
class RequestCodeEnterAddressHHEN(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, _):
        return {'display_region': 'en'}

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self._request = request
        data = await self._request.post()
        await RequestCodeCommon.get_postcode(self, request, data, 'HH', 'EN', 'en')


@routes.view('/cy/request-access-code/enter-address')
class RequestCodeEnterAddressHHCY(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, _):
        return {'display_region': 'cy', 'locale': 'cy'}

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self._request = request
        data = await self._request.post()
        await RequestCodeCommon.get_postcode(self, request, data, 'HH', 'CY', 'cy')


@routes.view('/ni/request-access-code/enter-address')
class RequestCodeEnterAddressHHNI(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, _):
        return {'display_region': 'ni'}

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self._request = request
        data = await self._request.post()
        await RequestCodeCommon.get_postcode(self, request, data, 'HH', 'NI', 'en')


@routes.view('/request-access-code/select-address')
class RequestCodeSelectAddressHHEN(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        address_content = await self.get_postcode_return(attributes["postcode"],
                                                         attributes["fulfillment_type"],
                                                         attributes["display_region"])
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        data = await request.post()

        try:
            form_return = ast.literal_eval(data["request-address-select"])
        except KeyError:
            logger.warn("No address selected", client_ip=self._client_ip)
            flash(request, ADDRESS_SELECT_CHECK_MSG)
            address_content = await self.get_postcode_return(attributes["postcode"],
                                                             attributes["fulfillment_type"],
                                                             attributes["display_region"])
            return address_content

        session = await get_session(request)
        session["attributes"]["address"] = form_return["address"]
        session["attributes"]["uprn"] = form_return["uprn"]
        session.changed()
        logger.info("Session updated", client_ip=self._client_ip)

        raise HTTPFound(self._request.app.router['RequestCodeConfirmAddressHHEN:get'].url_for())


@routes.view('/cy/request-access-code/select-address')
class RequestCodeSelectAddressHHCY(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        address_content = await self.get_postcode_return(attributes["postcode"],
                                                         attributes["fulfillment_type"],
                                                         attributes["display_region"])
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        data = await request.post()

        try:
            form_return = ast.literal_eval(data["request-address-select"])
        except KeyError:
            logger.warn("No address selected", client_ip=self._client_ip)
            flash(request, ADDRESS_SELECT_CHECK_MSG_CY)
            address_content = await self.get_postcode_return(attributes["postcode"],
                                                             attributes["fulfillment_type"],
                                                             attributes["display_region"])
            return address_content

        session = await get_session(request)
        session["attributes"]["address"] = form_return["address"]
        session["attributes"]["uprn"] = form_return["uprn"]
        session.changed()
        logger.info("Session updated", client_ip=self._client_ip)

        raise HTTPFound(self._request.app.router['RequestCodeConfirmAddressHHCY:get'].url_for())


@routes.view('/ni/request-access-code/select-address')
class RequestCodeSelectAddressHHNI(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        address_content = await self.get_postcode_return(attributes["postcode"],
                                                         attributes["fulfillment_type"],
                                                         attributes["display_region"])
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        data = await request.post()

        try:
            form_return = ast.literal_eval(data["request-address-select"])
        except KeyError:
            logger.warn("No address selected", client_ip=self._client_ip)
            flash(request, ADDRESS_SELECT_CHECK_MSG)
            address_content = await self.get_postcode_return(attributes["postcode"],
                                                             attributes["fulfillment_type"],
                                                             attributes["display_region"])
            return address_content

        session = await get_session(request)
        session["attributes"]["address"] = form_return["address"]
        session["attributes"]["uprn"] = form_return["uprn"]
        session.changed()
        logger.info("Session updated", client_ip=self._client_ip)

        raise HTTPFound(self._request.app.router['RequestCodeConfirmAddressHHNI:get'].url_for())


@routes.view('/request-access-code/confirm-address')
class RequestCodeConfirmAddressHHEN(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        data = await request.post()

        try:
            address_confirmation = data["request-address-confirmation"]
        except KeyError:
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session["attributes"]['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(uprn)
                session["attributes"]["case_id"] = uprn_return[0]["caseId"]
                session["attributes"]["region"] = uprn_return[0]["region"]
                session.changed()
                raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHHEN:get'].url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.warn("Unable to match UPRN", client_ip=self._client_ip)
                    raise HTTPFound(self._request.app.router['RequestCodeNotRequiredHHEN:get'].url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterAddressHHEN:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@routes.view('/cy/request-access-code/confirm-address')
class RequestCodeConfirmAddressHHCY(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        data = await request.post()

        try:
            address_confirmation = data["request-address-confirmation"]
        except KeyError:
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session["attributes"]['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(uprn)
                session["attributes"]["case_id"] = uprn_return[0]["caseId"]
                session["attributes"]["region"] = uprn_return[0]["region"]
                session.changed()
                raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHHCY:get'].url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.warn("Unable to match UPRN", client_ip=self._client_ip)
                    raise HTTPFound(self._request.app.router['RequestCodeNotRequiredHHCY:get'].url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterAddressHHCY:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes


@routes.view('/ni/request-access-code/confirm-address')
class RequestCodeConfirmAddressHHNI(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        data = await request.post()
        try:
            address_confirmation = data["request-address-confirmation"]
        except KeyError:
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session["attributes"]['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(uprn)
                session["attributes"]["case_id"] = uprn_return[0]["caseId"]
                session["attributes"]["region"] = uprn_return[0]["region"]
                session.changed()
                raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHHNI:get'].url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.warn("Unable to match UPRN", client_ip=self._client_ip)
                    raise HTTPFound(self._request.app.router['RequestCodeNotRequiredHHNI:get'].url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterAddressHHNI:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@routes.view('/request-access-code/not-required')
class RequestCodeNotRequiredHHEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        return attributes


@routes.view('/cy/request-access-code/not-required')
class RequestCodeNotRequiredHHCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        return attributes


@routes.view('/ni/request-access-code/not-required')
class RequestCodeNotRequiredHHNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        return attributes


@routes.view('/request-access-code/enter-mobile')
class RequestCodeEnterMobileHHEN(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(self, attributes, data, request)


@routes.view('/cy/request-access-code/enter-mobile')
class RequestCodeEnterMobileHHCY(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(self, attributes, data, request)


@routes.view('/ni/request-access-code/enter-mobile')
class RequestCodeEnterMobileHHNI(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(self, attributes, data, request)


@routes.view('/request-access-code/confirm-mobile')
class RequestCodeConfirmMobileHHEN(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        data = await request.post()
        try:
            mobile_confirmation = data["request-mobile-confirmation"]
        except KeyError:
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG)
            return attributes

        if mobile_confirmation == 'yes':

            try:
                available_fulfilments = await self.get_fulfilment('HH', attributes['region'], 'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'].startswith(attributes['display_region']):
                            attributes['fulfilmentCode'] = fulfilment['fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0]['fulfilmentCode']

                try:
                    await self.request_fulfilment(attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except ClientResponseError as ex:
                    raise ex

                raise HTTPFound(self._request.app.router['RequestCodeCodeSentHHEN:get'].url_for())
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHHEN:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG)
            return attributes


@routes.view('/cy/request-access-code/confirm-mobile')
class RequestCodeConfirmMobileHHCY(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        data = await request.post()

        try:
            mobile_confirmation = data["request-mobile-confirmation"]
        except KeyError:
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG_CY)
            return attributes

        if mobile_confirmation == 'yes':

            try:
                available_fulfilments = await self.get_fulfilment('HH', attributes['region'], 'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'].startswith(attributes['display_region']):
                            attributes['fulfilmentCode'] = fulfilment['fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0]['fulfilmentCode']

                try:
                    await self.request_fulfilment(attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except ClientResponseError as ex:
                    raise ex

                raise HTTPFound(self._request.app.router['RequestCodeCodeSentHHCY:get'].url_for())
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHHCY:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG_CY)
            return attributes


@routes.view('/ni/request-access-code/confirm-mobile')
class RequestCodeConfirmMobileHHNI(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        data = await request.post()

        try:
            mobile_confirmation = data["request-mobile-confirmation"]
        except KeyError:
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG)
            return attributes

        if mobile_confirmation == 'yes':

            try:
                available_fulfilments = await self.get_fulfilment('HH', attributes['region'], 'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'].startswith(attributes['display_region']):
                            attributes['fulfilmentCode'] = fulfilment['fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0]['fulfilmentCode']

                try:
                    await self.request_fulfilment(attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except ClientResponseError as ex:
                    raise ex

                raise HTTPFound(self._request.app.router['RequestCodeCodeSentHHNI:get'].url_for())
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHHNI:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG)
            return attributes


@routes.view('/request-access-code/code-sent')
class RequestCodeCodeSentHHEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        return attributes


@routes.view('/cy/request-access-code/code-sent')
class RequestCodeCodeSentHHCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        return attributes


@routes.view('/ni/request-access-code/code-sent')
class RequestCodeCodeSentHHNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        return attributes


@routes.view('/request-access-code/timeout')
class RequestCodeTimeoutHHEN(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, _):
        return {'fulfillment_type': 'HH', 'display_region': 'en'}


@routes.view('/request-access-code/timeout')
class RequestCodeTimeoutHHCY(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, _):
        return {'fulfillment_type': 'HH', 'display_region': 'cy', 'locale': 'cy'}


@routes.view('/request-access-code/timeout')
class RequestCodeTimeoutHHNI(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, _):
        return {'fulfillment_type': 'HH', 'display_region': 'ni'}


@routes.view('/request-individual-code')
class RequestCodeIndividualEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-individual.html')
    async def get(self, _):
        return {'display_region': 'en'}


@routes.view('/cy/request-individual-code')
class RequestCodeIndividualCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-individual.html')
    async def get(self, _):
        return {'display_region': 'cy', 'locale': 'cy'}


@routes.view('/ni/request-individual-code')
class RequestCodeIndividualNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-individual.html')
    async def get(self, _):
        return {'display_region': 'ni'}


@routes.view('/request-individual-code/enter-address')
class RequestCodeEnterAddressHIEN(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, _):
        return {'fulfillment_type': 'HI', 'display_region': 'en'}

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self._request = request
        data = await self._request.post()
        await RequestCodeCommon.get_postcode(self, request, data, 'HI', 'EN', 'en')


@routes.view('/cy/request-individual-code/enter-address')
class RequestCodeEnterAddressHICY(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, _):
        return {'fulfillment_type': 'HI', 'display_region': 'cy', 'locale': 'cy'}

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self._request = request
        data = await self._request.post()
        await RequestCodeCommon.get_postcode(self, request, data, 'HI', 'CY', 'cy')


@routes.view('/ni/request-individual-code/enter-address')
class RequestCodeEnterAddressHINI(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, _):
        return {'fulfillment_type': 'HI', 'display_region': 'ni'}

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self._request = request
        data = await self._request.post()
        await RequestCodeCommon.get_postcode(self, request, data, 'HI', 'NI', 'en')


@routes.view('/request-individual-code/select-address')
class RequestCodeSelectAddressHIEN(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        address_content = await self.get_postcode_return(attributes["postcode"],
                                                         attributes["fulfillment_type"],
                                                         attributes["display_region"])
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        data = await request.post()

        try:
            form_return = ast.literal_eval(data["request-address-select"])
        except KeyError:
            logger.warn("No address selected", client_ip=self._client_ip)
            flash(request, ADDRESS_SELECT_CHECK_MSG)
            address_content = await self.get_postcode_return(attributes["postcode"],
                                                             attributes["fulfillment_type"],
                                                             attributes["display_region"])
            return address_content

        session = await get_session(request)
        session["attributes"]["address"] = form_return["address"]
        session["attributes"]["uprn"] = form_return["uprn"]
        session.changed()
        logger.info("Session updated", client_ip=self._client_ip)

        raise HTTPFound(self._request.app.router['RequestCodeConfirmAddressHIEN:get'].url_for())


@routes.view('/cy/request-individual-code/select-address')
class RequestCodeSelectAddressHICY(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        address_content = await self.get_postcode_return(attributes["postcode"],
                                                         attributes["fulfillment_type"],
                                                         attributes["display_region"])
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        data = await request.post()

        try:
            form_return = ast.literal_eval(data["request-address-select"])
        except KeyError:
            logger.warn("No address selected", client_ip=self._client_ip)
            flash(request, ADDRESS_SELECT_CHECK_MSG_CY)
            address_content = await self.get_postcode_return(attributes["postcode"],
                                                             attributes["fulfillment_type"],
                                                             attributes["display_region"])
            return address_content

        session = await get_session(request)
        session["attributes"]["address"] = form_return["address"]
        session["attributes"]["uprn"] = form_return["uprn"]
        session.changed()
        logger.info("Session updated", client_ip=self._client_ip)

        raise HTTPFound(self._request.app.router['RequestCodeConfirmAddressHICY:get'].url_for())


@routes.view('/ni/request-individual-code/select-address')
class RequestCodeSelectAddressHINI(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        address_content = await self.get_postcode_return(attributes["postcode"],
                                                         attributes["fulfillment_type"],
                                                         attributes["display_region"])
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        data = await request.post()

        try:
            form_return = ast.literal_eval(data["request-address-select"])
        except KeyError:
            logger.warn("No address selected", client_ip=self._client_ip)
            flash(request, ADDRESS_SELECT_CHECK_MSG)
            address_content = await self.get_postcode_return(attributes["postcode"],
                                                             attributes["fulfillment_type"],
                                                             attributes["display_region"])
            return address_content

        session = await get_session(request)
        session["attributes"]["address"] = form_return["address"]
        session["attributes"]["uprn"] = form_return["uprn"]
        session.changed()
        logger.info("Session updated", client_ip=self._client_ip)

        raise HTTPFound(self._request.app.router['RequestCodeConfirmAddressHINI:get'].url_for())


@routes.view('/request-individual-code/confirm-address')
class RequestCodeConfirmAddressHIEN(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        data = await request.post()
        try:
            address_confirmation = data["request-address-confirmation"]
        except KeyError:
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session["attributes"]['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(uprn)
                session["attributes"]["case_id"] = uprn_return[0]["caseId"]
                session["attributes"]["region"] = uprn_return[0]["region"]
                session.changed()
                raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHIEN:get'].url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.warn("Unable to match UPRN", client_ip=self._client_ip)
                    raise HTTPFound(self._request.app.router['RequestCodeNotRequiredHIEN:get'].url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterAddressHIEN:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@routes.view('/cy/request-individual-code/confirm-address')
class RequestCodeConfirmAddressHICY(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        data = await request.post()
        try:
            address_confirmation = data["request-address-confirmation"]
        except KeyError:
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session["attributes"]['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(uprn)
                session["attributes"]["case_id"] = uprn_return[0]["caseId"]
                session["attributes"]["region"] = uprn_return[0]["region"]
                session.changed()
                raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHICY:get'].url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.warn("Unable to match UPRN", client_ip=self._client_ip)
                    raise HTTPFound(self._request.app.router['RequestCodeNotRequiredHICY:get'].url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterAddressHICY:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes


@routes.view('/ni/request-individual-code/confirm-address')
class RequestCodeConfirmAddressHINI(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        data = await request.post()
        try:
            address_confirmation = data["request-address-confirmation"]
        except KeyError:
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session["attributes"]['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(uprn)
                session["attributes"]["case_id"] = uprn_return[0]["caseId"]
                session["attributes"]["region"] = uprn_return[0]["region"]
                session.changed()
                raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHINI:get'].url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.warn("Unable to match UPRN", client_ip=self._client_ip)
                    raise HTTPFound(self._request.app.router['RequestCodeNotRequiredHINI:get'].url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterAddressHINI:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@routes.view('/request-individual-code/not-required')
class RequestCodeNotRequiredHIEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        return attributes


@routes.view('/cy/request-individual-code/not-required')
class RequestCodeNotRequiredHICY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        return attributes


@routes.view('/ni/request-individual-code/not-required')
class RequestCodeNotRequiredHINI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        return attributes


@routes.view('/request-individual-code/enter-mobile')
class RequestCodeEnterMobileHIEN(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(self, attributes, data, request)


@routes.view('/cy/request-individual-code/enter-mobile')
class RequestCodeEnterMobileHICY(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(self, attributes, data, request)


@routes.view('/ni/request-individual-code/enter-mobile')
class RequestCodeEnterMobileHINI(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(self, attributes, data, request)


@routes.view('/request-individual-code/confirm-mobile')
class RequestCodeConfirmMobileHIEN(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        data = await request.post()
        try:
            mobile_confirmation = data["request-mobile-confirmation"]
        except KeyError:
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG)
            return attributes

        if mobile_confirmation == 'yes':

            try:
                available_fulfilments = await self.get_fulfilment(attributes["fulfillment_type"],
                                                                  attributes['region'], 'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'].startswith(attributes['display_region']):
                            attributes['fulfilmentCode'] = fulfilment['fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0]['fulfilmentCode']

                try:
                    await self.request_fulfilment(attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except ClientResponseError as ex:
                    raise ex

                raise HTTPFound(self._request.app.router['RequestCodeCodeSentHIEN:get'].url_for())
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHIEN:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG)
            return attributes


@routes.view('/cy/request-individual-code/confirm-mobile')
class RequestCodeConfirmMobileHICY(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        data = await request.post()
        try:
            mobile_confirmation = data["request-mobile-confirmation"]
        except KeyError:
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG_CY)
            return attributes

        if mobile_confirmation == 'yes':

            try:
                available_fulfilments = await self.get_fulfilment(attributes["fulfillment_type"],
                                                                  attributes['region'], 'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'].startswith(attributes['display_region']):
                            attributes['fulfilmentCode'] = fulfilment['fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0]['fulfilmentCode']

                try:
                    await self.request_fulfilment(attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except ClientResponseError as ex:
                    raise ex

                raise HTTPFound(self._request.app.router['RequestCodeCodeSentHICY:get'].url_for())
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHICY:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG_CY)
            return attributes


@routes.view('/ni/request-individual-code/confirm-mobile')
class RequestCodeConfirmMobileHINI(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        data = await request.post()
        try:
            mobile_confirmation = data["request-mobile-confirmation"]
        except KeyError:
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG)
            return attributes

        if mobile_confirmation == 'yes':

            try:
                available_fulfilments = await self.get_fulfilment(attributes["fulfillment_type"],
                                                                  attributes['region'], 'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'].startswith(attributes['display_region']):
                            attributes['fulfilmentCode'] = fulfilment['fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0]['fulfilmentCode']

                try:
                    await self.request_fulfilment(attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except ClientResponseError as ex:
                    raise ex

                raise HTTPFound(self._request.app.router['RequestCodeCodeSentHINI:get'].url_for())
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterMobileHINI:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG)
            return attributes


@routes.view('/request-individual-code/code-sent')
class RequestCodeCodeSentHIEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        return attributes


@routes.view('/cy/request-individual-code/code-sent')
class RequestCodeCodeSentHICY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        return attributes


@routes.view('/ni/request-individual-code/code-sent')
class RequestCodeCodeSentHINI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        return attributes


@routes.view('/request-individual-code/timeout')
class RequestCodeTimeoutHIEN(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, _):
        return {'fulfillment_type': 'HI', 'display_region': 'en'}


@routes.view('/cy/request-individual-code/timeout')
class RequestCodeTimeoutHICY(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, _):
        return {'fulfillment_type': 'HI', 'display_region': 'cy', 'locale': 'cy'}


@routes.view('/ni/request-individual-code/timeout')
class RequestCodeTimeoutHINI(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, _):
        return {'fulfillment_type': 'HI', 'display_region': 'ni'}
