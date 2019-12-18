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


@static_routes.view('/start/accessibility/')
class AccessibilityEN(View):
    @aiohttp_jinja2.template('accessibility.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/accessibility')
        return {
            'display_region': 'en',
            'page_title': 'Census questionnaire accessibility statement'
        }


@static_routes.view('/dechrau/hygyrchedd/')
class AccessibilityCY(View):
    @aiohttp_jinja2.template('accessibility.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/accessibility')
        return {
            'display_region': 'cy',
            'locale': 'cy',
            'page_title': 'Datganiad hygyrchedd gwefan y cyfrifiad'
        }


@static_routes.view('/ni/start/accessibility/')
class AccessibilityNI(View):
    @aiohttp_jinja2.template('accessibility.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/accessibility')
        return {
            'display_region': 'ni',
            'page_title': 'Census questionnaire accessibility statement'
        }
