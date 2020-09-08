import aiohttp_jinja2
import re

from aiohttp.web import HTTPFound, RouteTableDef

from structlog import get_logger

from . import (WEBCHAT_MISSING_COUNTRY_MSG,
               WEBCHAT_MISSING_QUERY_MSG,
               WEBCHAT_MISSING_COUNTRY_MSG_CY,
               WEBCHAT_MISSING_QUERY_MSG_CY)
from .flash import flash
from .utils import View, FlashMessage

logger = get_logger('respondent-home')
web_form_routes = RouteTableDef()


class WebForm(View):
    email_validation_pattern = re.compile(
        r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    )

    @staticmethod
    def validate_form(request, data, display_region):

        form_valid = True

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

        if not data.get('name'):
            if display_region == 'cy':
                flash(request, FlashMessage.generate_flash_message('Nodwch eich enw',
                                                                   'ERROR', 'NAME_ENTER_ERROR', 'name'))
            else:
                flash(request, FlashMessage.generate_flash_message('Enter your name',
                                                                   'ERROR', 'NAME_ENTER_ERROR', 'name'))
            form_valid = False

        if not (data.get('email')):
            if display_region == 'cy':
                # TODO Add Welsh Translation
                flash(request, FlashMessage.generate_flash_message('No email provided',
                                                                   'ERROR', 'EMAIL_VALUE_ERROR', 'email'))
            else:
                flash(request, FlashMessage.generate_flash_message('No email provided',
                                                                   'ERROR', 'EMAIL_VALUE_ERROR', 'email'))
            form_valid = False

        elif not WebForm.email_validation_pattern.fullmatch(data.get('email')):
            if display_region == 'cy':
                # TODO: Add Welsh Translation
                flash(request, FlashMessage.generate_flash_message('Email address invalid',
                                                                   'ERROR', 'EMAIL_VALUE_ERROR', 'email'))
            else:
                flash(request, FlashMessage.generate_flash_message('Email address invalid',
                                                                   'ERROR', 'EMAIL_VALUE_ERROR', 'email'))

            form_valid = False

        return form_valid


@web_form_routes.view(r'/' + View.valid_display_regions + '/web-form/')
class WebForm(WebForm):
    @aiohttp_jinja2.template('web-form.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Web Form'
            locale = 'cy'
        else:
            page_title = 'Web Form'
            locale = 'en'
        self.log_entry(request, display_region + '/web-form')

        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }

    @aiohttp_jinja2.template('web-form.html')
    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Web Form'
            locale = 'cy'
        else:
            page_title = 'Web Form'
            locale = 'en'
        self.log_entry(request, display_region + '/web-form')

        data = await request.post()

        form_valid = self.validate_form(request, data, display_region)

        if not form_valid:
            logger.info('web form submission error', client_ip=request['client_ip'])
            return {
                'form_value_name': data.get('name'),
                'form_value_country': data.get('country'),
                'form_value_query': data.get('query'),
                'form_value_email': data.get('email'),
                'display_region': display_region,
                'page_title': page_title,
                'locale': locale,
                'page_url': View.gen_page_url(request)
            }

        else:
            logger.info('call web form endpoint', client_ip=request['client_ip'])
            # TODO Call new endpoint for form with data

            raise HTTPFound(
                request.app.router['WebFormSuccess:get'].url_for(display_region=display_region))


@web_form_routes.view(r'/' + View.valid_display_regions + '/web-form/success/')
class WebFormSuccess(WebForm):
    @aiohttp_jinja2.template('web-form-success.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            # TODO Add Welsh Translation
            page_title = 'Thank you for contacting us'
            locale = 'cy'
        else:
            page_title = 'Thank you for contacting us'
            locale = 'en'
        self.log_entry(request, display_region + '/web-form/success')
        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }
