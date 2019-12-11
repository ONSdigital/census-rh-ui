import aiohttp_jinja2

from aiohttp.client_exceptions import (ClientError)

from aiohttp.web import RouteTableDef

from datetime import datetime
from structlog import get_logger

from . import (WEBCHAT_MISSING_NAME_MSG,
               WEBCHAT_MISSING_COUNTRY_MSG,
               WEBCHAT_MISSING_QUERY_MSG,
               WEBCHAT_MISSING_NAME_MSG_CY,
               WEBCHAT_MISSING_COUNTRY_MSG_CY,
               WEBCHAT_MISSING_QUERY_MSG_CY)
from .flash import flash
from .utils import View

logger = get_logger('respondent-home')
webchat_routes = RouteTableDef()


class WebChat(View):
    @staticmethod
    def get_now():
        return datetime.utcnow()

    @staticmethod
    def check_open():

        year = WebChat.get_now().year
        month = WebChat.get_now().month
        day = WebChat.get_now().day
        weekday = WebChat.get_now().weekday()
        hour = WebChat.get_now().hour

        census_weekend_open = 8
        census_weekend_close = 16
        saturday_open = 8
        saturday_close = 13
        weekday_open = 8
        weekday_close = 19

        timezone_offset = 0

        if WebChat.get_now() < datetime(2019, 10, 27):
            logger.info('before switch to gmt - adjusting time', client_ip='')
            timezone_offset = 1

        if year == 2019 and month == 10 and (day == 12 or day == 13):
            if hour < (census_weekend_open - timezone_offset) or hour >= (
                    census_weekend_close - timezone_offset):
                return False
        elif weekday == 5:  # Saturday
            if hour < (saturday_open - timezone_offset) or hour >= (
                    saturday_close - timezone_offset):
                return False
        elif weekday == 6:  # Sunday
            return False
        else:
            if hour < (weekday_open - timezone_offset) or hour >= (
                    weekday_close - timezone_offset):
                return False

        return True

    @staticmethod
    def validate_form(request, data, display_region):

        form_valid = True

        if not data.get('screen_name'):
            if display_region == 'cy':
                flash(request, WEBCHAT_MISSING_NAME_MSG_CY)
            else:
                flash(request, WEBCHAT_MISSING_NAME_MSG)
            form_valid = False

        if not (data.get('country')):
            if display_region == 'cy':
                flash(request, WEBCHAT_MISSING_COUNTRY_MSG_CY)
            else:
                flash(request, WEBCHAT_MISSING_COUNTRY_MSG)
            form_valid = False

        if not (data.get('query')):
            if display_region == 'cy':
                flash(request, WEBCHAT_MISSING_QUERY_MSG_CY)
            else:
                flash(request, WEBCHAT_MISSING_QUERY_MSG)
            form_valid = False

        return form_valid

    async def get_webchat_closed(self, request):
        querystring = '?im_name=OOH&im_subject=ONS&im_countchars=1&info_email=EMAIL&info_country=COUNTRY&info_query=QUERY&info_language=LANGUAGEID'
        return await self._make_request(
            request, 'GET', request.app['WEBCHAT_SVC_URL'] + querystring,
            self._handle_response)


@webchat_routes.view('/webchat/chat')
class WebChatWindowEN(WebChat):
    @aiohttp_jinja2.template('webchat-window.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'webchat/chat')
        return {
            'display_region': 'en',
            'page_title': 'Web Chat'
        }


@webchat_routes.view('/gwe-sgwrs/chat')
class WebChatWindowCY(WebChat):
    @aiohttp_jinja2.template('webchat-window.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'webchat/chat')
        return {
            'display_region': 'cy',
            'locale': 'cy',
            'page_title': 'Gwe-sgwrs'
        }


@webchat_routes.view('/ni/webchat/chat')
class WebChatWindowNI(WebChat):
    @aiohttp_jinja2.template('webchat-window.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'webchat/chat')
        return {
            'display_region': 'ni',
            'page_title': 'Web Chat'
        }


@webchat_routes.view('/webchat')
class WebChatEN(WebChat):
    @aiohttp_jinja2.template('webchat-form.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'webchat')
        logger.info('date/time check', client_ip=request['client_ip'])
        if WebChat.check_open():
            return {
                'display_region': 'en',
                'page_title': 'Web Chat'
            }
        else:
            try:
                await self.get_webchat_closed(request)
            except ClientError:
                logger.error('failed to send webchat closed',
                             client_ip=request['client_ip'])

            logger.info('webchat closed', client_ip=request['client_ip'])
            return {
                'webchat_status': 'closed',
                'display_region': 'en',
                'page_title': 'Web Chat'
            }

    @aiohttp_jinja2.template('webchat-form.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'webchat')
        data = await request.post()

        form_valid = self.validate_form(request, data, 'en')

        if not form_valid:
            logger.info('form submission error',
                        client_ip=request['client_ip'])
            return {
                'form_value_screen_name': data.get('screen_name'),
                'form_value_country': data.get('country'),
                'form_value_query': data.get('query'),
                'display_region': 'en',
                'page_title': 'Web Chat'
            }

        context = {
            'screen_name': data.get('screen_name'),
            'language': 'en',
            'country': data.get('country'),
            'query': data.get('query'),
            'display_region': 'en',
            'page_title': 'Web Chat',
            'webchat_url': request.app['WEBCHAT_SVC_URL']
        }

        logger.info('date/time check', client_ip=request['client_ip'])
        if WebChat.check_open():
            return aiohttp_jinja2.render_template('webchat-window.html',
                                                  request, context)
        else:
            try:
                await self.get_webchat_closed(request)
            except ClientError:
                logger.error('failed to send webchat closed',
                             client_ip=request['client_ip'])

            logger.info('webchat closed', client_ip=request['client_ip'])
            return {
                'webchat_status': 'closed',
                'display_region': 'en',
                'page_title': 'Web Chat'
            }


@webchat_routes.view('/gwe-sgwrs')
class WebChatCY(WebChat):
    @aiohttp_jinja2.template('webchat-form.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'webchat')
        logger.info('date/time check', client_ip=request['client_ip'])
        if WebChat.check_open():
            return {
                'display_region': 'cy',
                'locale': 'cy',
                'page_title': 'Gwe-sgwrs'
            }
        else:
            try:
                await self.get_webchat_closed(request)
            except ClientError:
                logger.error('failed to send webchat closed',
                             client_ip=request['client_ip'])

            logger.info('webchat closed', client_ip=request['client_ip'])
            return {
                'webchat_status': 'closed',
                'display_region': 'cy',
                'locale': 'cy',
                'page_title': 'Gwe-sgwrs'
            }

    @aiohttp_jinja2.template('webchat-form.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'webchat')
        data = await request.post()

        form_valid = self.validate_form(request, data, 'cy')

        if not form_valid:
            logger.info('form submission error',
                        client_ip=request['client_ip'])
            return {
                'form_value_screen_name': data.get('screen_name'),
                'form_value_country': data.get('country'),
                'form_value_query': data.get('query'),
                'display_region': 'cy',
                'locale': 'cy',
                'page_title': 'Gwe-sgwrs'
            }

        context = {
            'screen_name': data.get('screen_name'),
            'language': 'cy',
            'country': data.get('country'),
            'query': data.get('query'),
            'display_region': 'cy',
            'locale': 'cy',
            'page_title': 'Gwe-sgwrs',
            'webchat_url': request.app['WEBCHAT_SVC_URL']
        }

        logger.info('date/time check', client_ip=request['client_ip'])
        if WebChat.check_open():
            return aiohttp_jinja2.render_template('webchat-window.html',
                                                  request, context)
        else:
            try:
                await self.get_webchat_closed(request)
            except ClientError:
                logger.error('failed to send webchat closed',
                             client_ip=request['client_ip'])

            logger.info('webchat closed', client_ip=request['client_ip'])
            return {
                'webchat_status': 'closed',
                'display_region': 'cy',
                'locale': 'cy',
                'page_title': 'Gwe-sgwrs'
            }


@webchat_routes.view('/ni/webchat')
class WebChatNI(WebChat):
    @aiohttp_jinja2.template('webchat-form.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'webchat')
        logger.info('date/time check', client_ip=request['client_ip'])
        if WebChat.check_open():
            return {
                'display_region': 'ni',
                'page_title': 'Web Chat'
            }
        else:
            try:
                await self.get_webchat_closed(request)
            except ClientError:
                logger.error('failed to send webchat closed',
                             client_ip=request['client_ip'])

            logger.info('webchat closed', client_ip=request['client_ip'])
            return {
                'webchat_status': 'closed',
                'display_region': 'ni',
                'page_title': 'Web Chat'
            }

    @aiohttp_jinja2.template('webchat-form.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'webchat')
        data = await request.post()

        form_valid = self.validate_form(request, data, 'ni')

        if not form_valid:
            logger.info('form submission error',
                        client_ip=request['client_ip'])
            return {
                'form_value_screen_name': data.get('screen_name'),
                'form_value_country': data.get('country'),
                'form_value_query': data.get('query'),
                'display_region': 'ni',
                'page_title': 'Web Chat'
            }

        context = {
            'screen_name': data.get('screen_name'),
            'language': 'en',
            'country': data.get('country'),
            'query': data.get('query'),
            'display_region': 'ni',
            'page_title': 'Web Chat',
            'webchat_url': request.app['WEBCHAT_SVC_URL']
        }

        logger.info('date/time check', client_ip=request['client_ip'])
        if WebChat.check_open():
            return aiohttp_jinja2.render_template('webchat-window.html',
                                                  request, context)
        else:
            try:
                await self.get_webchat_closed(request)
            except ClientError:
                logger.error('failed to send webchat closed',
                             client_ip=request['client_ip'])

            logger.info('webchat closed', client_ip=request['client_ip'])
            return {
                'webchat_status': 'closed',
                'display_region': 'ni',
                'page_title': 'Web Chat'
            }
