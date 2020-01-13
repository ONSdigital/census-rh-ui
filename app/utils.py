
from aiohttp.client_exceptions import (ClientConnectionError,
                                       ClientConnectorError,
                                       ClientResponseError)
from structlog import get_logger
logger = get_logger('respondent-home')


class View:
    valid_display_regions = r'{display_region:\ben|cy|ni\b}'

    @staticmethod
    def setup_request(request):
        request['client_ip'] = request.headers.get('X-Forwarded-For', None)

    @staticmethod
    def log_entry(request, endpoint):
        method = request.method
        logger.info(f"received {method} on endpoint '{endpoint}'",
                    method=request.method,
                    path=request.path)

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

    @staticmethod
    async def _make_request(request,
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
