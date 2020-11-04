import aiohttp_jinja2
import json

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
# eg start or requests


class CommonCommon(View):
    @staticmethod
    def common_check_session(request, user_journey, sub_user_journey):
        if request.cookies.get('RH_SESSION') is None:
            logger.info('session timed out', client_ip=request['client_ip'])
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
    def requests_confirm_address_routing(request, user_journey, sub_user_journey, display_region,
                                         case_type, address_level):

        if case_type == 'CE' and address_level == 'E':
            raise HTTPFound(
                request.app.router['CommonCEMangerQuestion:get'].url_for(user_journey=user_journey,
                                                                         sub_user_journey=sub_user_journey,
                                                                         display_region=display_region))
        else:
            if sub_user_journey == 'paper-form':
                raise HTTPFound(
                    request.app.router['RequestCommonEnterName:get'].url_for(
                        request_type=sub_user_journey, display_region=display_region))
            else:
                raise HTTPFound(
                    request.app.router['RequestCodeSelectMethod:get'].url_for(
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

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'This address is not part of the census for England and Wales'
            locale = 'cy'
        else:
            page_title = 'This address is not part of the census for England and Wales'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/address-in-scotland')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'user_journey': user_journey,
            'page_url': View.gen_page_url(request)
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

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'
        return {
            'display_region': display_region,
            'user_journey': user_journey,
            'sub_user_journey': sub_user_journey,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
        }

    @aiohttp_jinja2.template('common-enter-address.html')
    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/enter-address')

        if user_journey == 'start':
            await check_permission(request)

        data = await request.post()

        try:
            postcode = ProcessPostcode.validate_postcode(data['form-enter-address-postcode'], locale)
            logger.info('valid postcode', client_ip=request['client_ip'])

        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info('invalid postcode', client_ip=request['client_ip'])
            flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'POSTCODE_ENTER_ERROR', 'postcode')
            flash(request, flash_message)
            raise HTTPFound(
                request.app.router['CommonEnterAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))

        session = await get_session(request)

        if user_journey == 'start':
            session['attributes']['postcode'] = postcode
            session.changed()
        elif user_journey == 'requests':
            attributes = {
                'postcode': postcode
            }
            session['attributes'] = attributes

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
            page_title = 'Dewiswch eich cyfeiriad'
            locale = 'cy'
        else:
            page_title = 'Select your address'
            locale = 'en'

        attributes = await self.common_check_attributes(request, user_journey, sub_user_journey)

        address_content = await AddressIndex.get_postcode_return(request, attributes['postcode'], display_region)
        address_content['page_title'] = page_title
        address_content['display_region'] = display_region
        address_content['user_journey'] = user_journey
        address_content['sub_user_journey'] = sub_user_journey
        address_content['locale'] = locale
        address_content['page_url'] = View.gen_page_url(request)

        return address_content

    @aiohttp_jinja2.template('common-select-address.html')
    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        if user_journey == 'start':
            await check_permission(request)

        if display_region == 'cy':
            page_title = 'Dewiswch eich cyfeiriad'
            locale = 'cy'
        else:
            page_title = 'Select your address'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/select-address')

        attributes = await self.common_check_attributes(request, user_journey, sub_user_journey)

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
            address_content['user_journey'] = user_journey
            address_content['sub_user_journey'] = sub_user_journey
            address_content['locale'] = locale
            address_content['page_url'] = View.gen_page_url(request)
            return address_content

        if form_return['uprn'] == 'xxxx':
            raise HTTPFound(
                request.app.router['CommonCallContactCentre:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    error='address-not-found'))
        else:
            session = await get_session(request)
            session['attributes']['address'] = form_return['address']
            session['attributes']['uprn'] = form_return['uprn']
            session.changed()
            logger.info('session updated', client_ip=request['client_ip'])

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

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = "Is this the correct address?"
            locale = 'cy'
        else:
            page_title = 'Is this the correct address?'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/confirm-address')

        session = await get_session(request)
        attributes = await self.common_check_attributes(request, user_journey, sub_user_journey)

        uprn = attributes['uprn']
        uprn_ai_return = await AddressIndex.get_ai_uprn(request, uprn)

        attributes = {
            "addressLine1": uprn_ai_return['response']['address']['addressLine1'],
            "addressLine2": uprn_ai_return['response']['address']['addressLine2'],
            "addressLine3": uprn_ai_return['response']['address']['addressLine3'],
            "townName": uprn_ai_return['response']['address']['townName'],
            "postcode": uprn_ai_return['response']['address']['postcode'],
            "uprn": uprn_ai_return['response']['address']['uprn'],
            "countryCode": uprn_ai_return['response']['address']['countryCode'],
            "censusEstabType": uprn_ai_return['response']['address']['censusEstabType'],
            "censusAddressType": uprn_ai_return['response']['address']['censusAddressType']
        }

        session['attributes'] = attributes
        session.changed()

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['user_journey'] = user_journey
        attributes['sub_user_journey'] = sub_user_journey
        attributes['locale'] = locale
        attributes['page_url'] = View.gen_page_url(request)

        return attributes

    @aiohttp_jinja2.template('common-confirm-address.html')
    async def post(self, request):
        self.setup_request(request)

        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = "Is this the correct address?"
            locale = 'cy'
        else:
            page_title = 'Is this the correct address?'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/confirm-address')

        session = await get_session(request)
        attributes = await self.common_check_attributes(request, user_journey, sub_user_journey)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['user_journey'] = user_journey
        attributes['sub_user_journey'] = sub_user_journey
        attributes['locale'] = locale
        attributes['page_url'] = View.gen_page_url(request)

        data = await request.post()

        try:
            address_confirmation = data['form-confirm-address']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return attributes

        if address_confirmation == 'yes':

            try:
                if session['attributes']['countryCode'] == 'S':
                    logger.info('address is in Scotland', client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['CommonAddressInScotland:get'].
                        url_for(display_region=display_region, user_journey=user_journey))
            except KeyError:
                logger.info('unable to check for region', client_ip=request['client_ip'])

            try:
                if session['attributes']['censusAddressType'] == 'NA':
                    logger.info('censusAddressType is NA', client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['CommonCallContactCentre:get'].url_for(
                            display_region=display_region, user_journey=user_journey, error='unable-to-match-address'))
            except KeyError:
                logger.info('unable to check censusAddressType', client_ip=request['client_ip'])
                raise HTTPFound(
                    request.app.router['CommonCallContactCentre:get'].url_for(
                        display_region=display_region, user_journey=user_journey, error='unable-to-match-address'))

            if sub_user_journey == 'unlinked' or sub_user_journey == 'change-address':
                try:
                    uprn_return = await RHService.post_link_uac(request, session['case']['uacHash'],
                                                                session['attributes'])
                    session['case'] = uprn_return
                    session.changed()

                    self.validate_case(uprn_return)

                    if sub_user_journey == 'unlinked':
                        raise HTTPFound(
                            request.app.router['StartAddressHasBeenLinked:get'].url_for(display_region=display_region))

                    elif sub_user_journey == 'change-address':
                        raise HTTPFound(
                            request.app.router['StartAddressHasBeenChanged:get'].url_for(display_region=display_region))

                except ClientResponseError as ex:
                    if ex.status == 404:
                        logger.info('uac linking error - unable to find uac (' + str(ex.status) + ')',
                                    client_ip=request['client_ip'], status_code=ex.status)
                    elif ex.status == 400:
                        logger.info('uac linking error - invalid request (' + str(ex.status) + ')',
                                    client_ip=request['client_ip'], status_code=ex.status)
                    else:
                        logger.error('uac linking error - unknown issue (' + str(ex.status) + ')',
                                     client_ip=request['client_ip'], status_code=ex.status)

                    cc_error = ''
                    if sub_user_journey == 'unlinked':
                        cc_error = 'address-linking'
                    elif sub_user_journey == 'change-address':
                        cc_error = 'change-address'

                    raise HTTPFound(
                        request.app.router['CommonCallContactCentre:get'].url_for(
                            display_region=display_region, user_journey=user_journey, error=cc_error))

            elif user_journey == 'requests':
                try:
                    uprn_return = await RHService.get_case_by_uprn(request, session['attributes']['uprn'])
                    session['attributes']['case_id'] = uprn_return['caseId']
                    session['attributes']['region'] = uprn_return['region']
                    session['attributes']['case_type'] = uprn_return['caseType']
                    session['attributes']['address_level'] = uprn_return['addressLevel']
                    session.changed()

                    await self.requests_confirm_address_routing(request, user_journey, sub_user_journey,
                                                                display_region,
                                                                uprn_return['caseType'],
                                                                uprn_return['addressLevel'])

                except ClientResponseError as ex:
                    if ex.status == 404:
                        logger.info('get cases by uprn error - unable to match uprn (404)',
                                    client_ip=request['client_ip'])
                        logger.info('requesting new case', client_ip=request['client_ip'])
                        try:
                            case_creation_return = await RHService.post_case_create(request, session['attributes'])
                            session['attributes']['case_id'] = case_creation_return['caseId']
                            session['attributes']['region'] = case_creation_return['region']
                            session['attributes']['case_type'] = case_creation_return['caseType']
                            session['attributes']['address_level'] = case_creation_return['addressLevel']
                            session.changed()

                            await self.requests_confirm_address_routing(request, user_journey, sub_user_journey,
                                                                        display_region,
                                                                        case_creation_return['caseType'],
                                                                        case_creation_return['addressLevel'])

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
                        client_ip=request['client_ip'])
            flash(request, NO_SELECTION_CHECK_MSG)
            attributes['page_title'] = page_title
            attributes['display_region'] = display_region
            attributes['user_journey'] = user_journey
            attributes['sub_user_journey'] = sub_user_journey
            attributes['locale'] = locale
            attributes['page_url'] = View.gen_page_url(request)
            return attributes


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
            locale = 'cy'
            # TODO Add Welsh translation
            page_title = 'Are you a resident or manager of this establishment?'
        else:
            locale = 'en'
            page_title = 'Are you a resident or manager of this establishment?'
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

    @aiohttp_jinja2.template('common-resident-or-manager.html')
    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        if display_region == 'cy':
            locale = 'cy'
            # TODO Add Welsh translation
            page_title = 'Are you a resident or manager of this establishment?'
        else:
            locale = 'en'
            page_title = 'Are you a resident or manager of this establishment?'

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
                'postcode': session['attributes']['postcode']
            }

        if resident_or_manager == 'resident':

            session['attributes']['address_level'] = 'U'
            session.changed()

            if sub_user_journey == 'paper-form':
                raise HTTPFound(
                    request.app.router['RequestCommonEnterName:get'].url_for(
                        request_type=sub_user_journey, display_region=display_region))
            else:
                raise HTTPFound(
                    request.app.router['RequestCodeSelectMethod:get'].url_for(
                        request_type=sub_user_journey, display_region=display_region))

        elif resident_or_manager == 'manager':
            if sub_user_journey == 'paper-form':
                raise HTTPFound(
                    request.app.router['RequestFormManager:get'].url_for(
                        request_type=sub_user_journey, display_region=display_region))
            else:
                raise HTTPFound(
                    request.app.router['RequestCodeSelectMethod:get'].url_for(
                        request_type=sub_user_journey, display_region=display_region))

        else:
            # catch all just in case, should never get here
            logger.info('resident or manager question error',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
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
                'postcode': session['attributes']['postcode']
            }
