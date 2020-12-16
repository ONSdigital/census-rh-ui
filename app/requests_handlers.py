import aiohttp_jinja2

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from aiohttp_session import get_session
from structlog import get_logger

from . import (NO_SELECTION_CHECK_MSG,
               NO_SELECTION_CHECK_MSG_CY)

from .flash import flash
from .exceptions import SessionTimeout, TooManyRequests
from .utils import View, ProcessMobileNumber, InvalidDataError, InvalidDataErrorWelsh, \
    FlashMessage, RHService, ProcessName, ProcessNumberOfPeople

logger = get_logger('respondent-home')
requests_routes = RouteTableDef()

# Limit for last name field to include room number (60 char limit - 10 char room number value max - a comma and a space)
last_name_char_limit = 48


class RequestCommon(View):

    valid_request_types_code_only = r'{request_type:\baccess-code\b}'
    valid_request_types_form_only = r'{request_type:\bpaper-questionnaire|continuation-questionnaire\b}'
    valid_request_types_code_and_form = r'{request_type:\baccess-code|paper-questionnaire|continuation-questionnaire\b}'

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


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/access-code/individual-information/')
class RequestIndividualCode(RequestCommon):
    @aiohttp_jinja2.template('request-code-individual-introduction.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            page_title = 'Gofyn am god mynediad unigryw'
            locale = 'cy'
        else:
            page_title = 'Request an individual access code'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/access-code/individual-information')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        request_type = 'access-code'
        self.log_entry(request, display_region + '/requests/access-code/individual-information')

        session = await get_session(request)

        try:
            if request.cookies.get('RH_SESSION'):
                session['attributes']['individual'] = True
                session.changed()

                attributes = session['attributes']
                if attributes['case_type']:
                    logger.info('have session and case_type - directing to select method')
                    raise HTTPFound(
                        request.app.router['RequestCodeSelectMethod:get'].url_for(request_type=request_type,
                                                                                  display_region=display_region))
                else:
                    raise KeyError
            else:
                raise KeyError
        except KeyError:
            logger.info('no session - directing to enter address')
            attributes = {'individual': True}
            session['attributes'] = attributes
            raise HTTPFound(
                request.app.router['CommonEnterAddress:get'].url_for(user_journey='requests',
                                                                     sub_user_journey=request_type,
                                                                     display_region=display_region))


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/paper-questionnaire/individual-information/')
class RequestIndividualForm(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-individual-information.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Request an individual paper questionnaire'
            locale = 'cy'
        else:
            page_title = 'Request an individual paper questionnaire'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/paper-questionnaire/individual-information')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        request_type = 'paper-questionnaire'
        self.log_entry(request, display_region + '/requests/paper-questionnaire/individual-information')

        session = await get_session(request)
        session['attributes']['individual'] = True
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCommonEnterName:get'].url_for(user_journey='requests',
                                                                     request_type=request_type,
                                                                     display_region=display_region))


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/access-code/household-information/')
class RequestHouseholdCode(RequestCommon):
    @aiohttp_jinja2.template('request-code-household-information.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Request a new household access code'
            locale = 'cy'
        else:
            page_title = 'Request a new household access code'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/access-code/household-information')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        request_type = 'access-code'
        self.log_entry(request, display_region + '/requests/access-code/household-information')

        session = await get_session(request)
        session['attributes']['individual'] = False
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCodeSelectMethod:get'].url_for(request_type=request_type,
                                                                      display_region=display_region))


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/paper-questionnaire/household-information/')
class RequestHouseholdForm(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-household-information.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Request a household paper questionnaire'
            locale = 'cy'
        else:
            page_title = 'Request a household paper questionnaire'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/paper-questionnaire/household-information')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/requests/paper-questionnaire/household-information')

        session = await get_session(request)
        session['attributes']['individual'] = False
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCommonPeopleInHousehold:get'].url_for(display_region=display_region,
                                                                             request_type='paper-questionnaire'))


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
        attributes['contact_us_link'] = View.get_campaign_site_link(request, display_region, 'contact-us')

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
        attributes['contact_us_link'] = View.get_campaign_site_link(request, display_region, 'contact-us')

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
            if exc.message_type == 'empty':
                flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'MOBILE_ENTER_ERROR',
                                                                    'mobile_empty')
            else:
                flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'MOBILE_ENTER_ERROR',
                                                                    'mobile_invalid')
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
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return attributes

        if mobile_confirmation == 'yes':

            if attributes['individual']:
                fulfilment_individual = 'true'
            else:
                fulfilment_individual = 'false'

            if display_region == 'cy':
                fulfilment_language = 'W'
            else:
                fulfilment_language = 'E'

            logger.info(f"fulfilment query: case_type={attributes['case_type']}, region={attributes['region']}, "
                        f"individual={fulfilment_individual}",
                        client_ip=request['client_ip'])

            fulfilment_code_array = []

            try:
                available_fulfilments = await RHService.get_fulfilment(
                    request, attributes['case_type'], attributes['region'], 'SMS', 'UAC', fulfilment_individual)
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == fulfilment_language:
                            fulfilment_code_array.append(fulfilment['fulfilmentCode'])
                else:
                    fulfilment_code_array.append(available_fulfilments[0]['fulfilmentCode'])

                try:
                    await RHService.request_fulfilment_sms(request,
                                                           attributes['case_id'],
                                                           attributes['mobile_number'],
                                                           fulfilment_code_array)
                except (KeyError, ClientResponseError) as ex:
                    if ex.status == 429:
                        raise TooManyRequests(request_type)
                    else:
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
            flash(request, NO_SELECTION_CHECK_MSG)
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
            'address_level': attributes['address_level'],
            'roomNumber': attributes['roomNumber'],
            'individual': attributes['individual']
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
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)

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
                'address_level': attributes['address_level'],
                'roomNumber': attributes['roomNumber'],
                'individual': attributes['individual']
            }

        if name_address_confirmation == 'yes':

            if attributes['individual']:
                fulfilment_individual = 'true'
            else:
                fulfilment_individual = 'false'

            if display_region == 'cy':
                fulfilment_language = 'W'
            else:
                fulfilment_language = 'E'

            if (request_type == 'access-code') or (fulfilment_individual == 'true'):
                if request_type == 'access-code':
                    fulfilment_type = 'UAC'
                else:
                    if 'request-name-address-large-print' in data:
                        fulfilment_type = 'LARGE_PRINT'
                    else:
                        fulfilment_type = 'QUESTIONNAIRE'

                fulfilment_code_array = []
                fulfilment_type_array = []

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
                                fulfilment_code_array.append(fulfilment['fulfilmentCode'])
                    else:
                        fulfilment_code_array.append(available_fulfilments[0]['fulfilmentCode'])

                    fulfilment_type_array.append(fulfilment_type)

                    logger.info(
                        f"fulfilment query: case_type={attributes['case_type']}, "
                        f"fulfilment_type={fulfilment_type_array}, "
                        f"region={attributes['region']}, individual={fulfilment_individual}",
                        client_ip=request['client_ip'])

                    if attributes['roomNumber']:
                        if len(attributes['last_name']) < last_name_char_limit:
                            last_name = attributes['last_name'] + ', ' + attributes['roomNumber']
                            title = None
                        else:
                            last_name = attributes['last_name']
                            title = attributes['roomNumber']
                    else:
                        last_name = attributes['last_name']
                        title = None

                    try:
                        await RHService.request_fulfilment_post(request,
                                                                attributes['case_id'],
                                                                attributes['first_name'],
                                                                last_name,
                                                                fulfilment_code_array,
                                                                title)
                    except (KeyError, ClientResponseError) as ex:
                        if ex.status == 429:
                            raise TooManyRequests(request_type)
                        else:
                            raise ex

                    if request_type == 'access-code':
                        raise HTTPFound(
                            request.app.router['RequestCodeCodeSentPost:get'].url_for(display_region=display_region,
                                                                                      request_type=request_type))
                    else:
                        if 'request-name-address-large-print' in data:
                            raise HTTPFound(
                                request.app.router['RequestLargePrintSentPost:get'].url_for(
                                    display_region=display_region))
                        else:
                            raise HTTPFound(
                                request.app.router['RequestQuestionnaireSent:get'].url_for(
                                    display_region=display_region))

                except ClientResponseError as ex:
                    raise ex

            else:
                if 'request-name-address-large-print' in data:
                    large_print = True
                else:
                    large_print = False

                if request_type == 'continuation-questionnaire':
                    include_household = False
                else:
                    include_household = True

                fulfilment_code_array = []
                fulfilment_type_array = []

                required_forms = ProcessNumberOfPeople.form_calculation(
                    attributes['region'], attributes['number_of_people'],
                    include_household=include_household, large_print=large_print)

                logger.info(required_forms, client_ip=request['client_ip'])

                number_of_household_forms = required_forms['number_of_household_forms']
                number_of_continuation_forms = required_forms['number_of_continuation_forms']
                number_of_large_print_forms = required_forms['number_of_large_print_forms']

                try:
                    if number_of_household_forms == 1:
                        available_fulfilments = await RHService.get_fulfilment(
                            request,
                            attributes['case_type'],
                            attributes['region'],
                            'POST',
                            'QUESTIONNAIRE',
                            fulfilment_individual)

                        if len(available_fulfilments) > 1:
                            for fulfilment in available_fulfilments:
                                if fulfilment['language'] == fulfilment_language:
                                    fulfilment_code_array.append(fulfilment['fulfilmentCode'])
                        else:
                            fulfilment_code_array.append(available_fulfilments[0]['fulfilmentCode'])

                        fulfilment_type_array.append('QUESTIONNAIRE')

                    if number_of_continuation_forms > 0:
                        count = 1
                        fulfilment_code = ''
                        available_fulfilments = await RHService.get_fulfilment(
                            request,
                            attributes['case_type'],
                            attributes['region'],
                            'POST',
                            'CONTINUATION',
                            fulfilment_individual)

                        if len(available_fulfilments) > 1:
                            for fulfilment in available_fulfilments:
                                if fulfilment['language'] == fulfilment_language:
                                    fulfilment_code = fulfilment['fulfilmentCode']
                        else:
                            fulfilment_code = available_fulfilments[0]['fulfilmentCode']

                        while count <= number_of_continuation_forms:
                            fulfilment_code_array.append(fulfilment_code)
                            fulfilment_type_array.append('CONTINUATION')
                            count += 1

                    if number_of_large_print_forms > 0:
                        count = 1
                        fulfilment_code = ''
                        available_fulfilments = await RHService.get_fulfilment(
                            request,
                            attributes['case_type'],
                            attributes['region'],
                            'POST',
                            'LARGE_PRINT',
                            fulfilment_individual)

                        if len(available_fulfilments) > 1:
                            for fulfilment in available_fulfilments:
                                if fulfilment['language'] == fulfilment_language:
                                    fulfilment_code = fulfilment['fulfilmentCode']
                        else:
                            fulfilment_code = available_fulfilments[0]['fulfilmentCode']

                        while count <= number_of_large_print_forms:
                            fulfilment_code_array.append(fulfilment_code)
                            fulfilment_type_array.append('LARGE_PRINT')
                            count += 1

                    logger.info(
                        f"fulfilment query: case_type={attributes['case_type']}, "
                        f"fulfilment_type={fulfilment_type_array}, "
                        f"region={attributes['region']}, individual={fulfilment_individual}",
                        client_ip=request['client_ip'])

                    try:
                        await RHService.request_fulfilment_post(request,
                                                                attributes['case_id'],
                                                                attributes['first_name'],
                                                                attributes['last_name'],
                                                                fulfilment_code_array)
                    except (KeyError, ClientResponseError) as ex:
                        if ex.status == 429:
                            raise TooManyRequests(request_type)
                        else:
                            raise ex

                    if 'request-name-address-large-print' in data:
                        raise HTTPFound(
                            request.app.router['RequestLargePrintSentPost:get'].url_for(display_region=display_region))
                    elif request_type == 'continuation-questionnaire':
                        raise HTTPFound(
                            request.app.router['RequestContinuationSent:get'].url_for(display_region=display_region))
                    else:
                        raise HTTPFound(
                            request.app.router['RequestQuestionnaireSent:get'].url_for(display_region=display_region))

                except ClientResponseError as ex:
                    raise ex

        elif name_address_confirmation == 'no':
            if (request_type == 'paper-questionnaire') or (request_type == 'continuation-questionnaire'):
                raise HTTPFound(
                    request.app.router['RequestQuestionnaireCancelled:get'].url_for(display_region=display_region,
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
                flash(request, FlashMessage.generate_flash_message('Select an answer',
                                                                   'ERROR',
                                                                   'NAME_CONFIRMATION_ERROR',
                                                                   'request-name-confirmation'))
            else:
                flash(request, FlashMessage.generate_flash_message('Select an answer',
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
                'address_level': attributes['address_level'],
                'roomNumber': attributes['roomNumber'],
                'individual': attributes['individual']
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
                'census_home_link': View.get_campaign_site_link(request, display_region, 'census-home'),
                'first_name': attributes['first_name'],
                'last_name': attributes['last_name'],
                'addressLine1': attributes['addressLine1'],
                'addressLine2': attributes['addressLine2'],
                'addressLine3': attributes['addressLine3'],
                'townName': attributes['townName'],
                'postcode': attributes['postcode'],
                'case_type': attributes['case_type'],
                'address_level': attributes['address_level'],
                'roomNumber': attributes['roomNumber'],
                'individual': attributes['individual']
            }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types_form_only + '/number-of-people-in-your-household/')
class RequestCommonPeopleInHousehold(RequestCommon):
    @aiohttp_jinja2.template('request-common-people-in-household.html')
    async def get(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = "How many people are in your household?"
            locale = 'cy'
        else:
            page_title = 'How many people are in your household?'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/number-of-people-in-your-household')

        await self.get_check_attributes(request, request_type)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request)
        }

    @aiohttp_jinja2.template('request-common-people-in-household.html')
    async def post(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = "How many people are in your household?"
            locale = 'cy'
        else:
            page_title = 'How many people are in your household?'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/number-of-people-in-your-household')

        data = await request.post()

        form_valid = ProcessNumberOfPeople.validate_number_of_people(request, data, display_region, request_type)

        if not form_valid:
            logger.info('form submission error',
                        client_ip=request['client_ip'])
            return {
                'display_region': display_region,
                'page_title': page_title,
                'page_url': View.gen_page_url(request),
                'request_type': request_type,
                'locale': locale
            }

        session = await get_session(request)
        session['attributes']['number_of_people'] = data['number_of_people']
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCommonEnterName:get'].url_for(display_region=display_region,
                                                                     request_type=request_type))


@requests_routes.view(r'/' + View.valid_ew_display_regions + '/requests/paper-questionnaire/manager/')
class RequestQuestionnaireManager(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-manager.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = 'paper-questionnaire'
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Cannot send paper questionnaires to managers'
            locale = 'cy'
        else:
            page_title = 'Cannot send paper questionnaires to managers'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/manager')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request),
                'call_centre_number': View.get_call_centre_number(display_region)
            }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types_form_only + '/request-cancelled/')
class RequestQuestionnaireCancelled(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-cancelled.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Your request for a questionnaire has been cancelled'
            locale = 'cy'
        else:
            page_title = 'Your request for a questionnaire has been cancelled'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/request-cancelled')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request),
                'census_home_link': View.get_campaign_site_link(request, display_region, 'census-home'),
            }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/paper-questionnaire/sent/')
class RequestQuestionnaireSent(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-sent.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = 'paper-questionnaire'
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'A paper questionnaire will be sent'
            locale = 'cy'
        else:
            page_title = 'A paper questionnaire will be sent'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/sent')

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
                'address_level': attributes['address_level'],
                'roomNumber': attributes['roomNumber'],
                'individual': attributes['individual']
            }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/continuation-questionnaire/sent/')
class RequestContinuationSent(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-sent.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = 'continuation-questionnaire'
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'A continuation questionnaire will be sent'
            locale = 'cy'
        else:
            page_title = 'A continuation questionnaire will be sent'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/' + request_type + '/sent')

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
                'roomNumber': attributes['roomNumber'],
                'individual': attributes['individual']
            }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/paper-questionnaire/large-print-sent-post/')
class RequestLargePrintSentPost(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-sent.html')
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

        self.log_entry(request, display_region + '/requests/paper-questionnaire/large-print-sent-post')

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
                'address_level': attributes['address_level'],
                'roomNumber': attributes['roomNumber'],
                'individual': attributes['individual']
            }


@requests_routes.view(r'/ni/requests/access-code/ce-manager/')
class RequestCodeNIManager(RequestCommon):
    @aiohttp_jinja2.template('request-code-nisra-manager.html')
    async def get(self, request):
        self.setup_request(request)

        display_region = 'ni'
        page_title = 'You need to visit the Communal Establishment Manager Portal'
        locale = 'en'

        self.log_entry(request, display_region + '/requests/access-code/ce-manager')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale
            }


@requests_routes.view(r'/ni/requests/paper-questionnaire/ce-manager/')
class RequestFormNIManager(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-nisra-manager.html')
    async def get(self, request):
        self.setup_request(request)

        display_region = 'ni'
        page_title = 'You need to visit the Communal Establishment Manager Portal'
        locale = 'en'

        self.log_entry(request, display_region + '/requests/paper-questionnaire/ce-manager')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale
            }


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/continuation-questionnaire/not-a-household/')
class RequestContinuationNotAHousehold(RequestCommon):
    @aiohttp_jinja2.template('request-continuation-not-a-household.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'This address is not a household address'
            locale = 'cy'
        else:
            page_title = 'This address is not a household address'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/continuation-questionnaire/not-a-household')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'page_url': View.gen_page_url(request),
                'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
            }
