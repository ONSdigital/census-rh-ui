import string
import time
import re
import json
import aiohttp

from aiohttp.client_exceptions import (ClientConnectionError,
                                       ClientConnectorError,
                                       ClientResponseError)
from .exceptions import InactiveCaseError
from .exceptions import InvalidEqPayLoad
from aiohttp.web import HTTPFound

from sdc.crypto.encrypter import encrypt
from .eq import EqPayloadConstructor

from tenacity import retry, stop_after_attempt, retry_if_exception_message, retry_if_exception_type
from structlog import get_logger
logger = get_logger('respondent-home')

OBSCURE_WHITESPACE = (
    '\u180E'  # Mongolian vowel separator
    '\u200B'  # zero width space
    '\u200C'  # zero width non-joiner
    '\u200D'  # zero width joiner
    '\u2060'  # word joiner
    '\uFEFF'  # zero width non-breaking space
)

uk_prefix = '44'
attempts_retry_limit = 5


class View:
    valid_display_regions = r'{display_region:\ben|cy|ni\b}'
    valid_user_journeys = r'{user_journey:\bstart|requests\b}'
    valid_sub_user_journeys = r'{sub_user_journey:\bunlinked|household-code|individual-code\b}'

    @staticmethod
    def setup_request(request):
        request['client_ip'] = request.headers.get('X-Forwarded-For', None)

    @staticmethod
    def log_entry(request, endpoint):
        method = request.method
        logger.info(f"received {method} on endpoint '{endpoint}'",
                    method=request.method,
                    path=request.path)

    @staticmethod
    def _handle_response(response, attempt_number):
        try:
            response.raise_for_status()
        except ClientResponseError as ex:
            if ex.status == 503:
                if attempt_number < attempts_retry_limit:
                    logger.warn('503 returned. Could be during service scale back',
                                url=response.url,
                                status_code=response.status,
                                attempt_number=attempt_number)
                else:
                    logger.error('503 returned. Giving up retries',
                                 url=response.url,
                                 status_code=response.status)
            elif not ex.status == 404:
                logger.error('error in response',
                             url=response.url,
                             status_code=response.status)
            raise ex
        else:
            logger.debug('successfully connected to service',
                         url=str(response.url))

    @staticmethod
    @retry(reraise=True, stop=stop_after_attempt(attempts_retry_limit), retry=(
            retry_if_exception_message(match='503.*') | retry_if_exception_type((ClientConnectionError,
                                                                                ClientConnectorError))))
    async def _make_request(request,
                            method,
                            url,
                            func,
                            auth=None,
                            json=None,
                            return_json=False):
        """
        :param request: The AIOHTTP user request, used for logging and app access
        :param method: The HTTP verb
        :param url: The target URL
        :param auth: Authorization
        :param json: JSON payload to pass as request data
        :param func: Function to call on the response
        :param return_json: If True, the response JSON will be returned
        """
        logger.debug('making request with handler',
                     method=method,
                     url=url,
                     handler=func.__name__)

        attempt_number = View._make_request.retry.statistics['attempt_number']
        try:
            if attempt_number > 1:
                # sleep with a rising sleep time as the attempt numbers grow, starting at 0 seconds.
                wait_exp = float(request.app['WAIT_BEFORE_RETRY_EXPONENT'])
                base = attempt_number - 1
                wait_secs = 0 if (wait_exp == 0 or base == 0) else (base ** wait_exp)
                logger.info('retrying using basic connection', attempt_number=attempt_number, wait_secs=wait_secs)
                time.sleep(wait_secs)
                # basic request without keep-alive to avoid terminating service.
                async with aiohttp.request(
                        method, url, auth=auth, json=json) as resp:
                    func(resp, attempt_number)
                    if return_json:
                        return await resp.json()
                    else:
                        return None
            else:
                # normal path. pooled ; keep-alive request for performance
                async with request.app.http_session_pool.request(
                        method, url, auth=auth, json=json, ssl=False) as resp:
                    func(resp, attempt_number)
                    if return_json:
                        return await resp.json()
                    else:
                        return None
        except (ClientConnectionError, ClientConnectorError) as ex:
            if attempt_number < attempts_retry_limit:
                logger.warn('client failed to connect, could be during service scale back',
                            url=url,
                            client_ip=request['client_ip'],
                            attempt_number=attempt_number)
            else:
                logger.error('client failed to connect. Giving up retries',
                             url=url,
                             client_ip=request['client_ip'])
            raise ex

    @staticmethod
    def validate_case(case_json):
        if not case_json.get('active', False):
            raise InactiveCaseError(case_json.get('caseType'))
        if not case_json.get('caseStatus', None) == 'OK':
            raise InvalidEqPayLoad('CaseStatus is not OK')

    async def call_questionnaire(self, request, case, attributes, app,
                                 adlocation):
        eq_payload = await EqPayloadConstructor(case, attributes, app,
                                                adlocation).build()

        token = encrypt(eq_payload,
                        key_store=app['key_store'],
                        key_purpose='authentication')

        await self.post_surveylaunched(request, case, adlocation)

        logger.info('redirecting to eq', client_ip=request['client_ip'])
        eq_url = app['EQ_URL']
        raise HTTPFound(f'{eq_url}/session?token={token}')

    async def post_surveylaunched(self, request, case, adlocation):
        if not adlocation:
            adlocation = ''
        launch_json = {
            'questionnaireId': case['questionnaireId'],
            'caseId': case['caseId'],
            'agentId': adlocation
        }
        rhsvc_url = request.app['RHSVC_URL']
        return await self._make_request(request,
                                        'POST',
                                        f'{rhsvc_url}/surveyLaunched',
                                        self._handle_response,
                                        auth=request.app['RHSVC_AUTH'],
                                        json=launch_json)


class InvalidDataError(Exception):

    def __init__(self, message=None):
        super().__init__(message or 'The supplied value is invalid')


class InvalidDataErrorWelsh(Exception):

    def __init__(self, message=None):
        super().__init__(message or 'WELSH The supplied value is invalid')


class ProcessPostcode:

    postcode_validation_pattern = re.compile(
        r'^((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|BX|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}))|BFPO[ ]?\d{1,4}$'  # NOQA
    )

    @staticmethod
    def validate_postcode(postcode, locale):

        for character in string.whitespace + OBSCURE_WHITESPACE:
            postcode = postcode.replace(character, '')

        postcode = postcode.upper()

        if not postcode.isalnum():
            if locale == 'cy':
                raise InvalidDataErrorWelsh('The postcode must not contain symbols')
            else:
                raise InvalidDataError('The postcode must not contain symbols')

        if len(postcode) < 5:
            if locale == 'cy':
                raise InvalidDataErrorWelsh('The postcode does not contain enough characters')
            else:
                raise InvalidDataError('The postcode does not contain enough characters')

        if len(postcode) > 7:
            if locale == 'cy':
                raise InvalidDataErrorWelsh('The postcode contains too many characters')
            else:
                raise InvalidDataError('The postcode contains too many characters')

        if not ProcessPostcode.postcode_validation_pattern.fullmatch(postcode):
            if locale == 'cy':
                raise InvalidDataErrorWelsh('The postcode is not a valid UK postcode')
            else:
                raise InvalidDataError('The postcode is not a valid UK postcode')

        postcode_formatted = postcode[:-3] + ' ' + postcode[-3:]

        return postcode_formatted


class ProcessMobileNumber:

    @staticmethod
    def normalise_phone_number(number, locale):

        for character in string.whitespace + OBSCURE_WHITESPACE + '()-+':
            number = number.replace(character, '')

        try:
            list(map(int, number))
        except ValueError:
            if locale == 'cy':
                raise InvalidDataErrorWelsh('The mobile phone number must not contain letters or symbols')
            else:
                raise InvalidDataError('The mobile phone number must not contain letters or symbols')

        return number.lstrip('0')

    @staticmethod
    def validate_uk_mobile_phone_number(number, locale):

        number = ProcessMobileNumber.normalise_phone_number(number, locale).lstrip(uk_prefix).lstrip('0')

        if not number.startswith('7'):
            if locale == 'cy':
                raise InvalidDataErrorWelsh('The mobile phone number is not a UK mobile number')
            else:
                raise InvalidDataError('The mobile phone number is not a UK mobile number')

        if len(number) > 10:
            if locale == 'cy':
                raise InvalidDataErrorWelsh('The mobile phone number contains too many digits')
            else:
                raise InvalidDataError('The mobile phone number contains too many digits')

        if len(number) < 10:
            if locale == 'cy':
                raise InvalidDataErrorWelsh('The mobile phone number does not contain enough digits')
            else:
                raise InvalidDataError('The mobile phone number does not contain enough digits')

        return '{}{}'.format(uk_prefix, number)


class FlashMessage:

    @staticmethod
    def generate_flash_message(text, level, message_type, field):
        json_return = {'text': text, 'level': level, 'type': message_type, 'field': field}
        return json_return


class AddressIndex(View):

    @staticmethod
    async def get_postcode_return(request, postcode, display_region):
        postcode_return = await AddressIndex.get_ai_postcode(request, postcode)

        address_options = []

        if display_region == 'cy':
            cannot_find_text = 'I cannot find my address'
        else:
            cannot_find_text = 'I cannot find my address'

        for singleAddress in postcode_return['response']['addresses']:
            address_options.append({
                'value':
                json.dumps({
                    'uprn': singleAddress['uprn'],
                    'address': singleAddress['formattedAddress']
                }),
                'label': {
                    'text': singleAddress['formattedAddress']
                },
                'id':
                singleAddress['uprn']
            })

        address_options.append({
            'value':
            json.dumps({
                'uprn': 'xxxx',
                'address': cannot_find_text
            }),
            'label': {
                'text': cannot_find_text
            },
            'id': 'xxxx'
        })

        address_content = {
            'postcode': postcode,
            'addresses': address_options,
            'total_matches': postcode_return['response']['total']
        }

        return address_content

    @staticmethod
    async def get_ai_postcode(request, postcode):
        ai_svc_url = request.app['ADDRESS_INDEX_SVC_URL']
        url = f'{ai_svc_url}/addresses/rh/postcode/{postcode}'
        return await View._make_request(request,
                                        'GET',
                                        url,
                                        View._handle_response,
                                        auth=request.app['ADDRESS_INDEX_SVC_AUTH'],
                                        return_json=True)

    @staticmethod
    async def get_ai_uprn(request, uprn):
        ai_svc_url = request.app['ADDRESS_INDEX_SVC_URL']
        url = f'{ai_svc_url}/addresses/rh/uprn/{uprn}?addresstype=paf'
        return await View._make_request(request,
                                        'GET',
                                        url,
                                        View._handle_response,
                                        auth=request.app['ADDRESS_INDEX_SVC_AUTH'],
                                        return_json=True)


class RHService(View):

    @staticmethod
    async def get_cases_by_uprn(request, uprn):
        rhsvc_url = request.app['RHSVC_URL']
        return await View._make_request(request,
                                        'GET',
                                        f'{rhsvc_url}/cases/uprn/{uprn}',
                                        View._handle_response,
                                        return_json=True)

    @staticmethod
    async def post_unlinked_uac(request, uac, address):
        uac_hash = uac
        logger.info('request linked case',
                    uac_hash=uac_hash,
                    client_ip=request['client_ip'])
        rhsvc_url = request.app['RHSVC_URL']
        address_json = {
            "addressLine1": address['addressLine1'],
            "addressLine2": address['addressLine2'],
            "addressLine3": address['addressLine3'],
            "townName": address['townName'],
            "region": address['countryCode'],
            "postcode": address['postcode'],
            "uprn": address['uprn'],
            "estabType": address['censusEstabType'],
            "addressType": address['censusAddressType']
        }
        url = f'{rhsvc_url}/uacs/{uac_hash}/link'
        return await View._make_request(request,
                                        'POST',
                                        url,
                                        View._handle_response,
                                        auth=request.app['RHSVC_AUTH'],
                                        json=address_json,
                                        return_json=True)
