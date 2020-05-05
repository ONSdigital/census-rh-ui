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
from .utils import View, \
    ProcessPostcode, \
    ProcessMobileNumber, \
    InvalidDataError, \
    InvalidDataErrorWelsh, \
    FlashMessage, \
    AddressIndex, \
    RHService

logger = get_logger('respondent-home')
requests_routes = RouteTableDef()


class RequestCommon(View):

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

    async def get_fulfilment(self, request, case_type, region,
                             delivery_channel, product_group, individual):
        rhsvc_url = request.app['RHSVC_URL']
        url = f'{rhsvc_url}/fulfilments?caseType={case_type}&region={region}&deliveryChannel={delivery_channel}' \
              f'&productGroup={product_group}&individual={individual}'
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


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types + '-code/')
class RequestCode(RequestCommon):
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

        self.log_entry(request, display_region + '/requests/' + request_type + '-code')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'request_type': request_type,
            'partial_name': 'request-' + request_type + '-code',
            'page_url': '/requests/' + request_type + '-code/'
        }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types + '-code/select-address/')
class RequestCodeSelectAddress(RequestCommon):
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

        self.log_entry(request, display_region + '/requests/' + request_type + '-code/select-address')

        attributes = await self.get_check_attributes(request, request_type, display_region)
        address_content = await AddressIndex.get_postcode_return(request, attributes['postcode'], display_region)
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

        self.log_entry(request, display_region + '/requests/' + request_type + '-code/select-address')

        attributes = await self.get_check_attributes(request, request_type, display_region)
        data = await request.post()

        try:
            form_return = json.loads(data['form-select-address'])
        except KeyError:
            logger.info('no address selected', client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, ADDRESS_SELECT_CHECK_MSG_CY)
            else:
                flash(request, ADDRESS_SELECT_CHECK_MSG)
            address_content = await AddressIndex.get_postcode_return(request, attributes['postcode'], display_region)
            address_content['page_title'] = page_title
            address_content['display_region'] = display_region
            address_content['locale'] = locale
            address_content['request_type'] = request_type
            return address_content

        if form_return['uprn'] == 'xxxx':
            raise HTTPFound(
                request.app.router['CommonCallContactCentre:get'].url_for(
                    display_region=display_region,
                    user_journey='requests',
                    error='address-not-found'))
        else:
            session = await get_session(request)
            session['attributes']['address'] = form_return['address']
            session['attributes']['uprn'] = form_return['uprn']
            session.changed()
            logger.info('session updated', client_ip=request['client_ip'])

            raise HTTPFound(
                request.app.router['RequestCodeConfirmAddress:get'].url_for(
                    request_type=request_type, display_region=display_region))


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types + '-code/confirm-address/')
class RequestCodeConfirmAddress(RequestCommon):
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

        self.log_entry(request, display_region + '/requests/' + request_type + '-code/confirm-address')

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

        self.log_entry(request, display_region + '/requests/' + request_type + '-code/confirm-address')

        attributes = await self.get_check_attributes(request, request_type, display_region)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type

        data = await request.post()

        try:
            address_confirmation = data['form-confirm-address']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, ADDRESS_CHECK_MSG_CY)
            else:
                flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'yes':

            session = await get_session(request)
            uprn = session['attributes']['uprn']

            uprn_ai_return = await AddressIndex.get_ai_uprn(request, uprn)

            try:
                if uprn_ai_return['response']['address']['countryCode'] == 'S':
                    logger.info('address is in Scotland', client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['CommonAddressInScotland:get'].
                        url_for(display_region=display_region, user_journey='requests', request_type=request_type))
            except KeyError:
                logger.info('unable to check for region', client_ip=request['client_ip'])

            # uprn_return[0] will need updating/changing for multiple households - post 2019 issue
            try:
                uprn_return = await RHService.get_cases_by_uprn(request, uprn)
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
                        request.app.router['CommonCallContactCentre:get'].
                        url_for(request_type=request_type,
                                user_journey='requests',
                                display_region=display_region,
                                error='unable-to-match-address'))
                else:
                    raise ex

        elif address_confirmation == 'no':
            raise HTTPFound(
                request.app.router['CommonEnterAddress:get'].url_for(sub_user_journey=request_type + '-code',
                                                                     display_region=display_region,
                                                                     user_journey='requests'))

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


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types + '-code/enter-mobile/')
class RequestCodeEnterMobile(RequestCommon):
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

        self.log_entry(request, display_region + '/requests/' + request_type + '-code/enter-mobile')

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

        self.log_entry(request, display_region + '/requests/' + request_type + '-code/enter-mobile')

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


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types + '-code/confirm-mobile/')
class RequestCodeConfirmMobile(RequestCommon):
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

        self.log_entry(request, display_region + '/requests/' + request_type + '-code/confirm-mobile')

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

        self.log_entry(request, display_region + '/requests/' + request_type + '-code/confirm-mobile')

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
                fulfilment_individual = 'false'
            elif request_type == 'individual':
                fulfilment_case_type = 'HH'
                fulfilment_individual = 'true'
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
                    request, fulfilment_case_type, attributes['region'], 'SMS', 'UAC', fulfilment_individual)
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


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types + '-code/code-sent/')
class RequestCodeCodeSent(RequestCommon):
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

        self.log_entry(request, display_region + '/requests/' + request_type + '-code/code-sent')

        attributes = await self.get_check_attributes(request, request_type, display_region)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type

        return attributes


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types + '-code/timeout/')
class RequestCodeTimeout(RequestCommon):
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

        self.log_entry(request, display_region + '/requests/' + request_type + '-code/timeout')

        return {
            'request_type': request_type,
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale
        }
