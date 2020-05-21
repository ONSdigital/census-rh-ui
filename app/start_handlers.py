import aiohttp_jinja2
import re
import uuid

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from aiohttp_session import get_session
from structlog import get_logger

from . import (BAD_CODE_MSG, INVALID_CODE_MSG, ADDRESS_CHECK_MSG,
               ADDRESS_EDIT_MSG, SESSION_TIMEOUT_MSG,
               START_LANGUAGE_OPTION_MSG,
               BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY, ADDRESS_CHECK_MSG_CY,
               ADDRESS_EDIT_MSG_CY, SESSION_TIMEOUT_MSG_CY)

from .flash import flash
from .exceptions import InvalidEqPayLoad
from .security import remember, check_permission, forget, get_sha256_hash

from .utils import View

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

    async def get_uac_details(self, request):
        uac_hash = request['uac_hash']
        logger.info('making get request for uac',
                    uac_hash=uac_hash,
                    client_ip=request['client_ip'])
        rhsvc_url = request.app['RHSVC_URL']
        return await self._make_request(request,
                                        'GET',
                                        f'{rhsvc_url}/uacs/{uac_hash}',
                                        self._handle_response,
                                        auth=request.app['RHSVC_AUTH'],
                                        return_json=True)

    async def put_modify_address(self, request, case, address):
        rhsvc_url = request.app['RHSVC_URL']
        rhsvc_auth = request.app['RHSVC_AUTH']
        case_json = {
            'caseId': case['caseId'],
            'uprn': case['address']['uprn'],
            'addressLine1': address['addressLine1'],
            'addressLine2': address['addressLine2'],
            'addressLine3': address['addressLine3'],
            'townName': address['townName'],
            'postcode': address['postcode']
        }
        return await self._make_request(request,
                                        'PUT',
                                        f'{rhsvc_url}/cases/' +
                                        case['caseId'] + '/address',
                                        self._handle_response,
                                        auth=rhsvc_auth,
                                        json=case_json)

    @staticmethod
    def get_address_details(data: dict, attributes: dict):
        """
        Replace any changed address details in attributes to be sent to EQ
        :param data: Changed address details
        :param attributes: attributes to be sent
        :return: attributes with changed address
        """

        if not data['address-line-1'].strip():
            raise KeyError
        else:
            attributes['addressLine1'] = data['address-line-1'].strip()
            attributes['addressLine2'] = data['address-line-2'].strip()
            attributes['addressLine3'] = data['address-line-3'].strip()
            attributes['townName'] = data['address-town'].strip()
            attributes['postcode'] = data['address-postcode'].strip()

        return attributes


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
            page_title = "Dechrau'r Cyfrifiad"
        else:
            locale = 'en'
            page_title = 'Start Census'

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
                    'page_url': '/start/'
                }
            else:
                logger.warn('assisted digital query parameter not numeric - ignoring',
                            adlocation=adlocation,
                            client_ip=request['client_ip'])
                return {
                    'display_region': display_region,
                    'page_title': page_title,
                    'locale': locale,
                    'page_url': '/start/'
                }
        except KeyError:
            return {
                'display_region': display_region,
                'page_title': page_title,
                'locale': locale,
                'page_url': '/start/'
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
            page_title = "Dechrau'r Cyfrifiad"
        else:
            locale = 'en'
            page_title = 'Start Census'
        data = await request.post()
        self.setup_uac_hash(request, data.get('uac'), lang=display_region)

        try:
            uac_json = await self.get_uac_details(request)
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
                        'locale': locale
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
            'page_title': page_title
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
            page_title = "Ydy'r cyfeiriad hwn yn gywir?"
        else:
            locale = 'en'
            page_title = 'Is this address correct?'

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            if display_region == 'cy':
                flash(request, SESSION_TIMEOUT_MSG_CY)
            else:
                flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))

        return {'locale': locale,
                'page_title': page_title,
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
            page_title = "Ydy'r cyfeiriad hwn yn gywir?"
        else:
            locale = 'en'
            page_title = 'Is this address correct?'

        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
            attributes['page_title'] = 'Is this address correct?'
        except KeyError:
            if display_region == 'cy':
                flash(request, SESSION_TIMEOUT_MSG_CY)
            else:
                flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))

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
            raise HTTPFound(request.app.router['StartModifyAddress:get'].url_for(display_region=display_region))

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
                    'display_region': display_region,
                    'addressLine1': attributes['addressLine1'],
                    'addressLine2': attributes['addressLine2'],
                    'addressLine3': attributes['addressLine3'],
                    'townName': attributes['townName'],
                    'postcode': attributes['postcode']}


@start_routes.view(r'/' + View.valid_display_regions + '/start/modify-address/')
class StartModifyAddress(StartCommon):
    @aiohttp_jinja2.template('start-modify-address.html')
    async def get(self, request):
        """
        Address Edit get.
        """
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/modify-address')
        await check_permission(request)

        if display_region == 'cy':
            locale = 'cy'
            page_title = "Newid eich cyfeiriad"
        else:
            locale = 'en'
            page_title = 'Change your address'

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))

        return {'locale': locale,
                'page_title': page_title,
                'display_region': display_region,
                'addressLine1': attributes['addressLine1'],
                'addressLine2': attributes['addressLine2'],
                'addressLine3': attributes['addressLine3'],
                'townName': attributes['townName'],
                'postcode': attributes['postcode']}

    @aiohttp_jinja2.template('start-modify-address.html')
    async def post(self, request):
        """
        Address Edit flow. Edited address details.
        """
        self.setup_request(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/modify-address')
        await check_permission(request)
        data = await request.post()

        if display_region == 'cy':
            locale = 'cy'
            page_title = "Newid eich cyfeiriad"
        else:
            locale = 'en'
            page_title = 'Change your address'

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))

        try:
            attributes = StartCommon.get_address_details(data,
                                                         attributes)
        except KeyError:
            logger.info('address-line-1 has no value', client_ip=request['client_ip'])
            if display_region == 'cy':
                flash(request, ADDRESS_EDIT_MSG_CY)
            else:
                flash(request, ADDRESS_EDIT_MSG)
            return {'locale': locale,
                    'page_title': page_title,
                    'display_region': display_region,
                    'addressLine2': attributes['addressLine2'],
                    'addressLine3': attributes['addressLine3'],
                    'townName': attributes['townName'],
                    'postcode': attributes['postcode']}

        try:
            logger.info('raising address modification call',
                        client_ip=request['client_ip'])
            await self.put_modify_address(request, session['case'], attributes)
        except ClientResponseError as ex:
            logger.error('error raising address modification call',
                         client_ip=request['client_ip'])
            raise ex

        if case['region'][0] == 'N':
            session['attributes']['addressLine1'] = attributes['addressLine1']
            session['attributes']['addressLine2'] = attributes['addressLine2']
            session['attributes']['addressLine3'] = attributes['addressLine3']
            session['attributes']['townName'] = attributes['townName']
            session['attributes']['postcode'] = attributes['postcode']
            session.changed()
            raise HTTPFound(
                request.app.router['StartNILanguageOptions:get'].url_for())
        else:
            attributes['language'] = locale
            attributes['display_region'] = display_region
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))


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

        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['Start:get'].url_for(display_region='ni'))

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
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['Start:get'].url_for(display_region='ni'))

        try:
            language_option = data['language-option']
        except KeyError:
            logger.info('ni language option error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            return {'locale': 'en',
                    'page_title': 'Choose your language',
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
            'locale': locale
        }


@start_routes.view(r'/' + View.valid_display_regions + '/start/unlinked/address-has-been-linked/')
class StartAddressHasBeenLinked(StartCommon):
    @aiohttp_jinja2.template('start-unlinked-linked.html')
    async def get(self, request):
        self.setup_request(request)
        await check_permission(request)
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = 'Your address has been linked to your code'
            locale = 'cy'
        else:
            page_title = 'Your address has been linked to your code'
            locale = 'en'

        self.log_entry(request, display_region + '/start/unlinked/address-has-been-linked')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale
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
            if display_region == 'cy':
                flash(request, SESSION_TIMEOUT_MSG_CY)
            else:
                flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))

        if case['region'][0] == 'N':
            raise HTTPFound(
                request.app.router['StartNILanguageOptions:get'].url_for())
        else:
            attributes['language'] = locale
            attributes['display_region'] = display_region
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))
