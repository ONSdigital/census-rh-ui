import aiohttp_jinja2

from aiohttp.client_exceptions import (ClientConnectionError,
                                       ClientConnectorError,
                                       ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef, json_response
from sdc.crypto.encrypter import encrypt
from structlog import get_logger

from . import VERSION

from .eq import EqPayloadConstructor

logger = get_logger('respondent-home')
routes = RouteTableDef()


class View:
    """
    Common base class for views
    """
    def setup_request(self, request):
        request['client_ip'] = request.headers.get('X-Forwarded-For', None)

    @staticmethod
    def _handle_response(response):
        try:
            response.raise_for_status()
        except ClientResponseError as ex:
            if not ex.status == 404:
                logger.error('error in response',
                             url=response.url,
                             status_code=response.status)
            raise ex
        else:
            logger.debug('successfully connected to service',
                         url=str(response.url))

    async def _make_request(self,
                            request,
                            method,
                            url,
                            func,
                            auth=None,
                            json=None,
                            return_json=False):
        """
        :param request: The AIOHTTP user request, used for logging and app access
        :param method: The HTTP verb
        :param url: The target URL
        :param auth: Authorization
        :param json: JSON payload to pass as request data
        :param func: Function to call on the response
        :param return_json: If True, the response JSON will be returned
        """
        logger.debug('making request with handler',
                     method=method,
                     url=url,
                     handler=func.__name__)
        try:
            async with request.app.http_session_pool.request(
                    method, url, auth=auth, json=json, ssl=False) as resp:
                func(resp)
                if return_json:
                    return await resp.json()
                else:
                    return None
        except (ClientConnectionError, ClientConnectorError) as ex:
            logger.error('client failed to connect',
                         url=url,
                         client_ip=request['client_ip'])
            raise ex

    async def call_questionnaire(self, request, case, attributes, app,
                                 adlocation):
        eq_payload = await EqPayloadConstructor(case, attributes, app,
                                                adlocation).build()

        token = encrypt(eq_payload,
                        key_store=app['key_store'],
                        key_purpose='authentication')

        await self.post_surveylaunched(request, case, adlocation)

        logger.info('redirecting to eq', client_ip=request['client_ip'])
        eq_url = app['EQ_URL']
        raise HTTPFound(f'{eq_url}/session?token={token}')

    async def post_surveylaunched(self, request, case, adlocation):
        if not adlocation:
            adlocation = ''
        launch_json = {
            'questionnaireId': case['questionnaireId'],
            'caseId': case['caseId'],
            'agentId': adlocation
        }
        rhsvc_url = request.app['RHSVC_URL']
        return await self._make_request(request,
                                        'POST',
                                        f'{rhsvc_url}/surveyLaunched',
                                        self._handle_response,
                                        auth=request.app['RHSVC_AUTH'],
                                        json=launch_json)

    def log_entry(self, request, endpoint):
        method = request.method
        logger.info(f"received {method} on endpoint '{endpoint}'",
                    method=request.method,
                    path=request.path)


@routes.view('/info', use_prefix=False)
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


@routes.view('/start/accessibility/')
class AccessibilityEN(View):
    @aiohttp_jinja2.template('accessibility.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/accessibility')
        return {
            'display_region': 'en',
            'page_title': 'Census questionnaire accessibility statement'
        }


@routes.view('/dechrau/hygyrchedd/')
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


@routes.view('/ni/start/accessibility/')
class AccessibilityNI(View):
    @aiohttp_jinja2.template('accessibility.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/accessibility')
        return {
            'display_region': 'ni',
            'page_title': 'Census questionnaire accessibility statement'
        }
