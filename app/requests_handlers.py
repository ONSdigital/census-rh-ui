import aiohttp_jinja2
import re
import json

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from aiohttp_session import get_session
from datetime import datetime, timezone
from structlog import get_logger

from . import (ADDRESS_CHECK_MSG,
               MOBILE_ENTER_MSG, MOBILE_CHECK_MSG, POSTCODE_INVALID_MSG,
               ADDRESS_SELECT_CHECK_MSG,
               ADDRESS_CHECK_MSG_CY,
               MOBILE_ENTER_MSG_CY,
               MOBILE_CHECK_MSG_CY, POSTCODE_INVALID_MSG_CY,
               ADDRESS_SELECT_CHECK_MSG_CY)

from .flash import flash
from .utils import View

logger = get_logger('respondent-home')
requests_routes = RouteTableDef()


class RequestCodeCommon(View):

    @staticmethod
    def request_code_check_session(request, fulfillment_type,
                                   display_region):
        if request.cookies.get('RH_SESSION') is None:
            logger.info('session timed out', client_ip=request['client_ip'])
            raise HTTPFound(
                request.app.router['RequestCodeTimeout' + fulfillment_type +
                                   display_region + ':get'].url_for())

    async def get_check_attributes(self, request, fulfillment_type,
                                   display_region):
        self.request_code_check_session(request, fulfillment_type,
                                        display_region)
        session = await get_session(request)
        try:
            attributes = session['attributes']

        except KeyError:
            raise HTTPFound(
                request.app.router['RequestCodeTimeout' + fulfillment_type +
                                   display_region + ':get'].url_for())

        return attributes

    async def get_postcode_return(self, request, postcode, fulfillment_type,
                                  display_region, locale):
        postcode_return = await self.get_ai_postcode(request, postcode)

        address_options = []

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

        address_content = {
            'postcode': postcode,
            'addresses': address_options,
            'display_region': display_region,
            'locale': locale,
            'fulfillment_type': fulfillment_type,
            'total_matches': postcode_return['response']['total']
        }

        return address_content

    postcode_validation_pattern = re.compile(
        r'^((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|BX|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}))|BFPO[ ]?\d{1,4}$'  # NOQA
    )
    mobile_validation_pattern = re.compile(
        r'^(\+44\s?7(\d ?){3}|\(?07(\d ?){3}\)?)\s?(\d ?){3}\s?(\d ?){3}$')

    @staticmethod
    async def get_postcode(request, data, fulfillment_type,
                           display_region, locale):
        postcode_value = data['request-postcode'].upper().strip()
        postcode_value = re.sub(' +', ' ', postcode_value)
        if RequestCodeCommon.postcode_validation_pattern.fullmatch(
                postcode_value):

            logger.info('valid postcode', client_ip=request['client_ip'])

            attributes = {
                'postcode': postcode_value,
                'display_region': display_region.lower(),
                'locale': locale,
                'fulfillment_type': fulfillment_type
            }

            session = await get_session(request)
            session['attributes'] = attributes

            raise HTTPFound(
                request.app.router['RequestCodeSelectAddress' +
                                   fulfillment_type + display_region +
                                   ':get'].url_for())

        else:
            logger.info('attempt to use an invalid postcode',
                        client_ip=request['client_ip'])
            if display_region == 'CY':
                flash(request, POSTCODE_INVALID_MSG_CY)
            else:
                flash(request, POSTCODE_INVALID_MSG)
            raise HTTPFound(
                request.app.router['RequestCodeEnterAddress' +
                                   fulfillment_type + display_region +
                                   ':get'].url_for())

    @staticmethod
    async def post_enter_mobile(request, attributes, data):
        mobile_number = re.sub(' +', ' ', data['request-mobile-number'].strip())
        if RequestCodeCommon.mobile_validation_pattern.fullmatch(
                mobile_number):

            logger.info('valid mobile number',
                        client_ip=request['client_ip'])

            attributes['mobile_number'] = mobile_number
            session = await get_session(request)
            session['attributes'] = attributes

            raise HTTPFound(
                request.app.router['RequestCodeConfirmMobile' +
                                   attributes['fulfillment_type'] +
                                   attributes['display_region'].upper() +
                                   ':get'].url_for())

        else:
            logger.info('attempt to use an invalid mobile phone number',
                        client_ip=request['client_ip'])
            if attributes['display_region'] == 'cy':
                flash(request, MOBILE_ENTER_MSG_CY)
            else:
                flash(request, MOBILE_ENTER_MSG)
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobile' +
                                   attributes['fulfillment_type'] +
                                   attributes['display_region'].upper() +
                                   ':post'].url_for())

    async def get_ai_postcode(self, request, postcode):
        ai_svc_url = request.app['ADDRESS_INDEX_SVC_URL']
        url = f'{ai_svc_url}/addresses/postcode/{postcode}'
        return await self._make_request(request,
                                        'GET',
                                        url,
                                        self._handle_response,
                                        return_json=True)

    async def get_cases_by_uprn(self, request, uprn):
        rhsvc_url = request.app['RHSVC_URL']
        return await self._make_request(request,
                                        'GET',
                                        f'{rhsvc_url}/cases/uprn/{uprn}',
                                        self._handle_response,
                                        return_json=True)

    async def get_fulfilment(self, request, case_type, region,
                             delivery_channel):
        rhsvc_url = request.app['RHSVC_URL']
        url = f'{rhsvc_url}/fulfilments?caseType={case_type}&region={region}&deliveryChannel={delivery_channel}'
        return await self._make_request(request,
                                        'GET',
                                        url,
                                        self._handle_response,
                                        return_json=True)

    async def request_fulfilment(self, request, case_id, tel_no,
                                 fulfilment_code):
        rhsvc_url = request.app['RHSVC_URL']
        fulfilment_json = {
            'caseId': case_id,
            'telNo': tel_no,
            'fulfilmentCode': fulfilment_code,
            'dateTime': datetime.now(timezone.utc).isoformat()
        }
        url = f'{rhsvc_url}/cases/{case_id}/fulfilments/sms'
        return await self._make_request(request,
                                        'POST',
                                        url,
                                        self._handle_response,
                                        auth=request.app['RHSVC_AUTH'],
                                        json=fulfilment_json)


@requests_routes.view('/request-access-code')
class RequestCodeHouseholdEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-household.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code')
        return {
            'display_region': 'en',
            'page_title': 'Request a new access code'
        }


@requests_routes.view('/gofyn-am-god-mynediad')
class RequestCodeHouseholdCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-household.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code')
        return {
            'display_region': 'cy',
            'locale': 'cy',
            'page_title': 'Gofyn am god mynediad newydd'
        }


@requests_routes.view('/ni/request-access-code')
class RequestCodeHouseholdNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-household.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code')
        return {
            'display_region': 'ni',
            'page_title': 'Request a new access code'
        }


@requests_routes.view('/request-access-code/enter-address')
class RequestCodeEnterAddressHHEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-address')
        return {
            'display_region': 'en',
            'page_title': 'What is your postcode?'
        }

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-address')
        data = await request.post()
        await RequestCodeCommon.get_postcode(request, data, 'HH', 'EN',
                                             'en')


@requests_routes.view('/gofyn-am-god-mynediad/nodi-cyfeiriad')
class RequestCodeEnterAddressHHCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-address')
        return {
            'display_region': 'cy',
            'locale': 'cy',
            'page_title': 'Beth yw eich cod post?'
        }

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-address')
        data = await request.post()
        await RequestCodeCommon.get_postcode(request, data, 'HH', 'CY',
                                             'cy')


@requests_routes.view('/ni/request-access-code/enter-address')
class RequestCodeEnterAddressHHNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-address')
        return {
            'display_region': 'ni',
            'page_title': 'What is your postcode?'
        }

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-address')
        data = await request.post()
        await RequestCodeCommon.get_postcode(request, data, 'HH', 'NI',
                                             'en')


@requests_routes.view('/request-access-code/select-address')
class RequestCodeSelectAddressHHEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/select-address')
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        address_content = await self.get_postcode_return(
            request, attributes['postcode'], attributes['fulfillment_type'],
            attributes['display_region'], attributes['locale'])
        address_content['page_title'] = 'Select your address'
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/select-address')
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        data = await request.post()

        try:
            form_return = json.loads(data['request-address-select'])
        except KeyError:
            logger.info('no address selected', client_ip=request['client_ip'])
            flash(request, ADDRESS_SELECT_CHECK_MSG)
            address_content = await self.get_postcode_return(
                request, attributes['postcode'],
                attributes['fulfillment_type'], attributes['display_region'],
                attributes['locale'])
            address_content['page_title'] = 'Select your address'
            return address_content

        session = await get_session(request)
        session['attributes']['address'] = form_return['address']
        session['attributes']['uprn'] = form_return['uprn']
        session.changed()
        logger.info('session updated', client_ip=request['client_ip'])

        raise HTTPFound(
            request.app.router['RequestCodeConfirmAddressHHEN:get'].url_for())


@requests_routes.view('/gofyn-am-god-mynediad/dewis-cyfeiriad')
class RequestCodeSelectAddressHHCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/select-address')
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        address_content = await self.get_postcode_return(
            request, attributes['postcode'], attributes['fulfillment_type'],
            attributes['display_region'], attributes['locale'])
        address_content['page_title'] = 'Dewiswch eich cyfeiriad'
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/select-address')
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        data = await request.post()

        try:
            form_return = json.loads(data['request-address-select'])
        except KeyError:
            logger.info('no address selected', client_ip=request['client_ip'])
            flash(request, ADDRESS_SELECT_CHECK_MSG_CY)
            address_content = await self.get_postcode_return(
                request, attributes['postcode'],
                attributes['fulfillment_type'], attributes['display_region'],
                attributes['locale'])
            address_content['page_title'] = 'Dewiswch eich cyfeiriad'
            return address_content

        session = await get_session(request)
        session['attributes']['address'] = form_return['address']
        session['attributes']['uprn'] = form_return['uprn']
        session.changed()
        logger.info('session updated', client_ip=request['client_ip'])

        raise HTTPFound(
            request.app.router['RequestCodeConfirmAddressHHCY:get'].url_for())


@requests_routes.view('/ni/request-access-code/select-address')
class RequestCodeSelectAddressHHNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/select-address')
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        address_content = await self.get_postcode_return(
            request, attributes['postcode'], attributes['fulfillment_type'],
            attributes['display_region'], attributes['locale'])
        address_content['page_title'] = 'Select your address'
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/select-address')
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        data = await request.post()

        try:
            form_return = json.loads(data['request-address-select'])
        except KeyError:
            logger.info('no address selected', client_ip=request['client_ip'])
            flash(request, ADDRESS_SELECT_CHECK_MSG)
            address_content = await self.get_postcode_return(
                request, attributes['postcode'],
                attributes['fulfillment_type'], attributes['display_region'],
                attributes['locale'])
            address_content['page_title'] = 'Select your address'
            return address_content

        session = await get_session(request)
        session['attributes']['address'] = form_return['address']
        session['attributes']['uprn'] = form_return['uprn']
        session.changed()
        logger.info('session updated', client_ip=request['client_ip'])

        raise HTTPFound(
            request.app.router['RequestCodeConfirmAddressHHNI:get'].url_for())


@requests_routes.view('/request-access-code/confirm-address')
class RequestCodeConfirmAddressHHEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        attributes['page_title'] = 'Is this address correct?'
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        attributes['page_title'] = 'Is this address correct?'
        data = await request.post()

        try:
            address_confirmation = data['request-address-confirmation']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session['attributes']['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(request, uprn)
                session['attributes']['case_id'] = uprn_return[0]['caseId']
                session['attributes']['region'] = uprn_return[0]['region']
                session.changed()
                raise HTTPFound(
                    request.app.router['RequestCodeEnterMobileHHEN:get'].
                    url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.info('unable to match uprn',
                                client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['RequestCodeNotRequiredHHEN:get'].
                        url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterAddressHHEN:get'].url_for(
                ))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@requests_routes.view('/gofyn-am-god-mynediad/cadarnhau-cyfeiriad')
class RequestCodeConfirmAddressHHCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        attributes['page_title'] = "Ydy'r cyfeiriad hwn yn gywir?"
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        attributes['page_title'] = "Ydy'r cyfeiriad hwn yn gywir?"
        data = await request.post()

        try:
            address_confirmation = data['request-address-confirmation']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session['attributes']['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(request, uprn)
                session['attributes']['case_id'] = uprn_return[0]['caseId']
                session['attributes']['region'] = uprn_return[0]['region']
                session.changed()
                raise HTTPFound(
                    request.app.router['RequestCodeEnterMobileHHCY:get'].
                    url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.info('unable to match uprn',
                                client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['RequestCodeNotRequiredHHCY:get'].
                        url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterAddressHHCY:get'].url_for(
                ))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes


@requests_routes.view('/ni/request-access-code/confirm-address')
class RequestCodeConfirmAddressHHNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        attributes['page_title'] = 'Is this address correct?'
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        attributes['page_title'] = 'Is this address correct?'
        data = await request.post()
        try:
            address_confirmation = data['request-address-confirmation']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session['attributes']['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(request, uprn)
                session['attributes']['case_id'] = uprn_return[0]['caseId']
                session['attributes']['region'] = uprn_return[0]['region']
                session.changed()
                raise HTTPFound(
                    request.app.router['RequestCodeEnterMobileHHNI:get'].
                    url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.info('unable to match uprn',
                                client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['RequestCodeNotRequiredHHNI:get'].
                        url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterAddressHHNI:get'].url_for(
                ))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@requests_routes.view('/request-access-code/not-required')
class RequestCodeNotRequiredHHEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/not-required')
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        attributes[
            'page_title'] = 'Your address is not part of the 2019 rehearsal'
        return attributes


@requests_routes.view('/gofyn-am-god-mynediad/dim-angen')
class RequestCodeNotRequiredHHCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/not-required')
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        attributes[
            'page_title'] = 'Nid yw eich cyfeiriad yn rhan o ymarfer 2019'
        return attributes


@requests_routes.view('/ni/request-access-code/not-required')
class RequestCodeNotRequiredHHNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/not-required')
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        attributes[
            'page_title'] = 'Your address is not part of the 2019 rehearsal'
        return attributes


@requests_routes.view('/request-access-code/enter-mobile')
class RequestCodeEnterMobileHHEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        attributes['page_title'] = 'What is your mobile phone number?'
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        attributes['page_title'] = 'What is your mobile phone number?'
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(request, attributes,
                                                  data)


@requests_routes.view('/gofyn-am-god-mynediad/nodi-rhif-ffon-symudol')
class RequestCodeEnterMobileHHCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        attributes['page_title'] = 'Beth yw eich rhif ffôn symudol?'
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        attributes['page_title'] = 'Beth yw eich rhif ffôn symudol?'
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(request, attributes,
                                                  data)


@requests_routes.view('/ni/request-access-code/enter-mobile')
class RequestCodeEnterMobileHHNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        attributes['page_title'] = 'What is your mobile phone number?'
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        attributes['page_title'] = 'What is your mobile phone number?'
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(request, attributes,
                                                  data)


@requests_routes.view('/request-access-code/confirm-mobile')
class RequestCodeConfirmMobileHHEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        attributes['page_title'] = 'Is this mobile phone number correct?'
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        attributes['page_title'] = 'Is this mobile phone number correct?'
        data = await request.post()
        try:
            mobile_confirmation = data['request-mobile-confirmation']
        except KeyError:
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG)
            return attributes

        if mobile_confirmation == 'yes':

            try:
                available_fulfilments = await self.get_fulfilment(
                    request,
                    'HH', attributes['region'], 'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == 'eng':
                            attributes['fulfilmentCode'] = fulfilment[
                                'fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0][
                        'fulfilmentCode']

                try:
                    await self.request_fulfilment(request,
                                                  attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except (KeyError, ClientResponseError) as ex:
                    raise ex

                raise HTTPFound(
                    request.app.router['RequestCodeCodeSentHHEN:get'].url_for(
                    ))
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobileHHEN:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG)
            return attributes


@requests_routes.view('/gofyn-am-god-mynediad/cadarnhau-rhif-ffon-symudol')
class RequestCodeConfirmMobileHHCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        attributes['page_title'] = "Ydy'r rhif ffôn symudol hwn yn gywir?"
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        attributes['page_title'] = "Ydy'r rhif ffôn symudol hwn yn gywir?"
        data = await request.post()

        try:
            mobile_confirmation = data['request-mobile-confirmation']
        except KeyError:
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG_CY)
            return attributes

        if mobile_confirmation == 'yes':

            try:
                available_fulfilments = await self.get_fulfilment(
                    request,
                    'HH', attributes['region'], 'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == 'wel':
                            attributes['fulfilmentCode'] = fulfilment[
                                'fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0][
                        'fulfilmentCode']

                try:
                    await self.request_fulfilment(request,
                                                  attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except (KeyError, ClientResponseError) as ex:
                    raise ex

                raise HTTPFound(
                    request.app.router['RequestCodeCodeSentHHCY:get'].url_for(
                    ))
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobileHHCY:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG_CY)
            return attributes


@requests_routes.view('/ni/request-access-code/confirm-mobile')
class RequestCodeConfirmMobileHHNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        attributes['page_title'] = 'Is this mobile phone number correct?'
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        attributes['page_title'] = 'Is this mobile phone number correct?'
        data = await request.post()

        try:
            mobile_confirmation = data['request-mobile-confirmation']
        except KeyError:
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG)
            return attributes

        if mobile_confirmation == 'yes':

            try:
                available_fulfilments = await self.get_fulfilment(
                    request,
                    'HH', attributes['region'], 'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == 'eng':
                            attributes['fulfilmentCode'] = fulfilment[
                                'fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0][
                        'fulfilmentCode']

                try:
                    await self.request_fulfilment(request,
                                                  attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except (KeyError, ClientResponseError) as ex:
                    raise ex

                raise HTTPFound(
                    request.app.router['RequestCodeCodeSentHHNI:get'].url_for(
                    ))
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobileHHNI:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG)
            return attributes


@requests_routes.view('/request-access-code/code-sent')
class RequestCodeCodeSentHHEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/code-sent')
        attributes = await self.get_check_attributes(request, 'HH', 'EN')
        attributes['page_title'] = 'We have sent an access code'
        return attributes


@requests_routes.view('/gofyn-am-god-mynediad/wedi-anfon-cod')
class RequestCodeCodeSentHHCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/code-sent')
        attributes = await self.get_check_attributes(request, 'HH', 'CY')
        attributes['page_title'] = 'Rydym ni wedi anfon cod mynediad'
        return attributes


@requests_routes.view('/ni/request-access-code/code-sent')
class RequestCodeCodeSentHHNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/code-sent')
        attributes = await self.get_check_attributes(request, 'HH', 'NI')
        attributes['page_title'] = 'We have sent an access code'
        return attributes


@requests_routes.view('/request-access-code/timeout')
class RequestCodeTimeoutHHEN(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/timeout')
        return {
            'fulfillment_type': 'HH',
            'display_region': 'en',
            'page_title': 'Your session has timed out due to inactivity'
        }


@requests_routes.view('/gofyn-am-god-mynediad/terfyn-amser')
class RequestCodeTimeoutHHCY(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/timeout')
        return {
            'fulfillment_type': 'HH',
            'display_region': 'cy',
            'locale': 'cy',
            'page_title': 'Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch',
        }  # yapf: disable


@requests_routes.view('/ni/request-access-code/timeout')
class RequestCodeTimeoutHHNI(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-access-code/timeout')
        return {
            'fulfillment_type': 'HH',
            'display_region': 'ni',
            'page_title': 'Your session has timed out due to inactivity'
        }


@requests_routes.view('/request-individual-code')
class RequestCodeIndividualEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-individual.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code')
        return {
            'display_region': 'en',
            'page_title': 'Request an individual access code'
        }


@requests_routes.view('/gofyn-am-god-unigol')
class RequestCodeIndividualCY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-individual.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code')
        return {
            'display_region': 'cy',
            'locale': 'cy',
            'page_title': 'Gofyn am god mynediad unigryw'
        }


@requests_routes.view('/ni/request-individual-code')
class RequestCodeIndividualNI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-individual.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code')
        return {
            'display_region': 'ni',
            'page_title': 'Request an individual access code'
        }


@requests_routes.view('/request-individual-code/enter-address')
class RequestCodeEnterAddressHIEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-address')
        return {
            'fulfillment_type': 'HI',
            'display_region': 'en',
            'page_title': 'What is your postcode?'
        }

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-address')
        data = await request.post()
        await RequestCodeCommon.get_postcode(request, data, 'HI', 'EN',
                                             'en')


@requests_routes.view('/gofyn-am-god-unigol/nodi-cyfeiriad')
class RequestCodeEnterAddressHICY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-address')
        return {
            'fulfillment_type': 'HI',
            'display_region': 'cy',
            'locale': 'cy',
            'page_title': 'Beth yw eich cod post?'
        }

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-address')
        data = await request.post()
        await RequestCodeCommon.get_postcode(request, data, 'HI', 'CY',
                                             'cy')


@requests_routes.view('/ni/request-individual-code/enter-address')
class RequestCodeEnterAddressHINI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-address')
        return {
            'fulfillment_type': 'HI',
            'display_region': 'ni',
            'page_title': 'What is your postcode?'
        }

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-address')
        data = await request.post()
        await RequestCodeCommon.get_postcode(request, data, 'HI', 'NI',
                                             'en')


@requests_routes.view('/request-individual-code/select-address')
class RequestCodeSelectAddressHIEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/select-address')
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        address_content = await self.get_postcode_return(
            request, attributes['postcode'], attributes['fulfillment_type'],
            attributes['display_region'], attributes['locale'])
        address_content['page_title'] = 'Select your address'
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/select-address')
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        data = await request.post()

        try:
            form_return = json.loads(data['request-address-select'])
        except KeyError:
            logger.info('no address selected', client_ip=request['client_ip'])
            flash(request, ADDRESS_SELECT_CHECK_MSG)
            address_content = await self.get_postcode_return(
                request, attributes['postcode'],
                attributes['fulfillment_type'], attributes['display_region'],
                attributes['locale'])
            address_content['page_title'] = 'Select your address'
            return address_content

        session = await get_session(request)
        session['attributes']['address'] = form_return['address']
        session['attributes']['uprn'] = form_return['uprn']
        session.changed()
        logger.info('session updated', client_ip=request['client_ip'])

        raise HTTPFound(
            request.app.router['RequestCodeConfirmAddressHIEN:get'].url_for())


@requests_routes.view('/gofyn-am-god-unigol/dewis-cyfeiriad')
class RequestCodeSelectAddressHICY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/select-address')
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        address_content = await self.get_postcode_return(
            request, attributes['postcode'], attributes['fulfillment_type'],
            attributes['display_region'], attributes['locale'])
        address_content['page_title'] = 'Dewiswch eich cyfeiriad'
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/select-address')
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        data = await request.post()

        try:
            form_return = json.loads(data['request-address-select'])
        except KeyError:
            logger.info('no address selected', client_ip=request['client_ip'])
            flash(request, ADDRESS_SELECT_CHECK_MSG_CY)
            address_content = await self.get_postcode_return(
                request, attributes['postcode'],
                attributes['fulfillment_type'], attributes['display_region'],
                attributes['locale'])
            address_content['page_title'] = 'Dewiswch eich cyfeiriad'
            return address_content

        session = await get_session(request)
        session['attributes']['address'] = form_return['address']
        session['attributes']['uprn'] = form_return['uprn']
        session.changed()
        logger.info('session updated', client_ip=request['client_ip'])

        raise HTTPFound(
            request.app.router['RequestCodeConfirmAddressHICY:get'].url_for())


@requests_routes.view('/ni/request-individual-code/select-address')
class RequestCodeSelectAddressHINI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/select-address')
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        address_content = await self.get_postcode_return(
            request, attributes['postcode'], attributes['fulfillment_type'],
            attributes['display_region'], attributes['locale'])
        address_content['page_title'] = 'Select your address'
        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/select-address')
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        data = await request.post()

        try:
            form_return = json.loads(data['request-address-select'])
        except KeyError:
            logger.info('no address selected', client_ip=request['client_ip'])
            flash(request, ADDRESS_SELECT_CHECK_MSG)
            address_content = await self.get_postcode_return(
                request, attributes['postcode'],
                attributes['fulfillment_type'], attributes['display_region'],
                attributes['locale'])
            address_content['page_title'] = 'Select your address'
            return address_content

        session = await get_session(request)
        session['attributes']['address'] = form_return['address']
        session['attributes']['uprn'] = form_return['uprn']
        session.changed()
        logger.info('session updated', client_ip=request['client_ip'])

        raise HTTPFound(
            request.app.router['RequestCodeConfirmAddressHINI:get'].url_for())


@requests_routes.view('/request-individual-code/confirm-address')
class RequestCodeConfirmAddressHIEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        attributes['page_title'] = 'Is this address correct?'
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        attributes['page_title'] = 'Is this address correct?'
        data = await request.post()
        try:
            address_confirmation = data['request-address-confirmation']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session['attributes']['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(request, uprn)
                session['attributes']['case_id'] = uprn_return[0]['caseId']
                session['attributes']['region'] = uprn_return[0]['region']
                session.changed()
                raise HTTPFound(
                    request.app.router['RequestCodeEnterMobileHIEN:get'].
                    url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.info('unable to match uprn',
                                client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['RequestCodeNotRequiredHIEN:get'].
                        url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterAddressHIEN:get'].url_for(
                ))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@requests_routes.view('/gofyn-am-god-unigol/cadarnhau-cyfeiriad')
class RequestCodeConfirmAddressHICY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        attributes['page_title'] = "Ydy'r cyfeiriad hwn yn gywir?"
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        attributes['page_title'] = "Ydy'r cyfeiriad hwn yn gywir?"
        data = await request.post()
        try:
            address_confirmation = data['request-address-confirmation']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session['attributes']['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(request, uprn)
                session['attributes']['case_id'] = uprn_return[0]['caseId']
                session['attributes']['region'] = uprn_return[0]['region']
                session.changed()
                raise HTTPFound(
                    request.app.router['RequestCodeEnterMobileHICY:get'].
                    url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.info('unable to match uprn',
                                client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['RequestCodeNotRequiredHICY:get'].
                        url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterAddressHICY:get'].url_for(
                ))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes


@requests_routes.view('/ni/request-individual-code/confirm-address')
class RequestCodeConfirmAddressHINI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        attributes['page_title'] = 'Is this address correct?'
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-address')
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        attributes['page_title'] = 'Is this address correct?'
        data = await request.post()
        try:
            address_confirmation = data['request-address-confirmation']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session['attributes']['uprn']

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await self.get_cases_by_uprn(request, uprn)
                session['attributes']['case_id'] = uprn_return[0]['caseId']
                session['attributes']['region'] = uprn_return[0]['region']
                session.changed()
                raise HTTPFound(
                    request.app.router['RequestCodeEnterMobileHINI:get'].
                    url_for())
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.info('unable to match uprn',
                                client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['RequestCodeNotRequiredHINI:get'].
                        url_for())
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterAddressHINI:get'].url_for(
                ))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@requests_routes.view('/request-individual-code/not-required')
class RequestCodeNotRequiredHIEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/not-required')
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        attributes[
            'page_title'] = 'Your address is not part of the 2019 rehearsal'
        return attributes


@requests_routes.view('/gofyn-am-god-unigol/dim-angen')
class RequestCodeNotRequiredHICY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/not-required')
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        attributes[
            'page_title'] = 'Nid yw eich cyfeiriad yn rhan o ymarfer 2019'
        return attributes


@requests_routes.view('/ni/request-individual-code/not-required')
class RequestCodeNotRequiredHINI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/not-required')
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        attributes[
            'page_title'] = 'Your address is not part of the 2019 rehearsal'
        return attributes


@requests_routes.view('/request-individual-code/enter-mobile')
class RequestCodeEnterMobileHIEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        attributes['page_title'] = 'What is your mobile phone number?'
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        attributes['page_title'] = 'What is your mobile phone number?'
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(request, attributes,
                                                  data)


@requests_routes.view('/gofyn-am-god-unigol/nodi-rhif-ffon-symudol')
class RequestCodeEnterMobileHICY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        attributes['page_title'] = 'Beth yw eich rhif ffôn symudol?'
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        attributes['page_title'] = 'Beth yw eich rhif ffôn symudol?'
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(request, attributes,
                                                  data)


@requests_routes.view('/ni/request-individual-code/enter-mobile')
class RequestCodeEnterMobileHINI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        attributes['page_title'] = 'What is your mobile phone number?'
        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/enter-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        attributes['page_title'] = 'What is your mobile phone number?'
        data = await request.post()
        await RequestCodeCommon.post_enter_mobile(request, attributes,
                                                  data)


@requests_routes.view('/request-individual-code/confirm-mobile')
class RequestCodeConfirmMobileHIEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        attributes['page_title'] = 'Is this mobile phone number correct?'
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        attributes['page_title'] = 'Is this mobile phone number correct?'
        data = await request.post()
        try:
            mobile_confirmation = data['request-mobile-confirmation']
        except KeyError:
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG)
            return attributes

        if mobile_confirmation == 'yes':

            try:
                available_fulfilments = await self.get_fulfilment(
                    request,
                    attributes['fulfillment_type'], attributes['region'],
                    'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == 'eng':
                            attributes['fulfilmentCode'] = fulfilment[
                                'fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0][
                        'fulfilmentCode']

                try:
                    await self.request_fulfilment(request,
                                                  attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except (KeyError, ClientResponseError) as ex:
                    raise ex

                raise HTTPFound(
                    request.app.router['RequestCodeCodeSentHIEN:get'].url_for(
                    ))
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobileHIEN:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG)
            return attributes


@requests_routes.view('/gofyn-am-god-unigol/cadarnhau-rhif-ffon-symudol')
class RequestCodeConfirmMobileHICY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        attributes['page_title'] = "Ydy'r rhif ffôn symudol hwn yn gywir?"
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        attributes['page_title'] = "Ydy'r rhif ffôn symudol hwn yn gywir?"
        data = await request.post()
        try:
            mobile_confirmation = data['request-mobile-confirmation']
        except KeyError:
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG_CY)
            return attributes

        if mobile_confirmation == 'yes':

            try:
                available_fulfilments = await self.get_fulfilment(
                    request,
                    attributes['fulfillment_type'], attributes['region'],
                    'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == 'wel':
                            attributes['fulfilmentCode'] = fulfilment[
                                'fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0][
                        'fulfilmentCode']

                try:
                    await self.request_fulfilment(request,
                                                  attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except (KeyError, ClientResponseError) as ex:
                    raise ex

                raise HTTPFound(
                    request.app.router['RequestCodeCodeSentHICY:get'].url_for(
                    ))
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobileHICY:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG_CY)
            return attributes


@requests_routes.view('/ni/request-individual-code/confirm-mobile')
class RequestCodeConfirmMobileHINI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        attributes['page_title'] = 'Is this mobile phone number correct?'
        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/confirm-mobile')
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        attributes['page_title'] = 'Is this mobile phone number correct?'
        data = await request.post()
        try:
            mobile_confirmation = data['request-mobile-confirmation']
        except KeyError:
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG)
            return attributes

        if mobile_confirmation == 'yes':
            try:
                available_fulfilments = await self.get_fulfilment(
                    request,
                    attributes['fulfillment_type'], attributes['region'],
                    'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == 'eng':
                            attributes['fulfilmentCode'] = fulfilment[
                                'fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0][
                        'fulfilmentCode']

                try:
                    await self.request_fulfilment(request,
                                                  attributes['case_id'],
                                                  attributes['mobile_number'],
                                                  attributes['fulfilmentCode'])
                except (KeyError, ClientResponseError) as ex:
                    raise ex

                raise HTTPFound(
                    request.app.router['RequestCodeCodeSentHINI:get'].url_for(
                    ))
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobileHINI:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG)
            return attributes


@requests_routes.view('/request-individual-code/code-sent')
class RequestCodeCodeSentHIEN(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/code-sent')
        attributes = await self.get_check_attributes(request, 'HI', 'EN')
        attributes['page_title'] = 'We have sent an access code'
        return attributes


@requests_routes.view('/gofyn-am-god-unigol/wedi-anfon-cod')
class RequestCodeCodeSentHICY(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/code-sent')
        attributes = await self.get_check_attributes(request, 'HI', 'CY')
        attributes['page_title'] = 'Rydym ni wedi anfon cod mynediad'
        return attributes


@requests_routes.view('/ni/request-individual-code/code-sent')
class RequestCodeCodeSentHINI(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/code-sent')
        attributes = await self.get_check_attributes(request, 'HI', 'NI')
        attributes['page_title'] = 'We have sent an access code'
        return attributes


@requests_routes.view('/request-individual-code/timeout')
class RequestCodeTimeoutHIEN(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/timeout')
        return {
            'fulfillment_type': 'HI',
            'display_region': 'en',
            'page_title': 'Your session has timed out due to inactivity'
        }


@requests_routes.view('/gofyn-am-god-unigol/terfyn-amser')
class RequestCodeTimeoutHICY(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/timeout')
        return {
            'fulfillment_type': 'HI',
            'display_region': 'cy',
            'locale': 'cy',
            'page_title': 'Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch',
        }  # yapf: disable


@requests_routes.view('/ni/request-individual-code/timeout')
class RequestCodeTimeoutHINI(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'request-individual-code/timeout')
        return {
            'fulfillment_type': 'HI',
            'display_region': 'ni',
            'page_title': 'Your session has timed out due to inactivity'
        }
