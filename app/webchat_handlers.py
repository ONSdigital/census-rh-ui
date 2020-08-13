import aiohttp_jinja2

from aiohttp.web import RouteTableDef

from datetime import datetime
from structlog import get_logger
from pytz import timezone, utc

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

saturday_open = 8
saturday_close = 13
weekday_open = 8
weekday_close = 19
uk_zone = timezone('Europe/London')


class WebChat(View):
    @staticmethod
    def get_now_utc():
        return datetime.utcnow()

    @staticmethod
    def check_open():
        wall_clock = utc.localize(WebChat.get_now_utc()).astimezone(uk_zone)
        weekday = wall_clock.weekday()
        hour = wall_clock.hour

        if weekday == 5:  # Saturday
            return saturday_open <= hour < saturday_close
        elif weekday == 6:  # Sunday
            return False
        else:
            return weekday_open <= hour < weekday_close

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


@webchat_routes.view(r'/' + View.valid_display_regions + '/web-chat/chat/')
class WebChatWindow(WebChat):
    @aiohttp_jinja2.template('webchat-window.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            page_title = 'Gwe-sgwrs'
            locale = 'cy'
        else:
            page_title = 'Web Chat'
            locale = 'en'
        self.log_entry(request, display_region + '/web-chat/chat')
        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }


@webchat_routes.view(r'/' + View.valid_display_regions + '/web-chat/')
class WebChat(WebChat):
    @aiohttp_jinja2.template('webchat-form.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            page_title = 'Gwe-sgwrs'
            locale = 'cy'
        else:
            page_title = 'Web Chat'
            locale = 'en'
        self.log_entry(request, display_region + '/web-chat')

        logger.info('date/time check', client_ip=request['client_ip'])
        if WebChat.check_open():
            return {
                'display_region': display_region,
                'page_title': page_title,
                'locale': locale,
                'page_url': View.gen_page_url(request)
            }
        else:
            logger.info('webchat closed', client_ip=request['client_ip'])
            return {
                'webchat_status': 'closed',
                'display_region': display_region,
                'page_title': page_title,
                'locale': locale,
                'page_url': View.gen_page_url(request)
            }

    @aiohttp_jinja2.template('webchat-form.html')
    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            page_title = 'Gwe-sgwrs'
            locale = 'cy'
        else:
            page_title = 'Web Chat'
            locale = 'en'
        self.log_entry(request, display_region + '/web-chat')

        data = await request.post()

        form_valid = self.validate_form(request, data, display_region)

        if not form_valid:
            logger.info('form submission error',
                        client_ip=request['client_ip'])
            return {
                'form_value_screen_name': data.get('screen_name'),
                'form_value_country': data.get('country'),
                'form_value_query': data.get('query'),
                'display_region': display_region,
                'page_title': page_title,
                'locale': locale,
                'page_url': View.gen_page_url(request)
            }

        context = {
            'screen_name': data.get('screen_name'),
            'display_language': 'en',
            'country': data.get('country'),
            'query': data.get('query'),
            'display_region': display_region,
            'page_title': page_title,
            'webchat_url': request.app['WEBCHAT_SVC_URL'],
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }

        logger.info('date/time check', client_ip=request['client_ip'])
        if WebChat.check_open():
            return aiohttp_jinja2.render_template('webchat-window.html',
                                                  request, context)
        else:
            logger.info('webchat closed', client_ip=request['client_ip'])
            return {
                'webchat_status': 'closed',
                'display_region': display_region,
                'page_title': page_title,
                'locale': locale,
                'page_url': View.gen_page_url(request)
            }
