import aiohttp_jinja2
import json

from aiohttp.web import HTTPFound, RouteTableDef
from structlog import get_logger
from aiohttp_session import get_session

from . import (BAD_CODE_MSG, INVALID_CODE_MSG, ADDRESS_CHECK_MSG,
               ADDRESS_EDIT_MSG, SESSION_TIMEOUT_MSG,
               START_LANGUAGE_OPTION_MSG,
               ADDRESS_SELECT_CHECK_MSG,
               BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY, ADDRESS_CHECK_MSG_CY,
               ADDRESS_EDIT_MSG_CY, SESSION_TIMEOUT_MSG_CY,
               ADDRESS_SELECT_CHECK_MSG_CY)

from .flash import flash
from .security import check_permission
from .utils import View, ProcessPostcode, InvalidDataError, InvalidDataErrorWelsh, FlashMessage, AddressIndex, RHService

logger = get_logger('respondent-home')
common_routes = RouteTableDef()


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
        try:
            attributes = session['attributes']

        except KeyError:
            raise HTTPFound(
                request.app.router['CommonTimeout:get'].url_for(
                    display_region=display_region, user_journey=user_journey, sub_user_journey=sub_user_journey))

        return attributes


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


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys + '/address-in-scotland/')
class CommonAddressInScotland(CommonCommon):
    @aiohttp_jinja2.template('common-address-in-scotland.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']

        if display_region == 'cy':
            page_title = 'Your address is in Scotland'
            locale = 'cy'
        else:
            page_title = 'Your address is in Scotland'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/address-in-scotland')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'user_journey': user_journey
        }


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

            if user_journey == 'start':
                raise HTTPFound(
                    request.app.router['StartUnlinkedConfirmAddress:get'].url_for(
                        display_region=display_region,
                        user_journey=user_journey,
                        sub_user_journey=sub_user_journey
                    ))
            elif user_journey == 'requests':
                request_type = sub_user_journey.split('-', 1)[0]
                raise HTTPFound(
                    request.app.router['RequestCodeConfirmAddress:get'].url_for(
                        request_type=request_type, display_region=display_region))
