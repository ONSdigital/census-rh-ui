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
    Helper decorator for manually patching the encrypt function in handlers.py.

    This can be useful for tests that perform as a client but wish the server to skip encrypting a payload.

    The test case checks for and calls when possible .setUp and .tearDown attributes on each test method
    at server setUp (setUpAsync) and server tearDown (tearDownAsync).

    :param func: test method that requires the patch
    :param args: the test method's arguments
    :param args: the test method's keyword arguments
    :return: new method with patching functions attached as attributes
    """

    async def _override_sdc_encrypt(*_):
        from app import handlers

        def encrypt(payload, **_):
            return json.dumps(payload)

        handlers._bk_encrypt = handlers.encrypt
        handlers.encrypt = encrypt

    async def _reset_sdc_encrypt(*_):
        from app import handlers

        handlers.encrypt = handlers._bk_encrypt

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
        self.assertIn("REDIS_SERVER", app_config)
        self.assertIn("REDIS_PORT", app_config)
        self.assertIn("SESSION_AGE", app_config)
        return session_middleware(SimpleCookieStorage(cookie_name='RH_SESSION'))

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

    def assertLogLine(self, watcher, event, **kwargs):
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
                if (
                    event in message_json.get('event', '')
                    and all(message_json[key] == val for key, val in kwargs.items())
                ):
                    break
            except KeyError:
                pass
        else:
            self.fail(f'No matching log records present: {event}')

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

        self.assertIn(f'panel--{message["level"].lower()}', content)

    def setUp(self):
        super().setUp()  # NB: setUp the server first so we can use self.app
        with open('tests/test_data/rhsvc/uac.json') as fp:
            self.uac_json = json.load(fp)

        with open('tests/test_data/rhsvc/uac-ni.json') as fp:
            self.uac_json_ni = json.load(fp)

        self.get_info = self.app.router['Info:get'].url_for()
        self.get_index_en = self.app.router['IndexEN:get'].url_for()
        self.post_index_en = self.app.router['IndexEN:post'].url_for()
        self.get_address_confirmation_en = self.app.router['AddressConfirmationEN:get'].url_for()
        self.post_address_confirmation_en = self.app.router['AddressConfirmationEN:post'].url_for()
        self.get_address_edit_en = self.app.router['AddressEditEN:get'].url_for()
        self.post_address_edit_en = self.app.router['AddressEditEN:post'].url_for()
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
        self.eq_id = "census"
        self.survey = "CENSUS"
        self.form_type = "individual_gb_eng"
        self.jti = str(uuid.uuid4())
        self.uac_code = ''.join([str(n) for n in range(13)])
        self.uac1, self.uac2, self.uac3, self.uac4 = self.uac_code[:4], self.uac_code[4:8], self.uac_code[8:12], self.uac_code[12:]
        self.period_id = "1"
        self.user_id = "1234567890"
        self.uac = self.uac_json['uac']
        self.uprn = self.uac_json['address']['uprn']
        self.response_id = self.uac_json['questionnaireId']
        self.questionnaire_id = self.uac_json['questionnaireId']
        self.case_type = self.uac_json['caseType']
        self.channel = "rh"
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
        self.attributes_ni = {
            'addressLine1': self.uac_json['address']['addressLine1'],
            'addressLine2': self.uac_json['address']['addressLine2'],
            'addressLine3': self.uac_json['address']['addressLine3'],
            'townName': self.uac_json['address']['townName'],
            'postcode': self.uac_json['address']['postcode'],
            'uprn': self.uac_json['address']['uprn'],
            'language': 'ul',
            'display_region': 'ni'
        }
        self.eq_payload_en = {
            "jti": self.jti,
            "tx_id": self.jti,
            "iat": int(time.time()),
            "exp": int(time.time() + (5 * 60)),
            "case_type": self.case_type,
            "collection_exercise_sid": self.collection_exercise_id,
            "region_code": 'GB-ENG',
            "ru_ref": self.uprn,
            "case_id": self.case_id,
            "language_code": 'en',
            "display_address": f"{self.uac_json['address']['addressLine1']}, {self.uac_json['address']['addressLine2']}",
            "response_id": self.response_id,
            "account_service_url": f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}",
            "channel": self.channel,
            "user_id": "1234567890",
            "questionnaire_id": self.questionnaire_id,
            "eq_id": self.eq_id,
            "period_id": self.period_id,
            "form_type": self.form_type,
            "survey": self.survey
        }

        self.eq_payload_ni_ga = {
            "jti": self.jti,
            "tx_id": self.jti,
            "iat": int(time.time()),
            "exp": int(time.time() + (5 * 60)),
            "case_type": self.case_type,
            "collection_exercise_sid": self.collection_exercise_id,
            "region_code": 'GB-ENG',
            "ru_ref": self.uprn,
            "case_id": self.case_id,
            "language_code": 'ga',
            "display_address": f"{self.uac_json['address']['addressLine1']}, {self.uac_json['address']['addressLine2']}",
            "response_id": self.response_id,
            "account_service_url": f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}",
            "channel": self.channel,
            "user_id": "1234567890",
            "questionnaire_id": self.questionnaire_id,
            "eq_id": self.eq_id,
            "period_id": self.period_id,
            "form_type": self.form_type,
            "survey": self.survey
        }

        self.eq_payload_ni_ul = {
            "jti": self.jti,
            "tx_id": self.jti,
            "iat": int(time.time()),
            "exp": int(time.time() + (5 * 60)),
            "case_type": self.case_type,
            "collection_exercise_sid": self.collection_exercise_id,
            "region_code": 'GB-ENG',
            "ru_ref": self.uprn,
            "case_id": self.case_id,
            "language_code": 'ul',
            "display_address": f"{self.uac_json['address']['addressLine1']}, {self.uac_json['address']['addressLine2']}",
            "response_id": self.response_id,
            "account_service_url": f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}",
            "channel": self.channel,
            "user_id": "1234567890",
            "questionnaire_id": self.questionnaire_id,
            "eq_id": self.eq_id,
            "period_id": self.period_id,
            "form_type": self.form_type,
            "survey": self.survey
        }

        self.eq_payload_ni_en = {
            "jti": self.jti,
            "tx_id": self.jti,
            "iat": int(time.time()),
            "exp": int(time.time() + (5 * 60)),
            "case_type": self.case_type,
            "collection_exercise_sid": self.collection_exercise_id,
            "region_code": 'GB-ENG',
            "ru_ref": self.uprn,
            "case_id": self.case_id,
            "language_code": 'en',
            "display_address": f"{self.uac_json['address']['addressLine1']}, {self.uac_json['address']['addressLine2']}",
            "response_id": self.response_id,
            "account_service_url": f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}",
            "channel": self.channel,
            "user_id": "1234567890",
            "questionnaire_id": self.questionnaire_id,
            "eq_id": self.eq_id,
            "period_id": self.period_id,
            "form_type": self.form_type,
            "survey": self.survey
        }

        self.rhsvc_url = (
            f"{self.app['RHSVC_URL']}/uacs/{self.uac}"
        )

        self.rhsvc_url_surveylaunched = (
            f"{self.app['RHSVC_URL']}/surveyLaunched"
        )

        self.form_data = {
            'uac': self.uac, 'action[save_continue]': '',
        }

        self.address_confirmation_data = {
            'address-check-answer': 'Yes', 'action[save_continue]': ''
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
        self.get_webchat_ni = self.app.router['WebChatNI:get'].url_for()
        self.post_webchat_en = self.app.router['WebChatEN:post'].url_for()
        self.post_webchat_ni = self.app.router['WebChatNI:post'].url_for()
        self.get_webchat_chat_en = self.app.router['WebChatWindowEN:get'].url_for()
        self.get_webchat_chat_ni = self.app.router['WebChatWindowNI:get'].url_for()


        self.webchat_form_data = {
            'screen_name': 'Test', 'email': 'test@test.gov.uk', 'language': 'english', 'query': 'help', 'country': 'england'
        }

        self.webchatsvc_url = self.app['WEBCHAT_SVC_URL']

        self.addressindexsvc_url = f"{self.app['ADDRESS_INDEX_SVC_URL']}/addresses/postcode/"

        self.get_requestcode_en = self.app.router['RequestCodeEN:get'].url_for()
        self.get_requestcode_ni = self.app.router['RequestCodeNI:get'].url_for()
        self.post_requestcode_en = self.app.router['RequestCodeEN:post'].url_for()
        self.post_requestcode_ni = self.app.router['RequestCodeNI:post'].url_for()
        self.get_requestcode_selectaddress_en = self.app.router['RequestCodeSelectAddressEN:get'].url_for()
        self.get_requestcode_selectaddress_ni = self.app.router['RequestCodeSelectAddressNI:get'].url_for()
        self.post_requestcode_selectaddress_en = self.app.router['RequestCodeSelectAddressEN:post'].url_for()
        self.post_requestcode_selectaddress_ni = self.app.router['RequestCodeSelectAddressNI:post'].url_for()
        self.get_requestcode_address_confirmation_en = self.app.router['RequestCodeConfirmAddressEN:get'].url_for()
        self.get_requestcode_address_confirmation_ni = self.app.router['RequestCodeConfirmAddressNI:get'].url_for()
        self.post_requestcode_address_confirmation_en = self.app.router['RequestCodeConfirmAddressEN:post'].url_for()
        self.post_requestcode_address_confirmation_ni = self.app.router['RequestCodeConfirmAddressNI:post'].url_for()

        self.postcode_valid = 'EX2 6GA'
        self.postcode_invalid = 'ZZ99 9ZZ'
        self.postcode_no_results = 'GU34 5DU'

        self.post_requestcode_address_confirmation_data = {'request-address-select': "{'uprn': '10023122451', 'address': '1 Gate Reach, Exeter, EX2 6GA'}"}

        with open('tests/test_data/address_index/postcode_no_results.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_postcode_no_results = f

        with open('tests/test_data/address_index/postcode_results.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_postcode_results = f

        self.request_code_form_data_valid = {
            'request-postcode': self.postcode_valid, 'action[save_continue]': '',
        }

        self.request_code_form_data_no_results = {
            'request-postcode': self.postcode_no_results, 'action[save_continue]': '',
        }

        self.request_code_form_data_invalid = {
            'request-postcode': self.postcode_invalid, 'action[save_continue]': '',
        }

        self.request_code_address_confirmation_data = {
            'request-address-confirmation': 'Yes', 'action[save_continue]': ''
        }
