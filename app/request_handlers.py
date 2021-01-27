import aiohttp_jinja2

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from aiohttp_session import get_session
from structlog import get_logger

from . import (NO_SELECTION_CHECK_MSG,
               NO_SELECTION_CHECK_MSG_CY)

from .flash import flash

from .exceptions import TooManyRequests
from .security import invalidate

from .utils import View, ProcessMobileNumber, InvalidDataError, InvalidDataErrorWelsh, \
    FlashMessage, RHService, ProcessName, ProcessNumberOfPeople
from .session import get_existing_session, get_session_value

logger = get_logger('respondent-home')
request_routes = RouteTableDef()

# Limit for last name field to include room number (35 char limit - 10 char room number value max - a comma and a space)
last_name_char_limit = 23


class RequestCommon(View):

    valid_request_types_code_only = r'{request_type:\baccess-code\b}'
    valid_request_types_form_only = r'{request_type:\bpaper-questionnaire|continuation-questionnaire\b}'
    valid_request_types_code_and_form = r'{request_type:\baccess-code|paper-questionnaire|continuation-questionnaire\b}'


@request_routes.view(r'/' + View.valid_display_regions + '/request/access-code/individual/')
class RequestCodeIndividual(RequestCommon):
    @aiohttp_jinja2.template('request-code-individual.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            page_title = 'Gofyn am god mynediad unigol'
            locale = 'cy'
        else:
            page_title = 'Request individual access code'
            locale = 'en'

        self.log_entry(request, display_region + '/request/access-code/individual')
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
        self.log_entry(request, display_region + '/request/access-code/individual')

        session = await get_session(request)

        try:
            if not session.new:
                session['attributes']['individual'] = True
                session.changed()

                attributes = session['attributes']
                case_type_value = attributes['case_type']
                if case_type_value:
                    logger.info('have session and case_type - directing to select method',
                                is_individual=session['attributes']['individual'],
                                type_of_case=case_type_value)
                    raise HTTPFound(
                        request.app.router['RequestCodeSelectHowToReceive:get'].url_for(request_type=request_type,
                                                                                        display_region=display_region))
                else:
                    raise KeyError
            else:
                raise KeyError
        except KeyError:
            attributes = {'individual': True}
            session['attributes'] = attributes
            logger.info('no session - directing to enter address', session_attributes=attributes)
            raise HTTPFound(
                request.app.router['CommonEnterAddress:get'].url_for(user_journey='request',
                                                                     sub_user_journey=request_type,
                                                                     display_region=display_region))


@request_routes.view(r'/' + View.valid_display_regions + '/request/paper-questionnaire/individual/')
class RequestIndividualForm(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-individual.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Request individual paper questionnaire'
            locale = 'cy'
        else:
            page_title = 'Request individual paper questionnaire'
            locale = 'en'

        self.log_entry(request, display_region + '/request/paper-questionnaire/individual')
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
        self.log_entry(request, display_region + '/request/paper-questionnaire/individual')

        session = await get_existing_session(request, 'requests', request_type)
        session['attributes']['individual'] = True
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCommonEnterName:get'].url_for(user_journey='request',
                                                                     request_type=request_type,
                                                                     display_region=display_region))


@request_routes.view(r'/' + View.valid_display_regions + '/request/access-code/household/')
class RequestCodeHousehold(RequestCommon):
    @aiohttp_jinja2.template('request-code-household.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            page_title = 'Gofyn am god mynediad newydd ar gyfer y cartref'
            locale = 'cy'
        else:
            page_title = 'Request new household access code'
            locale = 'en'

        self.log_entry(request, display_region + '/request/access-code/household')
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
        self.log_entry(request, display_region + '/request/access-code/household')

        session = await get_existing_session(request, 'requests', 'access-code')
        session['attributes']['individual'] = False
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCodeSelectHowToReceive:get'].url_for(request_type=request_type,
                                                                            display_region=display_region))


@request_routes.view(r'/' + View.valid_display_regions + '/request/paper-questionnaire/household/')
class RequestHouseholdForm(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-household.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Request household paper questionnaire'
            locale = 'cy'
        else:
            page_title = 'Request household paper questionnaire'
            locale = 'en'

        self.log_entry(request, display_region + '/request/paper-questionnaire/household')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/request/paper-questionnaire/household')

        session = await get_existing_session(request, 'requests', 'paper-questionnaire')
        session['attributes']['individual'] = False
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCommonPeopleInHousehold:get'].url_for(display_region=display_region,
                                                                             request_type='paper-questionnaire'))


@request_routes.view(r'/' + View.valid_display_regions + '/request/' +
                     RequestCommon.valid_request_types_code_only + '/select-how-to-receive/')
class RequestCodeSelectHowToReceive(RequestCommon):
    @aiohttp_jinja2.template('request-code-select-how-to-receive.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/select-how-to-receive')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        if display_region == 'cy':
            if attributes['individual']:
                page_title = 'Dewis sut i anfon cod mynediad unigol'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = 'Dewis sut i gael cod mynediad rheolwr'
            else:
                page_title = 'Dewis sut i gael cod mynediad y cartref'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            if attributes['individual']:
                page_title = 'Select how to receive individual access code'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = 'Select how to receive manager access code'
            else:
                page_title = 'Select how to receive household access code'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)
        attributes['contact_us_link'] = View.get_campaign_site_link(request, display_region, 'contact-us')

        return attributes

    async def post(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/select-how-to-receive')

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
            raise HTTPFound(
                request.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

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
                        client_ip=request['client_ip'], method_selected=request_method)
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))


@request_routes.view(r'/' + View.valid_display_regions + '/request/' +
                     RequestCommon.valid_request_types_code_only + '/enter-mobile/')
class RequestCodeEnterMobile(RequestCommon):
    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = 'Nodi rhif ffôn symudol'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Enter mobile number'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-mobile')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes',  'requests', request_type)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        return attributes

    async def post(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-mobile')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        data = await request.post()

        try:
            mobile_number = ProcessMobileNumber.validate_uk_mobile_phone_number(data['request-mobile-number'],
                                                                                locale)

            logger.info('valid mobile number',
                        client_ip=request['client_ip'])

            attributes['mobile_number'] = mobile_number
            attributes['submitted_mobile_number'] = data['request-mobile-number']
            session.changed()

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
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobile:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))


@request_routes.view(r'/' + View.valid_display_regions + '/request/' +
                     RequestCommon.valid_request_types_code_only + '/confirm-send-by-text/')
class RequestCodeConfirmSendByText(RequestCommon):
    @aiohttp_jinja2.template('request-code-confirm-send-by-text.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/confirm-send-by-text')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        if display_region == 'cy':
            if attributes['individual']:
                page_title = 'Cadarnhau i anfon cod mynediad unigol drwy neges destun'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = 'Cadarnhau i anfon cod mynediad rheolwr drwy neges destun'
            else:
                page_title = 'Cadarnhau i anfon cod mynediad y cartref drwy neges destun'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            if attributes['individual']:
                page_title = 'Confirm to send individual access code by text'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = 'Confirm to send manager access code by text'
            else:
                page_title = 'Confirm to send household access code by text'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        return attributes

    async def post(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/confirm-send-by-text')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

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
            raise HTTPFound(
                request.app.router['RequestCodeConfirmSendByText:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

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
                        client_ip=request['client_ip'], postcode=attributes['postcode'])

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
                        client_ip=request['client_ip'], user_selection=mobile_confirmation)
            flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['RequestCodeConfirmSendByText:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))


@request_routes.view(r'/' + View.valid_display_regions + '/request/' +
                     RequestCommon.valid_request_types_code_and_form + '/enter-name/')
class RequestCommonEnterName(RequestCommon):
    @aiohttp_jinja2.template('request-common-enter-name.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = "Nodi enw"
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = "Enter name"
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-name')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        return attributes

    async def post(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-name')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        data = await request.post()

        form_valid = ProcessName.validate_name(request, data, display_region)

        if not form_valid:
            logger.info('form submission error',
                        client_ip=request['client_ip'],
                        region_of_site=display_region,
                        type_of_request=request_type)
            raise HTTPFound(
                request.app.router['RequestCommonEnterName:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

        name_first_name = data['name_first_name']
        name_last_name = data['name_last_name']

        attributes['first_name'] = name_first_name
        attributes['last_name'] = name_last_name
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCommonConfirmSendByPost:get'].url_for(display_region=display_region,
                                                                             request_type=request_type))


@request_routes.view(r'/' + View.valid_display_regions + '/request/' +
                     RequestCommon.valid_request_types_code_and_form + '/confirm-send-by-post/')
class RequestCommonConfirmSendByPost(RequestCommon):
    @aiohttp_jinja2.template('request-common-confirm-send-by-post.html')
    async def get(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/confirm-send-by-post')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        if request_type == 'access-code':
            if attributes['individual']:
                if display_region == 'cy':
                    page_title = "Cadarnhau i anfon cod mynediad unigol drwy'r post"
                else:
                    page_title = 'Confirm to send individual access code by post'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                if display_region == 'cy':
                    page_title = "Cadarnhau i anfon cod mynediad rheolwr drwy'r post"
                else:
                    page_title = 'Confirm to send manager access code by post'
            else:
                if display_region == 'cy':
                    page_title = "Cadarnhau i anfon cod mynediad y cartref drwy'r post"
                else:
                    page_title = 'Confirm to send household access code by post'
        elif request_type == 'continuation-questionnaire':
            if display_region == 'cy':
                page_title = 'Cadarnhau i anfon holiadur parhad'
            else:
                page_title = 'Confirm to send continuation questionnaire'
        else:
            if attributes['individual']:
                if display_region == 'cy':
                    # TODO Add Welsh Translation
                    page_title = 'Confirm to send individual paper questionnaire'
                else:
                    page_title = 'Confirm to send individual paper questionnaire'
            else:
                if display_region == 'cy':
                    page_title = 'Cadarnhau i anfon copi papur o Holiadur y Cartref'
                else:
                    page_title = 'Confirm to send household paper questionnaire'

        if request.get('flash'):
            if display_region == 'cy':
                page_title = View.page_title_error_prefix_cy + page_title
            else:
                page_title = View.page_title_error_prefix_en + page_title

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

    async def post(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/confirm-send-by-post')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        data = await request.post()
        try:
            name_address_confirmation = data['request-name-address-confirmation']
        except KeyError:
            logger.info('name confirmation error',
                        client_ip=request['client_ip'],
                        type_of_request=request_type,
                        region_of_site=display_region)
            if display_region == 'cy':
                # TODO Add Welsh Translation
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)

            raise HTTPFound(
                request.app.router['RequestCommonConfirmSendByPost:get'].url_for(display_region=display_region,
                                                                                 request_type=request_type))

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

                    room_number_value = attributes['roomNumber']
                    logger.info(
                        f"fulfilment query: case_type={attributes['case_type']}, "
                        f"fulfilment_type={fulfilment_type_array}, "
                        f"region={attributes['region']}, individual={fulfilment_individual}",
                        client_ip=request['client_ip'], postcode=attributes['postcode'],
                        room_number_entered=room_number_value)

                    if room_number_value:
                        if len(attributes['last_name']) < last_name_char_limit:
                            last_name = attributes['last_name'] + ', ' + room_number_value
                            title = None
                        else:
                            last_name = attributes['last_name']
                            title = room_number_value
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
                            request.app.router['RequestCodeSentByPost:get'].url_for(display_region=display_region,
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
                        client_ip=request['client_ip'], case_id=attributes['case_id'])

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
                    request.app.router['RequestCodeEnterMobile:get'].url_for(display_region=display_region,
                                                                             request_type=request_type))

        else:
            # catch all just in case, should never get here
            logger.info('name confirmation error',
                        client_ip=request['client_ip'], user_selection=name_address_confirmation,
                        region_of_site=display_region, type_of_request=request_type)
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

            raise HTTPFound(
                request.app.router['RequestCommonConfirmSendByPost:get'].url_for(display_region=display_region,
                                                                                 request_type=request_type))


@request_routes.view(r'/' + View.valid_display_regions + '/request/' +
                     RequestCommon.valid_request_types_code_only + '/code-sent-by-text/')
class RequestCodeSentByText(RequestCommon):
    @aiohttp_jinja2.template('request-code-sent-by-text.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/code-sent-by-text')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        if display_region == 'cy':
            if attributes['individual']:
                page_title = "Mae cod mynediad unigol wedi cael ei anfon drwy neges destun"
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = "Mae cod mynediad rheolwr wedi cael ei anfon drwy neges destun"
            else:
                page_title = "Mae cod mynediad y cartref wedi cael ei anfon drwy neges destun"
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

        await invalidate(request)

        return attributes


@request_routes.view(r'/' + View.valid_display_regions + '/request/' +
                     RequestCommon.valid_request_types_code_only + '/code-sent-by-post/')
class RequestCodeSentByPost(RequestCommon):
    @aiohttp_jinja2.template('request-code-sent-by-post.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/code-sent-by-post')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        if display_region == 'cy':
            if attributes['individual']:
                page_title = "Caiff cod mynediad unigol ei anfon drwy'r post"
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = "Caiff cod mynediad rheolwr ei anfon drwy'r post"
            else:
                page_title = "Caiff cod mynediad y cartref ei anfon drwy'r post"
            locale = 'cy'
        else:
            if attributes['individual']:
                page_title = 'Individual access code will be sent by post'
            elif (attributes['case_type'] == 'CE') and (attributes['address_level'] == 'E'):
                page_title = 'Manager access code will be sent by post'
            else:
                page_title = 'Household access code will be sent by post'
            locale = 'en'

        await invalidate(request)

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


@request_routes.view(r'/' + View.valid_display_regions + '/request/' +
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
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'How many people are in your household?'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/number-of-people-in-your-household')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        self.setup_request(request)
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/number-of-people-in-your-household')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        data = await request.post()

        form_valid = ProcessNumberOfPeople.validate_number_of_people(request, data, display_region, request_type)

        if not form_valid:
            logger.info('form submission error',
                        client_ip=request['client_ip'],
                        region_of_site=display_region,
                        type_of_request=request_type)
            raise HTTPFound(
                request.app.router['RequestCommonPeopleInHousehold:get'].url_for(display_region=display_region,
                                                                                 request_type=request_type))

        attributes['number_of_people'] = data['number_of_people']
        session.changed()

        raise HTTPFound(
            request.app.router['RequestCommonEnterName:get'].url_for(display_region=display_region,
                                                                     request_type=request_type))


@request_routes.view(r'/' + View.valid_ew_display_regions + '/request/paper-questionnaire/manager/')
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

        self.log_entry(request, display_region + '/request/' + request_type + '/manager')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request),
                'call_centre_number': View.get_call_centre_number(display_region)
            }


@request_routes.view(r'/' + View.valid_display_regions + '/request/' +
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

        self.log_entry(request, display_region + '/request/' + request_type + '/request-cancelled')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request),
                'census_home_link': View.get_campaign_site_link(request, display_region, 'census-home'),
            }


@request_routes.view(r'/' + View.valid_display_regions + '/request/paper-questionnaire/sent/')
class RequestQuestionnaireSent(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-sent.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = 'paper-questionnaire'
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/sent')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        if display_region == 'cy':
            if attributes['individual']:
                # TODO Add Welsh Translation
                page_title = 'Individual paper questionnaire will be sent'
            else:
                # TODO Add Welsh Translation
                page_title = 'Household paper questionnaire will be sent'
            locale = 'cy'
        else:
            if attributes['individual']:
                page_title = 'Individual paper questionnaire will be sent'
            else:
                page_title = 'Household paper questionnaire will be sent'
            locale = 'en'

        await invalidate(request)

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


@request_routes.view(r'/' + View.valid_display_regions + '/request/continuation-questionnaire/sent/')
class RequestContinuationSent(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-sent.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = 'continuation-questionnaire'
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Continuation questionnaire will be sent'
            locale = 'cy'
        else:
            page_title = 'Continuation questionnaire will be sent'
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/sent')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        await invalidate(request)

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


@request_routes.view(r'/' + View.valid_display_regions + '/request/paper-questionnaire/large-print-sent-post/')
class RequestLargePrintSentPost(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-sent.html')
    async def get(self, request):
        self.setup_request(request)

        request_type = 'large-print'
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/paper-questionnaire/large-print-sent-post')

        session = await get_existing_session(request, 'requests', request_type)
        attributes = get_session_value(session, 'attributes', 'requests', request_type)

        if display_region == 'cy':
            if attributes['individual']:
                # TODO Add Welsh Translation
                page_title = 'Large-print individual paper questionnaire will be sent'
            else:
                # TODO Add Welsh Translation
                page_title = 'Large-print household paper questionnaire will be sent'
            locale = 'cy'
        else:
            if attributes['individual']:
                page_title = 'Large-print individual paper questionnaire will be sent'
            else:
                page_title = 'Large-print household paper questionnaire will be sent'
            locale = 'en'

        await invalidate(request)

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


@request_routes.view(r'/ni/request/access-code/ce-manager/')
class RequestCodeNIManager(RequestCommon):
    @aiohttp_jinja2.template('request-code-nisra-manager.html')
    async def get(self, request):
        self.setup_request(request)

        display_region = 'ni'
        page_title = 'You need to visit the Communal Establishment Manager Portal'
        locale = 'en'

        self.log_entry(request, display_region + '/request/access-code/ce-manager')

        return {
                'page_title': page_title,
                'locale': locale
            }


@request_routes.view(r'/ni/request/paper-questionnaire/ce-manager/')
class RequestFormNIManager(RequestCommon):
    @aiohttp_jinja2.template('request-questionnaire-nisra-manager.html')
    async def get(self, request):
        self.setup_request(request)

        display_region = 'ni'
        page_title = 'You need to visit the Communal Establishment Manager Portal'
        locale = 'en'

        self.log_entry(request, display_region + '/request/paper-questionnaire/ce-manager')

        return {
                'page_title': page_title,
                'locale': locale
            }


@request_routes.view(r'/' + View.valid_display_regions + '/request/continuation-questionnaire/not-a-household/')
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

        self.log_entry(request, display_region + '/request/continuation-questionnaire/not-a-household')

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'page_url': View.gen_page_url(request),
                'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
            }
