import aiohttp_jinja2
import re
import uuid

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from aiohttp_session import get_session
from structlog import get_logger

from . import (BAD_CODE_MSG, INVALID_CODE_MSG, ADDRESS_CHECK_MSG,
               START_LANGUAGE_OPTION_MSG,
               BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY, ADDRESS_CHECK_MSG_CY)

from .flash import flash
from .exceptions import InvalidEqPayLoad, SessionTimeout
from .security import remember, check_permission, forget, get_sha256_hash

from .utils import View, RHService

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
                'en': BAD_CODE_MSG,
                'cy': BAD_CODE_MSG_CY,
                'ni': BAD_CODE_MSG,
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
        else:
            locale = 'en'
            page_title = 'Start census'

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
            return {
                'display_region': display_region,
                'page_title': page_title,
                'locale': locale,
                'page_url': View.gen_page_url(request)
            }

    @aiohttp_jinja2.template('start.html')
    async def post(self, request):
        """
        Forward to Address confirmation
        :param request:
        :return: address confirmation view
        """
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start')
        if display_region == 'cy':
            locale = 'cy'
            # TODO Confirm welsh translation
            page_title = "Dechrau'r cyfrifiad"
        else:
            locale = 'en'
            page_title = 'Start census'
        data = await request.post()
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
                return aiohttp_jinja2.render_template(
                    'start.html',
                    request, {
                        'display_region': display_region,
                        'page_title': page_title,
                        'locale': locale,
                        'page_url': View.gen_page_url(request)
                    },
                    status=401)
            else:
                raise ex

        logger.info('logging uac_json', uac_json=uac_json)

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
                sub_user_journey='unlinked'
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

        if session['case']['region'][0] == 'N':
            if display_region == 'ni':
                raise HTTPFound(request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))
            else:
                raise HTTPFound(request.app.router['StartRegionChange:get'].url_for(display_region='ni'))
        elif session['case']['region'][0] == 'W':
            if display_region == 'ni':
                raise HTTPFound(request.app.router['StartRegionChange:get'].url_for(display_region='en'))
            else:
                raise HTTPFound(request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))
        else:
            if display_region == 'en':
                raise HTTPFound(request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))
            else:
                raise HTTPFound(request.app.router['StartRegionChange:get'].url_for(display_region='en'))


@start_routes.view(r'/' + View.valid_display_regions + '/start/region-change/')
class StartRegionChange(StartCommon):
    @aiohttp_jinja2.template('start-region-change.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/region-change')

        await check_permission(request)

        locale = 'en'
        page_title = 'Change of region'

        self.log_entry(request, 'start/region-change')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_title': page_title,
            'page_url': View.gen_page_url(request),
            'page_show_signout': 'true'
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
        if display_region == 'cy':
            locale = 'cy'
            # TODO: add welsh translation
            page_title = "Is this the correct address?"
        else:
            locale = 'en'
            page_title = 'Is this the correct address?'

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            raise SessionTimeout('start')

        return {'locale': locale,
                'page_title': page_title,
                'page_url': View.gen_page_url(request),
                'page_show_signout': 'true',
                'display_region': display_region,
                'addressLine1': attributes['addressLine1'],
                'addressLine2': attributes['addressLine2'],
                'addressLine3': attributes['addressLine3'],
                'townName': attributes['townName'],
                'postcode': attributes['postcode']}

    @aiohttp_jinja2.template('start-confirm-address.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        self.setup_request(request)
        await check_permission(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/confirm-address')
        if display_region == 'cy':
            locale = 'cy'
            # TODO: add welsh translation
            page_title = "Is this the correct address?"
        else:
            locale = 'en'
            page_title = 'Is this the correct address?'

        data = await request.post()

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
                flash(request, ADDRESS_CHECK_MSG_CY)
            else:
                flash(request, ADDRESS_CHECK_MSG)
            return {'locale': locale,
                    'page_title': page_title,
                    'page_url': View.gen_page_url(request),
                    'page_show_signout': 'true',
                    'display_region': display_region,
                    'addressLine1': attributes['addressLine1'],
                    'addressLine2': attributes['addressLine2'],
                    'addressLine3': attributes['addressLine3'],
                    'townName': attributes['townName'],
                    'postcode': attributes['postcode']}

        if address_confirmation == 'Yes':
            if case['region'][0] == 'N':
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
                flash(request, ADDRESS_CHECK_MSG_CY)
            else:
                flash(request, ADDRESS_CHECK_MSG)
            return {'locale': locale,
                    'page_title': page_title,
                    'page_url': View.gen_page_url(request),
                    'page_show_signout': 'true',
                    'display_region': display_region,
                    'addressLine1': attributes['addressLine1'],
                    'addressLine2': attributes['addressLine2'],
                    'addressLine3': attributes['addressLine3'],
                    'townName': attributes['townName'],
                    'postcode': attributes['postcode']}


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

        return {'locale': 'en',
                'page_title': 'Would you like to complete the census in English?',
                'page_show_signout': 'true',
                'display_region': 'ni'}

    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'ni/start/language-options')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
            attributes[
                'page_title'] = 'Would you like to complete the census in English?'
            attributes['page_show_signout'] = 'true'

        except KeyError:
            raise SessionTimeout('start')

        try:
            language_option = data['language-option']
        except KeyError:
            logger.info('ni language option error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

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
            return {'locale': 'en',
                    'page_title': 'Would you like to complete the census in English?',
                    'page_show_signout': 'true',
                    'display_region': 'ni'}


@start_routes.view('/ni/start/select-language/')
class StartNISelectLanguage(StartCommon):
    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'ni/start/ni-select-language')
        await check_permission(request)

        return {'locale': 'en',
                'page_title': 'Choose your language',
                'page_show_signout': 'true',
                'display_region': 'ni'}

    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'ni/start/ni-select-language')
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
            return {'locale': 'en',
                    'page_title': 'Choose your language',
                    'page_show_signout': 'true',
                    'display_region': 'ni'}

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
            return {'locale': 'en',
                    'page_title': 'Choose your language',
                    'page_show_signout': 'true',
                    'display_region': 'ni'}

        attributes['display_region'] = 'ni'

        await self.call_questionnaire(request, case, attributes, request.app,
                                      session.get('adlocation'))


@start_routes.view(r'/' + View.valid_display_regions + '/start/save-and-exit/')
class StartSaveAndExit(StartCommon):
    @aiohttp_jinja2.template('save-and-exit.html')
    async def get(self, request):
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/save-and-exit')
        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'
        await forget(request)
        return {
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }


@start_routes.view(r'/' + View.valid_display_regions + '/start/unlinked/address-has-been-linked/')
class StartAddressHasBeenLinked(StartCommon):
    @aiohttp_jinja2.template('start-unlinked-linked.html')
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

        self.log_entry(request, display_region + '/start/unlinked/address-has-been-linked')

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

        self.log_entry(request, display_region + '/start/unlinked/address-has-been-linked')

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
        except KeyError:
            raise SessionTimeout('start')

        if case['region'][0] == 'N':
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

        if case['region'][0] == 'N':
            raise HTTPFound(
                request.app.router['StartNILanguageOptions:get'].url_for())
        else:
            attributes['language'] = locale
            attributes['display_region'] = display_region
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))
