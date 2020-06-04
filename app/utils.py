import string
import re
import json

from .exceptions import InactiveCaseError, InvalidEqPayLoad, InvalidDataError, InvalidDataErrorWelsh
from aiohttp.web import HTTPFound
from datetime import datetime, timezone

from sdc.crypto.encrypter import encrypt
from .eq import EqPayloadConstructor

from .request import RetryRequest
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


class View:
    valid_display_regions = r'{display_region:\ben|cy|ni\b}'
    valid_user_journeys = r'{user_journey:\bstart|requests\b}'
    valid_sub_user_journeys = r'{sub_user_journey:\bunlinked|household-code|individual-code|access-code\b}'

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
    async def _make_request(request,
                            method,
                            url,
                            auth=None,
                            json=None,
                            return_json=False):
        """
        :param request: The AIOHTTP user request, used for logging and app access
        :param method: The HTTP verb
        :param url: The target URL
        :param auth: Authorization
        :param json: JSON payload to pass as request data
        :param return_json: If True, the response JSON will be returned
        """
        retry_request = RetryRequest(request, method, url, auth, json, return_json)
        return await retry_request.make_request()

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

        await RHService.post_surveylaunched(request, case, adlocation)

        logger.info('redirecting to eq', client_ip=request['client_ip'])
        eq_url = app['EQ_URL']
        raise HTTPFound(f'{eq_url}/session?token={token}')


class ProcessPostcode:
    postcode_validation_pattern = re.compile(
        r'^((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|BX|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}))|BFPO[ ]?\d{1,4}$'  # NOQA
    )

    @staticmethod
    def validate_postcode(postcode, locale):

        for character in string.whitespace + OBSCURE_WHITESPACE:
            postcode = postcode.replace(character, '')

        postcode = postcode.upper()

        if len(postcode) == 0:
            if locale == 'cy':
                # TODO: Add Welsh Translation
                raise InvalidDataErrorWelsh('You have not entered a postcode')
            else:
                raise InvalidDataError('You have not entered a postcode')

        if not postcode.isalnum():
            if locale == 'cy':
                # TODO: Add Welsh Translation
                raise InvalidDataErrorWelsh('The postcode must not contain symbols')
            else:
                raise InvalidDataError('The postcode must not contain symbols')

        if len(postcode) < 5:
            if locale == 'cy':
                # TODO: Add Welsh Translation
                raise InvalidDataErrorWelsh('The postcode does not contain enough characters')
            else:
                raise InvalidDataError('The postcode does not contain enough characters')

        if len(postcode) > 7:
            if locale == 'cy':
                # TODO: Add Welsh Translation
                raise InvalidDataErrorWelsh('The postcode contains too many characters')
            else:
                raise InvalidDataError('The postcode contains too many characters')

        if not ProcessPostcode.postcode_validation_pattern.fullmatch(postcode):
            if locale == 'cy':
                # TODO: Add Welsh Translation
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
                # TODO: Add Welsh Translation
                raise InvalidDataErrorWelsh('The mobile phone number must not contain letters or symbols')
            else:
                raise InvalidDataError('The mobile phone number must not contain letters or symbols')

        return number.lstrip('0')

    @staticmethod
    def validate_uk_mobile_phone_number(number, locale):

        number = ProcessMobileNumber.normalise_phone_number(number, locale).lstrip(uk_prefix).lstrip('0')

        if not number.startswith('7'):
            if locale == 'cy':
                # TODO: Add Welsh Translation
                raise InvalidDataErrorWelsh('The mobile phone number is not a UK mobile number')
            else:
                raise InvalidDataError('The mobile phone number is not a UK mobile number')

        if len(number) > 10:
            if locale == 'cy':
                # TODO: Add Welsh Translation
                raise InvalidDataErrorWelsh('The mobile phone number contains too many digits')
            else:
                raise InvalidDataError('The mobile phone number contains too many digits')

        if len(number) < 10:
            if locale == 'cy':
                # TODO: Add Welsh Translation
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
            # TODO: Add Welsh Translation
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
        ai_epoch = request.app['ADDRESS_INDEX_EPOCH']
        url = f'{ai_svc_url}/addresses/rh/postcode/{postcode}?epoch={ai_epoch}'
        return await View._make_request(request,
                                        'GET',
                                        url,
                                        auth=request.app['ADDRESS_INDEX_SVC_AUTH'],
                                        return_json=True)

    @staticmethod
    async def get_ai_uprn(request, uprn):
        ai_svc_url = request.app['ADDRESS_INDEX_SVC_URL']
        ai_epoch = request.app['ADDRESS_INDEX_EPOCH']
        url = f'{ai_svc_url}/addresses/rh/uprn/{uprn}?addresstype=paf&epoch={ai_epoch}'
        return await View._make_request(request,
                                        'GET',
                                        url,
                                        auth=request.app['ADDRESS_INDEX_SVC_AUTH'],
                                        return_json=True)


class RHService(View):

    @staticmethod
    async def get_cases_by_uprn(request, uprn):
        rhsvc_url = request.app['RHSVC_URL']
        return await View._make_request(request,
                                        'GET',
                                        f'{rhsvc_url}/cases/uprn/{uprn}',
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
                                        auth=request.app['RHSVC_AUTH'],
                                        json=address_json,
                                        return_json=True)

    @staticmethod
    async def get_fulfilment(request, case_type, region,
                             delivery_channel, product_group, individual):
        rhsvc_url = request.app['RHSVC_URL']
        url = f'{rhsvc_url}/fulfilments?caseType={case_type}&region={region}&deliveryChannel={delivery_channel}' \
              f'&productGroup={product_group}&individual={individual}'
        return await View._make_request(request,
                                        'GET',
                                        url,
                                        return_json=True)

    @staticmethod
    async def request_fulfilment(request, case_id, tel_no,
                                 fulfilment_code):
        rhsvc_url = request.app['RHSVC_URL']
        fulfilment_json = {
            'caseId': case_id,
            'telNo': tel_no,
            'fulfilmentCode': fulfilment_code,
            'dateTime': datetime.now(timezone.utc).isoformat()
        }
        url = f'{rhsvc_url}/cases/{case_id}/fulfilments/sms'
        return await View._make_request(request,
                                        'POST',
                                        url,
                                        auth=request.app['RHSVC_AUTH'],
                                        json=fulfilment_json)

    @staticmethod
    async def get_uac_details(request):
        uac_hash = request['uac_hash']
        logger.info('making get request for uac',
                    uac_hash=uac_hash,
                    client_ip=request['client_ip'])
        rhsvc_url = request.app['RHSVC_URL']
        return await View._make_request(request,
                                        'GET',
                                        f'{rhsvc_url}/uacs/{uac_hash}',
                                        auth=request.app['RHSVC_AUTH'],
                                        return_json=True)

    @staticmethod
    async def put_modify_address(request, case, address):
        rhsvc_url = request.app['RHSVC_URL']
        rhsvc_auth = request.app['RHSVC_AUTH']
        case_json = {
            'caseId': case['caseId'],
            'uprn': case['address']['uprn'],
            'addressLine1': address['addressLine1'],
            'addressLine2': address['addressLine2'],
            'addressLine3': address['addressLine3'],
            'townName': address['townName'],
            'postcode': address['postcode']
        }
        return await View._make_request(request,
                                        'PUT',
                                        f'{rhsvc_url}/cases/' +
                                        case['caseId'] + '/address',
                                        auth=rhsvc_auth,
                                        json=case_json)

    @staticmethod
    async def post_surveylaunched(request, case, adlocation):
        if not adlocation:
            adlocation = ''
        launch_json = {
            'questionnaireId': case['questionnaireId'],
            'caseId': case['caseId'],
            'agentId': adlocation
        }
        rhsvc_url = request.app['RHSVC_URL']
        return await View._make_request(request,
                                        'POST',
                                        f'{rhsvc_url}/surveyLaunched',
                                        auth=request.app['RHSVC_AUTH'],
                                        json=launch_json)
