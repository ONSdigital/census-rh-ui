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
    FlashMessage, RHService, ProcessName

logger = get_logger('respondent-home')
requests_routes = RouteTableDef()

# Limit for last name field to include room number (60 char limit - 10 char room number value max - a comma and a space)
last_name_char_limit = 48


class RequestCommon(View):

    valid_request_types_code_only = r'{request_type:\baccess-code\b}'
    valid_request_types_code_and_form = r'{request_type:\baccess-code|paper-form\b}'

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


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/access-code/individual/')
class RequestCodeIndividual(RequestCommon):
    @aiohttp_jinja2.template('request-code-individual.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Request individual access code'
            locale = 'cy'
        else:
            page_title = 'Request individual access code'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/access-code/individual')
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
        self.log_entry(request, display_region + '/requests/access-code/individual')

        session = await get_session(request)

        try:
            if request.cookies.get('RH_SESSION'):
                session['attributes']['individual'] = True
                session.changed()

                attributes = session['attributes']
                if attributes['case_type']:
                    logger.info('have session and case_type - directing to select method')
                    raise HTTPFound(
                        request.app.router['RequestCodeSelectHowToReceive:get'].url_for(request_type=request_type,
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


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/paper-form/individual-information/')
class RequestIndividualForm(RequestCommon):
    @aiohttp_jinja2.template('request-form-individual-information.html')
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

        self.log_entry(request, display_region + '/requests/paper-form/individual-information')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        request_type = 'paper-form'
        self.log_entry(request, display_region + '/requests/paper-form/individual-information')

        session = await get_session(request)
        session['attributes']['individual'] = True
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCommonEnterName:get'].url_for(user_journey='requests',
                                                                     request_type=request_type,
                                                                     display_region=display_region))


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/access-code/household/')
class RequestCodeHousehold(RequestCommon):
    @aiohttp_jinja2.template('request-code-household.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Request new household access code'
            locale = 'cy'
        else:
            page_title = 'Request new household access code'
            locale = 'en'

        self.log_entry(request, display_region + '/requests/access-code/household')
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
        self.log_entry(request, display_region + '/requests/access-code/household')

        session = await get_session(request)
        session['attributes']['individual'] = False
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCodeSelectHowToReceive:get'].url_for(request_type=request_type,
                                                                            display_region=display_region))


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/paper-form/household-information/')
class RequestHouseholdForm(RequestCommon):
    @aiohttp_jinja2.template('request-form-household-information.html')
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

        self.log_entry(request, display_region + '/requests/paper-form/household-information')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        request_type = 'paper-form'
        self.log_entry(request, display_region + '/requests/paper-form/household-information')

        session = await get_session(request)
        session['attributes']['individual'] = False
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCommonEnterName:get'].url_for(user_journey='requests',
                                                                     request_type=request_type,
                                                                     display_region=display_region))


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types_code_only + '/select-how-to-receive/')
class RequestCodeSelectHowToReceive(RequestCommon):
    @aiohttp_jinja2.template('request-code-select-how-to-receive.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/requests/' + request_type + '/select-how-to-receive')

        attributes = await self.get_check_attributes(request, request_type)

        if display_region == 'cy':
            if attributes['individual']:
                # TODO Add Welsh Translation
                page_title = 'Select how to receive individual access code'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                # TODO Add Welsh Translation
                page_title = 'Select how to receive manager access code'
            else:
                # TODO Add Welsh Translation
                page_title = 'Select how to receive household access code'
            locale = 'cy'
        else:
            if attributes['individual']:
                page_title = 'Select how to receive individual access code'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = 'Select how to receive manager access code'
            else:
                page_title = 'Select how to receive household access code'
            locale = 'en'

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)
        attributes['contact_us_link'] = View.get_campaign_site_link(request, display_region, 'contact-us')

        return attributes

    @aiohttp_jinja2.template('request-code-select-how-to-receive.html')
    async def post(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/requests/' + request_type + '/select-how-to-receive')

        attributes = await self.get_check_attributes(request, request_type)

        if display_region == 'cy':
            if attributes['individual']:
                # TODO Add Welsh Translation
                page_title = 'Error: Select how to receive individual access code'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                # TODO Add Welsh Translation
                page_title = 'Error: Select how to receive manager access code'
            else:
                # TODO Add Welsh Translation
                page_title = 'Error: Select how to receive household access code'
            locale = 'cy'
        else:
            if attributes['individual']:
                page_title = 'Error: Select how to receive individual access code'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = 'Error: Select how to receive manager access code'
            else:
                page_title = 'Error: Select how to receive household access code'
            locale = 'en'

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
            # TODO Add Welsh Translation
            page_title = "Enter mobile number"
            locale = 'cy'
        else:
            page_title = 'Enter mobile number'
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
            # TODO Add Welsh Translation
            page_title = "Error: Enter mobile number"
            locale = 'cy'
        else:
            page_title = 'Error: Enter mobile number'
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
                request.app.router['RequestCodeConfirmSendByText:get'].url_for(request_type=request_type,
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

            return attributes


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types_code_only + '/confirm-send-by-text/')
class RequestCodeConfirmSendByText(RequestCommon):
    @aiohttp_jinja2.template('request-code-confirm-send-by-text.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/requests/' + request_type + '/confirm-send-by-text')

        attributes = await self.get_check_attributes(request, request_type)

        if display_region == 'cy':
            if attributes['individual']:
                # TODO Add Welsh Translation
                page_title = 'Confirm to send individual access code by text'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                # TODO Add Welsh Translation
                page_title = 'Confirm to send manager access code by text'
            else:
                # TODO Add Welsh Translation
                page_title = 'Confirm to send household access code by text'
            locale = 'cy'
        else:
            if attributes['individual']:
                page_title = 'Confirm to send individual access code by text'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = 'Confirm to send manager access code by text'
            else:
                page_title = 'Confirm to send household access code by text'
            locale = 'en'

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        return attributes

    @aiohttp_jinja2.template('request-code-confirm-send-by-text.html')
    async def post(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/requests/' + request_type + '/confirm-send-by-text')

        attributes = await self.get_check_attributes(request, request_type)

        if display_region == 'cy':
            if attributes['individual']:
                # TODO Add Welsh Translation
                page_title = 'Error: Confirm to send individual access code by text'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                # TODO Add Welsh Translation
                page_title = 'Error: Confirm to send manager access code by text'
            else:
                # TODO Add Welsh Translation
                page_title = 'Error: Confirm to send household access code by text'
            locale = 'cy'
        else:
            if attributes['individual']:
                page_title = 'Error: Confirm to send individual access code by text'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = 'Error: Confirm to send manager access code by text'
            else:
                page_title = 'Error: Confirm to send household access code by text'
            locale = 'en'

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
                    request.app.router['RequestCodeSentByText:get'].url_for(request_type=request_type,
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

            fulfilment_code_array = []

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

                if request_type == 'paper-form':
                    if 'request-name-address-large-print' in data:
                        raise HTTPFound(
                            request.app.router['RequestLargePrintSentPost:get'].url_for(display_region=display_region))
                    else:
                        raise HTTPFound(
                            request.app.router['RequestFormSentPost:get'].url_for(display_region=display_region))
                else:
                    raise HTTPFound(
                        request.app.router['RequestCodeSentByPost:get'].url_for(display_region=display_region,
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
                    request.app.router['RequestCodeSelectHowToReceive:get'].url_for(display_region=display_region,
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
                      RequestCommon.valid_request_types_code_only + '/code-sent-by-text/')
class RequestCodeSentByText(RequestCommon):
    @aiohttp_jinja2.template('request-code-sent-by-text.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/requests/' + request_type + '/code-sent-by-text')

        attributes = await self.get_check_attributes(request, request_type)

        if display_region == 'cy':
            if attributes['individual']:
                # TODO Add Welsh Translation
                page_title = 'Individual access code has been sent by text'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                # TODO Add Welsh Translation
                page_title = 'Manager access code has been sent by text'
            else:
                # TODO Add Welsh Translation
                page_title = 'Household access code has been sent by text'
            locale = 'cy'
        else:
            if attributes['individual']:
                page_title = 'Individual access code has been sent by text'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = 'Manager access code has been sent by text'
            else:
                page_title = 'Household access code has been sent by text'
            locale = 'en'

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        return attributes


@requests_routes.view(r'/' + View.valid_display_regions + '/requests/' +
                      RequestCommon.valid_request_types_code_only + '/code-sent-by-post/')
class RequestCodeSentByPost(RequestCommon):
    @aiohttp_jinja2.template('request-code-sent-by-post.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/requests/' + request_type + '/code-sent-by-post')

        attributes = await self.get_check_attributes(request, request_type)

        if display_region == 'cy':
            if attributes['individual']:
                # TODO Add Welsh Translation
                page_title = 'Individual access code will be sent by post'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                # TODO Add Welsh Translation
                page_title = 'Manager access code will be sent by post'
            else:
                # TODO Add Welsh Translation
                page_title = 'Household access code will be sent by post'
            locale = 'cy'
        else:
            if attributes['individual']:
                page_title = 'Individual access code will be sent by post'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = 'Manager access code will be sent by post'
            else:
                page_title = 'Household access code will be sent by post'
            locale = 'en'

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
                'address_level': attributes['address_level'],
                'roomNumber': attributes['roomNumber'],
                'individual': attributes['individual']
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
        page_title = 'You need to visit the Communal Establishment Portal'
        locale = 'en'

        self.log_entry(request, display_region + '/requests/access-code/ce-manager')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
            }


@requests_routes.view(r'/ni/requests/paper-form/ce-manager/')
class RequestFormNIManager(RequestCommon):
    @aiohttp_jinja2.template('request-form-nisra-manager.html')
    async def get(self, request):
        self.setup_request(request)

        display_region = 'ni'
        page_title = 'You need to visit the Communal Establishment Portal'
        locale = 'en'

        self.log_entry(request, display_region + '/requests/paper-form/ce-manager')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
            }
