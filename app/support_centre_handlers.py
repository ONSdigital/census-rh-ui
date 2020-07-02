import aiohttp_jinja2

from aiohttp.web import RouteTableDef, HTTPFound
from structlog import get_logger

from .flash import flash
from .utils import View, ProcessPostcode, InvalidDataError, InvalidDataErrorWelsh, FlashMessage

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
            # TODO Add welsh translation
            page_title = 'Find a support centre'
        else:
            locale = 'en'
            page_title = 'Find a support centre'
        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': '/find-a-support-centre/'
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
            postcode = ProcessPostcode.validate_postcode(data['form-enter-postcode'], locale)
            logger.info('valid postcode', client_ip=request['client_ip'])

        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info('invalid postcode', client_ip=request['client_ip'])
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
        domain_url_en = request.app['DOMAIN_URL_PROTOCOL'] + request.app[
            'DOMAIN_URL_EN']
        domain_url_cy = request.app['DOMAIN_URL_PROTOCOL'] + request.app[
            'DOMAIN_URL_CY']

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        try:
            postcode_value = ProcessPostcode.validate_postcode(request.match_info['postcode'], locale)
            logger.info('valid postcode', client_ip=request['client_ip'])

        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info('invalid postcode', client_ip=request['client_ip'])
            attributes = {
                'domain_url_en': domain_url_en,
                'domain_url_cy': domain_url_cy,
                'page_title': 'Error',
                'display_region': display_region,
                'locale': locale,
                'page_url': '/find-a-support-centre/' + postcode_value + '/'
            }
            return aiohttp_jinja2.render_template('404.html', request, attributes, status=404)

        self.log_entry(request, display_region + '/find-a-support-centre/' + postcode_value)

        if display_region == 'cy':
            # TODO Add welsh translation
            page_title = 'Support centres near ' + postcode_value
        else:
            page_title = 'Support centres near ' + postcode_value

        # list_of_centres_content = await AddressIndex.get_postcode_return(request, attributes['postcode'], display_region)
        list_of_centres_content = {}
        list_of_centres_content['page_title'] = page_title
        list_of_centres_content['postcode'] = page_title
        list_of_centres_content['display_region'] = display_region
        list_of_centres_content['locale'] = locale
        list_of_centres_content['page_url'] = '/find-a-support-centre/' + postcode_value + '/'

        return list_of_centres_content

