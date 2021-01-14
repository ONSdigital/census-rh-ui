import aiohttp_jinja2

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import RouteTableDef, HTTPFound
from structlog import get_logger

from .flash import flash
from .utils import View, ProcessPostcode, InvalidDataError, InvalidDataErrorWelsh, FlashMessage, ADLookUp

logger = get_logger('respondent-home')
support_centre_routes = RouteTableDef()


@support_centre_routes.view(r'/' + View.valid_ew_display_regions + '/find-a-support-centre/')
class SupportCentreEnterPostcode(View):
    @aiohttp_jinja2.template('support_centre_enter_postcode.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/find-a-support-centre')

        if display_region == 'cy':
            locale = 'cy'
            page_title = 'Chwilio am ganolfan gymorth'
        else:
            locale = 'en'
            page_title = 'Find a support centre'
        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }

    @aiohttp_jinja2.template('support_centre_enter_postcode.html')
    async def post(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        self.log_entry(request, display_region + '/find-a-support-centre')

        data = await request.post()

        try:
            postcode = ProcessPostcode.validate_postcode(data['form-enter-address-postcode'], locale)
            logger.info('valid postcode', client_ip=request['client_ip'], valid_postcode=postcode, region_of_site=display_region)

        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info('invalid postcode', client_ip=request['client_ip'], region_of_site=display_region)
            flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'POSTCODE_ENTER_ERROR', 'postcode')
            flash(request, flash_message)
            raise HTTPFound(
                request.app.router['SupportCentreEnterPostcode:get'].url_for(
                    display_region=display_region,
                ))

        raise HTTPFound(
            request.app.router['SupportCentreListCentres:get'].url_for(
                display_region=display_region,
                postcode=postcode
            ))


@support_centre_routes.view(r'/' + View.valid_ew_display_regions + '/find-a-support-centre/{postcode}/')
class SupportCentreListCentres(View):
    @aiohttp_jinja2.template('support_centre_list_of_centres.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        try:
            postcode_value = ProcessPostcode.validate_postcode(request.match_info['postcode'], locale)
            logger.info('valid postcode', client_ip=request['client_ip'], valid_postcode=postcode_value, region_of_site=display_region)

        except (InvalidDataError, InvalidDataErrorWelsh):
            logger.info('invalid postcode', client_ip=request['client_ip'], region_of_site=display_region)
            attributes = {
                'page_title': 'Error',
                'display_region': display_region,
                'locale': locale,
                'page_url': View.gen_page_url(request)
            }
            return aiohttp_jinja2.render_template('404.html', request, attributes, status=404)

        self.log_entry(request, display_region + '/find-a-support-centre/' + postcode_value)

        if display_region == 'cy':
            page_title = 'Canolfannau cymorth gerllaw ' + postcode_value
        else:
            page_title = 'Support centres near ' + postcode_value

        try:
            ad_response = await ADLookUp.get_ad_lookup_by_postcode(request, postcode_value)
        except ClientResponseError as ex:
            attributes = {
                'page_title': 'Error',
                'display_region': display_region,
                'locale': locale,
                'page_url': View.gen_page_url(request)
            }
            if ex.status == 404:
                logger.warn('AD Lookup API returned as postcode not existing', client_ip=request['client_ip'])
                return aiohttp_jinja2.render_template('404.html', request, attributes, status=404)
            else:
                logger.error('AD Lookup API not responding', client_ip=request['client_ip'])
                return aiohttp_jinja2.render_template('error.html', request, attributes, status=500)

        list_of_centres_content = {
            'ad_response': ad_response,
            'page_title': page_title,
            'postcode': postcode_value,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }

        return list_of_centres_content
