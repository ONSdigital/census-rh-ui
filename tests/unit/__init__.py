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
    response_id = '6tg2s16T1HClxcttXW3IJgpe198BuJkGE5oJg0dieOU='

    start_date = '2018-04-10'
    end_date = '2020-05-31'
    return_by = '2018-05-08'

    def session_storage(self, app_config):
        self.assertIn("REDIS_SERVER", app_config)
        self.assertIn("REDIS_PORT", app_config)
        self.assertIn("ABSOLUTE_SESSION_AGE", app_config)
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
        with open('tests/test_data/case/case.json') as fp:
            self.case_json = json.load(fp)
        with open('tests/test_data/collection_exercise/collection_exercise.json') as fp:
            self.collection_exercise_json = json.load(fp)
        with open('tests/test_data/collection_exercise/collection_exercise_events.json') as fp:
            self.collection_exercise_events_json = json.load(fp)
        with open('tests/test_data/collection_exercise/collection_exercise_events_closed.json') as fp:
            self.closed_ce_events_json = json.load(fp)
        with open('tests/test_data/collection_instrument/collection_instrument_eq.json') as fp:
            self.collection_instrument_json = json.load(fp)
        with open('tests/test_data/sample/sample_attributes.json') as fp:
            self.sample_attributes_json = json.load(fp)
        with open('tests/test_data/survey/survey.json') as fp:
            self.survey_json = json.load(fp)


        self.get_index = self.app.router['Index:get'].url_for()
        self.get_info = self.app.router['Info:get'].url_for()
        self.get_cookies_privacy = self.app.router['CookiesPrivacy:get'].url_for()
        self.get_contact_us = self.app.router['ContactUs:get'].url_for()
        self.post_index = self.app.router['Index:post'].url_for()
        self.post_address_confirmation = self.app.router['AddressConfirmation:post'].url_for()
        # self.action_plan_id = self.case_json['actionPlanId']
        self.case_id = self.uac_json['caseId']
        # self.case_group_id = self.case_json['caseGroup']['id']
        # self.case_ref = self.case_json['caseRef']
        self.collection_exercise_id = self.uac_json['collectionExerciseId']
        # self.collection_exercise_ref = self.collection_exercise_json['exerciseRef']
        # self.collection_exercise_user_desc = self.collection_exercise_json['userDescription']
        # self.collection_instrument_id = self.collection_instrument_json['id']
        self.eq_id = "census"
        self.form_type = "household"
        self.jti = str(uuid.uuid4())
        self.iac_code = ''.join([str(n) for n in range(11)])
        self.iac1, self.iac2, self.iac3 = self.iac_code[:4], self.iac_code[4:8], self.iac_code[8:]
        # self.iac_json = {'active': '1', 'caseId': self.case_id}
        # self.sample_unit_id = self.sample_attributes_json['id']
        # self.sample_unit_attributes = self.uac_json['address']
        # self.sample_unit_ref = self.case_json['caseGroup']['sampleUnitRef']
        # self.sample_unit_type = self.case_json['sampleUnitType']
        # self.survey_id = self.survey_json['id']
        # self.survey_ref = self.survey_json['surveyRef']
        self.period_id = "1"
        self.user_id = "1234567890"
        self.uac = self.uac_json['uac']
        self.uprn = self.uac_json['address']['uprn']
        self.response_id = self.uac_json['questionnaireId']
        self.questionnaire_id = self.uac_json['questionnaireId']
        self.case_type = self.uac_json['caseType']
        self.channel = "rh"
        self.eq_payload = {
            "jti": self.jti,
            "tx_id": self.jti,
            "iat": int(time.time()),
            "exp": int(time.time() + (5 * 60)),
            "case_type": self.case_type,
            "collection_exercise_sid": self.collection_exercise_id,
            "region_code": 'GB-ENG',
            "ru_ref": self.uprn,
            "case_id": self.case_id,
            "language_code": self.language_code,
            "display_address": f"{self.uac_json['address']['addressLine1']}, {self.uac_json['address']['addressLine2']}",
            "response_id": self.response_id,
            "account_service_url": f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}",
            "channel": self.channel,
            "user_id": "1234567890",
            "questionnare_id": self.questionnaire_id,
            "eq_id": self.eq_id,
            "period_id": self.period_id,
            "form_type": self.user_id
 }

        self.rhsvc_url = (
            f"{self.app['RHSVC_URL']}/uacs/{self.uac}"
        )
        """
        self.case_url = (
            f"{self.app['CASE_URL']}/cases/{self.case_id}"
        )
        self.case_events_url = (
            f"{self.app['CASE_URL']}/cases/{self.case_id}/events"
        )
        self.collection_instrument_url = (
            f"{self.app['COLLECTION_INSTRUMENT_URL']}"
            f"/collection-instrument-api/1.0.2/collectioninstrument/id/{self.collection_instrument_id}"
        )
        self.collection_exercise_url = (
            f"{self.app['COLLECTION_EXERCISE_URL']}"
            f"/collectionexercises/{self.collection_exercise_id}"
        )
        self.collection_exercise_events_url = (
            f"{self.app['COLLECTION_EXERCISE_URL']}"
            f"/collectionexercises/{self.collection_exercise_id}/events"
        )
        self.iac_url = (
            f"{self.app['IAC_URL']}/iacs/{self.iac_code}"
        )
        self.sample_attributes_url = (
            f"{self.app['SAMPLE_URL']}/samples/{self.sample_unit_id}/attributes"
        )
        self.survey_url = (
            f"{self.app['SURVEY_URL']}/surveys/{self.survey_id}"
        )
        """

        self.form_data = {
            'iac1': self.iac1, 'iac2': self.iac2, 'iac3': self.iac3, 'action[save_continue]': '',
        }

        self.address_confirmation_data = {
            'address-check-answer': 'Yes', 'action[save_continue]': ''
        }

        class DummyConstructor:
            _collex_id = self.collection_exercise_id
            _collex_events = self.collection_exercise_events_json
        self.dummy_eq = DummyConstructor()
