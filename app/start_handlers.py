import aiohttp_jinja2
import re
import uuid

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from aiohttp_session import get_session
from structlog import get_logger

from . import (BAD_CODE_MSG, INVALID_CODE_MSG, NO_SELECTION_CHECK_MSG,
               START_LANGUAGE_OPTION_MSG,
               BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY, NO_SELECTION_CHECK_MSG_CY)

from .flash import flash
from .exceptions import InvalidEqPayLoad, SessionTimeout
from .security import remember, check_permission, forget, get_sha256_hash

from .utils import View, RHService, FlashMessage

logger = get_logger('respondent-home')
start_routes = RouteTableDef()


class StartCommon(View):
    def setup_request(self, request):
        super().setup_request(request)

    def setup_uac_hash(self, request, uac, lang):
        try:
            request['uac_hash'] = self.uac_hash(uac)
        except TypeError:
            logger.warn('attempt to use a malformed access code',
                        client_ip=request['client_ip'])
            message = {
                'en': INVALID_CODE_MSG,
                'cy': INVALID_CODE_MSG_CY,
                'ni': INVALID_CODE_MSG,
            }[lang]
            flash(request, message)
            raise HTTPFound(request.app.router['Start:get'].url_for(display_region=lang))

    @staticmethod
    def uac_hash(uac, expected_length=16):
        if uac:
            combined = uac.upper().replace(' ', '')
        else:
            combined = ''

        uac_validation_pattern = re.compile(r'^[A-Z0-9]{16}$')

        if (len(combined) < expected_length) or not (uac_validation_pattern.fullmatch(combined)):  # yapf: disable
            raise TypeError

        return get_sha256_hash(combined)


@start_routes.view(r'/' + View.valid_display_regions + '/start/')
class Start(StartCommon):
    @aiohttp_jinja2.template('start.html')
    async def get(self, request):
        """
        RH home page to enter a UAC.
        Checks if URL carries query string assisted digital location and stores to session
        :param request:
        :return:
        """
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start')
        if display_region == 'cy':
            locale = 'cy'
            # TODO Confirm welsh translation
            page_title = "Dechrau'r cyfrifiad"
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
        else:
            locale = 'en'
            page_title = 'Start census'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title

        try:
            adlocation = request.query['adlocation']
            if adlocation.isdigit():
                logger.info('assisted digital query parameter found',
                            adlocation=adlocation,
                            client_ip=request['client_ip'])
                return {
                    'display_region': display_region,
                    'page_title': page_title,
                    'adlocation': request.query['adlocation'],
                    'locale': locale,
                    'page_url': View.gen_page_url(request)
                }
            else:
                logger.warn('assisted digital query parameter not numeric - ignoring',
                            adlocation=adlocation,
                            client_ip=request['client_ip'])
                return {
                    'display_region': display_region,
                    'page_title': page_title,
                    'locale': locale,
                    'page_url': View.gen_page_url(request)
                }
        except KeyError:
            logger.info('no adlocation present')
            return {
                'display_region': display_region,
                'page_title': page_title,
                'locale': locale,
                'page_url': View.gen_page_url(request)
            }

    async def post(self, request):
        """
        Forward to Address confirmation
        :param request:
        :return: address confirmation view
        """
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start')

        data = await request.post()

        if data.get('uac') == '':
            logger.info('access code not supplied', client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, BAD_CODE_MSG_CY)
            else:
                flash(request, BAD_CODE_MSG)
            raise HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))

        elif data.get('uac').upper()[0:3] == 'CE4':
            logger.info('CE4 case', client_ip=request['client_ip'])
            if display_region == 'ni':
                raise HTTPFound(request.app.router['StartNICE4Code:get'].url_for())
            else:
                raise HTTPFound(request.app.router['StartCodeForNorthernIreland:get'].
                                url_for(display_region=display_region))

        self.setup_uac_hash(request, data.get('uac'), lang=display_region)

        try:
            uac_json = await RHService.get_uac_details(request)
        except ClientResponseError as ex:
            if ex.status == 404:
                logger.warn('attempt to use an invalid access code',
                            client_ip=request['client_ip'])
                if display_region == 'cy':
                    flash(request, INVALID_CODE_MSG_CY)
                else:
                    flash(request, INVALID_CODE_MSG)
                raise HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))
            else:
                logger.error('error processing access code', client_ip=request['client_ip'])
                raise ex

        if uac_json['caseId'] is None:
            logger.info('unlinked case', client_ip=request['client_ip'])
            session = await get_session(request)
            session['attributes'] = {}
            session['case'] = uac_json
            if data.get('adlocation'):
                session['adlocation'] = data.get('adlocation')
            await remember(str(uuid.uuid4()), request)
            raise HTTPFound(request.app.router['CommonEnterAddress:get'].url_for(
                display_region=display_region,
                user_journey='start',
                sub_user_journey='link-address'
            ))
        else:
            await remember(uac_json['caseId'], request)

        self.validate_case(uac_json)

        try:
            attributes = uac_json['address']
        except KeyError:
            raise InvalidEqPayLoad('Could not retrieve address details')

        logger.debug('address confirmation displayed',
                     client_ip=request['client_ip'])
        session = await get_session(request)
        session['attributes'] = attributes
        session['case'] = uac_json

        if data.get('adlocation'):
            session['adlocation'] = data.get('adlocation')

        if 'transient' in session['case']['estabType'].lower():
            raise HTTPFound(request.app.router['StartTransientEnterTownName:get'].
                            url_for(display_region=display_region))

        if session['case']['region'] == 'N':
            if display_region == 'ni':
                raise HTTPFound(request.app.router['StartConfirmAddress:get'].url_for(display_region='ni'))
            else:
                raise HTTPFound(request.app.router['StartCodeForNorthernIreland:get'].
                                url_for(display_region=display_region))
        else:
            if display_region == 'ni':
                raise HTTPFound(request.app.router['StartCodeForEnglandAndWales:get'].url_for())
            else:
                raise HTTPFound(request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))


@start_routes.view(r'/' + View.valid_ew_display_regions + '/start/code-for-northern-ireland/')
class StartCodeForNorthernIreland(StartCommon):
    @aiohttp_jinja2.template('start-code-for-northern-ireland.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/code-for-northern-ireland')

        if display_region == 'cy':
            locale = 'cy'
            # TODO: add welsh translation
            page_title = "This access code is not part of the census for England and Wales"
        else:
            locale = 'en'
            page_title = 'This access code is not part of the census for England and Wales'

        await forget(request)

        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
        }


@start_routes.view('/ni/start/code-for-ce-manager/')
class StartNICE4Code(StartCommon):
    @aiohttp_jinja2.template('start-code-for-ni-ce-manager.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = 'ni'
        self.log_entry(request, display_region + '/start/code-for-ce-manager')

        locale = 'en'
        page_title = 'This access code is not part of the census for England and Wales'

        return {
            'locale': locale,
            'page_title': page_title
        }


@start_routes.view('/ni/start/code-for-england-and-wales/')
class StartCodeForEnglandAndWales(StartCommon):
    @aiohttp_jinja2.template('start-code-for-england-and-wales.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = 'ni'
        self.log_entry(request, display_region + '/start/code-for-england-and-wales')

        locale = 'en'
        page_title = 'This access code is not part of the census for Northern Ireland'

        await forget(request)

        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
        }


@start_routes.view(r'/' + View.valid_display_regions + '/start/confirm-address/')
class StartConfirmAddress(StartCommon):
    @aiohttp_jinja2.template('start-confirm-address.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        display_region = request.match_info['display_region']
        self.setup_request(request)
        self.log_entry(request, display_region + '/start/confirm-address')
        await check_permission(request)

        session = await get_session(request)

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Confirm address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Confirm address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        try:
            attributes = session['attributes']
        except KeyError:
            raise SessionTimeout('start')

        display_region_warning = False
        if (display_region == 'cy') and (session['case']['region'] == 'E'):
            logger.info('welsh url with english region - language_code will be set to en for eq',
                        client_ip=request['client_ip'])
            display_region_warning = True

        return {'locale': locale,
                'page_title': page_title,
                'page_url': View.gen_page_url(request),
                'page_show_signout': 'true',
                'display_region': display_region,
                'addressLine1': attributes['addressLine1'],
                'addressLine2': attributes['addressLine2'],
                'addressLine3': attributes['addressLine3'],
                'townName': attributes['townName'],
                'postcode': attributes['postcode'],
                'display_region_warning': display_region_warning
                }

    @aiohttp_jinja2.template('start-confirm-address.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        self.setup_request(request)
        await check_permission(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/confirm-address')

        data = await request.post()
        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
            attributes['page_title'] = 'Is this address correct?'
        except KeyError:
            raise SessionTimeout('start')

        try:
            address_confirmation = data['address-check-answer']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)

            raise HTTPFound(
                request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))

        if address_confirmation == 'Yes':
            if case['region'] == 'N':
                raise HTTPFound(
                    request.app.router['StartNILanguageOptions:get'].url_for())
            else:
                attributes['language'] = locale
                attributes['display_region'] = display_region
                await self.call_questionnaire(request, case, attributes,
                                              request.app,
                                              session.get('adlocation'))

        elif address_confirmation == 'No':
            raise HTTPFound(request.app.router['CommonEnterAddress:get'].url_for(
                display_region=display_region,
                user_journey='start',
                sub_user_journey='change-address'
            ))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))


@start_routes.view('/ni/start/language-options/')
class StartNILanguageOptions(StartCommon):
    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'ni/start/language-options')
        await check_permission(request)

        page_title = 'Confirm English or other language'
        if request.get('flash'):
            page_title = View.page_title_error_prefix_en + page_title

        return {'locale': 'en',
                'page_title': page_title,
                'page_show_signout': 'true',
                'display_region': 'ni'}

    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'ni/start/language-options')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
        except KeyError:
            raise SessionTimeout('start')

        try:
            language_option = data['language-option']
        except KeyError:
            logger.info('ni language option error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            raise HTTPFound(
                request.app.router['StartNILanguageOptions:get'].url_for())

        if language_option == 'Yes':
            attributes['language'] = 'en'
            attributes['display_region'] = 'ni'
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))

        elif language_option == 'No':
            raise HTTPFound(
                request.app.router['StartNISelectLanguage:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.info('language selection error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            raise HTTPFound(
                request.app.router['StartNILanguageOptions:get'].url_for())


@start_routes.view('/ni/start/select-language/')
class StartNISelectLanguage(StartCommon):
    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'ni/start/select-language')
        await check_permission(request)

        page_title = 'Choose language'
        if request.get('flash'):
            page_title = View.page_title_error_prefix_en + page_title

        return {'locale': 'en',
                'page_title': page_title,
                'page_show_signout': 'true',
                'display_region': 'ni'}

    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'ni/start/select-language')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']

        except KeyError:
            raise SessionTimeout('start')

        try:
            language_option = data['language-option']
        except KeyError:
            logger.info('ni language option error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            raise HTTPFound(
                request.app.router['StartNISelectLanguage:get'].url_for())

        if language_option == 'gaeilge':
            attributes['language'] = 'ga'

        elif language_option == 'ulster-scotch':
            attributes['language'] = 'eo'

        elif language_option == 'english':
            attributes['language'] = 'en'

        else:
            # catch all just in case, should never get here
            logger.info('language selection error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            raise HTTPFound(
                request.app.router['StartNISelectLanguage:get'].url_for())

        attributes['display_region'] = 'ni'

        await self.call_questionnaire(request, case, attributes, request.app,
                                      session.get('adlocation'))


@start_routes.view(r'/' + View.valid_display_regions + '/start/link-address/address-has-been-linked/')
class StartAddressHasBeenLinked(StartCommon):
    @aiohttp_jinja2.template('start-link-address-linked.html')
    async def get(self, request):
        self.setup_request(request)
        await check_permission(request)
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Your address has been linked to your code'
            locale = 'cy'
        else:
            page_title = 'Your address has been linked to your code'
            locale = 'en'

        self.log_entry(request, display_region + '/start/link-address/address-has-been-linked')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        self.setup_request(request)
        await check_permission(request)
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        self.log_entry(request, display_region + '/start/link-address/address-has-been-linked')

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
        except KeyError:
            raise SessionTimeout('start')

        if case['region'] == 'N':
            raise HTTPFound(
                request.app.router['StartNILanguageOptions:get'].url_for())
        else:
            attributes['language'] = locale
            attributes['display_region'] = display_region
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))


@start_routes.view(r'/' + View.valid_display_regions + '/start/change-address/address-has-been-changed/')
class StartAddressHasBeenChanged(StartCommon):
    @aiohttp_jinja2.template('start-address-changed.html')
    async def get(self, request):
        self.setup_request(request)
        await check_permission(request)
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Your address has been changed'
            locale = 'cy'
        else:
            page_title = 'Your address has been changed'
            locale = 'en'

        self.log_entry(request, display_region + '/start/change-address/address-has-been-changed')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        self.setup_request(request)
        await check_permission(request)
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        self.log_entry(request, display_region + '/start/change-address/address-has-been-changed')

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
        except KeyError:
            raise SessionTimeout('start')

        if case['region'] == 'N':
            raise HTTPFound(
                request.app.router['StartNILanguageOptions:get'].url_for())
        else:
            attributes['language'] = locale
            attributes['display_region'] = display_region
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))


@start_routes.view(r'/' + View.valid_display_regions + '/start/transient/enter-town-name/')
class StartTransientEnterTownName(StartCommon):
    @aiohttp_jinja2.template('start-transient-enter-town.html')
    async def get(self, request):
        self.setup_request(request)
        await check_permission(request)
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Nearest town or city'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Nearest town or city'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        self.log_entry(request, display_region + '/start/transient/enter-town-name')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'after-census-day': View.check_if_after_census_day(),
            'page_show_signout': 'true'
        }

    @aiohttp_jinja2.template('start-transient-enter-town.html')
    async def post(self, request):
        self.setup_request(request)
        await check_permission(request)
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/start/transient/enter-town-name')

        data = await request.post()

        session = await get_session(request)

        try:
            town_name = data['form-enter-town-name']
            if not town_name:
                raise KeyError
            session['attributes']['transientTownName'] = town_name
            session.changed()

            raise HTTPFound(
                request.app.router['StartTransientAccommodationType:get'].url_for(display_region=display_region)
            )

        except KeyError:
            logger.info('error town name empty',
                        client_ip=request['client_ip'])
            if display_region == 'cy':
                # TODO: add welsh translation
                flash(request, FlashMessage.generate_flash_message('Enter your nearest town or city', 'ERROR',
                                                                   'TOWN_NAME_ENTER_ERROR', 'error-enter-town-name'))
            else:
                flash(request, FlashMessage.generate_flash_message('Enter your nearest town or city', 'ERROR',
                                                                   'TOWN_NAME_ENTER_ERROR', 'error-enter-town-name'))
            raise HTTPFound(
                request.app.router['StartTransientEnterTownName:get'].url_for(display_region=display_region)
            )


@start_routes.view(r'/' + View.valid_display_regions + '/start/transient/accommodation-type/')
class StartTransientAccommodationType(StartCommon):
    @aiohttp_jinja2.template('start-transient-accommodation-type.html')
    async def get(self, request):
        self.setup_request(request)
        await check_permission(request)
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            # TODO: add welsh translation
            page_title = 'Which of the following best describes your type of accommodation?'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Which of the following best describes your type of accommodation?'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'en'

        self.log_entry(request, display_region + '/start/transient/accommodation-type')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'page_show_signout': 'true'
        }

    @aiohttp_jinja2.template('start-transient-accommodation-type.html')
    async def post(self, request):
        self.setup_request(request)
        await check_permission(request)
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        self.log_entry(request, display_region + '/start/transient/accommodation-type')

        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
        except KeyError:
            raise SessionTimeout('start')

        try:
            accommodation_type = data['accommodation-type']
            session['attributes']['transientAccommodationType'] = accommodation_type
            session.changed()

            if case['region'] == 'N':
                raise HTTPFound(
                    request.app.router['StartNILanguageOptions:get'].url_for())
            else:
                attributes['language'] = locale
                attributes['display_region'] = display_region
                await self.call_questionnaire(request, case,
                                              attributes, request.app,
                                              session.get('adlocation'))

        except KeyError:
            logger.info('transient accommodation type error', client_ip=request['client_ip'])
            if display_region == 'cy':
                # TODO: add welsh translation
                flash(request, FlashMessage.generate_flash_message('Select an answer', 'ERROR',
                                                                   'ACCOMMODATION_TYPE_ERROR',
                                                                   'error-accommodation-type'))
            else:
                flash(request, FlashMessage.generate_flash_message('Select an answer', 'ERROR',
                                                                   'ACCOMMODATION_TYPE_ERROR',
                                                                   'error-accommodation-type'))
            raise HTTPFound(
                request.app.router['StartTransientAccommodationType:get'].url_for(display_region=display_region)
            )
