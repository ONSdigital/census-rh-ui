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
from .security import get_permitted_session, forget
from .utils import View, ProcessPostcode, InvalidDataError, InvalidDataErrorWelsh, FlashMessage, AddressIndex, RHService
from .session import get_existing_session, get_session_value

logger = get_logger('respondent-home')
common_routes = RouteTableDef()

# common_handlers contains routes and supporting code for any route in more than top level journey path
# eg start or request


class CommonCommon(View):

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
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']

        if display_region == 'ni':
            page_title = 'Address not part of census for Northern Ireland'
            locale = 'en'
        elif display_region == 'cy':
            page_title = "Nid yw'r cyfeiriad yn rhan o'r cyfrifiad ar gyfer Cymru a Lloegr"
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
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']

        if display_region == 'cy':
            page_title = "Rhan cyfeiriad y cyfrifiad yng Ngogledd Iwerddon"
            locale = 'cy'
        else:
            page_title = 'Address part of census in Northern Ireland'
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
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        if display_region == 'cy':
            page_title = 'Cofrestru cyfeiriad'
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
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        error = request.match_info['error']

        if display_region == 'cy':
            page_title = "Ffoniwch Canolfan Gyswllt i Gwsmeriaid y Cyfrifiad"
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
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/enter-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_session(request)

        individual = False

        if user_journey == 'start':
            session['attributes']['individual'] = False
            session.changed()
            individual = False
        elif user_journey == 'request':
            await forget(request)  # Removes identity in case user has existing auth session
            try:
                individual = session['attributes']['individual']
            except KeyError:
                individual = False
                attributes = {'individual': False}
                session['attributes'] = attributes

        if display_region == 'cy':
            page_title = 'Nodi cyfeiriad'
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
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/enter-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_existing_session(request, user_journey, sub_user_journey)

        data = await request.post()

        try:
            postcode = ProcessPostcode.validate_postcode(data['form-enter-address-postcode'], display_region)
            logger.info('valid postcode',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        postcode_entered=postcode,
                        region_of_site=display_region)

        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info('invalid postcode',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
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
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/select-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_existing_session(request, user_journey, sub_user_journey)

        if display_region == 'cy':
            page_title = 'Dewis cyfeiriad'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Select address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)
        postcode = attributes['postcode']

        address_content = await AddressIndex.get_postcode_return(request, postcode, display_region)
        address_content['page_title'] = page_title
        address_content['display_region'] = display_region
        address_content['user_journey'] = user_journey
        address_content['sub_user_journey'] = sub_user_journey
        address_content['locale'] = locale
        address_content['page_url'] = View.gen_page_url(request)
        address_content['contact_us_link'] = View.get_campaign_site_link(request, display_region, 'contact-us')
        address_content['call_centre_number'] = View.get_call_centre_number(display_region)

        return address_content

    async def post(self, request):
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/select-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_existing_session(request, user_journey, sub_user_journey)

        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)

        data = await request.post()

        try:
            selected_uprn = data['form-pick-address']
        except KeyError:
            logger.info('no address selected',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        region_of_site=display_region,
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
            attributes['uprn'] = selected_uprn
            session.changed()
            logger.info('session updated',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        uprn_selected=selected_uprn,
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
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/confirm-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_existing_session(request, user_journey, sub_user_journey)

        if display_region == 'cy':
            page_title = 'Cadarnhau cyfeiriad'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Confirm address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)
        uprn = attributes['uprn']

        try:
            rhsvc_uprn_return = await RHService.get_case_by_uprn(request, uprn)
            logger.info('case matching uprn found in RHSvc',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'])
            attributes['addressLine1'] = rhsvc_uprn_return['addressLine1']
            attributes['addressLine2'] = rhsvc_uprn_return['addressLine2']
            attributes['addressLine3'] = rhsvc_uprn_return['addressLine3']
            attributes['townName'] = rhsvc_uprn_return['townName']
            attributes['postcode'] = rhsvc_uprn_return['postcode']
            attributes['uprn'] = rhsvc_uprn_return['uprn']
            attributes['countryCode'] = rhsvc_uprn_return['region']
            attributes['censusAddressType'] = rhsvc_uprn_return['addressType']
            attributes['case_id'] = rhsvc_uprn_return['caseId']
            attributes['region'] = rhsvc_uprn_return['region']
            attributes['case_type'] = rhsvc_uprn_return['caseType']
            attributes['address_level'] = rhsvc_uprn_return['addressLevel']
            attributes['censusEstabType'] = rhsvc_uprn_return['estabType']

        except ClientResponseError as ex:
            if ex.status == 404:
                logger.info('no case matching uprn in RHSvc - using AIMS data',
                            client_ip=request['client_ip'],
                            client_id=request['client_id'],
                            trace=request['trace'])

                aims_uprn_return = await AddressIndex.get_ai_uprn(request, uprn)

                # Ensure no session data from previous RM case used later
                if 'case_id' in attributes:
                    del attributes['case_id']
                    if 'region' in attributes:
                        del attributes['region']
                    if 'case_type' in attributes:
                        del attributes['case_type']
                    if 'address_level' in attributes:
                        del attributes['address_level']

                attributes['addressLine1'] = aims_uprn_return['response']['address']['addressLine1']
                attributes['addressLine2'] = aims_uprn_return['response']['address']['addressLine2']
                attributes['addressLine3'] = aims_uprn_return['response']['address']['addressLine3']
                attributes['townName'] = aims_uprn_return['response']['address']['townName']
                attributes['postcode'] = aims_uprn_return['response']['address']['postcode']
                attributes['uprn'] = aims_uprn_return['response']['address']['uprn']
                attributes['countryCode'] = aims_uprn_return['response']['address']['countryCode']
                attributes['censusEstabType'] = aims_uprn_return['response']['address']['censusEstabType']
                census_address_type = aims_uprn_return['response']['address']['censusAddressType']
                if census_address_type == 'NA':
                    logger.info('AIMS addressType is NA - setting to HH',
                                client_ip=request['client_ip'],
                                client_id=request['client_id'],
                                trace=request['trace'])
                    attributes['censusAddressType'] = 'HH'
                else:
                    attributes['censusAddressType'] = census_address_type
            else:
                logger.info('error response from RHSvc',
                            client_ip=request['client_ip'],
                            client_id=request['client_id'],
                            trace=request['trace'],
                            status_code=ex.status)
                raise ex

        try:
            room_number = attributes['roomNumber']
        except KeyError:
            room_number = None

        attributes['roomNumber'] = room_number
        session.changed()

        return {
            'page_title': page_title,
            'display_region': display_region,
            'user_journey': user_journey,
            'sub_user_journey': sub_user_journey,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'addressLine1': attributes['addressLine1'],
            'addressLine2': attributes['addressLine2'],
            'addressLine3': attributes['addressLine3'],
            'townName': attributes['townName'],
            'postcode': attributes['postcode'],
            'roomNumber': attributes['roomNumber'],
            'censusAddressType': attributes['censusAddressType']
        }

    async def post(self, request):
        tracking = {"client_ip": request['client_ip'], "client_id": request['client_id'], "trace": request['trace']}

        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/confirm-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_existing_session(request, user_journey, sub_user_journey)

        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)

        data = await request.post()

        try:
            address_confirmation = data['form-confirm-address']
        except KeyError:
            logger.info('address confirmation error', **tracking, region_of_site=display_region)
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

            if (attributes['censusAddressType'] == 'CE') and (sub_user_journey == 'continuation-questionnaire'):
                logger.info('continuation form for a CE - rejecting',
                            **tracking,
                            sub_journey=sub_user_journey,
                            census_addr_type=attributes['censusAddressType'])
                raise HTTPFound(
                    request.app.router['RequestContinuationNotAHousehold:get'].url_for(
                        display_region=display_region))

            try:
                country_code_value = attributes['countryCode']
                uprn = attributes['uprn']
                if country_code_value == 'S':
                    logger.info('address is in Scotland',
                                **tracking,
                                country_code_found=country_code_value,
                                uprn_value=uprn)
                    raise HTTPFound(
                        request.app.router['CommonAddressInScotland:get'].
                        url_for(display_region=display_region, user_journey=user_journey))
                elif country_code_value == 'N' and display_region != 'ni':
                    logger.info('address is in Northern Ireland but not display_region ni',
                                **tracking,
                                country_code_found=country_code_value,
                                region_of_site=display_region,
                                uprn_value=uprn)
                    raise HTTPFound(
                        request.app.router['CommonAddressInNorthernIreland:get'].
                        url_for(display_region=display_region, user_journey=user_journey))
                elif display_region == 'ni' and country_code_value == 'W':
                    logger.info('address is in Wales but display_region ni',
                                country_code_found=country_code_value,
                                **tracking,
                                region_of_site=display_region,
                                uprn_value=uprn)
                    raise HTTPFound(
                        request.app.router['CommonAddressInWales:get'].
                        url_for(display_region=display_region, user_journey=user_journey))
                elif display_region == 'ni' and country_code_value == 'E':
                    logger.info('address is in England but display_region ni',
                                **tracking,
                                country_code_found=country_code_value,
                                region_of_site=display_region,
                                uprn_value=uprn)
                    raise HTTPFound(
                        request.app.router['CommonAddressInEngland:get'].
                        url_for(display_region=display_region, user_journey=user_journey))
            except KeyError:
                logger.info('unable to check for region',
                            client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])

            if sub_user_journey == 'link-address' or sub_user_journey == 'change-address':
                try:
                    uprn_return = await RHService.post_link_uac(request, session['case']['uacHash'], attributes)
                    session['case'] = uprn_return
                    session.changed()

                    self.validate_case(uprn_return)

                    if display_region == 'cy':
                        locale = 'cy'
                    else:
                        locale = 'en'

                    case = get_session_value(session, 'case', user_journey, sub_user_journey)

                    if case['region'] == 'N':
                        raise HTTPFound(
                            request.app.router['StartNILanguageOptions:get'].url_for())
                    else:
                        attributes['language'] = locale
                        attributes['display_region'] = display_region
                        await self.call_questionnaire(request, case,
                                                      attributes, request.app,
                                                      session.get('adlocation'))

                except ClientResponseError as ex:
                    hashed_uac_value = session['case']['uacHash']
                    if ex.status == 404:
                        logger.info('uac linking error - unable to find uac (' + str(ex.status) + ')',
                                    **tracking,
                                    status_code=ex.status, uac_hashed=hashed_uac_value)
                    elif ex.status == 400:
                        logger.info('uac linking error - invalid request (' + str(ex.status) + ')',
                                    **tracking,
                                    status_code=ex.status,
                                    uac_hashed=hashed_uac_value)
                    else:
                        logger.error('uac linking error - unknown issue (' + str(ex.status) + ')',
                                     **tracking,
                                     status_code=ex.status,
                                     uac_hashed=hashed_uac_value)

                    cc_error = ''
                    if sub_user_journey == 'link-address':
                        cc_error = 'address-linking'
                    elif sub_user_journey == 'change-address':
                        cc_error = 'change-address'

                    raise HTTPFound(
                        request.app.router['CommonCallContactCentre:get'].url_for(
                            display_region=display_region, user_journey=user_journey, error=cc_error))

            elif user_journey == 'request':
                if attributes.get('case_id'):
                    if attributes['case_type'] == 'CE' and attributes['address_level'] == 'U':
                        attributes['individual'] = True
                    session.changed()

                    await self.request_confirm_address_routing(request, user_journey, sub_user_journey,
                                                               display_region,
                                                               attributes['case_type'],
                                                               attributes['address_level'],
                                                               attributes['individual'])
                else:
                    logger.info('requesting new case', **tracking)
                    try:
                        case_creation_return = await RHService.post_case_create(request, attributes)
                        attributes['case_id'] = case_creation_return['caseId']
                        attributes['region'] = case_creation_return['region']
                        attributes['case_type'] = case_creation_return['caseType']
                        attributes['address_level'] = case_creation_return['addressLevel']
                        if case_creation_return['caseType'] == 'CE' and case_creation_return['addressLevel'] == 'U':
                            attributes['individual'] = True
                        session.changed()

                        await self.request_confirm_address_routing(request, user_journey, sub_user_journey,
                                                                   display_region,
                                                                   case_creation_return['caseType'],
                                                                   case_creation_return['addressLevel'],
                                                                   attributes['individual'])

                    except ClientResponseError as ex:
                        logger.warn('error requesting new case', **tracking)
                        raise ex

        elif address_confirmation == 'no':

            raise HTTPFound(
                request.app.router['CommonEnterAddress:get'].url_for(display_region=display_region,
                                                                     user_journey=user_journey,
                                                                     sub_user_journey=sub_user_journey))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error', **tracking, user_selection=address_confirmation)
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
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/resident-or-manager')

        session = await get_existing_session(request, user_journey, sub_user_journey)
        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)

        if display_region == 'cy':
            page_title = 'Cadarnhau preswylydd neu reolwr'
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
            'addressLine1': attributes['addressLine1'],
            'addressLine2': attributes['addressLine2'],
            'addressLine3': attributes['addressLine3'],
            'townName': attributes['townName'],
            'postcode': attributes['postcode']
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/resident-or-manager')

        session = await get_existing_session(request, user_journey, sub_user_journey)
        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)

        data = await request.post()

        try:
            resident_or_manager = data['form-resident-or-manager']
        except KeyError:
            logger.info('resident or manager question error',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
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

            attributes['address_level'] = 'U'
            attributes['individual'] = True
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

            attributes['individual'] = False
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
                        client_id=request['client_id'],
                        trace=request['trace'],
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
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey +
                       '/enter-flat-or-room-number')

        session = await get_existing_session(request, user_journey, sub_user_journey)
        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)

        if display_region == 'cy':
            page_title = 'Nodi rhif fflat neu ystafell'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Enter flat or room number'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        if attributes['roomNumber']:
            room_number = attributes['roomNumber']
        else:
            room_number = None
        if attributes.get('first_name'):
            previous_page = 'send-by-post'
        else:
            previous_page = 'confirm-address'
        return {
            'display_region': display_region,
            'user_journey': user_journey,
            'sub_user_journey': sub_user_journey,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'page_title': page_title,
            'room_number': room_number,
            'previous_page': previous_page
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey +
                       '/enter-flat-or-room-number')

        session = await get_existing_session(request, user_journey, sub_user_journey)
        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)

        data = await request.post()

        try:
            room_number = data['form-enter-room-number']
            if len(room_number) > 10:
                raise KeyError
            attributes['roomNumber'] = room_number.strip()
            session.changed()
            try:
                if attributes['first_name']:
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
            logger.info('room number question error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        room_number_given=room_number_entered)
            if len(room_number_entered) > 10:
                if display_region == 'cy':
                    flash(request, FlashMessage.generate_flash_message(
                        "Rydych wedi defnyddio gormod o nodau. Rhowch hyd at 10 o nodau", 'ERROR',
                        'ROOM_NUMBER_ENTER_ERROR', 'error-room-number-len'))
                else:
                    flash(request, FlashMessage.generate_flash_message(
                        'You have entered too many characters. Enter up to 10 characters', 'ERROR',
                        'ROOM_NUMBER_ENTER_ERROR', 'error-room-number-len'))
            raise HTTPFound(
                request.app.router['CommonEnterRoomNumber:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))
