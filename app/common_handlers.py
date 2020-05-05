import aiohttp_jinja2

from aiohttp.web import HTTPFound, RouteTableDef
from structlog import get_logger
from aiohttp_session import get_session

from .flash import flash
from .security import check_permission
from .utils import View, ProcessPostcode, InvalidDataError, InvalidDataErrorWelsh, FlashMessage, AddressIndex, RHService

logger = get_logger('respondent-home')
common_routes = RouteTableDef()


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys + '/address-in-scotland/')
class CommonAddressInScotland(View):
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
class CommonCallContactCentre(View):
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
class CommonEnterAddress(View):
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

        if user_journey == 'start':
            raise HTTPFound(
                request.app.router['StartUnlinkedSelectAddress:get'].url_for(display_region=display_region))
        elif user_journey == 'requests':
            request_type = sub_user_journey.split('-', 1)[0]
            raise HTTPFound(
                request.app.router['RequestCodeSelectAddress:get'].url_for(
                    request_type=request_type, display_region=display_region))
