import aiohttp_jinja2
import json

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from aiohttp_session import get_session
from datetime import datetime, timezone
from structlog import get_logger

from . import (ADDRESS_CHECK_MSG,
               MOBILE_CHECK_MSG,
               ADDRESS_SELECT_CHECK_MSG,
               ADDRESS_CHECK_MSG_CY,
               MOBILE_CHECK_MSG_CY,
               ADDRESS_SELECT_CHECK_MSG_CY)

from .flash import flash
from .utils import View, ProcessPostcode, ProcessMobileNumber, InvalidDataError, InvalidDataErrorWelsh, FlashMessage

logger = get_logger('respondent-home')
requests_routes = RouteTableDef()


class RequestCodeCommon(View):

    valid_request_types = r'{request_type:\bhousehold|individual\b}'

    @staticmethod
    def request_code_check_session(request, request_type,
                                   display_region):
        if request.cookies.get('RH_SESSION') is None:
            logger.info('session timed out', client_ip=request['client_ip'])
            raise HTTPFound(
                request.app.router['RequestCodeTimeout:get'].url_for(
                    request_type=request_type, display_region=display_region))

    async def get_check_attributes(self, request, request_type,
                                   display_region):
        self.request_code_check_session(request, request_type,
                                        display_region)
        session = await get_session(request)
        try:
            attributes = session['attributes']

        except KeyError:
            raise HTTPFound(
                request.app.router['RequestCodeTimeout:get'].url_for(
                    request_type=request_type, display_region=display_region))

        return attributes

    async def get_postcode_return(self, request, postcode):
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
            'total_matches': postcode_return['response']['total']
        }

        return address_content

    @staticmethod
    async def post_enter_mobile(request, attributes, data):

        try:
            mobile_number = ProcessMobileNumber.validate_uk_mobile_phone_number(data['request-mobile-number'],
                                                                                attributes['locale'])

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

        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info(exc, client_ip=request['client_ip'])
            flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'MOBILE_ENTER_ERROR', 'mobile')
            flash(request, flash_message)
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


@requests_routes.view(r'/' + View.valid_display_regions + '/request-' +
                      RequestCodeCommon.valid_request_types + '-code/')
class RequestCode(RequestCodeCommon):
    @aiohttp_jinja2.template('template-main.html')
    async def get(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']
        if request_type == 'individual':
            if display_region == 'cy':
                page_title = 'Gofyn am god mynediad unigryw'
                locale = 'cy'
            else:
                page_title = 'Request an individual access code'
                locale = 'en'
        else:
            if display_region == 'cy':
                page_title = 'Gofyn am god mynediad newydd'
                locale = 'cy'
            else:
                page_title = 'Request a new access code'
                locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'request_type': request_type,
            'partial_name': 'request-' + request_type + '-code',
            'page_url': '/request-' + request_type + '-code/'
        }


@requests_routes.view(r'/' + View.valid_display_regions + '/request-' +
                      RequestCodeCommon.valid_request_types + '-code/enter-address/')
class RequestCodeEnterAddress(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = 'Beth yw eich cod post?'
            locale = 'cy'
        else:
            page_title = 'What is your postcode?'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/enter-address')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'request_type': request_type
        }

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def post(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = 'Beth yw eich cod post?'
            locale = 'cy'
        else:
            page_title = 'What is your postcode?'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/enter-address')

        data = await request.post()

        try:
            postcode = ProcessPostcode.validate_postcode(data['request-postcode'], locale)
            logger.info('valid postcode', client_ip=request['client_ip'])

        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info('invalid postcode', client_ip=request['client_ip'])
            flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'POSTCODE_ENTER_ERROR', 'postcode')
            flash(request, flash_message)
            raise HTTPFound(
                request.app.router['RequestCodeEnterAddress:get'].url_for(
                    request_type=request_type, display_region=display_region))

        attributes = {
            'postcode': postcode
        }

        session = await get_session(request)
        session['attributes'] = attributes

        raise HTTPFound(
            request.app.router['RequestCodeSelectAddress:get'].url_for(
                    request_type=request_type, display_region=display_region))


@requests_routes.view(r'/' + View.valid_display_regions + '/request-' +
                      RequestCodeCommon.valid_request_types + '-code/select-address/')
class RequestCodeSelectAddress(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = 'Dewiswch eich cyfeiriad'
            locale = 'cy'
        else:
            page_title = 'Select your address'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/select-address')

        attributes = await self.get_check_attributes(request, request_type, display_region)
        address_content = await self.get_postcode_return(request, attributes['postcode'])
        address_content['page_title'] = page_title
        address_content['display_region'] = display_region
        address_content['locale'] = locale
        address_content['request_type'] = request_type

        return address_content

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def post(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = 'Dewiswch eich cyfeiriad'
            locale = 'cy'
        else:
            page_title = 'Select your address'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/select-address')

        attributes = await self.get_check_attributes(request, request_type, display_region)
        data = await request.post()

        try:
            form_return = json.loads(data['request-address-select'])
        except KeyError:
            logger.info('no address selected', client_ip=request['client_ip'])
            flash(request, ADDRESS_SELECT_CHECK_MSG)
            address_content = await self.get_postcode_return(
                request, attributes['postcode'])
            address_content['page_title'] = page_title
            address_content['display_region'] = display_region
            address_content['locale'] = locale
            address_content['request_type'] = request_type
            return address_content

        session = await get_session(request)
        session['attributes']['address'] = form_return['address']
        session['attributes']['uprn'] = form_return['uprn']
        session.changed()
        logger.info('session updated', client_ip=request['client_ip'])

        raise HTTPFound(
            request.app.router['RequestCodeConfirmAddress:get'].url_for(
                request_type=request_type, display_region=display_region))


@requests_routes.view(r'/' + View.valid_display_regions + '/request-' +
                      RequestCodeCommon.valid_request_types + '-code/confirm-address/')
class RequestCodeConfirmAddress(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = "Ydy'r cyfeiriad hwn yn gywir?"
            locale = 'cy'
        else:
            page_title = 'Is this address correct?'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/confirm-address')

        attributes = await self.get_check_attributes(request, request_type, display_region)
        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type

        return attributes

    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def post(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = "Ydy'r cyfeiriad hwn yn gywir?"
            locale = 'cy'
        else:
            page_title = 'Is this address correct?'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/confirm-address')

        attributes = await self.get_check_attributes(request, request_type, display_region)

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
                    request.app.router['RequestCodeEnterMobile:get'].
                    url_for(request_type=request_type, display_region=display_region))
            except ClientResponseError as ex:
                if ex.status == 404:
                    logger.info('unable to match uprn',
                                client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['RequestCodeNotRequired:get'].
                        url_for(request_type=request_type, display_region=display_region))
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterAddress:get'].url_for(request_type=request_type,
                                                                          display_region=display_region))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            attributes['page_title'] = page_title
            attributes['display_region'] = display_region
            attributes['locale'] = locale
            attributes['request_type'] = request_type
            return attributes


@requests_routes.view(r'/' + View.valid_display_regions + '/request-' +
                      RequestCodeCommon.valid_request_types + '-code/not-required/')
class RequestCodeNotRequired(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-not-required.html')
    async def get(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = 'Nid yw eich cyfeiriad yn rhan o ymarfer 2019'
            locale = 'cy'
        else:
            page_title = 'Your address is not part of the 2019 rehearsal'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/confirm-address')

        attributes = await self.get_check_attributes(request, request_type, display_region)
        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        return attributes


@requests_routes.view(r'/' + View.valid_display_regions + '/request-' +
                      RequestCodeCommon.valid_request_types + '-code/enter-mobile/')
class RequestCodeEnterMobile(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = "Beth yw eich rhif ffôn symudol?"
            locale = 'cy'
        else:
            page_title = 'What is your mobile phone number?'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/enter-mobile')

        attributes = await self.get_check_attributes(request, request_type, display_region)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type

        return attributes

    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def post(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = "Beth yw eich rhif ffôn symudol?"
            locale = 'cy'
        else:
            page_title = 'What is your mobile phone number?'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/enter-mobile')

        attributes = await self.get_check_attributes(request, request_type, display_region)
        attributes['page_title'] = page_title
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['display_region'] = display_region

        data = await request.post()

        try:
            mobile_number = ProcessMobileNumber.validate_uk_mobile_phone_number(data['request-mobile-number'],
                                                                                locale)

            logger.info('valid mobile number',
                        client_ip=request['client_ip'])

            attributes['mobile_number'] = mobile_number
            session = await get_session(request)
            session['attributes'] = attributes

            raise HTTPFound(
                request.app.router['RequestCodeConfirmMobile:get'].url_for(request_type=request_type,
                                                                           display_region=display_region))

        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info(exc, client_ip=request['client_ip'])
            flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'MOBILE_ENTER_ERROR', 'mobile')
            flash(request, flash_message)
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobile:post'].url_for(request_type=request_type,
                                                                          display_region=display_region))


@requests_routes.view(r'/' + View.valid_display_regions + '/request-' +
                      RequestCodeCommon.valid_request_types + '-code/confirm-mobile/')
class RequestCodeConfirmMobile(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = "Ydy'r rhif ffôn symudol hwn yn gywir?"
            locale = 'cy'
        else:
            page_title = 'Is this mobile phone number correct?'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/confirm-mobile')

        attributes = await self.get_check_attributes(request, request_type, display_region)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type

        return attributes

    @aiohttp_jinja2.template('request-code-confirm-mobile.html')
    async def post(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = "Ydy'r rhif ffôn symudol hwn yn gywir?"
            locale = 'cy'
        else:
            page_title = 'Is this mobile phone number correct?'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/confirm-mobile/')

        attributes = await self.get_check_attributes(request, request_type, display_region)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type

        data = await request.post()
        try:
            mobile_confirmation = data['request-mobile-confirmation']
        except KeyError:
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, MOBILE_CHECK_MSG_CY)
            else:
                flash(request, MOBILE_CHECK_MSG)
            return attributes

        if mobile_confirmation == 'yes':

            if request_type == 'household':
                fulfilment_case_type = 'HH'
            elif request_type == 'individual':
                fulfilment_case_type = 'HI'
            else:
                # catch all just in case, should never get here
                logger.info('invalid request_type',
                            client_ip=request['client_ip'])
                raise KeyError

            if display_region == 'cy':
                fulfilment_language = 'wel'
            else:
                fulfilment_language = 'eng'

            try:
                available_fulfilments = await self.get_fulfilment(
                    request, fulfilment_case_type, attributes['region'], 'SMS')
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == fulfilment_language:
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
                    request.app.router['RequestCodeCodeSent:get'].url_for(request_type=request_type,
                                                                          display_region=display_region))
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobile:get'].url_for(request_type=request_type,
                                                                         display_region=display_region))

        else:
            # catch all just in case, should never get here
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'])
            flash(request, MOBILE_CHECK_MSG)
            return attributes


@requests_routes.view(r'/' + View.valid_display_regions + '/request-' +
                      RequestCodeCommon.valid_request_types + '-code/code-sent/')
class RequestCodeCodeSent(RequestCodeCommon):
    @aiohttp_jinja2.template('request-code-code-sent.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = 'Rydym ni wedi anfon cod mynediad'
            locale = 'cy'
        else:
            page_title = 'We have sent an access code'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/code-sent')

        attributes = await self.get_check_attributes(request, request_type, display_region)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type

        return attributes


@requests_routes.view(r'/' + View.valid_display_regions + '/request-' +
                      RequestCodeCommon.valid_request_types + '-code/timeout/')
class RequestCodeTimeout(RequestCodeCommon):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = 'Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch'
            locale = 'cy'
        else:
            page_title = 'Your session has timed out due to inactivity'
            locale = 'en'

        self.log_entry(request, display_region + '/request-' + request_type + '-code/timeout')

        return {
            'request_type': request_type,
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale
        }
