import aiohttp_jinja2

from aiohttp.web import HTTPFound, RouteTableDef
from structlog import get_logger
from aiohttp_session import get_session
from aiohttp.client_exceptions import (ClientResponseError)

from . import (ADDRESS_SELECT_CHECK_MSG,
               ADDRESS_SELECT_CHECK_MSG_CY,
               NO_SELECTION_CHECK_MSG,
               NO_SELECTION_CHECK_MSG_CY)

from .flash import flash
from .exceptions import SessionTimeout
from .security import check_permission
from .utils import View, ProcessPostcode, InvalidDataError, InvalidDataErrorWelsh, FlashMessage, AddressIndex, RHService

logger = get_logger('respondent-home')
common_routes = RouteTableDef()

# common_handlers contains routes and supporting code for any route in more than top level journey path
# eg start or request


class CommonCommon(View):
    @staticmethod
    def common_check_session(request, user_journey, sub_user_journey):
        if request.cookies.get('RH_SESSION') is None:
            logger.info('session timed out', client_ip=request['client_ip'], timed_out_journey=user_journey,
                        timed_out_sub_journey=sub_user_journey)
            raise SessionTimeout(user_journey, sub_user_journey)

    async def common_check_attributes(self, request, user_journey, sub_user_journey):
        self.common_check_session(request, user_journey, sub_user_journey)
        session = await get_session(request)

        if session['attributes']:
            attributes = session['attributes']
        else:
            raise SessionTimeout(user_journey, sub_user_journey)

        return attributes

    @staticmethod
    def request_confirm_address_routing(request, user_journey, sub_user_journey, display_region,
                                        case_type, address_level, individual):

        if case_type == 'CE' and address_level == 'E':
            raise HTTPFound(
                request.app.router['CommonCEMangerQuestion:get'].url_for(user_journey=user_journey,
                                                                         sub_user_journey=sub_user_journey,
                                                                         display_region=display_region))
        else:
            if sub_user_journey == 'paper-questionnaire':
                if (case_type == 'HH' or case_type == 'SPG') and not individual:
                    raise HTTPFound(
                        request.app.router['RequestHouseholdForm:get'].url_for(display_region=display_region))
                else:
                    raise HTTPFound(
                        request.app.router['RequestCommonEnterName:get'].url_for(
                            request_type=sub_user_journey, display_region=display_region))
            elif sub_user_journey == 'continuation-questionnaire':
                raise HTTPFound(
                    request.app.router['RequestCommonPeopleInHousehold:get'].url_for(
                        request_type=sub_user_journey, display_region=display_region))
            else:
                if (case_type == 'HH' or case_type == 'SPG') and not individual:
                    raise HTTPFound(
                        request.app.router['RequestCodeHousehold:get'].url_for(display_region=display_region))
                else:
                    raise HTTPFound(
                        request.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                            request_type=sub_user_journey, display_region=display_region))


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys + '/address-in-scotland/')
class CommonAddressInScotland(CommonCommon):
    """
    Route to render an 'Address in Scotland' page during address lookups
    """
    @aiohttp_jinja2.template('common-address-in-scotland.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']

        if display_region == 'ni':
            page_title = 'Address not part of census for Northern Ireland'
            locale = 'en'
        elif display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Address not part of census for England and Wales'
            locale = 'cy'
        else:
            page_title = 'Address not part of census for England and Wales'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/address-in-scotland')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'user_journey': user_journey,
            'page_url': View.gen_page_url(request)
        }


@common_routes.view(r'/' + View.valid_ew_display_regions + '/' + View.valid_user_journeys +
                    '/address-in-northern-ireland/')
class CommonAddressInNorthernIreland(CommonCommon):
    """
    Route to render an 'Address in Northern Ireland' page during address lookups if display_region is not 'ni'
    """
    @aiohttp_jinja2.template('common-address-in-northern-ireland.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Address not part of census for England and Wales'
            locale = 'cy'
        else:
            page_title = 'Address not part of census for England and Wales'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/address-in-northern-ireland')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
        }


@common_routes.view(r'/ni/' + View.valid_user_journeys + '/address-in-england/')
class CommonAddressInEngland(CommonCommon):
    """
    Route to render an 'Address in England' page during address lookups if display_region is 'ni'
    and selected addresses region is E
    """
    @aiohttp_jinja2.template('common-address-in-england.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = 'ni'
        user_journey = request.match_info['user_journey']

        page_title = 'Address not part of census for Northern Ireland'
        locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/address-in-england')

        return {
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
        }


@common_routes.view(r'/ni/' + View.valid_user_journeys + '/address-in-wales/')
class CommonAddressInWales(CommonCommon):
    """
    Route to render an 'Address in Wales' page during address lookups if display_region is 'ni'
    and selected addresses region is W
    """
    @aiohttp_jinja2.template('common-address-in-wales.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = 'ni'
        user_journey = request.match_info['user_journey']

        page_title = 'Address not part of census for Northern Ireland'
        locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/address-in-wales')

        return {
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
        }


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/register-address/')
class CommonRegisterAddress(CommonCommon):
    """
    Common route to render the 'Register address' page from any journey
    """
    @aiohttp_jinja2.template('common-register-address.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Register address'
            locale = 'cy'
        else:
            page_title = 'Register address'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/register-address')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us'),
            'call_centre_number': View.get_call_centre_number(display_region)
        }


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/call-contact-centre/{error}/')
class CommonCallContactCentre(CommonCommon):
    """
    Common route to render a 'Call the Contact Centre' page from any journey
    """
    @aiohttp_jinja2.template('common-contact-centre.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        error = request.match_info['error']

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Call Census Customer Contact Centre'
            locale = 'cy'
        else:
            page_title = 'Call Census Customer Contact Centre'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/call-contact-centre/' + error)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'user_journey': user_journey,
            'error': error,
            'page_url': View.gen_page_url(request),
            'call_centre_number': View.get_call_centre_number(display_region)
        }


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/enter-address/')
class CommonEnterAddress(CommonCommon):
    """
    Common route to enable address entry via postcode from start and request journeys
    """
    @aiohttp_jinja2.template('common-enter-address.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/enter-address')

        if user_journey == 'start':
            await check_permission(request)

        session = await get_session(request)

        individual = False

        if user_journey == 'start':
            session['attributes']['individual'] = False
            session.changed()
            individual = False
        elif user_journey == 'request':
            try:
                individual = session['attributes']['individual']
            except KeyError:
                individual = False
                attributes = {'individual': False}
                session['attributes'] = attributes
                session.changed()

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Enter address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Enter address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        return {
            'display_region': display_region,
            'page_title': page_title,
            'user_journey': user_journey,
            'sub_user_journey': sub_user_journey,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us'),
            'individual': individual
        }

    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/enter-address')

        if user_journey == 'start':
            await check_permission(request)

        data = await request.post()

        session = await get_session(request)

        try:
            postcode = ProcessPostcode.validate_postcode(data['form-enter-address-postcode'], display_region)
            logger.info('valid postcode', client_ip=request['client_ip'], postcode_entered=postcode,
                        region_of_site=display_region)
            
        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info('invalid postcode', client_ip=request['client_ip'])
            if exc.message_type == 'empty':
                flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'POSTCODE_ENTER_ERROR',
                                                                    'error_postcode_empty')
            else:
                flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'POSTCODE_ENTER_ERROR',
                                                                    'error_postcode_invalid')
            flash(request, flash_message)
            raise HTTPFound(
                request.app.router['CommonEnterAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))

        session['attributes']['postcode'] = postcode
        session.changed()

        raise HTTPFound(
            request.app.router['CommonSelectAddress:get'].url_for(
                display_region=display_region,
                user_journey=user_journey,
                sub_user_journey=sub_user_journey
            ))


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/select-address/')
class CommonSelectAddress(CommonCommon):
    """
    Common route to enable address selection from start and request journeys
    """
    @aiohttp_jinja2.template('common-select-address.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/select-address')

        if user_journey == 'start':
            await check_permission(request)

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Select address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Select address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        attributes = await self.common_check_attributes(request, user_journey, sub_user_journey)

        try:
            postcode = attributes['postcode']
        except KeyError:
            raise SessionTimeout(user_journey, sub_user_journey)

        address_content = await AddressIndex.get_postcode_return(request, postcode, display_region)
        address_content['page_title'] = page_title
        address_content['display_region'] = display_region
        address_content['user_journey'] = user_journey
        address_content['sub_user_journey'] = sub_user_journey
        address_content['locale'] = locale
        address_content['page_url'] = View.gen_page_url(request)
        address_content['contact_us_link'] = View.get_campaign_site_link(request, display_region, 'contact-us')

        return address_content

    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        if user_journey == 'start':
            await check_permission(request)

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/select-address')

        data = await request.post()

        try:
            selected_uprn = data['form-pick-address']
        except KeyError:
            logger.info('no address selected', client_ip=request['client_ip'], region_of_site=display_region,
                        journey_requiring_address=user_journey)
            if display_region == 'cy':
                flash(request, ADDRESS_SELECT_CHECK_MSG_CY)
            else:
                flash(request, ADDRESS_SELECT_CHECK_MSG)
            raise HTTPFound(
                request.app.router['CommonSelectAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))

        if selected_uprn == 'xxxx':
            raise HTTPFound(
                request.app.router['CommonRegisterAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey))
        else:
            session = await get_session(request)
            session['attributes']['uprn'] = selected_uprn
            session.changed()
            logger.info('session updated', client_ip=request['client_ip'], uprn_selected=selected_uprn,
                        region_of_site=display_region)

        raise HTTPFound(
            request.app.router['CommonConfirmAddress:get'].url_for(
                display_region=display_region,
                user_journey=user_journey,
                sub_user_journey=sub_user_journey
            ))


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/confirm-address/')
class CommonConfirmAddress(CommonCommon):
    """
    Common route to enable address confirmation from start and request journeys
    """
    @aiohttp_jinja2.template('common-confirm-address.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        if user_journey == 'start':
            await check_permission(request)

        session = await get_session(request)

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Confirm address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Confirm address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/confirm-address')

        attributes = await self.common_check_attributes(request, user_journey, sub_user_journey)

        uprn = attributes['uprn']
        uprn_ai_return = await AddressIndex.get_ai_uprn(request, uprn)

        try:
            room_number = session['attributes']['roomNumber']
        except KeyError:
            room_number = None

        session['attributes']['addressLine1'] = uprn_ai_return['response']['address']['addressLine1']
        session['attributes']['addressLine2'] = uprn_ai_return['response']['address']['addressLine2']
        session['attributes']['addressLine3'] = uprn_ai_return['response']['address']['addressLine3']
        session['attributes']['townName'] = uprn_ai_return['response']['address']['townName']
        session['attributes']['postcode'] = uprn_ai_return['response']['address']['postcode']
        session['attributes']['uprn'] = uprn_ai_return['response']['address']['uprn']
        session['attributes']['countryCode'] = uprn_ai_return['response']['address']['countryCode']
        session['attributes']['censusEstabType'] = uprn_ai_return['response']['address']['censusEstabType']
        session['attributes']['censusAddressType'] = uprn_ai_return['response']['address']['censusAddressType']
        session['attributes']['roomNumber'] = room_number
        session.changed()

        return {
            'page_title': page_title,
            'display_region': display_region,
            'user_journey': user_journey,
            'sub_user_journey': sub_user_journey,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'addressLine1': session['attributes']['addressLine1'],
            'addressLine2': session['attributes']['addressLine2'],
            'addressLine3': session['attributes']['addressLine3'],
            'townName': session['attributes']['townName'],
            'postcode': session['attributes']['postcode'],
            'roomNumber': session['attributes']['roomNumber'],
            'censusAddressType': session['attributes']['censusAddressType']
        }

    async def post(self, request):
        self.setup_request(request)

        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/confirm-address')

        session = await get_session(request)

        data = await request.post()

        try:
            address_confirmation = data['form-confirm-address']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'],
                        region_of_site=display_region)
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['CommonConfirmAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))

        if address_confirmation == 'yes':

            try:
                census_address_type_value = session['attributes']['censusAddressType']
                if census_address_type_value == 'NA':
                    logger.info('censusAddressType is NA', client_ip=request['client_ip'],
                                user_selection=address_confirmation)
                    raise HTTPFound(
                        request.app.router['CommonCallContactCentre:get'].url_for(
                            display_region=display_region, user_journey=user_journey, error='unable-to-match-address'))
                elif (census_address_type_value == 'CE') and \
                        (sub_user_journey == 'continuation-questionnaire'):
                    logger.info('continuation form for a CE - rejecting', client_ip=request['client_ip'],
                                sub_journey=sub_user_journey,
                                census_addr_type=census_address_type_value)
                    raise HTTPFound(
                        request.app.router['RequestContinuationNotAHousehold:get'].url_for(
                            display_region=display_region))
            except KeyError:
                logger.info('unable to check censusAddressType', client_ip=request['client_ip'])
                raise HTTPFound(
                    request.app.router['CommonCallContactCentre:get'].url_for(
                        display_region=display_region, user_journey=user_journey, error='unable-to-match-address'))

            try:
                country_code_value = session['attributes']['countryCode']
                uprn = session['attributes']['uprn']
                if country_code_value == 'S':
                    logger.info('address is in Scotland', client_ip=request['client_ip'],
                                country_code_found=country_code_value, uprn_value=uprn)
                    raise HTTPFound(
                        request.app.router['CommonAddressInScotland:get'].
                        url_for(display_region=display_region, user_journey=user_journey))
                elif country_code_value == 'N' and display_region != 'ni':
                    logger.info('address is in Northern Ireland but not display_region ni',
                                client_ip=request['client_ip'],
                                country_code_found=country_code_value,
                                region_of_site=display_region,
                                uprn_value=uprn)
                    raise HTTPFound(
                        request.app.router['CommonAddressInNorthernIreland:get'].
                        url_for(display_region=display_region, user_journey=user_journey))
                elif display_region == 'ni' and country_code_value == 'W':
                    logger.info('address is in Wales but display_region ni',
                                client_ip=request['client_ip'],
                                country_code_found=country_code_value,
                                region_of_site=display_region,
                                uprn_value=uprn)
                    raise HTTPFound(
                        request.app.router['CommonAddressInWales:get'].
                        url_for(display_region=display_region, user_journey=user_journey))
                elif display_region == 'ni' and country_code_value == 'E':
                    logger.info('address is in England but display_region ni',
                                client_ip=request['client_ip'],
                                country_code_found=country_code_value,
                                region_of_site=display_region,
                                uprn_value=uprn)
                    raise HTTPFound(
                        request.app.router['CommonAddressInEngland:get'].
                        url_for(display_region=display_region, user_journey=user_journey))
            except KeyError:
                logger.info('unable to check for region', client_ip=request['client_ip'])

            if sub_user_journey == 'link-address' or sub_user_journey == 'change-address':
                try:
                    uprn_return = await RHService.post_link_uac(request, session['case']['uacHash'],
                                                                session['attributes'])
                    session['case'] = uprn_return
                    session.changed()

                    self.validate_case(uprn_return)

                    if sub_user_journey == 'link-address':
                        raise HTTPFound(
                            request.app.router['StartAddressHasBeenLinked:get'].url_for(display_region=display_region))

                    elif sub_user_journey == 'change-address':
                        raise HTTPFound(
                            request.app.router['StartAddressHasBeenChanged:get'].url_for(display_region=display_region))

                except ClientResponseError as ex:
                    hashed_uac_value = session['case']['uacHash']
                    if ex.status == 404:
                        logger.info('uac linking error - unable to find uac (' + str(ex.status) + ')',
                                    client_ip=request['client_ip'], status_code=ex.status, uac_hashed=hashed_uac_value)
                    elif ex.status == 400:
                        logger.info('uac linking error - invalid request (' + str(ex.status) + ')',
                                    client_ip=request['client_ip'], status_code=ex.status, uac_hashed=hashed_uac_value)
                    else:
                        logger.error('uac linking error - unknown issue (' + str(ex.status) + ')',
                                     client_ip=request['client_ip'], status_code=ex.status, uac_hashed=hashed_uac_value)

                    cc_error = ''
                    if sub_user_journey == 'link-address':
                        cc_error = 'address-linking'
                    elif sub_user_journey == 'change-address':
                        cc_error = 'change-address'

                    raise HTTPFound(
                        request.app.router['CommonCallContactCentre:get'].url_for(
                            display_region=display_region, user_journey=user_journey, error=cc_error))

            elif user_journey == 'request':
                try:
                    uprn_return = await RHService.get_case_by_uprn(request, session['attributes']['uprn'])
                    session['attributes']['case_id'] = uprn_return['caseId']
                    session['attributes']['region'] = uprn_return['region']
                    session['attributes']['case_type'] = uprn_return['caseType']
                    session['attributes']['address_level'] = uprn_return['addressLevel']
                    if uprn_return['caseType'] == 'CE' and uprn_return['addressLevel'] == 'U':
                        session['attributes']['individual'] = True
                    session.changed()

                    await self.request_confirm_address_routing(request, user_journey, sub_user_journey,
                                                               display_region,
                                                               uprn_return['caseType'],
                                                               uprn_return['addressLevel'],
                                                               session['attributes']['individual'])

                except ClientResponseError as ex:
                    if ex.status == 404:
                        logger.info('get cases by uprn error - unable to match uprn (404)',
                                    client_ip=request['client_ip'], unmatched_uprn=session['attributes']['uprn'])
                        logger.info('requesting new case', client_ip=request['client_ip'])
                        try:
                            case_creation_return = await RHService.post_case_create(request, session['attributes'])
                            session['attributes']['case_id'] = case_creation_return['caseId']
                            session['attributes']['region'] = case_creation_return['region']
                            session['attributes']['case_type'] = case_creation_return['caseType']
                            session['attributes']['address_level'] = case_creation_return['addressLevel']
                            if case_creation_return['caseType'] == 'CE' and case_creation_return['addressLevel'] == 'U':
                                session['attributes']['individual'] = True
                            session.changed()

                            await self.request_confirm_address_routing(request, user_journey, sub_user_journey,
                                                                       display_region,
                                                                       case_creation_return['caseType'],
                                                                       case_creation_return['addressLevel'],
                                                                       session['attributes']['individual'])

                        except ClientResponseError as ex:
                            logger.warn('error requesting new case', client_ip=request['client_ip'])
                            raise ex
                    else:
                        raise ex

        elif address_confirmation == 'no':

            raise HTTPFound(
                request.app.router['CommonEnterAddress:get'].url_for(display_region=display_region,
                                                                     user_journey=user_journey,
                                                                     sub_user_journey=sub_user_journey))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'], user_selection=address_confirmation)
            flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['CommonConfirmAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/resident-or-manager/')
class CommonCEMangerQuestion(CommonCommon):
    """
    Common route to ask whether user is a resident or manager if they select a CE Estab as an address in fulfilments
    """
    @aiohttp_jinja2.template('common-resident-or-manager.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/resident-or-manager')

        session = await get_session(request)
        await self.common_check_attributes(request, user_journey, sub_user_journey)

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Confirm resident or manager'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Confirm resident or manager'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        return {
            'display_region': display_region,
            'user_journey': user_journey,
            'sub_user_journey': sub_user_journey,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'page_title': page_title,
            'addressLine1': session['attributes']['addressLine1'],
            'addressLine2': session['attributes']['addressLine2'],
            'addressLine3': session['attributes']['addressLine3'],
            'townName': session['attributes']['townName'],
            'postcode': session['attributes']['postcode']
        }

    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/resident-or-manager')

        session = await get_session(request)
        await self.common_check_attributes(request, user_journey, sub_user_journey)

        data = await request.post()

        try:
            resident_or_manager = data['form-resident-or-manager']
        except KeyError:
            logger.info('resident or manager question error',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['CommonCEMangerQuestion:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))

        if resident_or_manager == 'resident':

            session['attributes']['address_level'] = 'U'
            session['attributes']['individual'] = True
            session.changed()

            if sub_user_journey == 'paper-questionnaire':
                raise HTTPFound(
                    request.app.router['RequestCommonEnterName:get'].url_for(
                        request_type=sub_user_journey, display_region=display_region))
            else:
                raise HTTPFound(
                    request.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                        request_type=sub_user_journey, display_region=display_region))

        elif resident_or_manager == 'manager':

            session['attributes']['individual'] = False
            session.changed()

            if sub_user_journey == 'paper-questionnaire':
                if display_region == 'ni':
                    raise HTTPFound(
                        request.app.router['RequestFormNIManager:get'].url_for())
                else:
                    raise HTTPFound(
                        request.app.router['RequestQuestionnaireManager:get'].url_for(
                            request_type=sub_user_journey, display_region=display_region))
            else:
                if display_region == 'ni':
                    raise HTTPFound(
                        request.app.router['RequestCodeNIManager:get'].url_for())
                else:
                    raise HTTPFound(
                        request.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                            request_type=sub_user_journey, display_region=display_region))

        else:
            # catch all just in case, should never get here
            logger.info('resident or manager question error',
                        client_ip=request['client_ip'],
                        manager_or_resident=resident_or_manager)
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['CommonCEMangerQuestion:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/enter-flat-or-room-number/')
class CommonEnterRoomNumber(CommonCommon):
    """
    Common route to allow user to enter a room number if in a CE
    """
    @aiohttp_jinja2.template('common-enter-room-number.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey +
                       '/enter-flat-or-room-number')

        session_attributes = await self.common_check_attributes(request, user_journey, sub_user_journey)

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Enter flat or room number'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Enter flat or room number'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        if session_attributes['roomNumber']:
            room_number = session_attributes['roomNumber']
        else:
            room_number = None
        return {
            'display_region': display_region,
            'user_journey': user_journey,
            'sub_user_journey': sub_user_journey,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'page_title': page_title,
            'room_number': room_number
        }

    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey +
                       '/enter-flat-or-room-number')

        session = await get_session(request)
        session_attributes = await self.common_check_attributes(request, user_journey, sub_user_journey)

        data = await request.post()

        try:
            room_number = data['form-enter-room-number']
            if (room_number == '') or (len(room_number) > 10):
                raise KeyError
            session['attributes']['roomNumber'] = room_number
            session.changed()
            try:
                if session_attributes['first_name']:
                    raise HTTPFound(
                        request.app.router['RequestCommonConfirmSendByPost:get'].url_for(
                            display_region=display_region,
                            user_journey=user_journey,
                            request_type=sub_user_journey
                        ))
            except KeyError:
                raise HTTPFound(
                    request.app.router['CommonConfirmAddress:get'].url_for(
                        display_region=display_region,
                        user_journey=user_journey,
                        sub_user_journey=sub_user_journey
                    ))

        except KeyError:
            room_number_entered = data['form-enter-room-number']
            logger.info('room number question error', client_ip=request['client_ip'],
                        room_number_given=room_number_entered)
            if len(room_number_entered) > 10:
                if display_region == 'cy':
                    # TODO Add Welsh translation
                    flash(request, FlashMessage.generate_flash_message(
                        'You have entered too many characters. Enter up to 10 characters', 'ERROR',
                        'ROOM_NUMBER_ENTER_ERROR', 'error-room-number-len'))
                else:
                    flash(request, FlashMessage.generate_flash_message(
                        'You have entered too many characters. Enter up to 10 characters', 'ERROR',
                        'ROOM_NUMBER_ENTER_ERROR', 'error-room-number-len'))
            else:
                if display_region == 'cy':
                    # TODO Add Welsh translation
                    flash(request, FlashMessage.generate_flash_message('Enter your flat or room number', 'ERROR',
                                                                       'ROOM_NUMBER_ENTER_ERROR', 'error-room-number'))
                else:
                    flash(request, FlashMessage.generate_flash_message('Enter your flat or room number', 'ERROR',
                                                                       'ROOM_NUMBER_ENTER_ERROR', 'error-room-number'))
            raise HTTPFound(
                request.app.router['CommonEnterRoomNumber:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))
