import aiohttp_jinja2

from aiohttp.web import RouteTableDef
from structlog import get_logger

from .utils import View

logger = get_logger('respondent-home')
common_routes = RouteTableDef()


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_journeys + '/address-in-scotland/')
class CommonAddressInScotland(View):
    @aiohttp_jinja2.template('common-address-in-scotland.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['journey']

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


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_journeys + '/call-contact-centre/{error}')
class CommonCallContactCentre(View):
    @aiohttp_jinja2.template('common-contact-centre.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        user_journey = request.match_info['journey']
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
