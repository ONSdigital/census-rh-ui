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
    SESSION_TIMEOUT_MSG, WEBCHAT_MISSING_NAME_MSG, WEBCHAT_MISSING_LANGUAGE_MSG,
    WEBCHAT_MISSING_QUERY_MSG, MOBILE_ENTER_MSG, MOBILE_CHECK_MSG, POSTCODE_INVALID_MSG)
from .exceptions import InactiveCaseError
from .eq import EqPayloadConstructor
from .flash import flash
from .exceptions import InvalidEqPayLoad
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

    async def get_webchat_closed(self):
        querystring = '?im_name=closed&im_subject=ONS&im_countchars=1&info_email=closed&info_country=closed&info_query=closed&info_language=closed'  # NOQA
        return await self._make_request(
            Request("GET", self._webchat_service_url + querystring, None,
                    None, self._handle_response, None))

    async def get_ai_postcode(self, postcode):
        return await self._make_request(
            Request("GET", self._ai_url_postcode + postcode, None,
                    None, self._handle_response, "json"))

    async def get_cases_by_uprn(self, uprn):
        return await self._make_request(
            Request("GET", self._rhsvc_get_cases_by_uprn + uprn, None,
                    None, self._handle_response, "json"))

    async def get_fulfilment(self, caseType, region, deliveryChannel):
        querystring = '?caseType=' + caseType + '&region=' + region + '&deliveryChannel=' + deliveryChannel # NOQA
        return await self._make_request(
            Request("GET", self._rhsvc_get_fulfilments + querystring, None,
                    None, self._handle_response, "json"))

    async def request_fulfilment(self, caseId, telNo, fulfilmentCode):
        json = {'caseId': caseId, 'telNo': telNo, 'fulfilmentCode': fulfilmentCode, 'dateTime': datetime.now(timezone.utc).isoformat()}
        return await self._make_request(
            Request("POST", self._rhsvc_request_fulfilment + caseId + '/fulfilments/sms', self._request.app["RHSVC_AUTH"],
                    json, self._handle_response, None))


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
        if data.get('uac'):
            combined = data.get('uac').lower().replace(" ", "")
        else:
            combined = ''

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
            Request("GET", self._rhsvc_url, self._request.app["RHSVC_AUTH"], None, self._handle_response, "json"))

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
            attributes["townName"] = data["address-town"].strip()
            attributes["postcode"] = data["address-postcode"].strip()

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


@routes.view('/webchat/chat')
class WebChatWindow:
    @aiohttp_jinja2.template('webchat-window.html')
    async def get(self, _):
        return {}


@routes.view('/webchat')
class WebChat(View):

    @staticmethod
    def get_now():
        return datetime.now()

    @staticmethod
    def check_open():

        year = WebChat.get_now().year
        month = WebChat.get_now().month
        day = WebChat.get_now().day
        weekday = WebChat.get_now().weekday()
        hour = WebChat.get_now().hour
        if year == 2019 and month == 10 and (day == 12 or day == 13):
            if hour < 8 or hour >= 16:
                return False
        elif weekday == 5:
            if hour < 8 or hour >= 13:
                return False
        elif weekday == 6:
            return False
        else:
            if hour < 8 or hour >= 19:
                return False

        return True

    def validate_form(self, data):

        form_valid = True

        if not data.get('screen_name'):
            flash(self._request, WEBCHAT_MISSING_NAME_MSG)
            form_valid = False

        if not(data.get('language')):
            flash(self._request, WEBCHAT_MISSING_LANGUAGE_MSG)
            form_valid = False

        if not(data.get('query')):
            flash(self._request, WEBCHAT_MISSING_QUERY_MSG)
            form_valid = False

        return form_valid

    @aiohttp_jinja2.template('webchat-form.html')
    async def get(self, request):

        self._request = request
        logger.info("Date/time check", client_ip=self._client_ip)
        if WebChat.check_open():
            return {}
        else:
            try:
                await self.get_webchat_closed()
            except ClientError:
                logger.error("Failed to send WebChat Closed", client_ip=self._client_ip)

            logger.info("WebChat Closed", client_ip=self._client_ip)
            return {'webchat_status': 'closed'}

    @aiohttp_jinja2.template('webchat-form.html')
    async def post(self, request):

        data = await request.post()
        self._request = request

        form_valid = self.validate_form(data)

        if not form_valid:
            logger.info("Form submission error", client_ip=self._client_ip)
            return {'form_value_screen_name': data.get('screen_name'),
                    'form_value_language': data.get('language'),
                    'form_value_query': data.get('query')}

        context = {'screen_name': data.get('screen_name'),
                   'language': data.get('language'),
                   'query': data.get('query'),
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
            return {'webchat_status': 'closed'}


class RequestCodeCommon(View):

    async def get_check_attributes(self, request):
        self._request = request

        self.check_session()
        session = await get_session(request)
        try:
            attributes = session["attributes"]

        except KeyError:
            flash(self._request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(self._request.app.router['RequestCode:get'].url_for())

        return attributes

    async def get_postcode_return(self, postcode, display_region):
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
                           'total_matches': postcode_return['response']['total']}

        return address_content

    postcode_validation_pattern = re.compile(r'^([A-PR-UWYZa-pr-uwyz]([0-9]{1,2}|([A-HK-Ya-hk-y][0-9]|[A-HK-Ya-hk-y][0-9]([0-9]|[ABEHMNPRV-Yabehmnprv-y]))|[0-9][A-HJKS-UWa-hjks-uw])\ {0,1}[0-9][ABD-HJLNP-UW-Zabd-hjlnp-uw-z]{2}|([Gg][Ii][Rr]\ 0[Aa][Aa])|([Ss][Aa][Nn]\ {0,1}[Tt][Aa]1)|([Bb][Ff][Pp][Oo]\ {0,1}([Cc]\/[Oo]\ )?[0-9]{1,4})|(([Aa][Ss][Cc][Nn]|[Bb][Bb][Nn][Dd]|[BFSbfs][Ii][Qq][Qq]|[Pp][Cc][Rr][Nn]|[Ss][Tt][Hh][Ll]|[Tt][Dd][Cc][Uu]|[Tt][Kk][Cc][Aa])\ {0,1}1[Zz][Zz]))$')  # NOQA
    mobile_validation_pattern = re.compile(r'^(\+44\s?7(\d ?){3}|\(?07(\d ?){3}\)?)\s?(\d ?){3}\s?(\d ?){3}$')

@routes.view('/request-access-code')
class RequestCode(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-household.html')
    async def get(self, _):
        return {}

    @aiohttp_jinja2.template('request-code-household.html')
    async def post(self, request):

        self._request = request
        data = await self._request.post()

        if RequestCodeCommon.postcode_validation_pattern.fullmatch(data["request-postcode"]):

            logger.info("Valid postcode", client_ip=self._client_ip)

            attributes = {}
            attributes["postcode"] = data["request-postcode"].upper()
            attributes["display_region"] = 'en'

            session = await get_session(request)
            session["attributes"] = attributes

            raise HTTPFound(self._request.app.router['RequestCodeSelectAddress:get'].url_for())

        else:
            logger.warn("Attempt to use an invalid postcode", client_ip=self._client_ip)
            flash(self._request, POSTCODE_INVALID_MSG)
            raise HTTPFound(self._request.app.router['RequestCode:post'].url_for())


@routes.view('/request-access-code/select-address')
class RequestCodeSelectAddress(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):

        attributes = await self.get_check_attributes(request)

        address_content = await self.get_postcode_return(attributes["postcode"], attributes["display_region"])

        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        await self.get_check_attributes(request)
        data = await request.post()

        form_return = ast.literal_eval(data["request-address-select"])

        session = await get_session(request)
        session["attributes"]["address"] = form_return["address"]
        session["attributes"]["uprn"] = form_return["uprn"]
        session.changed()

        raise HTTPFound(self._request.app.router['RequestCodeConfirmAddress:get'].url_for())


@routes.view('/request-access-code/confirm-address')
class RequestCodeConfirmAddress(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request)
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request)
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

            try:
                uprn_return = await self.get_cases_by_uprn(uprn)
                session["attributes"]["case_id"] = uprn_return[0]["id"]
                session["attributes"]["region"] = uprn_return[0]["region"]
                session.changed()
                raise HTTPFound(self._request.app.router['RequestCodeEnterMobile:get'].url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.warn("Unable to match UPRN", client_ip=self._client_ip)
                    raise HTTPFound(self._request.app.router['RequestCodeNotRequired:get'].url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCode:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Address confirmation error", client_ip=self._client_ip)
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@routes.view('/request-access-code/not-required')
class RequestCodeNotRequired(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request)
        return attributes


@routes.view('/request-access-code/enter-mobile')
class RequestCodeEnterMobile(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request)
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request)
        data = await request.post()

        if RequestCodeCommon.mobile_validation_pattern.fullmatch(data['request-mobile-number']):

            attributes["mobile_number"] = data["request-mobile-number"]
            session = await get_session(request)
            session["attributes"] = attributes

            raise HTTPFound(self._request.app.router['RequestCodeConfirmMobile:get'].url_for())

        else:
            logger.warn("Attempt to use an invalid mobile number", client_ip=self._client_ip)
            flash(self._request, MOBILE_ENTER_MSG)
            raise HTTPFound(self._request.app.router['RequestCodeEnterMobile:post'].url_for())


@routes.view('/request-access-code/confirm-mobile')
class RequestCodeConfirmMobile(RequestCodeCommon):

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request)
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        attributes = await self.get_check_attributes(request)
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
                    await self.request_fulfilment(attributes['case_id'], attributes['mobile_number'],
                                              attributes['fulfilmentCode'])
                except ClientResponseError as ex:
                    raise ex

                raise HTTPFound(self._request.app.router['RequestCodeCodeSent:get'].url_for())
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(self._request.app.router['RequestCodeEnterMobile:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn("Mobile confirmation error", client_ip=self._client_ip)
            flash(request, MOBILE_CHECK_MSG)
            return attributes


@routes.view('/request-access-code/code-sent')
class RequestCodeCodeSent(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        attributes = await self.get_check_attributes(request)
        return attributes
