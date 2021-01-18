import aiohttp_jinja2

from aiohttp.web import RouteTableDef, json_response, HTTPFound
from structlog import get_logger

from . import VERSION
from .security import forget
from .utils import View

logger = get_logger('respondent-home')
static_routes = RouteTableDef()


@static_routes.view('/info', use_prefix=False)
class Info(View):
    async def get(self, request):
        self.setup_request(request)
        info = {
            'name': 'respondent-home-ui',
            'version': VERSION,
        }
        if 'check' in request.query:
            info['ready'] = await request.app.check_services()
        return json_response(info)


@static_routes.view(r'/' + View.valid_display_regions + '/start/launch-eq/')
class LaunchEQ(View):
    @aiohttp_jinja2.template('start-launch-eq.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/launch-eq')
        if display_region == 'cy':
            locale = 'cy'
            page_title = 'Launch EQ'
        else:
            locale = 'en'
            page_title = 'Launch EQ'
        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'token': request.query['token'],
            'page_url': View.gen_page_url(request)
        }

    @aiohttp_jinja2.template('start-launch-eq.html')
    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/launch-eq')

        data = await request.post()

        token = data.get('token')

        logger.info('redirecting to eq', client_ip=request['client_ip'], region_of_site=display_region)
        eq_url = request.app['EQ_URL']
        raise HTTPFound(f'{eq_url}/session?token={token}')


@static_routes.view(r'/' + View.valid_display_regions + '/signed-out/')
class SignedOut(View):
    @aiohttp_jinja2.template('signed-out.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/signed-out')
        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Progress saved'
            locale = 'cy'
        else:
            page_title = 'Progress saved'
            locale = 'en'
        await forget(request)
        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }
