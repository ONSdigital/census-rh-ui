import aiohttp_jinja2
import re

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from .exceptions import TooManyRequestsWebForm
from structlog import get_logger

from . import (WEBFORM_MISSING_COUNTRY_MSG,
               WEBFORM_MISSING_CATEGORY_MSG,
               WEBFORM_MISSING_DESCRIPTION_MSG,
               WEBFORM_MISSING_NAME_MSG,
               WEBFORM_MISSING_EMAIL_EMPTY_MSG,
               WEBFORM_MISSING_EMAIL_INVALID_MSG,
               WEBFORM_MISSING_COUNTRY_MSG_CY,
               WEBFORM_MISSING_CATEGORY_MSG_CY,
               WEBFORM_MISSING_DESCRIPTION_MSG_CY,
               WEBFORM_MISSING_NAME_MSG_CY,
               WEBFORM_MISSING_EMAIL_EMPTY_MSG_CY,
               WEBFORM_MISSING_EMAIL_INVALID_MSG_CY
               )
from .flash import flash
from .utils import View, RHService

logger = get_logger('respondent-home')
web_form_routes = RouteTableDef()


@web_form_routes.view(r'/' + View.valid_display_regions + '/web-form/')
class WebForm(View):
    @aiohttp_jinja2.template('web-form.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            page_title = 'Gwe-ffurflen'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Web form'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'
        self.log_entry(request, display_region + '/web-form')

        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'privacy_link': View.get_campaign_site_link(request, display_region, 'privacy'),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
        }

    @aiohttp_jinja2.template('web-form.html')
    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/web-form')

        data = await request.post()

        email_validation_pattern = re.compile(
            r'(^[^@\s]+@[^@\s]+\.[^@\s]+$)'
        )

        form_valid = True

        if not (data.get('country')):
            if display_region == 'cy':
                flash(request, WEBFORM_MISSING_COUNTRY_MSG_CY)
            else:
                flash(request, WEBFORM_MISSING_COUNTRY_MSG)
            form_valid = False

        if not (data.get('category')):
            if display_region == 'cy':
                flash(request, WEBFORM_MISSING_CATEGORY_MSG_CY)
            else:
                flash(request, WEBFORM_MISSING_CATEGORY_MSG)
            form_valid = False

        if not data.get('description'):
            if display_region == 'cy':
                flash(request, WEBFORM_MISSING_DESCRIPTION_MSG_CY)
            else:
                flash(request, WEBFORM_MISSING_DESCRIPTION_MSG)
            form_valid = False

        if not data.get('name'):
            if display_region == 'cy':
                flash(request, WEBFORM_MISSING_NAME_MSG_CY)
            else:
                flash(request, WEBFORM_MISSING_NAME_MSG)
            form_valid = False

        if not (data.get('email')):
            if display_region == 'cy':
                flash(request, WEBFORM_MISSING_EMAIL_EMPTY_MSG_CY)
            else:
                flash(request, WEBFORM_MISSING_EMAIL_EMPTY_MSG)
            form_valid = False

        elif not email_validation_pattern.fullmatch(str(data.get('email'))):
            if display_region == 'cy':
                flash(request, WEBFORM_MISSING_EMAIL_INVALID_MSG_CY)
            else:
                flash(request, WEBFORM_MISSING_EMAIL_INVALID_MSG)
            form_valid = False

        if not form_valid:
            logger.info('web form submission error', client_ip=request['client_ip'], region_of_site=display_region)
            raise HTTPFound(
                request.app.router['WebForm:get'].url_for(display_region=display_region))

        else:
            logger.info('call web form endpoint', client_ip=request['client_ip'], region_of_site=display_region)
            if display_region == 'cy':
                language = 'CY'
            else:
                language = 'EN'
            form_data = {
                'category': data.get('category'),
                'region': data.get('country'),
                'language': language,
                'name': data.get('name'),
                'description': data.get('description'),
                'email': data.get('email')
            }

            try:
                await RHService.post_webform(request, form_data)
            except ClientResponseError as ex:
                if ex.status == 429:
                    raise TooManyRequestsWebForm()
                else:
                    raise ex

            raise HTTPFound(
                request.app.router['WebFormSuccess:get'].url_for(display_region=display_region))


@web_form_routes.view(r'/' + View.valid_display_regions + '/web-form/success/')
class WebFormSuccess(View):
    @aiohttp_jinja2.template('web-form-success.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        if display_region == 'cy':
            page_title = "Diolch am gysylltu â ni"
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
