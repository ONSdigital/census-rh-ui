import aiohttp_jinja2

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from aiohttp_session import get_session
from structlog import get_logger

from . import (MOBILE_CHECK_MSG,
               MOBILE_CHECK_MSG_CY,
               NO_SELECTION_CHECK_MSG,
               NO_SELECTION_CHECK_MSG_CY)

from .flash import flash
from .exceptions import SessionTimeout
from .utils import View, ProcessMobileNumber, InvalidDataError, InvalidDataErrorWelsh, \
    FlashMessage, RHService, ProcessName

logger = get_logger('respondent-home')
requests_routes = RouteTableDef()


class RequestCommon(View):

    valid_request_types_code_only = r'{request_type:\bindividual-code|access-code\b}'
    valid_request_types_code_and_form = r'{request_type:\bindividual-code|access-code|paper-form\b}'

    @staticmethod
    def request_code_check_session(request, request_type):
        if request.cookies.get('RH_SESSION') is None:
            logger.info('session timed out', client_ip=request['client_ip'])
            raise SessionTimeout('requests', request_type)

    async def get_check_attributes(self, request, request_type):
        self.request_code_check_session(request, request_type)
        session = await get_session(request)
        try:
            attributes = session['attributes']

        except KeyError:
            raise SessionTimeout('requests', request_type)

        return attributes


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/individual-code/')
class RequestCode(RequestCommon):
    @aiohttp_jinja2.template('template-main.html')
    async def get(self, request):
        self.setup_request(request)
        request_type = 'individual-code'
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            page_title = 'Gofyn am god mynediad unigryw'
            locale = 'cy'
        else:
            page_title = 'Request an individual access code'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type)
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'request_type': request_type,
            'partial_name': 'request-' + request_type,
            'page_url': View.gen_page_url(request)
        }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types_code_only + '/select-method/')
class RequestCodeSelectMethod(RequestCommon):
    @aiohttp_jinja2.template('request-code-select-method.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'How would you like to receive a new access code?'
            locale = 'cy'
        else:
            page_title = 'How would you like to receive a new access code?'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/select-method')

        attributes = await self.get_check_attributes(request, request_type)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        return attributes

    @aiohttp_jinja2.template('request-code-select-method.html')
    async def post(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'How would you like to receive a new access code?'
            locale = 'cy'
        else:
            page_title = 'How would you like to receive a new access code?'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/select-method')

        attributes = await self.get_check_attributes(request, request_type)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        data = await request.post()
        try:
            request_method = data['form-select-method']
        except KeyError:
            logger.info('request method selection error',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return attributes

        if request_method == 'sms':
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobile:get'].url_for(request_type=request_type,
                                                                         display_region=display_region))

        elif request_method == 'post':
            raise HTTPFound(
                request.app.router['RequestCommonEnterName:get'].url_for(request_type=request_type,
                                                                         display_region=display_region))

        else:
            # catch all just in case, should never get here
            logger.info('request method selection error',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return attributes


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types_code_only + '/enter-mobile/')
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

        self.log_entry(request, display_region + '/requests/' + request_type + '/enter-mobile')

        attributes = await self.get_check_attributes(request, request_type)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

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

        self.log_entry(request, display_region + '/requests/' + request_type + '/enter-mobile')

        attributes = await self.get_check_attributes(request, request_type)
        attributes['page_title'] = page_title
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['display_region'] = display_region
        attributes['page_url'] = View.gen_page_url(request)

        data = await request.post()

        try:
            mobile_number = ProcessMobileNumber.validate_uk_mobile_phone_number(data['request-mobile-number'],
                                                                                locale)

            logger.info('valid mobile number',
                        client_ip=request['client_ip'])

            attributes['mobile_number'] = mobile_number
            attributes['submitted_mobile_number'] = data['request-mobile-number']
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
                      RequestCommon.valid_request_types_code_only + '/confirm-mobile/')
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

        self.log_entry(request, display_region + '/requests/' + request_type + '/confirm-mobile')

        attributes = await self.get_check_attributes(request, request_type)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

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

        self.log_entry(request, display_region + '/requests/' + request_type + '/confirm-mobile')

        attributes = await self.get_check_attributes(request, request_type)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

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

            if request_type == 'individual-code':
                fulfilment_individual = 'true'
            elif attributes['case_type'] == 'CE':
                if attributes['address_level'] == 'U':
                    fulfilment_individual = 'true'
                else:
                    fulfilment_individual = 'false'
            else:
                fulfilment_individual = 'false'

            if display_region == 'cy':
                fulfilment_language = 'wel'
            else:
                fulfilment_language = 'eng'

            logger.info(f"fulfilment query: case_type={attributes['case_type']}, region={attributes['region']}, "
                        f"individual={fulfilment_individual}",
                        client_ip=request['client_ip'])

            try:
                available_fulfilments = await RHService.get_fulfilment(
                    request, attributes['case_type'], attributes['region'], 'SMS', 'UAC', fulfilment_individual)
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == fulfilment_language:
                            attributes['fulfilmentCode'] = fulfilment[
                                'fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0][
                        'fulfilmentCode']

                try:
                    await RHService.request_fulfilment_sms(request,
                                                           attributes['case_id'],
                                                           attributes['mobile_number'],
                                                           attributes['fulfilmentCode'])
                except (KeyError, ClientResponseError) as ex:
                    raise ex

                raise HTTPFound(
                    request.app.router['RequestCodeCodeSentSMS:get'].url_for(request_type=request_type,
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
                      RequestCommon.valid_request_types_code_and_form + '/enter-name/')
class RequestCommonEnterName(RequestCommon):
    @aiohttp_jinja2.template('request-common-enter-name.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = "What is your name?"
            locale = 'cy'
        else:
            page_title = 'What is your name?'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/enter-name')

        attributes = await self.get_check_attributes(request, request_type)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        return attributes

    @aiohttp_jinja2.template('request-common-enter-name.html')
    async def post(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = "What is your name?"
            locale = 'cy'
        else:
            page_title = 'What is your name?'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/enter-name')

        attributes = await self.get_check_attributes(request, request_type)
        attributes['page_title'] = page_title
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['display_region'] = display_region
        attributes['page_url'] = View.gen_page_url(request)

        data = await request.post()

        form_valid = ProcessName.validate_name(request, data, display_region)

        if not form_valid:
            logger.info('form submission error',
                        client_ip=request['client_ip'])
            return {
                'form_value_name_first_name': data.get('name_first_name'),
                'form_value_name_last_name': data.get('name_last_name'),
                'display_region': display_region,
                'request_type': request_type,
                'page_title': page_title,
                'page_url': View.gen_page_url(request),
                'locale': locale
            }

        name_first_name = data['name_first_name']
        name_last_name = data['name_last_name']

        attributes['first_name'] = name_first_name
        attributes['last_name'] = name_last_name

        session = await get_session(request)
        session['attributes'] = attributes

        raise HTTPFound(
            request.app.router['RequestCommonConfirmNameAddress:get'].url_for(display_region=display_region,
                                                                              request_type=request_type))


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types_code_and_form + '/confirm-name-address/')
class RequestCommonConfirmNameAddress(RequestCommon):
    @aiohttp_jinja2.template('request-common-confirm-name-address.html')
    async def get(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Do you want to send a new access code to this address?'
            locale = 'cy'
        else:
            page_title = 'Do you want to send a new access code to this address?'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/confirm-name-address')

        attributes = await self.get_check_attributes(request, request_type)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'first_name': attributes['first_name'],
            'last_name': attributes['last_name'],
            'addressLine1': attributes['addressLine1'],
            'addressLine2': attributes['addressLine2'],
            'addressLine3': attributes['addressLine3'],
            'townName': attributes['townName'],
            'postcode': attributes['postcode'],
            'case_type': attributes['case_type'],
            'address_level': attributes['address_level']
        }

    @aiohttp_jinja2.template('request-common-confirm-name-address.html')
    async def post(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Do you want to send a new access code to this address?'
            locale = 'cy'
        else:
            page_title = 'Do you want to send a new access code to this address?'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/confirm-name-address')

        attributes = await self.get_check_attributes(request, request_type)

        data = await request.post()
        try:
            name_address_confirmation = data['request-name-address-confirmation']
        except KeyError:
            logger.info('name confirmation error',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                # TODO Add Welsh Translation
                flash(request, FlashMessage.generate_flash_message('Please check and confirm the name and address.',
                                                                   'ERROR',
                                                                   'NAME_CONFIRMATION_ERROR',
                                                                   'request-name-address-confirmation'))
            else:
                flash(request, FlashMessage.generate_flash_message('Please check and confirm the name and address.',
                                                                   'ERROR',
                                                                   'NAME_CONFIRMATION_ERROR',
                                                                   'request-name-address-confirmation'))
            return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request),
                'first_name': attributes['first_name'],
                'last_name': attributes['last_name'],
                'addressLine1': attributes['addressLine1'],
                'addressLine2': attributes['addressLine2'],
                'addressLine3': attributes['addressLine3'],
                'townName': attributes['townName'],
                'postcode': attributes['postcode'],
                'case_type': attributes['case_type'],
                'address_level': attributes['address_level']
            }

        if name_address_confirmation == 'yes':

            if request_type == 'individual-code':
                fulfilment_individual = 'true'
            elif attributes['case_type'] == 'CE':
                if attributes['address_level'] == 'U':
                    fulfilment_individual = 'true'
                else:
                    fulfilment_individual = 'false'
            else:
                fulfilment_individual = 'false'

            if display_region == 'cy':
                fulfilment_language = 'wel'
            else:
                fulfilment_language = 'eng'

            if request_type == 'paper-form':

                if 'request-name-address-large-print' in data:
                    fulfilment_type = 'LARGE_PRINT'
                else:
                    fulfilment_type = 'QUESTIONNAIRE'

            else:
                fulfilment_type = 'UAC'

            logger.info(f"fulfilment query: case_type={attributes['case_type']}, fulfilment_type={fulfilment_type}, "
                        f"region={attributes['region']}, individual={fulfilment_individual}",
                        client_ip=request['client_ip'])

            try:
                available_fulfilments = await RHService.get_fulfilment(
                    request,
                    attributes['case_type'],
                    attributes['region'],
                    'POST',
                    fulfilment_type,
                    fulfilment_individual)

                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == fulfilment_language:
                            attributes['fulfilmentCode'] = fulfilment[
                                'fulfilmentCode']
                else:
                    attributes['fulfilmentCode'] = available_fulfilments[0][
                        'fulfilmentCode']

                try:
                    await RHService.request_fulfilment_post(request,
                                                            attributes['case_id'],
                                                            attributes['first_name'],
                                                            attributes['last_name'],
                                                            attributes['fulfilmentCode'])
                except (KeyError, ClientResponseError) as ex:
                    raise ex

                if request_type == 'paper-form':
                    if 'request-name-address-large-print' in data:
                        raise HTTPFound(
                            request.app.router['RequestLargePrintSentPost:get'].url_for(display_region=display_region))
                    else:
                        raise HTTPFound(
                            request.app.router['RequestFormSentPost:get'].url_for(display_region=display_region))
                else:
                    raise HTTPFound(
                        request.app.router['RequestCodeCodeSentPost:get'].url_for(display_region=display_region,
                                                                                  request_type=request_type))

            except ClientResponseError as ex:
                raise ex

        elif name_address_confirmation == 'no':
            if request_type == 'paper-form':
                raise HTTPFound(
                    request.app.router['RequestFormCancelled:get'].url_for(display_region=display_region,
                                                                           request_type=request_type))
            else:
                raise HTTPFound(
                    request.app.router['RequestCodeSelectMethod:get'].url_for(display_region=display_region,
                                                                              request_type=request_type))

        else:
            # catch all just in case, should never get here
            logger.info('name confirmation error',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                # TODO Add Welsh Translation
                flash(request, FlashMessage.generate_flash_message('Please check and confirm the name and address.',
                                                                   'ERROR',
                                                                   'NAME_CONFIRMATION_ERROR',
                                                                   'request-name-confirmation'))
            else:
                flash(request, FlashMessage.generate_flash_message('Please check and confirm the name and address.',
                                                                   'ERROR',
                                                                   'NAME_CONFIRMATION_ERROR',
                                                                   'request-name-confirmation'))
            return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request),
                'first_name': attributes['first_name'],
                'last_name': attributes['last_name'],
                'addressLine1': attributes['addressLine1'],
                'addressLine2': attributes['addressLine2'],
                'addressLine3': attributes['addressLine3'],
                'townName': attributes['townName'],
                'postcode': attributes['postcode'],
                'case_type': attributes['case_type'],
                'address_level': attributes['address_level']
            }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types_code_only + '/code-sent-sms/')
class RequestCodeCodeSentSMS(RequestCommon):
    @aiohttp_jinja2.template('request-code-code-sent-sms.html')
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

        self.log_entry(request, display_region + '/requests/' + request_type + '/code-sent-sms')

        attributes = await self.get_check_attributes(request, request_type)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        return attributes


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types_code_only + '/code-sent-post/')
class RequestCodeCodeSentPost(RequestCommon):
    @aiohttp_jinja2.template('request-code-code-sent-post.html')
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

        self.log_entry(request, display_region + '/requests/' + request_type + '/code-sent-post')

        attributes = await self.get_check_attributes(request, request_type)

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request),
                'first_name': attributes['first_name'],
                'last_name': attributes['last_name'],
                'addressLine1': attributes['addressLine1'],
                'addressLine2': attributes['addressLine2'],
                'addressLine3': attributes['addressLine3'],
                'townName': attributes['townName'],
                'postcode': attributes['postcode'],
                'case_type': attributes['case_type'],
                'address_level': attributes['address_level']
            }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/paper-form/form-manager/')
class RequestFormManager(RequestCommon):
    @aiohttp_jinja2.template('request-form-manager.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = 'paper-form'
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'We cannot send census forms to managers by post'
            locale = 'cy'
        else:
            page_title = 'We cannot send census forms to managers by post'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/form-manager')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request),
                'call_centre_number': View.get_call_centre_number(display_region)
            }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/paper-form/request-cancelled/')
class RequestFormCancelled(RequestCommon):
    @aiohttp_jinja2.template('request-form-cancelled.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = 'paper-form'
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Your request for a paper form has been cancelled'
            locale = 'cy'
        else:
            page_title = 'Your request for a paper form has been cancelled'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/request-cancelled')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request)
            }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/paper-form/form-sent-post/')
class RequestFormSentPost(RequestCommon):
    @aiohttp_jinja2.template('request-form-sent-post.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = 'paper-form'
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'A paper questionnaire will be sent'
            locale = 'cy'
        else:
            page_title = 'A paper questionnaire will be sent'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/form-sent-post')

        attributes = await self.get_check_attributes(request, request_type)

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request),
                'first_name': attributes['first_name'],
                'last_name': attributes['last_name'],
                'addressLine1': attributes['addressLine1'],
                'addressLine2': attributes['addressLine2'],
                'addressLine3': attributes['addressLine3'],
                'townName': attributes['townName'],
                'postcode': attributes['postcode'],
                'case_type': attributes['case_type'],
                'address_level': attributes['address_level']
            }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/paper-form/large-print-sent-post/')
class RequestLargePrintSentPost(RequestCommon):
    @aiohttp_jinja2.template('request-form-sent-post.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = 'large-print'
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'A large-print paper questionnaire will be sent'
            locale = 'cy'
        else:
            page_title = 'A large-print paper questionnaire will be sent'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/paper-form/large-print-sent-post')

        attributes = await self.get_check_attributes(request, request_type)

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request),
                'first_name': attributes['first_name'],
                'last_name': attributes['last_name'],
                'addressLine1': attributes['addressLine1'],
                'addressLine2': attributes['addressLine2'],
                'addressLine3': attributes['addressLine3'],
                'townName': attributes['townName'],
                'postcode': attributes['postcode'],
                'case_type': attributes['case_type'],
                'address_level': attributes['address_level']
            }
