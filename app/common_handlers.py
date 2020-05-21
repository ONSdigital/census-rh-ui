import aiohttp_jinja2
import json

from aiohttp.web import HTTPFound, RouteTableDef
from structlog import get_logger
from aiohttp_session import get_session
from aiohttp.client_exceptions import (ClientResponseError)

from . import (ADDRESS_CHECK_MSG,
               ADDRESS_SELECT_CHECK_MSG,
               ADDRESS_CHECK_MSG_CY,
               ADDRESS_SELECT_CHECK_MSG_CY)

from .flash import flash
from .security import check_permission
from .utils import View, ProcessPostcode, InvalidDataError, InvalidDataErrorWelsh, FlashMessage, AddressIndex, RHService

logger = get_logger('respondent-home')
common_routes = RouteTableDef()

# common_handlers contains routes and supporting code for any route in more than top level journey path
# eg start or requests


class CommonCommon(View):
    @staticmethod
    def common_check_session(request, user_journey, sub_user_journey, display_region):
        if request.cookies.get('RH_SESSION') is None:
            logger.info('session timed out', client_ip=request['client_ip'])
            raise HTTPFound(
                request.app.router['CommonTimeout:get'].url_for(
                    display_region=display_region, user_journey=user_journey, sub_user_journey=sub_user_journey))

    async def common_check_attributes(self, request, user_journey, sub_user_journey, display_region):
        self.common_check_session(request, user_journey, sub_user_journey, display_region)
        session = await get_session(request)

        if session['attributes'] != {}:
            attributes = session['attributes']
        else:
            raise HTTPFound(
                request.app.router['CommonTimeout:get'].url_for(
                    display_region=display_region, user_journey=user_journey, sub_user_journey=sub_user_journey))

        return attributes


# Route to render a Timeout page that can be triggered during start/unlinked journey and all requests journeys
@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/timeout/')
class CommonTimeout(CommonCommon):
    @aiohttp_jinja2.template('common-timeout.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/timeout')

        if display_region == 'cy':
            page_title = 'Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch'
            locale = 'cy'
        else:
            page_title = 'Your session has timed out due to inactivity'
            locale = 'en'

        return {
            'display_region': display_region,
            'user_journey': user_journey,
            'sub_user_journey': sub_user_journey,
            'page_title': page_title,
            'locale': locale
        }


# Route to render an 'Address in Scotland' page during address lookups
@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys + '/address-in-scotland/')
class CommonAddressInScotland(CommonCommon):
    @aiohttp_jinja2.template('common-address-in-scotland.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']

        if display_region == 'cy':
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
            'user_journey': user_journey
        }


# Common route to render a 'Call the Contact Centre' page from any journey
@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys + '/call-contact-centre/{error}')
class CommonCallContactCentre(CommonCommon):
    @aiohttp_jinja2.template('common-contact-centre.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        error = request.match_info['error']

        if display_region == 'cy':
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
            'error': error
        }


# Common route to enable address entry via postcode from start and request journeys
@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/enter-address/')
class CommonEnterAddress(CommonCommon):
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
            'locale': locale
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


# Common route to enable address selection from start and request journeys
@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/select-address/')
class CommonSelectAddress(CommonCommon):
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

        attributes = await self.common_check_attributes(request, user_journey, sub_user_journey, display_region)

        address_content = await AddressIndex.get_postcode_return(request, attributes['postcode'], display_region)
        address_content['page_title'] = page_title
        address_content['display_region'] = display_region
        address_content['user_journey'] = user_journey
        address_content['sub_user_journey'] = sub_user_journey
        address_content['locale'] = locale

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

        attributes = await self.common_check_attributes(request, user_journey, sub_user_journey, display_region)

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


# Common route to enable address confirmation from start and request journeys
@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/confirm-address/')
class CommonConfirmAddress(CommonCommon):
    @aiohttp_jinja2.template('common-confirm-address.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        if user_journey == 'start':
            await check_permission(request)

        if display_region == 'cy':
            page_title = "Ydy'r cyfeiriad hwn yn gywir?"
            locale = 'cy'
        else:
            page_title = 'Is this address correct?'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/confirm-address')

        session = await get_session(request)
        attributes = await self.common_check_attributes(request, user_journey, sub_user_journey, display_region)

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
        attributes['country_code'] = uprn_ai_return['response']['address']['countryCode']

        return attributes

    @aiohttp_jinja2.template('common-confirm-address.html')
    async def post(self, request):
        self.setup_request(request)

        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        if display_region == 'cy':
            page_title = "Ydy'r cyfeiriad hwn yn gywir?"
            locale = 'cy'
        else:
            page_title = 'Is this address correct?'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/confirm-address')

        session = await get_session(request)
        attributes = await self.common_check_attributes(request, user_journey, sub_user_journey, display_region)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['user_journey'] = user_journey
        attributes['sub_user_journey'] = sub_user_journey
        attributes['locale'] = locale

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

            try:
                if session['attributes']['countryCode'] == 'S':
                    logger.info('address is in Scotland', client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['CommonAddressInScotland:get'].
                        url_for(display_region=display_region, user_journey=user_journey))
            except KeyError:
                logger.info('unable to check for region', client_ip=request['client_ip'])

            if sub_user_journey == 'unlinked':
                try:
                    uprn_return = await RHService.post_unlinked_uac(request, session['case']['uacHash'],
                                                                    session['attributes'])
                    session['case'] = uprn_return
                    session.changed()

                    self.validate_case(uprn_return)

                    raise HTTPFound(
                        request.app.router['StartAddressHasBeenLinked:get'].url_for(display_region=display_region))

                except ClientResponseError as ex:
                    if ex.status == 404:
                        logger.error('uac linking error - unable to find uac (' + ex.status + ')',
                                     client_ip=request['client_ip'])
                    elif ex.status == 400:
                        logger.error('uac linking error - invalid request (' + ex.status + ')',
                                     client_ip=request['client_ip'])
                    else:
                        logger.error('uac linking error - unknown issue (' + ex.status + ')',
                                     client_ip=request['client_ip'])
                    raise HTTPFound(
                        request.app.router['CommonCallContactCentre:get'].url_for(
                            display_region=display_region, user_journey=user_journey, error='address-linking'))

            elif user_journey == 'requests':
                try:
                    uprn_return = await RHService.get_cases_by_uprn(request, session['attributes']['uprn'])
                    session['attributes']['case_id'] = uprn_return[0]['caseId']
                    session['attributes']['region'] = uprn_return[0]['region']
                    session.changed()
                    raise HTTPFound(
                        request.app.router['RequestCodeEnterMobile:get'].url_for(request_type=sub_user_journey,
                                                                                 display_region=display_region))
                except ClientResponseError as ex:
                    if ex.status == 404:
                        logger.info('get cases by uprn error - unable to match uprn (404)',
                                    client_ip=request['client_ip'])
                        raise HTTPFound(
                            request.app.router['CommonCallContactCentre:get'].url_for(user_journey=user_journey,
                                                                                      display_region=display_region,
                                                                                      error='unable-to-match-address'))
                    else:
                        raise ex

        elif address_confirmation == 'change':
            raise HTTPFound(
                request.app.router['CommonCallContactCentre:get'].url_for(user_journey=user_journey,
                                                                          display_region=display_region,
                                                                          error='address-not-found'))

        elif address_confirmation == 'no':
            raise HTTPFound(
                request.app.router['CommonEnterAddress:get'].url_for(display_region=display_region,
                                                                     user_journey=user_journey,
                                                                     sub_user_journey=sub_user_journey))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            attributes['page_title'] = page_title
            attributes['display_region'] = display_region
            attributes['user_journey'] = user_journey
            attributes['sub_user_journey'] = sub_user_journey
            attributes['locale'] = locale
            return attributes
