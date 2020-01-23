import asyncio
import functools
import json
import time
import uuid

from aiohttp.test_utils import AioHTTPTestCase

from app import app

from app import session
from aiohttp_session import session_middleware
from aiohttp_session import SimpleCookieStorage


def skip_build_eq(func, *args, **kwargs):
    """
    Helper decorator for manually patching the methods of app.eq.EqPayloadConstructor.

    This can be useful for tests that perform as a client but wish the server to skip the builder functionality.

    The test case checks for and calls when possible .setUp and .tearDown attributes on each test method
    at server setUp (setUpAsync) and server tearDown (tearDownAsync).

    :param func: test method that requires the patch
    :param args: the test method's arguments
    :param args: the test method's keyword arguments
    :return: new method with patching functions attached as attributes
    """
    async def _override_eq_payload_constructor(test_case, *_):
        from app import eq

        async def build(_):
            return test_case.eq_payload

        eq.EqPayloadConstructor._bk__init__ = eq.EqPayloadConstructor.__init__
        eq.EqPayloadConstructor.__init__ = lambda *args: None
        eq.EqPayloadConstructor._bk_build = eq.EqPayloadConstructor.build
        eq.EqPayloadConstructor.build = build

    async def _reset_eq_payload_constructor(*_):
        from app import eq

        eq.EqPayloadConstructor.__init__ = eq.EqPayloadConstructor._bk__init__
        eq.EqPayloadConstructor.build = eq.EqPayloadConstructor._bk_build

    @functools.wraps(func, *args, **kwargs)
    def new_func(self, *inner_args, **inner_kwargs):
        return func(self, *inner_args, **inner_kwargs)

    new_func.setUp = _override_eq_payload_constructor
    new_func.tearDown = _reset_eq_payload_constructor

    return new_func


def build_eq_raises(func, *args, **kwargs):
    """
    Helper decorator for manually patching the methods of app.eq.EqPayloadConstructor.

    This can be useful for tests that perform as a client but wish the server to raise InvalidEqPayLoad when .build()
    is called on an instance of app.eq.EqPayloadConstructor.

    The test case checks for and calls when possible .setUp and .tearDown attributes on each test method
    at server setUp (setUpAsync) and server tearDown (tearDownAsync).

    :param func: test method that requires the patch
    :param args: the test method's arguments
    :param args: the test method's keyword arguments
    :return: new method with patching functions attached as attributes
    """
    async def _override_eq_build_with_error(*_):
        from app import eq

        async def build(_):
            raise eq.InvalidEqPayLoad('')

        eq.EqPayloadConstructor._bk__init__ = eq.EqPayloadConstructor.__init__
        eq.EqPayloadConstructor.__init__ = lambda *args: None
        eq.EqPayloadConstructor._bk_build = eq.EqPayloadConstructor.build
        eq.EqPayloadConstructor.build = build

    async def _reset_eq_payload_constructor(*_):
        from app import eq

        eq.EqPayloadConstructor.__init__ = eq.EqPayloadConstructor._bk__init__
        eq.EqPayloadConstructor.build = eq.EqPayloadConstructor._bk_build

    @functools.wraps(func, *args, **kwargs)
    def new_func(self, *inner_args, **inner_kwargs):
        return func(self, *inner_args, **inner_kwargs)

    new_func.setUp = _override_eq_build_with_error
    new_func.tearDown = _reset_eq_payload_constructor

    return new_func


def skip_encrypt(func, *args, **kwargs):
    """
    Helper decorator for manually patching the encrypt function in start_handlers.py.

    This can be useful for tests that perform as a client but wish the server to skip encrypting a payload.

    The test case checks for and calls when possible .setUp and .tearDown attributes on each test method
    at server setUp (setUpAsync) and server tearDown (tearDownAsync).

    :param func: test method that requires the patch
    :param args: the test method's arguments
    :param args: the test method's keyword arguments
    :return: new method with patching functions attached as attributes
    """
    async def _override_sdc_encrypt(*_):
        from app import start_handlers

        def encrypt(payload, **_):
            return json.dumps(payload)

        start_handlers._bk_encrypt = start_handlers.encrypt
        start_handlers.encrypt = encrypt

    async def _reset_sdc_encrypt(*_):
        from app import start_handlers

        start_handlers.encrypt = start_handlers._bk_encrypt

    @functools.wraps(func, *args, **kwargs)
    def new_func(self, *inner_args, **inner_kwargs):
        return func(self, *inner_args, **inner_kwargs)

    new_func.setUp = _override_sdc_encrypt
    new_func.tearDown = _reset_sdc_encrypt

    return new_func


class RHTestCase(AioHTTPTestCase):

    language_code = 'en'
    response_id = '2vfBHlIsGPImYlWTvXLiBeXw14NkzoicZcDJB8pZ9FQ='

    start_date = '2018-04-10'
    end_date = '2020-05-31'
    return_by = '2018-05-08'

    def session_storage(self, app_config):
        self.assertIn('REDIS_SERVER', app_config)
        self.assertIn('REDIS_PORT', app_config)
        self.assertIn('SESSION_AGE', app_config)
        return session_middleware(
            SimpleCookieStorage(cookie_name='RH_SESSION'))

    async def get_application(self):
        # Monkey patch the session setup function to remove Redis dependency for unit tests
        session.setup = self.session_storage
        return app.create_app('TestingConfig')

    async def setUpAsync(self):
        test_method = getattr(self, self._testMethodName)
        if hasattr(test_method, 'setUp'):
            await test_method.setUp(self)

    async def tearDownAsync(self):
        test_method = getattr(self, self._testMethodName)
        if hasattr(test_method, 'tearDown'):
            await test_method.tearDown(self)

    def assertLogJson(self, watcher, event, **kwargs):
        """
        Helper method for asserting the contents of structlog records caught by self.assertLogs.

        Fails if no match is found. A match is based on the main log message (event) and all additional
        items passed in kwargs.

        :param watcher: context manager returned by `with self.assertLogs(LOGGER, LEVEL)`
        :param event: event logged; use empty string to ignore or no message
        :param kwargs: other structlog key value pairs to assert for
        """
        for record in watcher.records:
            message_json = json.loads(record.message)
            try:
                if (event in message_json.get('event', '')
                        and all(message_json[key] == val
                                for key, val in kwargs.items())):
                    break
            except KeyError:
                pass
        else:
            self.fail(f'No matching log records present: {event}')

    def assertLogEvent(self, watcher, event, **kwargs):
        """
        Helper method for asserting the contents of RH records caught by self.assertLogs.

        Fails if no match is found. A match is based on the static message string (event) and all additional
        items passed in kwargs.

        :param watcher: context manager returned by `with self.assertLogs(LOGGER, LEVEL)`
        :param event: event logged; use empty string to ignore or no message
        :param kwargs: other structlog key value pairs to assert for
        """
        for record in watcher.records:
            try:
                if (event in record.message
                        and all(record.__dict__[key] == val
                                for key, val in kwargs.items())):
                    break
            except KeyError:
                pass
        else:
            self.fail(
                f"No matching log records with event: '{event}' and parameters: {kwargs}"
            )

    def assertMessagePanel(self, message, content):
        """
        Helper method for asserting the rendered content includes the required message panels.

        :param message: message dict
        :param content: rendered HTML str
        """
        if message.get('clickable', False):
            self.assertIn('js-inpagelink', content)

        for message_line in message['text'].split('\n'):
            self.assertIn(message_line, content)

        level = message['level'].lower()
        self.assertIn(f'panel--{level}', content)

    def setUp(self):
        # This section gets ugly if YAPF reformats it
        # yapf: disable
        super().setUp()  # NB: setUp the server first so we can use self.app
        with open('tests/test_data/rhsvc/uac.json') as fp:
            self.uac_json = json.load(fp)

        with open('tests/test_data/rhsvc/uac-cy.json') as fp:
            self.uac_json_cy = json.load(fp)

        with open('tests/test_data/rhsvc/uac-ni.json') as fp:
            self.uac_json_ni = json.load(fp)

        # URLs used in later statements
        url_path_prefix = self.app['URL_PATH_PREFIX']
        account_svc_url = self.app['ACCOUNT_SERVICE_URL']
        rh_svc_url = self.app['RHSVC_URL']
        address_index_svc_url = self.app['ADDRESS_INDEX_SVC_URL']

        self.get_info = self.app.router['Info:get'].url_for()

        self.get_start_adlocation_valid_en = self.app.router['IndexEN:get'].url_for().with_query(
            {"adlocation": "1234567890"})
        self.get_start_adlocation_invalid_en = self.app.router['IndexEN:get'].url_for().with_query(
            {"adlocation": "invalid"})
        self.get_start_adlocation_valid_cy = self.app.router['IndexCY:get'].url_for().with_query(
            {"adlocation": "1234567890"})
        self.get_start_adlocation_invalid_cy = self.app.router['IndexCY:get'].url_for().with_query(
            {"adlocation": "invalid"})
        self.get_start_adlocation_valid_ni = self.app.router['IndexNI:get'].url_for().with_query(
            {"adlocation": "1234567890"})
        self.get_start_adlocation_invalid_ni = self.app.router['IndexNI:get'].url_for().with_query(
            {"adlocation": "invalid"})

        self.get_index_en = self.app.router['IndexEN:get'].url_for()
        self.post_index_en = self.app.router['IndexEN:post'].url_for()
        self.get_address_confirmation_en = self.app.router['AddressConfirmationEN:get'].url_for()
        self.post_address_confirmation_en = self.app.router['AddressConfirmationEN:post'].url_for()
        self.get_address_edit_en = self.app.router['AddressEditEN:get'].url_for()
        self.post_address_edit_en = self.app.router['AddressEditEN:post'].url_for()
        self.get_language_options_en = self.app.router['StartLanguageOptionsEN:get'].url_for()
        self.post_language_options_en = self.app.router['StartLanguageOptionsEN:post'].url_for()
        self.get_select_language_en = self.app.router['StartSelectLanguageEN:get'].url_for()
        self.post_select_language_en = self.app.router['StartSelectLanguageEN:post'].url_for()

        self.get_index_cy = self.app.router['IndexCY:get'].url_for()
        self.post_index_cy = self.app.router['IndexCY:post'].url_for()
        self.get_address_confirmation_cy = self.app.router['AddressConfirmationCY:get'].url_for()
        self.post_address_confirmation_cy = self.app.router['AddressConfirmationCY:post'].url_for()
        self.get_address_edit_cy = self.app.router['AddressEditCY:get'].url_for()
        self.post_address_edit_cy = self.app.router['AddressEditCY:post'].url_for()
        self.get_language_options_cy = self.app.router['StartLanguageOptionsCY:get'].url_for()
        self.post_language_options_cy = self.app.router['StartLanguageOptionsCY:post'].url_for()
        self.get_select_language_cy = self.app.router['StartSelectLanguageCY:get'].url_for()
        self.post_select_language_cy = self.app.router['StartSelectLanguageCY:post'].url_for()

        self.get_index_ni = self.app.router['IndexNI:get'].url_for()
        self.post_index_ni = self.app.router['IndexNI:post'].url_for()
        self.get_address_confirmation_ni = self.app.router['AddressConfirmationNI:get'].url_for()
        self.post_address_confirmation_ni = self.app.router['AddressConfirmationNI:post'].url_for()
        self.get_address_edit_ni = self.app.router['AddressEditNI:get'].url_for()
        self.post_address_edit_ni = self.app.router['AddressEditNI:post'].url_for()
        self.get_language_options_ni = self.app.router['StartLanguageOptionsNI:get'].url_for()
        self.post_language_options_ni = self.app.router['StartLanguageOptionsNI:post'].url_for()
        self.get_select_language_ni = self.app.router['StartSelectLanguageNI:get'].url_for()
        self.post_select_language_ni = self.app.router['StartSelectLanguageNI:post'].url_for()

        self.case_id = self.uac_json['caseId']
        self.collection_exercise_id = self.uac_json['collectionExerciseId']
        self.eq_id = 'census'
        self.survey = 'CENSUS'
        self.form_type = 'individual_gb_eng'
        self.jti = str(uuid.uuid4())
        self.uac_code = ''.join([str(n) for n in range(13)])
        self.uac1, self.uac2, self.uac3, self.uac4 = self.uac_code[:4], self.uac_code[4:8], self.uac_code[8:12], self.uac_code[12:]
        self.period_id = '2019'
        self.uac = 'w4nwwpphjjptp7fn'
        self.uacHash = self.uac_json['uacHash']
        self.uprn = self.uac_json['address']['uprn']
        self.response_id = self.uac_json['questionnaireId']
        self.questionnaire_id = self.uac_json['questionnaireId']
        self.case_type = self.uac_json['caseType']
        self.channel = 'rh'
        self.attributes_en = {
            'addressLine1': self.uac_json['address']['addressLine1'],
            'addressLine2': self.uac_json['address']['addressLine2'],
            'addressLine3': self.uac_json['address']['addressLine3'],
            'townName': self.uac_json['address']['townName'],
            'postcode': self.uac_json['address']['postcode'],
            'uprn': self.uac_json['address']['uprn'],
            'language': 'en',
            'display_region': 'en'
        }
        self.attributes_cy = {
            **self.attributes_en,
            'language': 'cy',
            'display_region': 'cy',
            'locale': 'cy'
        }
        self.attributes_ni = {
            **self.attributes_en,
            'language': 'ul',
            'display_region': 'ni'
        }

        self.eq_payload = {
            'jti': self.jti,
            'tx_id': self.jti,
            'iat': int(time.time()),
            'exp': int(time.time() + (5 * 60)),
            'case_type': self.case_type,
            'collection_exercise_sid': self.collection_exercise_id,
            'region_code': 'GB-ENG',
            'ru_ref': self.uprn,
            'case_id': self.case_id,
            'language_code': 'en',
            'display_address': self.uac_json['address']['addressLine1'] + ', ' + self.uac_json['address']['addressLine2'],
            'response_id': self.response_id,
            'account_service_url': f'{account_svc_url}{url_path_prefix}/start/',
            'account_service_log_out_url': f'{account_svc_url}{url_path_prefix}/start/save-and-exit',
            'channel': self.channel,
            'user_id': '',
            'questionnaire_id': self.questionnaire_id,
            'eq_id': self.eq_id,
            'period_id': self.period_id,
            'form_type': self.form_type,
            'survey': self.survey
        }

        self.account_service_url_en = '/start/'
        self.account_service_url_cy = '/dechrau/'
        self.account_service_url_ni = '/ni/start/'
        self.account_service_log_out_url_en = '/start/save-and-exit'
        self.account_service_log_out_url_cy = '/dechrau/cadw-a-gadael'
        self.account_service_log_out_url_ni = '/ni/start/save-and-exit'

        self.survey_launched_json = {
            'questionnaireId': self.questionnaire_id,
            'caseId': self.case_id,
            'agentId': ''
        }

        self.survey_launched_json = {
            'questionnaireId': self.questionnaire_id,
            'caseId': self.case_id,
            'agentId': ''
        }

        self.rhsvc_url = (
            f'{rh_svc_url}/uacs/{self.uacHash}'
        )

        self.rhsvc_url_surveylaunched = (
            f'{rh_svc_url}/surveyLaunched'
        )

        self.rhsvc_url_fulfilments = (
            f'{rh_svc_url}/fulfilments'
        )

        self.rhsvc_cases_by_uprn_url = (
            f'{rh_svc_url}/cases/uprn/'
        )

        self.rhsvc_cases_url = (
            f'{rh_svc_url}/cases/'
        )

        self.form_data = {
            'uac': self.uac, 'action[save_continue]': '',
        }

        self.post_start_form_data_with_adlocation = {
            'uac': self.uac, 'adlocation': '1234567890', 'action[save_continue]': '',
        }

        self.address_confirmation_data = {
            'address-check-answer': 'Yes', 'action[save_continue]': ''
        }

        self.address_confirmation_data_edit = {
            'address-check-answer': 'No', 'action[save_continue]': ''
        }

        self.address_edit_data = {
            'address-line-1': 'ONS',
            'address-line-2': 'Segensworth Road',
            'address-line-3': 'Titchfield',
            'address-town': 'Fareham',
            'address-postcode': 'PO15 5RR'
        }

        self.modify_address_data = {
            'caseId': self.case_id,
            'uprn': self.uprn,
            'addressLine1': self.uac_json['address']['addressLine1'],
            'addressLine2': self.uac_json['address']['addressLine2'],
            'addressLine3': self.uac_json['address']['addressLine3'],
            'townName': self.uac_json['address']['townName'],
            'postcode': self.uac_json['address']['postcode']
            }

        self.language_options_ni_eng_data = {
            'language-option': 'Yes', 'action[save_continue]': ''
        }

        self.language_options_ni_not_eng_data = {
            'language-option': 'No', 'action[save_continue]': ''
        }

        self.select_language_ni_ul_data = {
            'language-option': 'ulster-scotch', 'action[save_continue]': ''
        }

        self.select_language_ni_ga_data = {
            'language-option': 'gaeilge', 'action[save_continue]': ''
        }

        self.select_language_ni_en_data = {
            'language-option': 'english', 'action[save_continue]': ''
        }

        self.get_webchat_en = self.app.router['WebChatEN:get'].url_for()
        self.get_webchat_cy = self.app.router['WebChatCY:get'].url_for()
        self.get_webchat_ni = self.app.router['WebChatNI:get'].url_for()
        self.post_webchat_en = self.app.router['WebChatEN:post'].url_for()
        self.post_webchat_cy = self.app.router['WebChatCY:post'].url_for()
        self.post_webchat_ni = self.app.router['WebChatNI:post'].url_for()
        self.get_webchat_chat_en = self.app.router['WebChatWindowEN:get'].url_for()
        self.get_webchat_chat_cy = self.app.router['WebChatWindowCY:get'].url_for()
        self.get_webchat_chat_ni = self.app.router['WebChatWindowNI:get'].url_for()

        self.webchat_form_data = {
            'screen_name': 'Test',
            'email': 'test@test.gov.uk',
            'language': 'english',
            'query': 'help',
            'country': 'england'
        }

        self.webchat_form_data_cy = {
            **self.webchat_form_data,
            'language': 'welsh',
            'country': 'wales',
        }

        self.webchatsvc_url = self.app['WEBCHAT_SVC_URL']

        self.addressindexsvc_url = f'{address_index_svc_url}/addresses/postcode/'

        self.get_requestcode_household_en = self.app.router['RequestCodeHouseholdEN:get'].url_for()
        self.get_requestcode_household_cy = self.app.router['RequestCodeHouseholdCY:get'].url_for()
        self.get_requestcode_household_ni = self.app.router['RequestCodeHouseholdNI:get'].url_for()
        self.get_requestcode_enter_address_hh_en = self.app.router['RequestCodeEnterAddressHHEN:get'].url_for()
        self.get_requestcode_enter_address_hh_cy = self.app.router['RequestCodeEnterAddressHHCY:get'].url_for()
        self.get_requestcode_enter_address_hh_ni = self.app.router['RequestCodeEnterAddressHHNI:get'].url_for()
        self.post_requestcode_enter_address_hh_en = self.app.router['RequestCodeEnterAddressHHEN:post'].url_for()
        self.post_requestcode_enter_address_hh_cy = self.app.router['RequestCodeEnterAddressHHCY:post'].url_for()
        self.post_requestcode_enter_address_hh_ni = self.app.router['RequestCodeEnterAddressHHNI:post'].url_for()
        self.get_requestcode_selectaddress_hh_en = self.app.router['RequestCodeSelectAddressHHEN:get'].url_for()
        self.get_requestcode_selectaddress_hh_cy = self.app.router['RequestCodeSelectAddressHHCY:get'].url_for()
        self.get_requestcode_selectaddress_hh_ni = self.app.router['RequestCodeSelectAddressHHNI:get'].url_for()
        self.post_requestcode_selectaddress_hh_en = self.app.router['RequestCodeSelectAddressHHEN:post'].url_for()
        self.post_requestcode_selectaddress_hh_cy = self.app.router['RequestCodeSelectAddressHHCY:post'].url_for()
        self.post_requestcode_selectaddress_hh_ni = self.app.router['RequestCodeSelectAddressHHNI:post'].url_for()
        self.get_requestcode_address_confirmation_hh_en = self.app.router['RequestCodeConfirmAddressHHEN:get'].url_for()
        self.get_requestcode_address_confirmation_hh_cy = self.app.router['RequestCodeConfirmAddressHHCY:get'].url_for()
        self.get_requestcode_address_confirmation_hh_ni = self.app.router['RequestCodeConfirmAddressHHNI:get'].url_for()
        self.post_requestcode_address_confirmation_hh_en = self.app.router['RequestCodeConfirmAddressHHEN:post'].url_for()
        self.post_requestcode_address_confirmation_hh_cy = self.app.router['RequestCodeConfirmAddressHHCY:post'].url_for()
        self.post_requestcode_address_confirmation_hh_ni = self.app.router['RequestCodeConfirmAddressHHNI:post'].url_for()

        self.get_requestcode_individual_en = self.app.router['RequestCodeIndividualEN:get'].url_for()
        self.get_requestcode_individual_cy = self.app.router['RequestCodeIndividualCY:get'].url_for()
        self.get_requestcode_individual_ni = self.app.router['RequestCodeIndividualNI:get'].url_for()
        self.get_requestcode_enter_address_hi_en = self.app.router['RequestCodeEnterAddressHIEN:get'].url_for()
        self.get_requestcode_enter_address_hi_cy = self.app.router['RequestCodeEnterAddressHICY:get'].url_for()
        self.get_requestcode_enter_address_hi_ni = self.app.router['RequestCodeEnterAddressHINI:get'].url_for()
        self.post_requestcode_enter_address_hi_en = self.app.router['RequestCodeEnterAddressHIEN:post'].url_for()
        self.post_requestcode_enter_address_hi_cy = self.app.router['RequestCodeEnterAddressHICY:post'].url_for()
        self.post_requestcode_enter_address_hi_ni = self.app.router['RequestCodeEnterAddressHINI:post'].url_for()
        self.get_requestcode_selectaddress_hi_en = self.app.router['RequestCodeSelectAddressHIEN:get'].url_for()
        self.get_requestcode_selectaddress_hi_cy = self.app.router['RequestCodeSelectAddressHICY:get'].url_for()
        self.get_requestcode_selectaddress_hi_ni = self.app.router['RequestCodeSelectAddressHINI:get'].url_for()
        self.post_requestcode_selectaddress_hi_en = self.app.router['RequestCodeSelectAddressHIEN:post'].url_for()
        self.post_requestcode_selectaddress_hi_cy = self.app.router['RequestCodeSelectAddressHICY:post'].url_for()
        self.post_requestcode_selectaddress_hi_ni = self.app.router['RequestCodeSelectAddressHINI:post'].url_for()
        self.get_requestcode_address_confirmation_hi_en = self.app.router['RequestCodeConfirmAddressHIEN:get'].url_for()
        self.get_requestcode_address_confirmation_hi_cy = self.app.router['RequestCodeConfirmAddressHICY:get'].url_for()
        self.get_requestcode_address_confirmation_hi_ni = self.app.router['RequestCodeConfirmAddressHINI:get'].url_for()
        self.post_requestcode_address_confirmation_hi_en = self.app.router['RequestCodeConfirmAddressHIEN:post'].url_for()
        self.post_requestcode_address_confirmation_hi_cy = self.app.router['RequestCodeConfirmAddressHICY:post'].url_for()
        self.post_requestcode_address_confirmation_hi_ni = self.app.router['RequestCodeConfirmAddressHINI:post'].url_for()

        self.get_requestcode_entermobile_hh_en = self.app.router['RequestCodeEnterMobileHHEN:get'].url_for()
        self.get_requestcode_entermobile_hh_cy = self.app.router['RequestCodeEnterMobileHHCY:get'].url_for()
        self.get_requestcode_entermobile_hh_ni = self.app.router['RequestCodeEnterMobileHHNI:get'].url_for()
        self.get_requestcode_entermobile_hi_en = self.app.router['RequestCodeEnterMobileHIEN:get'].url_for()
        self.get_requestcode_entermobile_hi_cy = self.app.router['RequestCodeEnterMobileHICY:get'].url_for()
        self.get_requestcode_entermobile_hi_ni = self.app.router['RequestCodeEnterMobileHINI:get'].url_for()
        self.post_requestcode_entermobile_hh_en = self.app.router['RequestCodeEnterMobileHHEN:post'].url_for()
        self.post_requestcode_entermobile_hh_cy = self.app.router['RequestCodeEnterMobileHHCY:post'].url_for()
        self.post_requestcode_entermobile_hh_ni = self.app.router['RequestCodeEnterMobileHHNI:post'].url_for()
        self.post_requestcode_entermobile_hi_en = self.app.router['RequestCodeEnterMobileHIEN:post'].url_for()
        self.post_requestcode_entermobile_hi_cy = self.app.router['RequestCodeEnterMobileHICY:post'].url_for()
        self.post_requestcode_entermobile_hi_ni = self.app.router['RequestCodeEnterMobileHINI:post'].url_for()

        self.get_requestcode_confirm_mobile_hh_en = self.app.router['RequestCodeConfirmMobileHHEN:get'].url_for()
        self.get_requestcode_confirm_mobile_hh_cy = self.app.router['RequestCodeConfirmMobileHHCY:get'].url_for()
        self.get_requestcode_confirm_mobile_hh_ni = self.app.router['RequestCodeConfirmMobileHHNI:get'].url_for()
        self.get_requestcode_confirm_mobile_hi_en = self.app.router['RequestCodeConfirmMobileHIEN:get'].url_for()
        self.get_requestcode_confirm_mobile_hi_cy = self.app.router['RequestCodeConfirmMobileHICY:get'].url_for()
        self.get_requestcode_confirm_mobile_hi_ni = self.app.router['RequestCodeConfirmMobileHINI:get'].url_for()
        self.post_requestcode_confirm_mobile_hh_en = self.app.router['RequestCodeConfirmMobileHHEN:post'].url_for()
        self.post_requestcode_confirm_mobile_hh_cy = self.app.router['RequestCodeConfirmMobileHHCY:post'].url_for()
        self.post_requestcode_confirm_mobile_hh_ni = self.app.router['RequestCodeConfirmMobileHHNI:post'].url_for()
        self.post_requestcode_confirm_mobile_hi_en = self.app.router['RequestCodeConfirmMobileHIEN:post'].url_for()
        self.post_requestcode_confirm_mobile_hi_cy = self.app.router['RequestCodeConfirmMobileHICY:post'].url_for()
        self.post_requestcode_confirm_mobile_hi_ni = self.app.router['RequestCodeConfirmMobileHINI:post'].url_for()

        self.get_requestcode_notrequired_hh_en = self.app.router['RequestCodeNotRequiredHHEN:get'].url_for()
        self.get_requestcode_notrequired_hh_cy = self.app.router['RequestCodeNotRequiredHHCY:get'].url_for()
        self.get_requestcode_notrequired_hh_ni = self.app.router['RequestCodeNotRequiredHHNI:get'].url_for()
        self.get_requestcode_notrequired_hi_en = self.app.router['RequestCodeNotRequiredHIEN:get'].url_for()
        self.get_requestcode_notrequired_hi_cy = self.app.router['RequestCodeNotRequiredHICY:get'].url_for()
        self.get_requestcode_notrequired_hi_ni = self.app.router['RequestCodeNotRequiredHINI:get'].url_for()

        self.get_requestcode_codesent_hh_en = self.app.router['RequestCodeCodeSentHHEN:get'].url_for()
        self.get_requestcode_codesent_hh_cy = self.app.router['RequestCodeCodeSentHHCY:get'].url_for()
        self.get_requestcode_codesent_hh_ni = self.app.router['RequestCodeCodeSentHHNI:get'].url_for()
        self.get_requestcode_codesent_hi_en = self.app.router['RequestCodeCodeSentHIEN:get'].url_for()
        self.get_requestcode_codesent_hi_cy = self.app.router['RequestCodeCodeSentHICY:get'].url_for()
        self.get_requestcode_codesent_hi_ni = self.app.router['RequestCodeCodeSentHINI:get'].url_for()

        self.get_requestcode_household_timeout_en = self.app.router['RequestCodeTimeoutHHEN:get'].url_for()
        self.get_requestcode_household_timeout_cy = self.app.router['RequestCodeTimeoutHHCY:get'].url_for()
        self.get_requestcode_household_timeout_ni = self.app.router['RequestCodeTimeoutHHNI:get'].url_for()
        self.get_requestcode_individual_timeout_en = self.app.router['RequestCodeTimeoutHIEN:get'].url_for()
        self.get_requestcode_individual_timeout_cy = self.app.router['RequestCodeTimeoutHICY:get'].url_for()
        self.get_requestcode_individual_timeout_ni = self.app.router['RequestCodeTimeoutHINI:get'].url_for()

        self.get_accessibility_statement_en = self.app.router['AccessibilityEN:get'].url_for()
        self.get_accessibility_statement_cy = self.app.router['AccessibilityCY:get'].url_for()
        self.get_accessibility_statement_ni = self.app.router['AccessibilityNI:get'].url_for()

        self.get_start_saveandexit_en = self.app.router['SaveAndExitEN:get'].url_for()
        self.get_start_saveandexit_cy = self.app.router['SaveAndExitCY:get'].url_for()
        self.get_start_saveandexit_ni = self.app.router['SaveAndExitNI:get'].url_for()

        self.postcode_valid = 'EX2 6GA'
        self.postcode_invalid = 'ZZ99 9ZZ'
        self.postcode_no_results = 'GU34 5DU'

        self.post_requestcode_select_address_form_data_valid = \
            '{"uprn": "10023122451", "address": "1 Gate Reach, Exeter, EX2 6GA"}'

        self.selected_uprn = '10023122451'

        self.mobile_valid = '07012345678'
        self.mobile_invalid_short = '07012'
        self.mobile_invalid_long = '0701234567890123456'
        self.mobile_invalid_character = '0701234567$'

        self.field_empty = None

        with open('tests/test_data/address_index/postcode_no_results.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_postcode_no_results = f

        with open('tests/test_data/address_index/postcode_results.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_postcode_results = f

        with open('tests/test_data/rhsvc/case_by_uprn_en.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_cases_by_uprn_en = f

        with open('tests/test_data/rhsvc/case_by_uprn_cy.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_cases_by_uprn_cy = f

        with open('tests/test_data/rhsvc/case_by_uprn_ni.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_cases_by_uprn_ni = f

        with open('tests/test_data/rhsvc/get_fulfilment_multi.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_multi = f

        with open('tests/test_data/rhsvc/get_fulfilment_single.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_single = f

        with open('tests/test_data/rhsvc/request_fulfilment.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_request_fulfilment = f

        self.request_code_form_data_valid = {
            'request-postcode': self.postcode_valid, 'action[save_continue]': '',
        }

        self.request_code_form_data_no_results = {
            'request-postcode': self.postcode_no_results, 'action[save_continue]': '',
        }

        self.request_code_form_data_invalid = {
            'request-postcode': self.postcode_invalid, 'action[save_continue]': '',
        }

        self.request_code_address_confirmation_data_yes = {
            'request-address-confirmation': 'yes', 'action[save_continue]': ''
        }

        self.request_code_address_confirmation_data_no = {
            'request-address-confirmation': 'no', 'action[save_continue]': ''
        }

        self.request_code_address_confirmation_data_invalid = {
            'request-address-confirmation': 'invalid', 'action[save_continue]': ''
        }

        self.request_code_select_address_form_data_empty = {}

        self.request_code_confirm_address_form_data_empty = {}

        self.request_code_select_address_form_data_valid = {
            'request-address-select': self.post_requestcode_select_address_form_data_valid,
            'action[save_continue]': '',
        }

        self.request_code_enter_mobile_form_data_valid = {
            'request-mobile-number': self.mobile_valid, 'action[save_continue]': '',
        }

        self.request_code_enter_mobile_form_data_invalid = {
            'request-mobile-number': self.mobile_invalid_short, 'action[save_continue]': '',
        }

        self.request_code_mobile_confirmation_data_yes = {
            'request-mobile-confirmation': 'yes', 'action[save_continue]': ''
        }

        self.request_code_mobile_confirmation_data_no = {
            'request-mobile-confirmation': 'no', 'action[save_continue]': ''
        }

        self.request_code_mobile_confirmation_data_invalid = {
            'request-mobile-confirmation': 'invalid', 'action[save_continue]': ''
        }

        self.request_code_mobile_confirmation_data_empty = {}

        self.ons_logo_en = '/img/ons-logo-pos-en.svg'
        self.ons_logo_cy = '/img/ons-logo-pos-cy.svg'
        self.nisra_logo = '/img/nisra-logo-en.svg'

        self.content_request_household_title_en = 'Request a new access code'
        self.content_request_household_title_cy = 'Gofyn am god mynediad newydd'
        self.content_request_individual_title_en = 'Request an individual access code'
        self.content_request_individual_title_cy = 'Gofyn am god mynediad unigryw'
        self.content_request_secondary_en = 'You will need to provide:'
        self.content_request_secondary_cy = 'Bydd angen i chi ddarparu:'

        self.content_request_enter_address_title_en = 'What is your postcode?'
        self.content_request_enter_address_error_en = 'Enter a valid UK postcode to continue'
        self.content_request_enter_address_secondary_en = \
            'To text you a new code we need to know the address for which you are answering.'
        self.content_request_enter_address_title_cy = 'Beth yw eich cod post?'
        self.content_request_enter_address_error_cy = 'Nodwch god post dilys yn y Deyrnas Unedig i barhau'
        self.content_request_enter_address_secondary_cy = \
            "Er mwyn i ni anfon cod newydd atoch chi, mae angen i ni wybod ar gyfer pa gyfeiriad rydych chi\\\'n ateb."

        self.content_request_select_address_title_en = 'Select your address'
        self.content_request_select_address_error_en = 'Select an address'
        self.content_request_select_address_value_en = '1 Gate Reach'
        self.content_request_select_address_no_results_en = 'We cannot find your address'
        self.content_request_select_address_title_cy = 'Dewiswch eich cyfeiriad'
        self.content_request_select_address_error_cy = 'Dewiswch gyfeiriad'
        self.content_request_select_address_value_cy = '1 Gate Reach'
        self.content_request_select_address_no_results_cy = 'Allwn ni ddim dod o hyd'

        self.content_request_confirm_address_title_en = 'Is this address correct?'
        self.content_request_confirm_address_error_en = 'Check and confirm the address'
        self.content_request_confirm_address_value_en = '1 Gate Reach, Exeter, EX2 6GA'
        self.content_request_confirm_address_title_cy = "Ydy\\\'r cyfeiriad hwn yn gywir?"
        self.content_request_confirm_address_error_cy = "Edrychwch eto ar y cyfeiriad a\\\'i gadarnhau"
        self.content_request_confirm_address_value_cy = '1 Gate Reach, Exeter, EX2 6GA'

        self.content_request_enter_mobile_title_en = 'What is your mobile phone number?'
        self.content_request_enter_mobile_error_en = ''
        self.content_request_enter_mobile_secondary_en = 'We will send an access code by text to this number.'
        self.content_request_enter_mobile_title_cy = 'Beth yw eich rhif ff\\xc3\\xb4n symudol?'
        self.content_request_enter_mobile_error_cy = ""
        self.content_request_enter_mobile_secondary_cy = "Byddwn ni\\\'n anfon cod mynediad drwy neges destun i\\\'r rhif hwn."

        self.content_request_confirm_mobile_title_en = 'Is this mobile phone number correct?'
        self.content_request_confirm_mobile_error_en = 'Check and confirm your mobile phone number'
        self.content_request_confirm_mobile_title_cy = "Ydy\\\'r rhif ff\\xc3\\xb4n symudol hwn yn gywir?"
        self.content_request_confirm_mobile_error_cy = "Edrychwch eto ar eich rhif ff\\xc3\\xb4n symudol a\\\'i gadarnhau"

        self.content_request_code_sent_title_en = 'We have sent an access code'
        self.content_request_code_sent_title_cy = 'Rydym ni wedi anfon cod mynediad'

        self.content_500_error_en = 'Sorry, something went wrong'
        self.content_500_error_cy = "Mae\\'n flin gennym, aeth rhywbeth o\\'i le"

        self.content_timeout_en = 'Your session has timed out due to inactivity'
        self.content_timeout_cy = 'Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch'

        self.content_request_not_required_en = 'Your address is not part of the 2019 rehearsal'
        self.content_request_not_required_cy = 'Nid yw eich cyfeiriad yn rhan o ymarfer 2019'

        self.content_start_title_en = 'Start Census'
        self.content_start_uac_title_en = 'Enter the 16 character code printed on the letter'
        self.content_start_title_cy = "Dechrau'r Cyfrifiad"
        self.content_start_uac_title_cy = "Rhowch y cod 16 nod sydd wedi'i argraffu ar y llythyr"

        self.content_start_confirm_address_title_en = 'Is this address correct?'
        self.content_start_confirm_address_title_cy = "Ydy'r cyfeiriad hwn yn gywir?"

        # yapf: enable
