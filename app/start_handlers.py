import aiohttp_jinja2
import re

from sdc.crypto.encrypter import encrypt
from .eq import EqPayloadConstructor

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from aiohttp_session import get_session
from structlog import get_logger

from . import (BAD_CODE_MSG, INVALID_CODE_MSG, ADDRESS_CHECK_MSG,
               ADDRESS_EDIT_MSG, SESSION_TIMEOUT_MSG,
               START_LANGUAGE_OPTION_MSG,
               BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY, ADDRESS_CHECK_MSG_CY,
               ADDRESS_EDIT_MSG_CY, SESSION_TIMEOUT_MSG_CY,
               START_LANGUAGE_OPTION_MSG_CY)
from .exceptions import InactiveCaseError
from .flash import flash
from .exceptions import InvalidEqPayLoad
from .security import remember, check_permission, forget, get_sha256_hash

# from .handlers import View
from .utils import View

logger = get_logger('respondent-home')
start_routes = RouteTableDef()


class Start(View):
    def setup_request(self, request):
        super().setup_request(request)

    def setup_uac_hash(self, request, uac, lang):
        try:
            request['uac_hash'] = self.uac_hash(uac)
        except TypeError:
            logger.warn('attempt to use a malformed access code',
                        client_ip=request['client_ip'])
            message = {
                'EN': BAD_CODE_MSG,
                'CY': BAD_CODE_MSG_CY,
                'NI': BAD_CODE_MSG,
            }[lang]
            endpoint = {
                'EN': 'IndexEN:get',
                'CY': 'IndexCY:get',
                'NI': 'IndexNI:get',
            }[lang]
            flash(request, message)
            raise HTTPFound(request.app.router[endpoint].url_for())

    @staticmethod
    def uac_hash(uac, expected_length=16):
        if uac:
            combined = uac.lower().replace(' ', '')
        else:
            combined = ''

        uac_validation_pattern = re.compile(r'^[a-z0-9]{16}$')

        if (len(combined) < expected_length) or not (uac_validation_pattern.fullmatch(combined)):  # yapf: disable
            raise TypeError

        return get_sha256_hash(combined)

    async def call_questionnaire(self, request, case, attributes, app,
                                 adlocation):
        eq_payload = await EqPayloadConstructor(case, attributes, app,
                                                adlocation).build()

        token = encrypt(eq_payload,
                        key_store=app['key_store'],
                        key_purpose='authentication')

        await self.post_surveylaunched(request, case, adlocation)

        logger.info('redirecting to eq', client_ip=request['client_ip'])
        eq_url = app['EQ_URL']
        raise HTTPFound(f'{eq_url}/session?token={token}')

    async def post_surveylaunched(self, request, case, adlocation):
        if not adlocation:
            adlocation = ''
        launch_json = {
            'questionnaireId': case['questionnaireId'],
            'caseId': case['caseId'],
            'agentId': adlocation
        }
        rhsvc_url = request.app['RHSVC_URL']
        return await self._make_request(request,
                                        'POST',
                                        f'{rhsvc_url}/surveyLaunched',
                                        self._handle_response,
                                        auth=request.app['RHSVC_AUTH'],
                                        json=launch_json)

    @staticmethod
    def validate_case(case_json):
        if not case_json.get('active', False):
            raise InactiveCaseError(case_json.get('caseType'))
        if not case_json.get('caseStatus', None) == 'OK':
            raise InvalidEqPayLoad('CaseStatus is not OK')

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
    def get_address_details(request, data: dict, attributes: dict):
        """
        Replace any changed address details in attributes to be sent to EQ
        :param request:
        :param data: Changed address details
        :param attributes: attributes to be sent
        :return: attributes with changed address
        """

        if not data['address-line-1'].strip():
            ip = request['client_ip']
            raise InvalidEqPayLoad(f'Mandatory address field not present {ip}')
        else:
            attributes['addressLine1'] = data['address-line-1'].strip()
            attributes['addressLine2'] = data['address-line-2'].strip()
            attributes['addressLine3'] = data['address-line-3'].strip()
            attributes['townName'] = data['address-town'].strip()
            attributes['postcode'] = data['address-postcode'].strip()

        return attributes


@start_routes.view('/start/')
class IndexEN(Start):
    @aiohttp_jinja2.template('index.html')
    async def get(self, request):
        """
        RH home page to enter a UAC.
        Checks if URL carries query string assisted digital location and stores to session
        :param request:
        :return:
        """
        self.setup_request(request)
        self.log_entry(request, 'start')

        try:
            adlocation = request.query['adlocation']
            if adlocation.isdigit():
                logger.info('assisted digital query parameter found',
                            adlocation=adlocation,
                            client_ip=request['client_ip'])
                return {
                    'display_region': 'en',
                    'page_title': 'Start Census',
                    'adlocation': request.query['adlocation']
                }
            else:
                logger.warn('assisted digital query parameter not numeric - ignoring',
                            adlocation=adlocation,
                            client_ip=request['client_ip'])
                return {
                    'display_region': 'en',
                    'page_title': 'Start Census'
                }
        except KeyError:
            return {
                'display_region': 'en',
                'page_title': 'Start Census'
            }

    @aiohttp_jinja2.template('index.html')
    async def post(self, request):
        """
        Forward to Address confirmation
        :param request:
        :return: address confirmation view
        """
        self.setup_request(request)
        self.log_entry(request, 'start')
        data = await request.post()
        self.setup_uac_hash(request, data.get('uac'), lang='EN')

        try:
            uac_json = await self.get_uac_details(request)
        except ClientResponseError as ex:
            if ex.status == 404:
                logger.warn('attempt to use an invalid access code',
                            client_ip=request['client_ip'])
                flash(request, INVALID_CODE_MSG)
                return aiohttp_jinja2.render_template(
                    'index.html',
                    request, {
                        'display_region': 'en',
                        'page_title': 'Start Census'
                    },
                    status=401)
            else:
                raise ex

        await remember(uac_json['caseId'], request)

        self.validate_case(uac_json)

        try:
            attributes = uac_json['address']
        except KeyError:
            raise InvalidEqPayLoad('Could not retrieve address details')

        # SOMEHOW NEED TO MAP ADDRESS DETAILS TO ATTRIBUTES SO CAN BE DISPLAYED

        logger.debug('address confirmation displayed',
                     client_ip=request['client_ip'])
        session = await get_session(request)
        session['attributes'] = attributes
        session['case'] = uac_json
        session['attributes']['display_region'] = 'en'

        if data.get('adlocation'):
            session['adlocation'] = data.get('adlocation')

        raise HTTPFound(
            request.app.router['AddressConfirmationEN:get'].url_for())


@start_routes.view('/dechrau/')
class IndexCY(Start):
    @aiohttp_jinja2.template('index.html')
    async def get(self, request):
        """
        RH home page to enter a UAC. Checks if URL carries query string assisted digital location and stores to session
        :param request:
        :return:
        """
        self.setup_request(request)
        self.log_entry(request, 'start')

        try:
            adlocation = request.query['adlocation']
            if adlocation.isdigit():
                logger.info('assisted digital query parameter found',
                            adlocation=adlocation,
                            client_ip=request['client_ip'])
                return {
                    'display_region': 'cy',
                    'locale': 'cy',
                    'page_title': "Dechrau'r Cyfrifiad",
                    'adlocation': request.query['adlocation']
                }
            else:
                logger.warn('assisted digital query parameter not numeric - ignoring',
                            adlocation=adlocation,
                            client_ip=request['client_ip'])
                return {
                    'display_region': 'cy',
                    'locale': 'cy',
                    'page_title': "Dechrau'r Cyfrifiad"
                }
        except KeyError:
            return {
                'display_region': 'cy',
                'locale': 'cy',
                'page_title': "Dechrau'r Cyfrifiad"
            }

    async def post(self, request):
        """
        Forward to Address confirmation
        :param request:
        :return: address confirmation view
        """
        self.setup_request(request)
        self.log_entry(request, 'start')
        data = await request.post()
        self.setup_uac_hash(request, data.get('uac'), lang='CY')

        try:
            uac_json = await self.get_uac_details(request)
        except ClientResponseError as ex:
            if ex.status == 404:
                logger.warn('attempt to use an invalid access code',
                            client_ip=request['client_ip'])
                flash(request, INVALID_CODE_MSG_CY)
                return aiohttp_jinja2.render_template(
                    'index.html',
                    request, {
                        'display_region': 'cy',
                        'locale': 'cy',
                        'page_title': "Dechrau'r Cyfrifiad"
                    },
                    status=401)
            else:
                raise ex

        await remember(uac_json['caseId'], request)

        self.validate_case(uac_json)

        try:
            attributes = uac_json['address']
        except KeyError:
            raise InvalidEqPayLoad('Could not retrieve address details')

        # SOMEHOW NEED TO MAP ADDRESS DETAILS TO ATTRIBUTES SO CAN BE DISPLAYED

        logger.debug('address confirmation displayed',
                     client_ip=request['client_ip'])
        session = await get_session(request)
        session['attributes'] = attributes
        session['case'] = uac_json
        session['attributes']['display_region'] = 'cy'
        session['attributes']['locale'] = 'cy'

        if data.get('adlocation'):
            session['adlocation'] = data.get('adlocation')

        raise HTTPFound(
            request.app.router['AddressConfirmationCY:get'].url_for())


@start_routes.view('/ni/start/')
class IndexNI(Start):
    @aiohttp_jinja2.template('index.html')
    async def get(self, request):
        """
        RH home page to enter a UAC. Checks if URL carries query string assisted digital location and stores to session
        :param request:
        :return:
        """
        self.setup_request(request)
        self.log_entry(request, 'start')

        try:
            adlocation = request.query['adlocation']
            if adlocation.isdigit():
                logger.info('assisted digital query parameter found',
                            adlocation=adlocation,
                            client_ip=request['client_ip'])
                return {
                    'display_region': 'ni',
                    'page_title': 'Start Census',
                    'adlocation': request.query['adlocation']
                }
            else:
                logger.warn('assisted digital query parameter not numeric - ignoring',
                            adlocation=adlocation,
                            client_ip=request['client_ip'])
                return {
                    'display_region': 'ni',
                    'page_title': 'Start Census'
                }
        except KeyError:
            return {
                'display_region': 'ni',
                'page_title': 'Start Census'
            }

    async def post(self, request):
        """
        Forward to Address confirmation
        :param request:
        :return: address confirmation view
        """
        self.setup_request(request)
        self.log_entry(request, 'start')
        data = await request.post()
        self.setup_uac_hash(request, data.get('uac'), lang='NI')

        try:
            uac_json = await self.get_uac_details(request)
        except ClientResponseError as ex:
            if ex.status == 404:
                logger.warn('attempt to use an invalid access code',
                            client_ip=request['client_ip'])
                flash(request, INVALID_CODE_MSG)
                return aiohttp_jinja2.render_template(
                    'index.html',
                    request, {
                        'display_region': 'ni',
                        'page_title': 'Start Census'
                    },
                    status=401)
            else:
                raise ex

        await remember(uac_json['caseId'], request)

        self.validate_case(uac_json)

        try:
            attributes = uac_json['address']
        except KeyError:
            raise InvalidEqPayLoad('Could not retrieve address details')

        # SOMEHOW NEED TO MAP ADDRESS DETAILS TO ATTRIBUTES SO CAN BE DISPLAYED

        logger.debug('address confirmation displayed',
                     client_ip=request['client_ip'])
        session = await get_session(request)
        session['attributes'] = attributes
        session['case'] = uac_json
        session['attributes']['display_region'] = 'ni'

        if data.get('adlocation'):
            session['adlocation'] = data.get('adlocation')

        raise HTTPFound(
            request.app.router['AddressConfirmationNI:get'].url_for())


@start_routes.view('/start/address-confirmation')
class AddressConfirmationEN(Start):
    @aiohttp_jinja2.template('address-confirmation.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-confirmation')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexEN:get'].url_for())

        attributes['page_title'] = 'Is this address correct?'

        return attributes

    @aiohttp_jinja2.template('address-confirmation.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-confirmation')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
            attributes['page_title'] = 'Is this address correct?'
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexEN:get'].url_for())

        try:
            address_confirmation = data['address-check-answer']
        except KeyError:
            logger.warn('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'Yes':
            if case['region'][0] == 'N':
                raise HTTPFound(
                    request.app.router['StartLanguageOptionsEN:get'].url_for())
            else:
                attributes['language'] = 'en'
                await self.call_questionnaire(request, case, attributes,
                                              request.app,
                                              session.get('adlocation'))

        elif address_confirmation == 'No':
            raise HTTPFound(request.app.router['AddressEditEN:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@start_routes.view('/dechrau/cadarnhad-o-gyfeiriad')
class AddressConfirmationCY(Start):
    @aiohttp_jinja2.template('address-confirmation.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-confirmation')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(request.app.router['IndexCY:get'].url_for())

        attributes['page_title'] = "Ydy'r cyfeiriad hwn yn gywir?"
        if session['case']['region'][0] == 'E':
            logger.info('welsh url with english region - language_code will be set to en for eq',
                        client_ip=request['client_ip'])
            attributes['display_region_warning'] = 'yes'

        return attributes

    @aiohttp_jinja2.template('address-confirmation.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-confirmation')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            attributes['page_title'] = "Ydy'r cyfeiriad hwn yn gywir?"
            case = session['case']

        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(request.app.router['IndexCY:get'].url_for())

        try:
            address_confirmation = data['address-check-answer']
        except KeyError:
            logger.warn('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes

        if address_confirmation == 'Yes':
            if case['region'][0] == 'N':
                raise HTTPFound(
                    request.app.router['StartLanguageOptionsCY:get'].url_for())
            else:
                attributes['language'] = 'cy'
                await self.call_questionnaire(request, case, attributes,
                                              request.app,
                                              session.get('adlocation'))

        elif address_confirmation == 'No':
            raise HTTPFound(request.app.router['AddressEditCY:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG_CY)
            return attributes


@start_routes.view('/ni/start/address-confirmation')
class AddressConfirmationNI(Start):
    @aiohttp_jinja2.template('address-confirmation.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-confirmation')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexNI:get'].url_for())

        attributes['page_title'] = 'Is this address correct?'

        return attributes

    @aiohttp_jinja2.template('address-confirmation.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-confirmation')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
            attributes['page_title'] = 'Is this address correct?'

        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexNI:get'].url_for())

        try:
            address_confirmation = data['address-check-answer']
        except KeyError:
            logger.warn('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes

        if address_confirmation == 'Yes':
            if case['region'][0] == 'N':
                raise HTTPFound(
                    request.app.router['StartLanguageOptionsNI:get'].url_for())
            else:
                attributes['language'] = 'en'
                await self.call_questionnaire(request, case, attributes,
                                              request.app,
                                              session.get('adlocation'))

        elif address_confirmation == 'No':
            raise HTTPFound(request.app.router['AddressEditNI:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn('address confirmation error',
                        client_ip=request['client_ip'])
            flash(request, ADDRESS_CHECK_MSG)
            return attributes


@start_routes.view('/start/address-edit')
class AddressEditEN(Start):
    @aiohttp_jinja2.template('address-edit.html')
    async def get(self, request):
        """
        Address Edit get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-edit')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexEN:get'].url_for())

        attributes['page_title'] = 'Change your address'

        return attributes

    @aiohttp_jinja2.template('address-edit.html')
    async def post(self, request):
        """
        Address Edit flow. Edited address details.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-edit')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexEN:get'].url_for())

        try:
            attributes = Start.get_address_details(request, data,
                                                   attributes)
        except InvalidEqPayLoad:
            logger.info(
                'error editing address, mandatory field required by eq',
                client_ip=request['client_ip'])
            flash(request, ADDRESS_EDIT_MSG)
            return attributes

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
                request.app.router['StartLanguageOptionsEN:get'].url_for())
        else:
            attributes['language'] = 'en'
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))


@start_routes.view('/dechrau/golygu-cyfeiriad')
class AddressEditCY(Start):
    @aiohttp_jinja2.template('address-edit.html')
    async def get(self, request):
        """
        Address Edit get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-edit')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(request.app.router['IndexCY:get'].url_for())

        attributes['page_title'] = 'Newid eich cyfeiriad'

        return attributes

    @aiohttp_jinja2.template('address-edit.html')
    async def post(self, request):
        """
        Address Edit flow. Edited address details.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-edit')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(request.app.router['IndexCY:get'].url_for())

        try:
            attributes = Start.get_address_details(request, data,
                                                   attributes)
        except InvalidEqPayLoad:
            logger.info(
                'error editing address, mandatory field required by eq',
                client_ip=request['client_ip'])
            flash(request, ADDRESS_EDIT_MSG_CY)
            return attributes

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
                request.app.router['StartLanguageOptionsCY:get'].url_for())
        else:
            attributes['language'] = 'cy'
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))


@start_routes.view('/ni/start/address-edit')
class AddressEditNI(Start):
    @aiohttp_jinja2.template('address-edit.html')
    async def get(self, request):
        """
        Address Edit get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-edit')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexNI:get'].url_for())

        attributes['page_title'] = 'Change your address'

        return attributes

    @aiohttp_jinja2.template('address-edit.html')
    async def post(self, request):
        """
        Address Edit flow. Edited address details.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/address-edit')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexNI:get'].url_for())

        try:
            attributes = Start.get_address_details(request, data,
                                                   attributes)
        except InvalidEqPayLoad:
            logger.info(
                'error editing address, mandatory field required by eq',
                client_ip=request['client_ip'])
            flash(request, ADDRESS_EDIT_MSG)
            return attributes

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
                request.app.router['StartLanguageOptionsNI:get'].url_for())
        else:
            attributes['language'] = 'en'
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))


@start_routes.view('/start/language-options')
class StartLanguageOptionsEN(Start):
    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/language-options')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexEN:get'].url_for())

        attributes[
            'page_title'] = 'Would you like to complete the census in English?'

        return attributes

    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/language-options')
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
            raise HTTPFound(request.app.router['IndexEN:get'].url_for())

        try:
            language_option = data['language-option']
        except KeyError:
            logger.warn('ni language option error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        if language_option == 'Yes':
            attributes['language'] = 'en'
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))

        elif language_option == 'No':
            raise HTTPFound(
                request.app.router['StartSelectLanguageEN:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn('language selection error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes


@start_routes.view('/dechrau/language-options')
class StartLanguageOptionsCY(Start):
    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/language-options')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(request.app.router['IndexCY:get'].url_for())

        attributes[
            'page_title'] = 'Would you like to complete the census in English?'

        return attributes

    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/language-options')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
            attributes[
                'page_title'] = 'Would you like to complete the census in English?'

        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(request.app.router['IndexCY:get'].url_for())

        try:
            language_option = data['language-option']
        except KeyError:
            logger.warn('ni language option error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG_CY)
            return attributes

        if language_option == 'Yes':
            attributes['language'] = 'en'
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))

        elif language_option == 'No':
            raise HTTPFound(
                request.app.router['StartSelectLanguageCY:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn('language selection error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG_CY)
            return attributes


@start_routes.view('/ni/start/language-options')
class StartLanguageOptionsNI(Start):
    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/language-options')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexNI:get'].url_for())

        attributes[
            'page_title'] = 'Would you like to complete the census in English?'

        return attributes

    @aiohttp_jinja2.template('start-ni-language-options.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/language-options')
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
            raise HTTPFound(request.app.router['IndexNI:get'].url_for())

        try:
            language_option = data['language-option']
        except KeyError:
            logger.warn('ni language option error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        if language_option == 'Yes':
            attributes['language'] = 'en'
            await self.call_questionnaire(request, case,
                                          attributes, request.app,
                                          session.get('adlocation'))

        elif language_option == 'No':
            raise HTTPFound(
                request.app.router['StartSelectLanguageNI:get'].url_for())

        else:
            # catch all just in case, should never get here
            logger.warn('language selection error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes


@start_routes.view('/start/select-language')
class StartSelectLanguageEN(Start):
    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/select-language')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexEN:get'].url_for())

        attributes['page_title'] = 'Choose your language'

        return attributes

    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/select-language')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
            attributes['page_title'] = 'Choose your language'

        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexEN:get'].url_for())

        try:
            language_option = data['language-option']
        except KeyError:
            logger.warn('ni language option error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        if language_option == 'gaeilge':
            attributes['language'] = 'ga'

        elif language_option == 'ulster-scotch':
            attributes['language'] = 'eo'

        elif language_option == 'english':
            attributes['language'] = 'en'

        else:
            # catch all just in case, should never get here
            logger.warn('language selection error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        await self.call_questionnaire(request, case, attributes, request.app,
                                      session.get('adlocation'))


@start_routes.view('/dechrau/select-language')
class StartSelectLanguageCY(Start):
    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/select-language')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(request.app.router['IndexCY:get'].url_for())

        attributes['page_title'] = 'Choose your language'

        return attributes

    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/select-language')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
            attributes['page_title'] = 'Choose your language'

        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG_CY)
            raise HTTPFound(request.app.router['IndexCY:get'].url_for())

        try:
            language_option = data['language-option']
        except KeyError:
            logger.warn('ni language option error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG_CY)
            return attributes

        if language_option == 'gaeilge':
            attributes['language'] = 'ga'

        elif language_option == 'ulster-scotch':
            attributes['language'] = 'eo'

        elif language_option == 'english':
            attributes['language'] = 'en'

        else:
            # catch all just in case, should never get here
            logger.warn('language selection error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG_CY)
            return attributes

        await self.call_questionnaire(request, case, attributes, request.app,
                                      session.get('adlocation'))


@start_routes.view('/ni/start/select-language')
class StartSelectLanguageNI(Start):
    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        self.setup_request(request)
        self.log_entry(request, 'start/select-language')
        await check_permission(request)

        session = await get_session(request)
        try:
            attributes = session['attributes']
        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexNI:get'].url_for())

        attributes['page_title'] = 'Choose your language'

        return attributes

    @aiohttp_jinja2.template('start-ni-select-language.html')
    async def post(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/select-language')
        await check_permission(request)
        data = await request.post()

        session = await get_session(request)
        try:
            attributes = session['attributes']
            case = session['case']
            attributes['page_title'] = 'Choose your language'

        except KeyError:
            flash(request, SESSION_TIMEOUT_MSG)
            raise HTTPFound(request.app.router['IndexNI:get'].url_for())

        try:
            language_option = data['language-option']
        except KeyError:
            logger.warn('ni language option error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        if language_option == 'gaeilge':
            attributes['language'] = 'ga'

        elif language_option == 'ulster-scotch':
            attributes['language'] = 'eo'

        elif language_option == 'english':
            attributes['language'] = 'en'

        else:
            # catch all just in case, should never get here
            logger.warn('language selection error',
                        client_ip=request['client_ip'])
            flash(request, START_LANGUAGE_OPTION_MSG)
            return attributes

        await self.call_questionnaire(request, case, attributes, request.app,
                                      session.get('adlocation'))


@start_routes.view('/start/timeout')
class UACTimeout(View):
    @aiohttp_jinja2.template('timeout.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/timeout')
        return {}


@start_routes.view('/start/save-and-exit')
class SaveAndExitEN(View):
    @aiohttp_jinja2.template('save-and-exit.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/save-and-exit')
        await forget(request)
        return {
            'display_region': 'en'
        }


@start_routes.view('/dechrau/cadw-a-gadael')
class SaveAndExitCY(View):
    @aiohttp_jinja2.template('save-and-exit.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/save-and-exit')
        await forget(request)
        return {
            'display_region': 'cy',
            'locale': 'cy'
        }


@start_routes.view('/ni/start/save-and-exit')
class SaveAndExitNI(View):
    @aiohttp_jinja2.template('save-and-exit.html')
    async def get(self, request):
        self.setup_request(request)
        self.log_entry(request, 'start/save-and-exit')
        await forget(request)
        return {
            'display_region': 'ni'
        }
