import aiohttp_jinja2

from aiohttp.web import RouteTableDef, json_response
from structlog import get_logger

from . import VERSION

from .utils import View

logger = get_logger('respondent-home')
static_routes = RouteTableDef()


@static_routes.view('/info', use_prefix=False)
class Info(View):
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'info')
        info = {
            'name': 'respondent-home-ui',
            'version': VERSION,
        }
        if 'check' in request.query:
            info['ready'] = await request.app.check_services()
        return json_response(info)


@static_routes.view(r'/' + View.valid_display_regions + '/start/accessibility/')
class Accessibility(View):
    @aiohttp_jinja2.template('accessibility.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/accessibility')
        if display_region == 'cy':
            locale = 'cy'
            page_title = 'Datganiad hygyrchedd gwefan y cyfrifiad'
        else:
            locale = 'en'
            page_title = 'Census questionnaire accessibility statement'
        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale
        }
