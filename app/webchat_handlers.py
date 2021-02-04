import aiohttp_jinja2

from aiohttp.web import HTTPFound, RouteTableDef

from datetime import datetime, date
from structlog import get_logger
from pytz import timezone, utc

from .flash import flash
from .utils import View

logger = get_logger('respondent-home')
webchat_routes = RouteTableDef()

bank_holidays = [
    date(2021, 4, 2),
    date(2021, 4, 5),
    date(2021, 5, 3),
    date(2021, 5, 31)
]

census_saturday = date(2021, 3, 20)
census_sunday = date(2021, 3, 21)

census_saturday_open = 8
census_saturday_close = 20

census_sunday_open = 8
census_sunday_close = 20

saturday_open = 8
saturday_close = 13

weekday_open = 8
weekday_close = 20

uk_zone = timezone('Europe/London')


class WebChat(View):
    @staticmethod
    def get_now_utc():
        return datetime.utcnow()

    @staticmethod
    def todays_opening_hours() -> (int, int, int):
        wall_clock = utc.localize(WebChat.get_now_utc()).astimezone(uk_zone)
        now_date = wall_clock.date()
        weekday = wall_clock.weekday()
        hour = wall_clock.hour

        if now_date == census_saturday:
            return census_saturday_open, census_saturday_close, hour
        elif now_date == census_sunday:
            return census_sunday_open, census_sunday_close, hour
        elif weekday == 5:  # Saturday
            return saturday_open, saturday_close, hour
        elif weekday == 6 or now_date in bank_holidays:  # Sunday or bank holiday
            return None, None, None
        else:
            return weekday_open, weekday_close, hour

    @staticmethod
    def check_open() -> bool:
        opening, closing, hour = WebChat.todays_opening_hours()
        if opening is None:
            return False

        return opening <= hour < closing

    @staticmethod
    def validate_form(request, data, display_region):

        form_valid = True

        if not data.get('screen_name'):
            if display_region == 'cy':
                flash(request, {'text': 'Nodwch eich enw', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE',
                                'field': 'error_screen_name', 'screen_name': data.get('screen_name'),
                                'country': data.get('country'), 'query': data.get('query')})
            else:
                flash(request, {'text': 'Enter your name', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE',
                                'field': 'error_screen_name', 'screen_name': data.get('screen_name'),
                                'country': data.get('country'), 'query': data.get('query')})
            form_valid = False

        if not (data.get('country')):
            if display_region == 'cy':
                flash(request, {'text': 'Dewiswch eich gwlad', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE',
                                'field': 'error_country', 'screen_name': data.get('screen_name'),
                                'country': data.get('country'), 'query': data.get('query')})
            else:
                flash(request, {'text': 'Select your country', 'clickable': True, 'level': 'ERROR', 'type': 'BAD_CODE',
                                'field': 'error_country', 'screen_name': data.get('screen_name'),
                                'country': data.get('country'), 'query': data.get('query')})
            form_valid = False

        if not (data.get('query')):
            if display_region == 'cy':
                flash(request, {'text': 'Pa fath o ymholiad sydd gennych chi?', 'clickable': True, 'level': 'ERROR',
                                'type': 'BAD_CODE', 'field': 'error_query', 'screen_name': data.get('screen_name'),
                                'country': data.get('country'), 'query': data.get('query')})
            else:
                flash(request, {'text': 'What type of query do you have?', 'clickable': True, 'level': 'ERROR',
                                'type': 'BAD_CODE', 'field': 'error_query', 'screen_name': data.get('screen_name'),
                                'country': data.get('country'), 'query': data.get('query')})
            form_valid = False

        return form_valid


@webchat_routes.view(r'/' + View.valid_display_regions + '/web-chat/')
class WebChat(WebChat):
    @aiohttp_jinja2.template('webchat-form.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            page_title = 'Gwe-sgwrs'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Web chat'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'
        self.log_entry(request, display_region + '/web-chat')
        if WebChat.check_open():
            return {
                'display_region': display_region,
                'page_title': page_title,
                'locale': locale,
                'page_url': View.gen_page_url(request),
                'privacy_link': View.get_campaign_site_link(request, display_region, 'privacy')
            }
        else:
            logger.info('webchat closed', client_ip=request['client_ip'], region_of_site=display_region)
            return {
                'webchat_status': 'closed',
                'display_region': display_region,
                'page_title': page_title,
                'locale': locale,
                'page_url': View.gen_page_url(request),
                'census_saturday_open': census_saturday_open,
                'census_saturday_close':  census_saturday_close,
                'census_sunday_open': census_sunday_open,
                'census_sunday_close': census_sunday_close,
                'saturday_open': saturday_open,
                'saturday_close': saturday_close,
                'weekday_open': weekday_open,
                'weekday_close': weekday_close
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
                        client_ip=request['client_ip'],
                        region_of_site=display_region)
            raise HTTPFound(
                request.app.router['WebChat:get'].url_for(display_region=display_region))

        context = {
            'screen_name': data.get('screen_name'),
            'display_language': locale,
            'country': data.get('country'),
            'query': data.get('query'),
            'display_region': display_region,
            'page_title': page_title,
            'webchat_url': request.app['WEBCHAT_SVC_URL'],
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }

        logger.info('date/time check', client_ip=request['client_ip'], region_of_site=display_region)
        if WebChat.check_open():
            return aiohttp_jinja2.render_template('webchat-window.html',
                                                  request, context)
        else:
            logger.info('webchat closed', client_ip=request['client_ip'], region_of_site=display_region)
            return {
                'webchat_status': 'closed',
                'display_region': display_region,
                'page_title': page_title,
                'locale': locale,
                'page_url': View.gen_page_url(request),
                'census_saturday_open': census_saturday_open,
                'census_saturday_close': census_saturday_close,
                'census_sunday_open': census_sunday_open,
                'census_sunday_close': census_sunday_close,
                'saturday_open': saturday_open,
                'saturday_close': saturday_close,
                'weekday_open': weekday_open,
                'weekday_close': weekday_close
            }
