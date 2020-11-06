import string
import re
import json

from .exceptions import InactiveCaseError, InvalidEqPayLoad, InvalidDataError, InvalidDataErrorWelsh
from aiohttp.web import HTTPFound
from datetime import datetime, timezone

from sdc.crypto.encrypter import encrypt
from .eq import EqPayloadConstructor
from .flash import flash
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
    valid_ew_display_regions = r'{display_region:\ben|cy\b}'
    valid_user_journeys = r'{user_journey:\bstart|requests\b}'
    valid_sub_user_journeys = r'{sub_user_journey:\bunlinked|change-address|individual-code|access-code|paper-form\b}'

    @staticmethod
    def setup_request(request):
        request['client_ip'] = request.headers.get('X-Forwarded-For', None)

    @staticmethod
    def single_client_ip(request):
        if request['client_ip']:
            single_ip = request['client_ip'].split(',', 1)[0]
        elif request.headers.get('Origin', None) and 'localhost' in request.headers.get('Origin', None):
            single_ip = '127.0.0.1'
        else:
            single_ip = ''
        return single_ip

    @staticmethod
    def log_entry(request, endpoint):
        method = request.method
        logger.info(f"received {method} on endpoint '{endpoint}'",
                    method=request.method,
                    path=request.path)

    @staticmethod
    def gen_page_url(request):
        full_url = str(request.rel_url)
        if full_url[:3] == '/en' or full_url[:3] == '/cy' or full_url[:3] == '/ni':
            generic_url = full_url[3:]
        else:
            generic_url = full_url
        return generic_url

    @staticmethod
    def get_call_centre_number(display_region):
        if display_region == 'ni':
            call_centre_number = '0800 328 2021'
        elif display_region == 'cy':
            call_centre_number = '0800 169 2021'
        else:
            call_centre_number = '0800 141 2021'
        return call_centre_number

    @staticmethod
    def get_campaign_site_link(request, display_region, requested_link):
        base_en = request.app['DOMAIN_URL_PROTOCOL'] + request.app['DOMAIN_URL_EN']
        base_cy = request.app['DOMAIN_URL_PROTOCOL'] + request.app['DOMAIN_URL_CY']
        base_ni = request.app['DOMAIN_URL_PROTOCOL'] + request.app['DOMAIN_URL_EN'] + '/ni'

        link = '/'

        if requested_link == 'census-home':
            if display_region == 'ni':
                link = base_ni
            elif display_region == 'cy':
                link = base_cy
            else:
                link = base_en
        elif requested_link == 'contact-us':
            if display_region == 'ni':
                link = base_ni + '/contact-us'
            elif display_region == 'cy':
                link = base_cy + '/cysylltu-a-ni'
            else:
                link = base_en + '/contact-us'

        return link

    @staticmethod
    async def _make_request(request,
                            method,
                            url,
                            auth=None,
                            headers=None,
                            request_json=None,
                            return_json=False):
        """
        :param request: The AIOHTTP user request, used for logging and app access
        :param method: The HTTP verb
        :param url: The target URL
        :param auth: Authorization
        :param headers: Any needed headers as a python dictionary
        :param request_json: JSON payload to pass as request data
        :param return_json: If True, the response JSON will be returned
        """
        retry_request = RetryRequest(request, method, url, auth, headers, request_json, return_json)
        return await retry_request.make_request()

    @staticmethod
    def validate_case(case_json):
        if not case_json.get('active', False):
            raise InactiveCaseError(case_json.get('caseType'))
        if not case_json.get('caseStatus', None) == 'OK':
            raise InvalidEqPayLoad('CaseStatus is not OK')

    @staticmethod
    async def call_questionnaire(request, case, attributes, app, adlocation):
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
                raise InvalidDataErrorWelsh("Nid ydych wedi nodi cod post")
            else:
                raise InvalidDataError('You have not entered a postcode')

        if not postcode.isalnum():
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Ni ddylai'r cod post gynnwys symbolau")
            else:
                raise InvalidDataError('The postcode must not contain symbols')

        if len(postcode) < 5:
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Nid yw'r cod post yn cynnwys digon o nodau")
            else:
                raise InvalidDataError('The postcode does not contain enough characters')

        if len(postcode) > 7:
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Mae'r cod post yn cynnwys gormod o nodau")
            else:
                raise InvalidDataError('The postcode contains too many characters')

        if not ProcessPostcode.postcode_validation_pattern.fullmatch(postcode):
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Nid yw'r cod post yn god post dilys yn y Deyrnas Unedig")
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
                raise InvalidDataErrorWelsh('Enter a UK mobile number in a valid format, for example, '
                                            '07700 900345 or +44 7700 900345', message_type='invalid')
            else:
                raise InvalidDataError('Enter a UK mobile number in a valid format, for example, '
                                       '07700 900345 or +44 7700 900345', message_type='invalid')

        return number.lstrip('0')

    @staticmethod
    def validate_uk_mobile_phone_number(number, locale):

        number = ProcessMobileNumber.normalise_phone_number(number, locale).lstrip(uk_prefix).lstrip('0')

        if len(number) == 0:
            if locale == 'cy':
                # TODO: Add Welsh Translation
                raise InvalidDataErrorWelsh('Enter your mobile number', message_type='empty')
            else:
                raise InvalidDataError('Enter your mobile number', message_type='empty')

        if not number.startswith('7'):
            if locale == 'cy':
                # TODO: Add Welsh Translation
                raise InvalidDataErrorWelsh('Enter a UK mobile number in a valid format, for example, '
                                            '07700 900345 or +44 7700 900345', message_type='invalid')
            else:
                raise InvalidDataError('Enter a UK mobile number in a valid format, for example, '
                                       '07700 900345 or +44 7700 900345', message_type='invalid')

        if len(number) > 10:
            if locale == 'cy':
                # TODO: Add Welsh Translation
                raise InvalidDataErrorWelsh('Enter a UK mobile number in a valid format, for example, '
                                            '07700 900345 or +44 7700 900345', message_type='invalid')
            else:
                raise InvalidDataError('Enter a UK mobile number in a valid format, for example, '
                                       '07700 900345 or +44 7700 900345', message_type='invalid')

        if len(number) < 10:
            if locale == 'cy':
                # TODO: Add Welsh Translation
                raise InvalidDataErrorWelsh('Enter a UK mobile number in a valid format, for example, '
                                            '07700 900345 or +44 7700 900345', message_type='invalid')
            else:
                raise InvalidDataError('Enter a UK mobile number in a valid format, for example, '
                                       '07700 900345 or +44 7700 900345', message_type='invalid')

        return '{}{}'.format(uk_prefix, number)


class ProcessName:

    @staticmethod
    def validate_name(request, data, display_region):

        name_valid = True

        if not (data.get('name_first_name')):
            if display_region == 'cy':
                # TODO Add Welsh Translation
                flash(request, FlashMessage.generate_flash_message('Enter your first name',
                                                                   'ERROR', 'NAME_ENTER_ERROR', 'name_first_name'))
            else:
                flash(request, FlashMessage.generate_flash_message('Enter your first name',
                                                                   'ERROR', 'NAME_ENTER_ERROR', 'name_first_name'))
            name_valid = False

        if not (data.get('name_last_name')):
            if display_region == 'cy':
                # TODO Add Welsh Translation
                flash(request, FlashMessage.generate_flash_message('Enter your last name',
                                                                   'ERROR', 'NAME_ENTER_ERROR', 'name_last_name'))
            else:
                flash(request, FlashMessage.generate_flash_message('Enter your last name',
                                                                   'ERROR', 'NAME_ENTER_ERROR', 'name_last_name'))
            name_valid = False

        return name_valid


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
    async def get_case_by_uprn(request, uprn):
        rhsvc_url = request.app['RHSVC_URL']
        return await View._make_request(request,
                                        'GET',
                                        f'{rhsvc_url}/cases/uprn/{uprn}',
                                        return_json=True)

    @staticmethod
    async def post_link_uac(request, uac, address):
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
                                        request_json=address_json,
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
    async def request_fulfilment_sms(request, case_id, tel_no, fulfilment_code_array):
        rhsvc_url = request.app['RHSVC_URL']
        fulfilment_json = {
            'caseId': case_id,
            'telNo': tel_no,
            'fulfilmentCodes': fulfilment_code_array,
            'dateTime': datetime.now(timezone.utc).isoformat(),
            'clientIP': View.single_client_ip(request)
        }
        url = f'{rhsvc_url}/cases/{case_id}/fulfilments/sms'
        return await View._make_request(request,
                                        'POST',
                                        url,
                                        auth=request.app['RHSVC_AUTH'],
                                        request_json=fulfilment_json)

    @staticmethod
    async def request_fulfilment_post(request, case_id, first_name, last_name, fulfilment_code_array, title=None):
        rhsvc_url = request.app['RHSVC_URL']
        if title:
            fulfilment_json = {
                'caseId': case_id,
                'title': title,
                'forename': first_name,
                'surname': last_name,
                'fulfilmentCodes': fulfilment_code_array,
                'dateTime': datetime.now(timezone.utc).isoformat(),
                'clientIP': View.single_client_ip(request)
            }
        else:
            fulfilment_json = {
                'caseId': case_id,
                'forename': first_name,
                'surname': last_name,
                'fulfilmentCodes': fulfilment_code_array,
                'dateTime': datetime.now(timezone.utc).isoformat(),
                'clientIP': View.single_client_ip(request)
            }
        url = f'{rhsvc_url}/cases/{case_id}/fulfilments/post'
        return await View._make_request(request,
                                        'POST',
                                        url,
                                        auth=request.app['RHSVC_AUTH'],
                                        request_json=fulfilment_json)

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
    async def post_case_create(request, address):
        rhsvc_url = request.app['RHSVC_URL']
        rhsvc_auth = request.app['RHSVC_AUTH']
        case_json = {
            'uprn': address['uprn'],
            'addressLine1': address['addressLine1'],
            'addressLine2': address['addressLine2'],
            'addressLine3': address['addressLine3'],
            'townName': address['townName'],
            'postcode': address['postcode'],
            'region': address['countryCode'],
            'estabType': address['censusEstabType'],
            'addressType': address['censusAddressType']
        }
        return await View._make_request(request,
                                        'POST',
                                        f'{rhsvc_url}/cases/create',
                                        auth=rhsvc_auth,
                                        request_json=case_json,
                                        return_json=True)

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
                                        request_json=launch_json)


class ADLookUp(View):

    @staticmethod
    async def get_ad_lookup_by_postcode(request, postcode):
        ai_svc_url = request.app['AD_LOOK_UP_SVC_URL']
        url = f'{ai_svc_url}/centres/postcode?postcode={postcode}&limit=10'
        headers = {'x-api-key': request.app['AD_LOOK_UP_SVC_APIKEY'],
                   'x-app-id': request.app['AD_LOOK_UP_SVC_APPID']}
        return await View._make_request(request,
                                        'GET',
                                        url,
                                        auth=request.app['AD_LOOK_UP_SVC_AUTH'],
                                        headers=headers,
                                        return_json=True)
