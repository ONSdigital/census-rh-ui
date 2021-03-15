import aiohttp
from aiohttp.client_exceptions import (ClientConnectionError,
                                       ClientConnectorError,
                                       ClientResponseError)

from tenacity import (retry,
                      stop_after_attempt,
                      retry_if_exception_message,
                      retry_if_exception_type,
                      wait_exponential,
                      RetryError)
from structlog import get_logger

logger = get_logger('respondent-home')

pooled_attempts_limit = 2
basic_attempt_limit = 3
wait_multiplier = 0.01


def after_failed_attempt(request_type, retry_state):
    logger.warn(request_type + ' request attempt failed', attempts=retry_state.attempt_number)


def after_failed_basic(retry_state):
    after_failed_attempt('basic', retry_state)


def after_failed_pooled(retry_state):
    after_failed_attempt('pooled', retry_state)


class RetryRequest:
    """
    Make requests to a URL, but retry under certain conditions to tolerate server graceful shutdown.
    """
    def __init__(self, request, method, url, auth, request_headers, request_json, return_json):
        self.request = request
        self.method = method
        self.url = url
        self.auth = auth
        self.headers = request_headers
        self.json = request_json
        self.return_json = return_json

    def __handle_response(self, response):
        try:
            response.raise_for_status()
        except ClientResponseError as ex:
            raise ex
        else:
            logger.debug('successfully connected to service',
                         client_ip=self.request['client_ip'],
                         client_id=self.request['client_id'],
                         trace=self.request['trace'],
                         url=self.url)

    @retry(reraise=True, stop=stop_after_attempt(basic_attempt_limit),
           wait=wait_exponential(multiplier=wait_multiplier, exp_base=25),
           after=after_failed_basic,
           retry=(retry_if_exception_message(match='503.*') | retry_if_exception_type((ClientConnectionError,
                                                                                       ClientConnectorError))))
    async def _request_basic(self):
        # basic request without keep-alive to avoid terminating service.
        logger.info('request using basic connection',
                    client_ip=self.request['client_ip'],
                    client_id=self.request['client_id'],
                    trace=self.request['trace'])

        async with aiohttp.request(
                self.method, self.url, auth=self.auth, json=self.json, headers=self.headers) as resp:
            self.__handle_response(resp)
            if self.return_json:
                return await resp.json()
            else:
                return None

    @retry(stop=stop_after_attempt(pooled_attempts_limit),
           wait=wait_exponential(multiplier=wait_multiplier),
           after=after_failed_pooled,
           retry=(retry_if_exception_message(match='503.*') | retry_if_exception_type((ClientConnectionError,
                                                                                       ClientConnectorError))))
    async def _request_using_pool(self):
        async with self.request.app.http_session_pool.request(
                self.method, self.url, auth=self.auth, json=self.json, headers=self.headers, ssl=False) as resp:
            self.__handle_response(resp)
            if self.return_json:
                return await resp.json()
            else:
                return None

    async def make_request(self):
        """
        Make a request with retries.
        First the fast pooled connection will be tried, but if certain failures are detected, then it will be retried.
        If the retry limit is reached then a basic connection will be tried (and retried if necessary)
        Finally the error will be propagated.
        """
        logger.debug('making request with handler',
                     client_ip=self.request['client_ip'],
                     client_id=self.request['client_id'],
                     trace=self.request['trace'],
                     method=self.method,
                     url=self.url)
        try:
            try:
                return await self._request_using_pool()
            except RetryError as retry_ex:
                attempts = retry_ex.last_attempt.attempt_number
                logger.warn('Could not make request using normal pooled connection',
                            client_ip=self.request['client_ip'],
                            client_id=self.request['client_id'],
                            trace=self.request['trace'],
                            attempts=attempts)
                return await self._request_basic()
        except ClientResponseError as ex:
            if ex.status not in [400, 404, 429]:
                logger.error('error in response',
                             client_ip=self.request['client_ip'],
                             client_id=self.request['client_id'],
                             trace=self.request['trace'],
                             url=self.url,
                             status_code=ex.status)
            elif ex.status == 429:
                logger.warn('too many requests',
                            client_ip=self.request['client_ip'],
                            client_id=self.request['client_id'],
                            trace=self.request['trace'],
                            url=self.url,
                            status_code=ex.status)
            elif ex.status == 400:
                logger.warn('bad request',
                            client_ip=self.request['client_ip'],
                            client_id=self.request['client_id'],
                            trace=self.request['trace'],
                            url=self.url,
                            status_code=ex.status)
            raise ex
        except (ClientConnectionError, ClientConnectorError) as ex:
            logger.error('client failed to connect',
                         client_ip=self.request['client_ip'],
                         client_id=self.request['client_id'],
                         trace=self.request['trace'],
                         url=self.url)
            raise ex
