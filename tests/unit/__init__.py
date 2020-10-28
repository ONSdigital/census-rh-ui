import asyncio
import functools
import json
import time
import uuid

from aiohttp.test_utils import AioHTTPTestCase
from tenacity import wait_exponential

from app import app

from app import session, request
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
        from app import utils

        def encrypt(payload, **_):
            return json.dumps(payload)

        utils._bk_encrypt = utils.encrypt
        utils.encrypt = encrypt

    async def _reset_sdc_encrypt(*_):
        from app import utils

        utils.encrypt = utils._bk_encrypt

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
        # Monkey patch request retry wait time for faster tests
        request.RetryRequest._request_using_pool.retry.wait = wait_exponential(multiplier=0)
        request.RetryRequest._request_basic.retry.wait = wait_exponential(multiplier=0)
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
        with open('tests/test_data/rhsvc/uac_e.json') as fp:
            self.uac_json_e = json.load(fp)

        with open('tests/test_data/rhsvc/uac-w.json') as fp:
            self.uac_json_w = json.load(fp)

        with open('tests/test_data/rhsvc/uac-n.json') as fp:
            self.uac_json_n = json.load(fp)

        # URLs used in later statements
        url_path_prefix = self.app['URL_PATH_PREFIX']
        account_svc_url = self.app['ACCOUNT_SERVICE_URL']
        rh_svc_url = self.app['RHSVC_URL']
        address_index_svc_url = self.app['ADDRESS_INDEX_SVC_URL']
        aims_epoch = self.app['ADDRESS_INDEX_EPOCH']
        ad_look_up_svc_url = self.app['AD_LOOK_UP_SVC_URL']

        self.get_info = self.app.router['Info:get'].url_for()

        # Common

        # Test Data

        self.postcode_valid = 'EX2 6GA'
        self.postcode_invalid = 'ZZ99 9ZZ'
        self.postcode_no_results = 'GU34 6DU'
        self.postcode_empty = ''

        self.common_form_data_empty = {}

        self.post_common_select_address_form_data_valid = \
            '{"uprn": "10023122451", "address": "1 Gate Reach, Exeter, EX2 6GA"}'

        self.post_common_select_address_form_data_not_listed_en = \
            '{"uprn": "xxxx", "address": "I cannot find my address"}'

        self.post_common_select_address_form_data_not_listed_cy = \
            '{"uprn": "xxxx", "address": "I cannot find my address"}'

        self.common_select_address_input_valid = {
            'form-select-address': self.post_common_select_address_form_data_valid,
            'action[save_continue]': '',
        }

        self.common_select_address_input_not_listed_en = {
            'form-select-address': self.post_common_select_address_form_data_not_listed_en,
            'action[save_continue]': '',
        }

        self.common_select_address_input_not_listed_cy = {
            'form-select-address': self.post_common_select_address_form_data_not_listed_cy,
            'action[save_continue]': '',
        }

        self.common_confirm_address_input_yes = {
            'form-confirm-address': 'yes', 'action[save_continue]': ''
        }

        self.common_confirm_address_input_no = {
            'form-confirm-address': 'no', 'action[save_continue]': ''
        }

        self.common_confirm_address_input_invalid = {
            'form-confirm-address': 'invalid', 'action[save_continue]': ''
        }

        self.common_resident_or_manager_input_resident = {
            'form-resident-or-manager': 'resident', 'action[save_continue]': ''
        }

        self.common_resident_or_manager_input_manager = {
            'form-resident-or-manager': 'manager', 'action[save_continue]': ''
        }

        self.common_resident_or_manager_input_invalid = {
            'form-resident-or-manager': 'invalid', 'action[save_continue]': ''
        }

        self.common_postcode_input_valid = {
            'form-enter-address-postcode': self.postcode_valid, 'action[save_continue]': '',
        }

        self.common_postcode_input_no_results = {
            'form-enter-address-postcode': self.postcode_no_results, 'action[save_continue]': '',
        }

        self.common_postcode_input_invalid = {
            'form-enter-address-postcode': self.postcode_invalid, 'action[save_continue]': '',
        }

        self.common_postcode_input_empty = {
            'form-enter-address-postcode': self.postcode_empty, 'action[save_continue]': '',
        }

        with open('tests/test_data/address_index/postcode_no_results.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_postcode_no_results = f

        with open('tests/test_data/address_index/postcode_results.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_postcode_results = f

        with open('tests/test_data/address_index/uprn_valid.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result = f

        with open('tests/test_data/address_index/uprn_scotland.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_scotland = f

        with open('tests/test_data/address_index/uprn_censusaddresstype_na.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_censusaddresstype_na = f

        # Content
        self.ons_logo_en = '/img/ons-logo-pos-en.svg'
        self.ons_logo_cy = '/img/ons-logo-pos-cy.svg'
        self.nisra_logo = '/img/nisra-logo-en.svg'

        self.content_call_centre_number_ew = '0800 141 2021'
        self.content_call_centre_number_cy = '0800 169 2021'
        self.content_call_centre_number_ni = '0800 328 2021'

        self.content_common_address_in_scotland_en = 'This address is not part of the census for England and Wales'
        # TODO: add welsh translation
        self.content_common_address_in_scotland_cy = 'This address is not part of the census for England and Wales'

        self.content_common_enter_address_error_en = 'The postcode is not a valid UK postcode'
        # TODO: add welsh translation
        self.content_common_enter_address_error_cy = 'The postcode is not a valid UK postcode'

        self.content_common_enter_address_error_empty_en = 'You have not entered a postcode'
        # TODO: add welsh translation
        self.content_common_enter_address_error_empty_cy = 'You have not entered a postcode'

        self.content_common_select_address_title_en = 'Select your address'
        self.content_common_select_address_error_en = 'Select an address'
        self.content_common_select_address_value_en = '1 Gate Reach'
        self.content_common_select_address_no_results_en = 'We cannot find your address'
        self.content_common_select_address_title_cy = 'Dewiswch eich cyfeiriad'
        self.content_common_select_address_error_cy = 'Dewiswch gyfeiriad'
        self.content_common_select_address_value_cy = '1 Gate Reach'
        self.content_common_select_address_no_results_cy = 'Allwn ni ddim dod o hyd'

        self.content_common_confirm_address_title_en = 'Is this the correct address?'
        self.content_common_confirm_address_error_en = 'Check and confirm the address'
        self.content_common_confirm_address_value_yes_en = 'Yes, this is the correct address'
        self.content_common_confirm_address_value_no_en = 'No, search for address again'
        # TODO: add welsh translation
        self.content_common_confirm_address_title_cy = "Is this the correct address?"
        # TODO: add welsh translation
        self.content_common_confirm_address_error_cy = "Edrychwch eto ar y cyfeiriad a\\\'i gadarnhau"
        # TODO: add welsh translation
        self.content_common_confirm_address_value_yes_cy = "Yes, this is the correct address"
        # TODO: add welsh translation
        self.content_common_confirm_address_value_no_cy = 'No, search for address again'

        self.content_common_call_contact_centre_address_not_found_title_en = \
            'Register an address'
        # TODO: add welsh translation
        self.content_common_call_contact_centre_address_not_found_title_cy = \
            'Register an address'
        self.content_common_call_contact_centre_address_not_found_text_en = \
            'If you can\\xe2\\x80\\x99t find your address or part of your address has changed, ' \
            'it may not be registered on our system.'
        # TODO: add welsh translation
        self.content_common_call_contact_centre_address_not_found_text_cy = \
            'If you can\\xe2\\x80\\x99t find your address or part of your address has changed, ' \
            'it may not be registered on our system.'
        self.content_common_call_contact_centre_address_linking_en = \
            'There is an issue linking your address via the website.'
        # TODO: add welsh translation
        self.content_common_call_contact_centre_address_linking_cy = \
            'There is an issue linking your address via the website.'
        self.content_common_call_contact_centre_change_address_en = \
            'There is an issue changing your address via the website.'
        # TODO: add welsh translation
        self.content_common_call_contact_centre_change_address_cy = \
            'There is an issue changing your address via the website.'

        self.content_common_call_contact_centre_title_en = 'You need to call the Census customer contact centre'
        # TODO: add welsh translation
        self.content_common_call_contact_centre_title_cy = 'You need to call the Census customer contact centre'

        self.content_common_call_contact_centre_unable_to_match_address_en = \
            'There is an issue processing your address via the website.'
        # TODO: add welsh translation
        self.content_common_call_contact_centre_unable_to_match_address_cy = \
            'There is an issue processing your address via the website.'

        self.content_common_500_error_en = 'Sorry, something went wrong'
        self.content_common_500_error_cy = "Mae\\'n flin gennym, aeth rhywbeth o\\'i le"

        self.content_common_404_error_title_en = 'Page not found'
        self.content_common_404_error_secondary_en = 'If you entered a web address, check it is correct.'
        self.content_common_404_error_title_cy = "Heb ddod o hyd i\\\'r dudalen"
        self.content_common_404_error_secondary_cy = \
            "Os gwnaethoch nodi cyfeiriad gwefan, gwnewch yn si\\xc5\\xb5r ei fod yn gywir."

        self.content_common_timeout_en = 'Your session has timed out due to inactivity'
        self.content_common_timeout_cy = 'Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch'

        self.content_common_429_error_uac_title_en = \
            'You have reached the maximum number of access codes you can request online'
        self.content_common_429_error_form_title_en = \
            'You have reached the maximum number of paper questionnaires you can request online'
        # TODO: add welsh translation
        self.content_common_429_error_uac_title_cy = \
            'You have reached the maximum number of access codes you can request online'
        # TODO: add welsh translation
        self.content_common_429_error_form_title_cy = \
            'You have reached the maximum number of paper questionnaires you can request online'

        self.content_common_resident_or_manager_title_en = 'Are you a resident or manager of this establishment?'
        self.content_common_resident_or_manager_option_resident_en = 'Resident'
        self.content_common_resident_or_manager_description_resident_en = \
            'Residents are responsible for answering the census questions about themselves'
        self.content_common_resident_or_manager_option_manager_en = 'Manager'
        self.content_common_resident_or_manager_description_manager_en = \
            'A manager is responsible for answering the census questions about this establishment'
        self.content_common_resident_or_manager_error_en = 'Please select an option'
        # TODO: add welsh translation
        self.content_common_resident_or_manager_title_cy = 'Are you a resident or manager of this establishment?'
        # TODO: add welsh translation
        self.content_common_resident_or_manager_option_resident_cy = 'Resident'
        # TODO: add welsh translation
        self.content_common_resident_or_manager_description_resident_cy = \
            'Residents are responsible for answering the census questions about themselves'
        # TODO: add welsh translation
        self.content_common_resident_or_manager_option_manager_cy = 'Manager'
        # TODO: add welsh translation
        self.content_common_resident_or_manager_description_manager_cy = \
            'A manager is responsible for answering the census questions about this establishment'
        # TODO: add welsh translation
        self.content_common_resident_or_manager_error_cy = 'Please select an option'

        self.content_common_save_and_exit_link_en = 'Exit'
        # TODO: add welsh translation
        self.content_common_save_and_exit_link_cy = 'Exit'
        # End Common

        # Start Journey

        # Content

        self.content_start_title_en = 'Start census'
        self.content_start_uac_title_en = 'Enter your 16-character access code'
        # TODO: add welsh translation
        self.content_start_title_cy = "Start census"
        # TODO: add welsh translation
        self.content_start_uac_title_cy = "Enter your 16-character access code"

        self.content_start_uac_expired_en = 'Your unique access code has expired'
        self.content_start_uac_expired_cy = 'Mae eich cod mynediad unigryw wedi dod i ben'

        self.content_start_confirm_address_title_en = 'Is this the correct address?'
        self.content_start_confirm_address_option_yes_en = 'Yes, this is the correct address'
        self.content_start_confirm_address_option_no_en = 'No, this is not the correct address'
        self.content_start_confirm_address_error_en = 'Check and confirm the address is correct'
        # TODO: add welsh translation
        self.content_start_confirm_address_title_cy = "Is this the correct address?"
        # TODO: add welsh translation
        self.content_start_confirm_address_option_yes_cy = "Yes, this is the correct address"
        # TODO: add welsh translation
        self.content_start_confirm_address_option_no_cy = "No, this is not the correct address"
        # TODO: add welsh translation
        self.content_start_confirm_address_error_cy = 'Check and confirm the address is correct'

        self.content_start_ni_language_options_title = 'Would you like to complete the census in English?'
        self.content_start_ni_language_options_option_title = 'Select a language option'
        self.content_start_ni_language_options_option_yes = 'Yes, continue in English'

        self.content_start_ni_select_language_title = 'Choose your language'
        self.content_start_ni_select_language_option_title = 'Select a language option'
        self.content_start_ni_select_language_option = 'Continue in English'
        self.content_start_ni_select_language_switch_back = 'You can change your language back to English at any time.'

        self.content_start_save_and_exit_title_en = 'Your progress has been saved'
        self.content_start_save_and_exit_title_cy = 'Mae eich cynnydd wedi cael ei gadw'

        self.content_start_timeout_title_en = 'Your session has timed out due to inactivity'
        self.content_start_timeout_title_cy = 'Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch'
        self.content_start_timeout_secondary_en = 'To protect your information we have timed you out'
        self.content_start_timeout_secondary_cy = \
            'Er mwyn diogelu eich gwybodaeth, mae eich sesiwn wedi cyrraedd y terfyn amser'
        self.content_start_timeout_restart_en = 're-enter your access code'
        self.content_start_timeout_restart_cy = 'nodi eich cod mynediad eto'

        # End Start Journey

        self.get_start_en = self.app.router['Start:get'].url_for(display_region='en')
        self.get_start_adlocation_valid_en = self.app.router['Start:get'].url_for(display_region='en').with_query(
            {"adlocation": "1234567890"})
        self.get_start_adlocation_invalid_en = self.app.router['Start:get'].url_for(display_region='en').with_query(
            {"adlocation": "invalid"})
        self.post_start_en = self.app.router['Start:post'].url_for(display_region='en')
        self.get_start_region_change_en = self.app.router['StartRegionChange:get'].url_for(display_region='en')
        self.get_start_confirm_address_en = self.app.router['StartConfirmAddress:get'].url_for(display_region='en')
        self.post_start_confirm_address_en = self.app.router['StartConfirmAddress:post'].url_for(display_region='en')
        self.get_start_save_and_exit_en = self.app.router['StartSaveAndExit:get'].url_for(display_region='en')

        self.get_start_cy = self.app.router['Start:get'].url_for(display_region='cy')
        self.get_start_adlocation_valid_cy = self.app.router['Start:get'].url_for(display_region='cy').with_query(
            {"adlocation": "1234567890"})
        self.get_start_adlocation_invalid_cy = self.app.router['Start:get'].url_for(display_region='cy').with_query(
            {"adlocation": "invalid"})
        self.post_start_cy = self.app.router['Start:post'].url_for(display_region='cy')
        self.get_start_region_change_cy = self.app.router['StartRegionChange:get'].url_for(display_region='cy')
        self.get_start_confirm_address_cy = self.app.router['StartConfirmAddress:get'].url_for(display_region='cy')
        self.post_start_confirm_address_cy = self.app.router['StartConfirmAddress:post'].url_for(display_region='cy')
        self.get_start_save_and_exit_cy = self.app.router['StartSaveAndExit:get'].url_for(display_region='cy')

        self.get_start_ni = self.app.router['Start:get'].url_for(display_region='ni')
        self.get_start_adlocation_valid_ni = self.app.router['Start:get'].url_for(display_region='ni').with_query(
            {"adlocation": "1234567890"})
        self.get_start_adlocation_invalid_ni = self.app.router['Start:get'].url_for(display_region='ni').with_query(
            {"adlocation": "invalid"})
        self.post_start_ni = self.app.router['Start:post'].url_for(display_region='ni')
        self.get_start_region_change_ni = self.app.router['StartRegionChange:get'].url_for(display_region='ni')
        self.get_start_confirm_address_ni = self.app.router['StartConfirmAddress:get'].url_for(display_region='ni')
        self.post_start_confirm_address_ni = self.app.router['StartConfirmAddress:post'].url_for(display_region='ni')

        self.get_start_language_options_ni = self.app.router['StartNILanguageOptions:get'].url_for()
        self.post_start_language_options_ni = self.app.router['StartNILanguageOptions:post'].url_for()
        self.get_start_select_language_ni = self.app.router['StartNISelectLanguage:get'].url_for()
        self.post_start_select_language_ni = self.app.router['StartNISelectLanguage:post'].url_for()
        self.get_start_save_and_exit_ni = self.app.router['StartSaveAndExit:get'].url_for(display_region='ni')

        self.case_id = self.uac_json_e['caseId']
        self.collection_exercise_id = self.uac_json_e['collectionExerciseId']
        self.eq_id = 'census'
        self.survey = 'CENSUS'
        self.form_type = self.uac_json_e['formType']
        self.jti = str(uuid.uuid4())
        self.uac_code = ''.join([str(n) for n in range(13)])
        self.uac1, self.uac2, self.uac3, self.uac4 = self.uac_code[:4], self.uac_code[4:8], self.uac_code[8:12], self.uac_code[12:]
        self.period_id = '2019'
        self.uac = 'w4nwwpphjjptp7fn'
        self.uacHash = self.uac_json_e['uacHash']
        self.uprn = self.uac_json_e['address']['uprn']
        self.response_id = self.uac_json_e['questionnaireId']
        self.questionnaire_id = self.uac_json_e['questionnaireId']
        self.case_type = self.uac_json_e['caseType']
        self.channel = 'rh'
        self.attributes_en = {
            'addressLine1': self.uac_json_e['address']['addressLine1'],
            'addressLine2': self.uac_json_e['address']['addressLine2'],
            'addressLine3': self.uac_json_e['address']['addressLine3'],
            'townName': self.uac_json_e['address']['townName'],
            'postcode': self.uac_json_e['address']['postcode'],
            'uprn': self.uac_json_e['address']['uprn'],
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
            'display_address': self.uac_json_e['address']['addressLine1'] + ', '
                               + self.uac_json_e['address']['addressLine2'],
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

        self.account_service_url = '/start/'
        self.account_service_log_out_url = '/start/save-and-exit/'

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

        self.rhsvc_post_create_case_url = (
            f'{rh_svc_url}/cases/create'
        )

        self.rhsvc_put_modify_address = (
            f'{rh_svc_url}/cases/e37b0d05-3643-445e-8e71-73f7df3ff95e/address'
        )

        self.rhsvc_cases_url = (
            f'{rh_svc_url}/cases/'
        )

        self.rhsvc_url_link_uac = (
            f'{rh_svc_url}/uacs/{self.uacHash}/link'
        )

        self.start_data_valid = {
            'uac': self.uac, 'action[save_continue]': '',
        }

        self.start_data_valid_with_adlocation = {
            'uac': self.uac, 'adlocation': '1234567890', 'action[save_continue]': '',
        }

        self.start_confirm_address_data_yes = {
            'address-check-answer': 'Yes', 'action[save_continue]': ''
        }

        self.start_confirm_address_data_no = {
            'address-check-answer': 'No', 'action[save_continue]': ''
        }

        self.start_confirm_address_data_invalid = {
            'address-check-answer': 'Invalid', 'action[save_continue]': ''
        }

        self.start_confirm_address_data_empty = {}

        self.start_ni_language_option_data_yes = {
            'language-option': 'Yes', 'action[save_continue]': ''
        }

        self.start_ni_language_option_data_no = {
            'language-option': 'No', 'action[save_continue]': ''
        }

        self.start_ni_language_option_data_invalid = {
            'language-option': 'Invalid', 'action[save_continue]': ''
        }

        self.start_ni_language_option_data_empty = {}

        self.start_modify_address_data_valid = {
            'address-line-1': 'ONS',
            'address-line-2': 'Segensworth Road',
            'address-line-3': 'Titchfield',
            'address-town': 'Fareham',
            'address-postcode': 'PO15 5RR'
        }

        self.start_modify_address_data_incomplete = {
            'address-line-2': 'Segensworth Road',
            'address-line-3': 'Titchfield',
            'address-town': 'Fareham',
            'address-postcode': 'PO15 5RR'
        }

        self.start_modify_address_data = {
            'caseId': self.case_id,
            'uprn': self.uprn,
            'addressLine1': self.uac_json_e['address']['addressLine1'],
            'addressLine2': self.uac_json_e['address']['addressLine2'],
            'addressLine3': self.uac_json_e['address']['addressLine3'],
            'townName': self.uac_json_e['address']['townName'],
            'postcode': self.uac_json_e['address']['postcode']
            }

        self.start_ni_select_language_data_ul = {
            'language-option': 'ulster-scotch', 'action[save_continue]': ''
        }

        self.start_ni_select_language_data_ga = {
            'language-option': 'gaeilge', 'action[save_continue]': ''
        }

        self.start_ni_select_language_data_en = {
            'language-option': 'english', 'action[save_continue]': ''
        }

        self.start_ni_select_language_data_invalid = {
            'language-option': 'invalid', 'action[save_continue]': ''
        }

        self.start_ni_select_language_data_empty = {}

        self.get_webchat_en = self.app.router['WebChat:get'].url_for(display_region='en')
        self.get_webchat_cy = self.app.router['WebChat:get'].url_for(display_region='cy')
        self.get_webchat_ni = self.app.router['WebChat:get'].url_for(display_region='ni')
        self.post_webchat_en = self.app.router['WebChat:post'].url_for(display_region='en')
        self.post_webchat_cy = self.app.router['WebChat:post'].url_for(display_region='cy')
        self.post_webchat_ni = self.app.router['WebChat:post'].url_for(display_region='ni')

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

        self.addressindexsvc_url = f'{address_index_svc_url}/addresses/rh/postcode/'
        self.address_index_epoch_param = f'?epoch={aims_epoch}'
        self.address_index_epoch_param_test = f'?epoch=test'

        self.get_start_saveandexit_en = self.app.router['StartSaveAndExit:get'].url_for(display_region='en')
        self.get_start_saveandexit_cy = self.app.router['StartSaveAndExit:get'].url_for(display_region='cy')
        self.get_start_saveandexit_ni = self.app.router['StartSaveAndExit:get'].url_for(display_region='ni')

        self.selected_uprn = '10023122451'

        self.mobile_valid = '07012345678'
        self.mobile_invalid_short = '07012'
        self.mobile_invalid_long = '0701234567890123456'
        self.mobile_invalid_character = '0701234567$'

        self.field_empty = None

        with open('tests/test_data/rhsvc/case_by_uprn_hh_e.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_hh_e = f

        with open('tests/test_data/rhsvc/case_by_uprn_hh_w.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_hh_w = f

        with open('tests/test_data/rhsvc/case_by_uprn_hh_n.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_hh_n = f

        with open('tests/test_data/rhsvc/case_by_uprn_spg_e.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_spg_e = f

        with open('tests/test_data/rhsvc/case_by_uprn_spg_w.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_spg_w = f

        with open('tests/test_data/rhsvc/case_by_uprn_spg_n.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_spg_n = f

        with open('tests/test_data/rhsvc/case_by_uprn_ce_m_e.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_ce_m_e = f

        with open('tests/test_data/rhsvc/case_by_uprn_ce_m_w.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_ce_m_w = f

        with open('tests/test_data/rhsvc/case_by_uprn_ce_m_n.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_ce_m_n = f

        with open('tests/test_data/rhsvc/case_by_uprn_ce_r_e.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_ce_r_e = f

        with open('tests/test_data/rhsvc/case_by_uprn_ce_r_w.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_ce_r_w = f

        with open('tests/test_data/rhsvc/case_by_uprn_ce_r_n.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_ce_r_n = f

        with open('tests/test_data/rhsvc/get_fulfilment_multi_sms.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_multi_sms = f

        with open('tests/test_data/rhsvc/get_fulfilment_single_sms.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_single_sms = f

        with open('tests/test_data/rhsvc/get_fulfilment_multi_post.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_multi_post = f

        with open('tests/test_data/rhsvc/get_fulfilment_single_post.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_single_post = f

        with open('tests/test_data/rhsvc/request_fulfilment_sms.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_request_fulfilment_sms = f

        with open('tests/test_data/rhsvc/request_fulfilment_post.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_request_fulfilment_post = f

        self.request_code_select_method_data_sms = {
            'form-select-method': 'sms', 'action[save_continue]': ''
        }

        self.request_code_select_method_data_post = {
            'form-select-method': 'post', 'action[save_continue]': ''
        }

        self.request_code_select_method_data_invalid = {
            'form-select-method': 'invalid', 'action[save_continue]': ''
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

        self.request_common_enter_name_form_data_valid = {
            'name_first_name': 'Bob', 'name_last_name': 'Bobbington', 'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_no_first = {
            'name_last_name': 'Bobbington', 'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_no_last = {
            'name_first_name': 'Bob', 'action[save_continue]': '',
        }

        self.request_common_confirm_name_address_data_yes = {
            'request-name-address-confirmation': 'yes', 'action[save_continue]': ''
        }

        self.request_common_confirm_name_address_data_yes_large_print = {
            'request-name-address-confirmation': 'yes',
            'request-name-address-large-print': 'large-print',
            'action[save_continue]': ''
        }

        self.request_common_confirm_name_address_data_no = {
            'request-name-address-confirmation': 'no', 'action[save_continue]': ''
        }

        self.request_common_confirm_name_address_data_invalid = {
            'request-name-address-confirmation': 'invalid', 'action[save_continue]': ''
        }

        self.content_request_household_title_en = 'Request a new access code'
        self.content_request_household_title_cy = 'Gofyn am god mynediad newydd'
        self.content_request_individual_title_en = 'Request an individual access code'
        self.content_request_individual_title_cy = 'Gofyn am god mynediad unigryw'
        self.content_request_secondary_en = 'You will need to provide:'
        self.content_request_secondary_cy = 'Bydd angen i chi ddarparu:'

        self.content_request_enter_address_title_en = 'What is your postcode?'
        self.content_request_enter_address_secondary_en = \
            'To request an access code, we need your address.'
        self.content_request_enter_address_title_cy = 'Beth yw eich cod post?'
        # TODO: add welsh translation
        self.content_request_enter_address_secondary_cy = \
            'To request an access code, we need your address.'

        self.content_request_code_select_method_individual_response_question_en = \
            'Need to answer separately from your household?'
        self.content_request_code_select_method_error_en = 'Please select an option'
        self.content_request_code_select_method_secondary_en = 'Select how to send access code'
        self.content_request_code_select_method_option_text_en = 'Text message'
        self.content_request_code_select_method_option_post_en = 'Post'

        # TODO Add Welsh Translation
        self.content_request_code_select_method_individual_response_question_cy = \
            'Need to answer separately from your household?'
        # TODO Add Welsh Translation
        self.content_request_code_select_method_error_cy = "Please select an option"
        # TODO Add Welsh Translation
        self.content_request_code_select_method_secondary_cy = "Select how to send access code"
        # TODO Add Welsh Translation
        self.content_request_code_select_method_option_text_cy = 'Text message'
        # TODO Add Welsh Translation
        self.content_request_code_select_method_option_post_cy = 'Post'

        self.content_request_code_select_method_household_title_en = \
            'How would you like to receive a new household access code?'
        # TODO Add Welsh Translation
        self.content_request_code_select_method_household_title_cy = \
            'How would you like to receive a new household access code?'

        self.content_request_code_select_method_individual_title_en = \
            'How would you like to receive a new individual access code?'
        # TODO Add Welsh Translation
        self.content_request_code_select_method_individual_title_cy = \
            'How would you like to receive a new individual access code?'

        self.content_request_code_select_method_manager_title_en = \
            'How would you like to receive a new manager access code?'
        # TODO Add Welsh Translation
        self.content_request_code_select_method_manager_title_cy = \
            'How would you like to receive a new manager access code?'

        self.content_request_code_enter_mobile_title_en = 'What is your mobile phone number?'
        self.content_request_code_enter_mobile_error_en = ''
        self.content_request_code_enter_mobile_secondary_en = \
            'This will not be stored and only used once to send the access code'
        self.content_request_code_enter_mobile_title_cy = 'Beth yw eich rhif ff\\xc3\\xb4n symudol?'
        self.content_request_code_enter_mobile_error_cy = ""
        # TODO Add Welsh Translation
        self.content_request_code_enter_mobile_secondary_cy = \
            "This will not be stored and only used once to send the access code"

        self.content_request_code_confirm_mobile_title_en = 'Is this mobile phone number correct?'
        self.content_request_code_confirm_mobile_error_en = 'Check and confirm your mobile phone number'
        self.content_request_code_confirm_mobile_title_cy = "Ydy\\\'r rhif ff\\xc3\\xb4n symudol hwn yn gywir?"
        self.content_request_code_confirm_mobile_error_cy = \
            "Edrychwch eto ar eich rhif ff\\xc3\\xb4n symudol a\\\'i gadarnhau"

        self.content_request_code_sent_sms_title_en = 'We have sent an access code'
        self.content_request_code_sent_sms_secondary_individual_en = \
            'The text message with a new individual access code should arrive soon for you to start your census'
        self.content_request_code_sent_sms_secondary_manager_en = \
            'The text message with a new manager access code should arrive soon for you to start your census'
        self.content_request_code_sent_sms_secondary_household_en = \
            'The text message with a new household access code should arrive soon for you to start your census'
        self.content_request_code_sent_sms_title_cy = 'Rydym ni wedi anfon cod mynediad'
        # TODO Add Welsh Translation
        self.content_request_code_sent_sms_secondary_individual_cy = \
            'The text message with a new individual access code should arrive soon for you to start your census'
        # TODO Add Welsh Translation
        self.content_request_code_sent_sms_secondary_manager_cy = \
            'The text message with a new manager access code should arrive soon for you to start your census'
        # TODO Add Welsh Translation
        self.content_request_code_sent_sms_secondary_household_cy = \
            'The text message with a new household access code should arrive soon for you to start your census'

        self.content_request_common_enter_name_title_en = 'What is your name?'
        self.content_request_common_enter_name_error_first_name_en = 'Enter a first name to continue'
        self.content_request_common_enter_name_error_last_name_en = 'Enter a last name to continue'
        # TODO Add Welsh Translation
        self.content_request_common_enter_name_title_cy = 'What is your name?'
        # TODO Add Welsh Translation
        self.content_request_common_enter_name_error_first_name_cy = "Enter a first name to continue"
        # TODO Add Welsh Translation
        self.content_request_common_enter_name_error_last_name_cy = 'Enter a last name to continue'

        self.content_request_common_confirm_name_address_title_individual_en = \
            'Do you want to send a new individual access code to this address?'
        self.content_request_common_confirm_name_address_title_manager_en = \
            'Do you want to send a new manager access code to this address?'
        self.content_request_common_confirm_name_address_title_household_en = \
            'Do you want to send a new household access code to this address?'
        self.content_request_common_confirm_name_address_error_en = 'Please check and confirm the name and address'
        self.content_request_common_confirm_name_address_option_yes_en = 'Yes, send the access code by post'
        self.content_request_common_confirm_name_address_option_no_en = 'No, send it another way'
        # TODO Add Welsh Translation
        self.content_request_common_confirm_name_address_title_individual_cy = \
            'Do you want to send a new individual access code to this address?'
        # TODO Add Welsh Translation
        self.content_request_common_confirm_name_address_title_manager_cy = \
            'Do you want to send a new manager access code to this address?'
        # TODO Add Welsh Translation
        self.content_request_common_confirm_name_address_title_household_cy = \
            'Do you want to send a new household access code to this address?'
        # TODO Add Welsh Translation
        self.content_request_common_confirm_name_address_error_cy = \
            "Please check and confirm the name and address"
        # TODO Add Welsh Translation
        self.content_request_common_confirm_name_address_option_yes_cy = 'Yes, send the access code by post'
        # TODO Add Welsh Translation
        self.content_request_common_confirm_name_address_option_no_cy = 'No, send it another way'

        self.content_request_code_sent_post_title_en = \
            'A letter will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        self.content_request_code_sent_post_secondary_individual_en = \
            'The letter with a new individual access code should arrive soon for you to start the census'
        self.content_request_code_sent_post_secondary_manager_en = \
            'The letter with a new manager access code should arrive soon for you to start the census'
        self.content_request_code_sent_post_secondary_household_en = \
            'The letter with a new household access code should arrive soon for you to start the census'
        self.content_request_code_sent_post_title_cy = \
            'A letter will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        # TODO Add Welsh Translation
        self.content_request_code_sent_post_secondary_individual_cy = \
            'The letter with a new individual access code should arrive soon for you to start the census'
        # TODO Add Welsh Translation
        self.content_request_code_sent_post_secondary_manager_cy = \
            'The letter with a new manager access code should arrive soon for you to start the census'
        # TODO Add Welsh Translation
        self.content_request_code_sent_post_secondary_household_cy = \
            'The letter with a new household access code should arrive soon for you to start the census'

        self.content_request_contact_centre_en = 'You need to call the Census customer contact centre'
        # TODO: add welsh translation
        self.content_request_contact_centre_cy = 'You need to call the Census customer contact centre'

        self.content_request_timeout_error_en = 're-enter your postcode'
        self.content_request_timeout_error_cy = 'nodi eich cod post eto'

        # Unlinked UACs

        # URLs
        self.get_start_unlinked_enter_address_en = \
            self.app.router['CommonEnterAddress:get'].url_for(display_region='en', user_journey='start',
                                                              sub_user_journey='unlinked')
        self.get_start_unlinked_enter_address_cy = \
            self.app.router['CommonEnterAddress:get'].url_for(display_region='cy', user_journey='start',
                                                              sub_user_journey='unlinked')
        self.get_start_unlinked_enter_address_ni = \
            self.app.router['CommonEnterAddress:get'].url_for(display_region='ni', user_journey='start',
                                                              sub_user_journey='unlinked')
        self.post_start_unlinked_enter_address_en = \
            self.app.router['CommonEnterAddress:post'].url_for(display_region='en', user_journey='start',
                                                               sub_user_journey='unlinked')
        self.post_start_unlinked_enter_address_cy = \
            self.app.router['CommonEnterAddress:post'].url_for(display_region='cy', user_journey='start',
                                                               sub_user_journey='unlinked')
        self.post_start_unlinked_enter_address_ni = \
            self.app.router['CommonEnterAddress:post'].url_for(display_region='ni', user_journey='start',
                                                               sub_user_journey='unlinked')

        self.get_start_unlinked_select_address_en = \
            self.app.router['CommonSelectAddress:get'].url_for(display_region='en', user_journey='start',
                                                               sub_user_journey='unlinked')
        self.get_start_unlinked_select_address_cy = \
            self.app.router['CommonSelectAddress:get'].url_for(display_region='cy', user_journey='start',
                                                               sub_user_journey='unlinked')
        self.get_start_unlinked_select_address_ni = \
            self.app.router['CommonSelectAddress:get'].url_for(display_region='ni', user_journey='start',
                                                               sub_user_journey='unlinked')
        self.post_start_unlinked_select_address_en = \
            self.app.router['CommonSelectAddress:post'].url_for(display_region='en', user_journey='start',
                                                                sub_user_journey='unlinked')
        self.post_start_unlinked_select_address_cy = \
            self.app.router['CommonSelectAddress:post'].url_for(display_region='cy', user_journey='start',
                                                                sub_user_journey='unlinked')
        self.post_start_unlinked_select_address_ni = \
            self.app.router['CommonSelectAddress:post'].url_for(display_region='ni', user_journey='start',
                                                                sub_user_journey='unlinked')

        self.get_start_unlinked_confirm_address_en = \
            self.app.router['CommonConfirmAddress:get'].url_for(display_region='en', user_journey='start',
                                                                sub_user_journey='unlinked')
        self.get_start_unlinked_confirm_address_cy = \
            self.app.router['CommonConfirmAddress:get'].url_for(display_region='cy', user_journey='start',
                                                                sub_user_journey='unlinked')
        self.get_start_unlinked_confirm_address_ni = \
            self.app.router['CommonConfirmAddress:get'].url_for(display_region='ni', user_journey='start',
                                                                sub_user_journey='unlinked')
        self.post_start_unlinked_confirm_address_en = \
            self.app.router['CommonConfirmAddress:post'].url_for(display_region='en', user_journey='start',
                                                                 sub_user_journey='unlinked')
        self.post_start_unlinked_confirm_address_cy = \
            self.app.router['CommonConfirmAddress:post'].url_for(display_region='cy', user_journey='start',
                                                                 sub_user_journey='unlinked')
        self.post_start_unlinked_confirm_address_ni = \
            self.app.router['CommonConfirmAddress:post'].url_for(display_region='ni', user_journey='start',
                                                                 sub_user_journey='unlinked')

        self.get_start_unlinked_address_has_been_linked_en = \
            self.app.router['StartAddressHasBeenLinked:get'].url_for(display_region='en')
        self.get_start_unlinked_address_has_been_linked_cy = \
            self.app.router['StartAddressHasBeenLinked:get'].url_for(display_region='cy')
        self.get_start_unlinked_address_has_been_linked_ni = \
            self.app.router['StartAddressHasBeenLinked:get'].url_for(display_region='ni')
        self.post_start_unlinked_address_has_been_linked_en = \
            self.app.router['StartAddressHasBeenLinked:post'].url_for(display_region='en')
        self.post_start_unlinked_address_has_been_linked_cy = \
            self.app.router['StartAddressHasBeenLinked:post'].url_for(display_region='cy')
        self.post_start_unlinked_address_has_been_linked_ni = \
            self.app.router['StartAddressHasBeenLinked:post'].url_for(display_region='ni')

        # Test Data
        with open('tests/test_data/rhsvc/uac_unlinked_e.json') as fp:
            self.unlinked_uac_json_e = json.load(fp)
        with open('tests/test_data/rhsvc/uac_unlinked_w.json') as fp:
            self.unlinked_uac_json_w = json.load(fp)
        with open('tests/test_data/rhsvc/uac_unlinked_n.json') as fp:
            self.unlinked_uac_json_n = json.load(fp)

        with open('tests/test_data/rhsvc/uac_linked_e.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_post_linked_uac_e = f
        with open('tests/test_data/rhsvc/uac_linked_w.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_post_linked_uac_w = f
        with open('tests/test_data/rhsvc/uac_linked_n.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_post_linked_uac_n = f

        self.start_address_linked = {
            'action[save_continue]': ''
        }

        # Content
        self.content_start_unlinked_enter_address_question_title_en = 'What is your postcode?'
        # TODO: add welsh translation
        self.content_start_unlinked_enter_address_question_title_cy = 'Beth yw eich cod post?'

        self.content_start_unlinked_address_has_been_linked_title_en = 'Your address has been linked to your code'
        # TODO: add welsh translation
        self.content_start_unlinked_address_has_been_linked_title_cy = 'Your address has been linked to your code'
        self.content_start_unlinked_address_has_been_linked_secondary_en = \
            'You are now ready to start your Census questions'
        # TODO: add welsh translation
        self.content_start_unlinked_address_has_been_linked_secondary_cy = \
            'You are now ready to start your Census questions'

        self.content_unlinked_timeout_error_en = 're-enter your access code'
        self.content_unlinked_timeout_error_cy = 'nodi eich cod mynediad eto'

        # Start Change Address

        # URLs
        self.get_start_change_address_enter_address_en = \
            self.app.router['CommonEnterAddress:get'].url_for(display_region='en', user_journey='start',
                                                              sub_user_journey='change-address')
        self.get_start_change_address_enter_address_cy = \
            self.app.router['CommonEnterAddress:get'].url_for(display_region='cy', user_journey='start',
                                                              sub_user_journey='change-address')
        self.get_start_change_address_enter_address_ni = \
            self.app.router['CommonEnterAddress:get'].url_for(display_region='ni', user_journey='start',
                                                              sub_user_journey='change-address')
        self.post_start_change_address_enter_address_en = \
            self.app.router['CommonEnterAddress:post'].url_for(display_region='en', user_journey='start',
                                                               sub_user_journey='change-address')
        self.post_start_change_address_enter_address_cy = \
            self.app.router['CommonEnterAddress:post'].url_for(display_region='cy', user_journey='start',
                                                               sub_user_journey='change-address')
        self.post_start_change_address_enter_address_ni = \
            self.app.router['CommonEnterAddress:post'].url_for(display_region='ni', user_journey='start',
                                                               sub_user_journey='change-address')

        self.get_start_change_address_select_address_en = \
            self.app.router['CommonSelectAddress:get'].url_for(display_region='en', user_journey='start',
                                                               sub_user_journey='change-address')
        self.get_start_change_address_select_address_cy = \
            self.app.router['CommonSelectAddress:get'].url_for(display_region='cy', user_journey='start',
                                                               sub_user_journey='change-address')
        self.get_start_change_address_select_address_ni = \
            self.app.router['CommonSelectAddress:get'].url_for(display_region='ni', user_journey='start',
                                                               sub_user_journey='change-address')
        self.post_start_change_address_select_address_en = \
            self.app.router['CommonSelectAddress:post'].url_for(display_region='en', user_journey='start',
                                                                sub_user_journey='change-address')
        self.post_start_change_address_select_address_cy = \
            self.app.router['CommonSelectAddress:post'].url_for(display_region='cy', user_journey='start',
                                                                sub_user_journey='change-address')
        self.post_start_change_address_select_address_ni = \
            self.app.router['CommonSelectAddress:post'].url_for(display_region='ni', user_journey='start',
                                                                sub_user_journey='change-address')

        self.get_start_change_address_confirm_address_en = \
            self.app.router['CommonConfirmAddress:get'].url_for(display_region='en', user_journey='start',
                                                                sub_user_journey='change-address')
        self.get_start_change_address_confirm_address_cy = \
            self.app.router['CommonConfirmAddress:get'].url_for(display_region='cy', user_journey='start',
                                                                sub_user_journey='change-address')
        self.get_start_change_address_confirm_address_ni = \
            self.app.router['CommonConfirmAddress:get'].url_for(display_region='ni', user_journey='start',
                                                                sub_user_journey='change-address')
        self.post_start_change_address_confirm_address_en = \
            self.app.router['CommonConfirmAddress:post'].url_for(display_region='en', user_journey='start',
                                                                 sub_user_journey='change-address')
        self.post_start_change_address_confirm_address_cy = \
            self.app.router['CommonConfirmAddress:post'].url_for(display_region='cy', user_journey='start',
                                                                 sub_user_journey='change-address')
        self.post_start_change_address_confirm_address_ni = \
            self.app.router['CommonConfirmAddress:post'].url_for(display_region='ni', user_journey='start',
                                                                 sub_user_journey='change-address')

        self.get_start_change_address_address_has_been_changed_en = \
            self.app.router['StartAddressHasBeenChanged:get'].url_for(display_region='en')
        self.get_start_change_address_address_has_been_changed_cy = \
            self.app.router['StartAddressHasBeenChanged:get'].url_for(display_region='cy')
        self.get_start_change_address_address_has_been_changed_ni = \
            self.app.router['StartAddressHasBeenChanged:get'].url_for(display_region='ni')
        self.post_start_change_address_address_has_been_changed_en = \
            self.app.router['StartAddressHasBeenChanged:post'].url_for(display_region='en')
        self.post_start_change_address_address_has_been_changed_cy = \
            self.app.router['StartAddressHasBeenChanged:post'].url_for(display_region='cy')
        self.post_start_change_address_address_has_been_changed_ni = \
            self.app.router['StartAddressHasBeenChanged:post'].url_for(display_region='ni')

        # Test Data
        with open('tests/test_data/rhsvc/uac_linked_e.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_post_linked_uac_e = f
        with open('tests/test_data/rhsvc/uac_linked_w.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_post_linked_uac_w = f
        with open('tests/test_data/rhsvc/uac_linked_n.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_post_linked_uac_n = f

        self.start_address_changed = {
            'action[save_continue]': ''
        }

        # Content
        self.content_start_change_address_enter_address_question_title_en = 'What is your postcode?'
        # TODO: add welsh translation
        self.content_start_change_address_enter_address_question_title_cy = 'Beth yw eich cod post?'

        self.content_start_change_address_address_has_been_changed_title_en = 'Your address has been changed'
        # TODO: add welsh translation
        self.content_start_change_address_address_has_been_changed_title_cy = 'Your address has been changed'
        self.content_start_change_address_address_has_been_changed_secondary_en = \
            'You are now ready to start your Census questions'
        # TODO: add welsh translation
        self.content_start_change_address_address_has_been_changed_secondary_cy = \
            'You are now ready to start your Census questions'

        self.content_start_change_address_timeout_error_en = 're-enter your access code'
        self.content_start_change_address_timeout_error_cy = 'nodi eich cod mynediad eto'

        # Start Request Access Code

        # URLs

        self.get_request_access_code_enter_address_en = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='access-code'
        )
        self.get_request_access_code_enter_address_cy = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='access-code'
        )
        self.get_request_access_code_enter_address_ni = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='access-code'
        )
        self.post_request_access_code_enter_address_en = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='access-code'
        )
        self.post_request_access_code_enter_address_cy = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='access-code'
        )
        self.post_request_access_code_enter_address_ni = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='access-code'
        )

        self.get_request_access_code_select_address_en = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='access-code'
        )
        self.get_request_access_code_select_address_cy = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='access-code'
        )
        self.get_request_access_code_select_address_ni = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='access-code'
        )
        self.post_request_access_code_select_address_en = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='access-code'
        )
        self.post_request_access_code_select_address_cy = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='access-code'
        )
        self.post_request_access_code_select_address_ni = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='access-code'
        )

        self.get_request_access_code_confirm_address_en = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='access-code'
        )
        self.get_request_access_code_confirm_address_cy = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='access-code'
        )
        self.get_request_access_code_confirm_address_ni = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='access-code'
        )
        self.post_request_access_code_confirm_address_en = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='access-code'
        )
        self.post_request_access_code_confirm_address_cy = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='access-code'
        )
        self.post_request_access_code_confirm_address_ni = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='access-code'
        )

        self.post_request_access_code_resident_or_manager_en = self.app.router['CommonCEMangerQuestion:post'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='access-code'
        )
        self.post_request_access_code_resident_or_manager_cy = self.app.router['CommonCEMangerQuestion:post'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='access-code'
        )
        self.post_request_access_code_resident_or_manager_ni = self.app.router['CommonCEMangerQuestion:post'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='access-code'
        )

        self.get_request_access_code_select_method_en = self.app.router['RequestCodeSelectMethod:get'].url_for(
            request_type='access-code', display_region='en'
        )
        self.get_request_access_code_select_method_cy = self.app.router['RequestCodeSelectMethod:get'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.get_request_access_code_select_method_ni = self.app.router['RequestCodeSelectMethod:get'].url_for(
            request_type='access-code', display_region='ni'
        )
        self.post_request_access_code_select_method_en = self.app.router['RequestCodeSelectMethod:post'].url_for(
            request_type='access-code', display_region='en'
        )
        self.post_request_access_code_select_method_cy = self.app.router['RequestCodeSelectMethod:post'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.post_request_access_code_select_method_ni = self.app.router['RequestCodeSelectMethod:post'].url_for(
            request_type='access-code', display_region='ni'
        )

        self.get_request_access_code_enter_mobile_en = self.app.router['RequestCodeEnterMobile:get'].url_for(
            request_type='access-code', display_region='en'
        )
        self.get_request_access_code_enter_mobile_cy = self.app.router['RequestCodeEnterMobile:get'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.get_request_access_code_enter_mobile_ni = self.app.router['RequestCodeEnterMobile:get'].url_for(
            request_type='access-code', display_region='ni'
        )
        self.post_request_access_code_enter_mobile_en = self.app.router['RequestCodeEnterMobile:post'].url_for(
            request_type='access-code', display_region='en'
        )
        self.post_request_access_code_enter_mobile_cy = self.app.router['RequestCodeEnterMobile:post'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.post_request_access_code_enter_mobile_ni = self.app.router['RequestCodeEnterMobile:post'].url_for(
            request_type='access-code', display_region='ni'
        )

        self.get_request_access_code_confirm_mobile_en = self.app.router['RequestCodeConfirmMobile:get'].url_for(
            request_type='access-code', display_region='en'
        )
        self.get_request_access_code_confirm_mobile_cy = self.app.router['RequestCodeConfirmMobile:get'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.get_request_access_code_confirm_mobile_ni = self.app.router['RequestCodeConfirmMobile:get'].url_for(
            request_type='access-code', display_region='ni'
        )
        self.post_request_access_code_confirm_mobile_en = self.app.router['RequestCodeConfirmMobile:post'].url_for(
            request_type='access-code', display_region='en'
        )
        self.post_request_access_code_confirm_mobile_cy = self.app.router['RequestCodeConfirmMobile:post'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.post_request_access_code_confirm_mobile_ni = self.app.router['RequestCodeConfirmMobile:post'].url_for(
            request_type='access-code', display_region='ni'
        )

        self.post_request_access_code_enter_name_en = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='access-code', display_region='en'
        )
        self.post_request_access_code_enter_name_cy = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.post_request_access_code_enter_name_ni = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='access-code', display_region='ni'
        )

        self.post_request_access_code_confirm_name_address_en = \
            self.app.router['RequestCommonConfirmNameAddress:post'].url_for(request_type='access-code',
                                                                            display_region='en')
        self.post_request_access_code_confirm_name_address_cy = \
            self.app.router['RequestCommonConfirmNameAddress:post'].url_for(request_type='access-code',
                                                                            display_region='cy')
        self.post_request_access_code_confirm_name_address_ni = \
            self.app.router['RequestCommonConfirmNameAddress:post'].url_for(request_type='access-code',
                                                                            display_region='ni')

        # Start Request Individual Code

        # URLs

        self.get_request_individual_code_en = self.app.router['RequestCode:get'].url_for(
            request_type='individual-code', display_region='en'
        )
        self.get_request_individual_code_cy = self.app.router['RequestCode:get'].url_for(
            request_type='individual-code', display_region='cy'
        )
        self.get_request_individual_code_ni = self.app.router['RequestCode:get'].url_for(
            request_type='individual-code', display_region='ni'
        )

        self.get_request_individual_code_enter_address_en = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='individual-code'
        )
        self.get_request_individual_code_enter_address_cy = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='individual-code'
        )
        self.get_request_individual_code_enter_address_ni = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='individual-code'
        )
        self.post_request_individual_code_enter_address_en = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='individual-code'
        )
        self.post_request_individual_code_enter_address_cy = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='individual-code'
        )
        self.post_request_individual_code_enter_address_ni = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='individual-code'
        )

        self.get_request_individual_code_select_address_en = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='individual-code'
        )
        self.get_request_individual_code_select_address_cy = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='individual-code'
        )
        self.get_request_individual_code_select_address_ni = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='individual-code'
        )
        self.post_request_individual_code_select_address_en = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='individual-code'
        )
        self.post_request_individual_code_select_address_cy = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='individual-code'
        )
        self.post_request_individual_code_select_address_ni = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='individual-code'
        )

        self.get_request_individual_code_confirm_address_en = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='individual-code'
        )
        self.get_request_individual_code_confirm_address_cy = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='individual-code'
        )
        self.get_request_individual_code_confirm_address_ni = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='individual-code'
        )
        self.post_request_individual_code_confirm_address_en = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='individual-code'
        )
        self.post_request_individual_code_confirm_address_cy = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='individual-code'
        )
        self.post_request_individual_code_confirm_address_ni = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='individual-code'
        )

        self.get_request_individual_code_select_method_en = self.app.router['RequestCodeSelectMethod:get'].url_for(
            request_type='individual-code', display_region='en'
        )
        self.get_request_individual_code_select_method_cy = self.app.router['RequestCodeSelectMethod:get'].url_for(
            request_type='individual-code', display_region='cy'
        )
        self.get_request_individual_code_select_method_ni = self.app.router['RequestCodeSelectMethod:get'].url_for(
            request_type='individual-code', display_region='ni'
        )
        self.post_request_individual_code_select_method_en = self.app.router['RequestCodeSelectMethod:post'].url_for(
            request_type='individual-code', display_region='en'
        )
        self.post_request_individual_code_select_method_cy = self.app.router['RequestCodeSelectMethod:post'].url_for(
            request_type='individual-code', display_region='cy'
        )
        self.post_request_individual_code_select_method_ni = self.app.router['RequestCodeSelectMethod:post'].url_for(
            request_type='individual-code', display_region='ni'
        )

        self.get_request_individual_code_enter_mobile_en = self.app.router['RequestCodeEnterMobile:get'].url_for(
            request_type='individual-code', display_region='en'
        )
        self.get_request_individual_code_enter_mobile_cy = self.app.router['RequestCodeEnterMobile:get'].url_for(
            request_type='individual-code', display_region='cy'
        )
        self.get_request_individual_code_enter_mobile_ni = self.app.router['RequestCodeEnterMobile:get'].url_for(
            request_type='individual-code', display_region='ni'
        )
        self.post_request_individual_code_enter_mobile_en = self.app.router['RequestCodeEnterMobile:post'].url_for(
            request_type='individual-code', display_region='en'
        )
        self.post_request_individual_code_enter_mobile_cy = self.app.router['RequestCodeEnterMobile:post'].url_for(
            request_type='individual-code', display_region='cy'
        )
        self.post_request_individual_code_enter_mobile_ni = self.app.router['RequestCodeEnterMobile:post'].url_for(
            request_type='individual-code', display_region='ni'
        )

        self.get_request_individual_code_confirm_mobile_en = self.app.router['RequestCodeConfirmMobile:get'].url_for(
            request_type='individual-code', display_region='en'
        )
        self.get_request_individual_code_confirm_mobile_cy = self.app.router['RequestCodeConfirmMobile:get'].url_for(
            request_type='individual-code', display_region='cy'
        )
        self.get_request_individual_code_confirm_mobile_ni = self.app.router['RequestCodeConfirmMobile:get'].url_for(
            request_type='individual-code', display_region='ni'
        )
        self.post_request_individual_code_confirm_mobile_en = self.app.router['RequestCodeConfirmMobile:post'].url_for(
            request_type='individual-code', display_region='en'
        )
        self.post_request_individual_code_confirm_mobile_cy = self.app.router['RequestCodeConfirmMobile:post'].url_for(
            request_type='individual-code', display_region='cy'
        )
        self.post_request_individual_code_confirm_mobile_ni = self.app.router['RequestCodeConfirmMobile:post'].url_for(
            request_type='individual-code', display_region='ni'
        )

        self.post_request_individual_code_enter_name_en = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='individual-code', display_region='en'
        )
        self.post_request_individual_code_enter_name_cy = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='individual-code', display_region='cy'
        )
        self.post_request_individual_code_enter_name_ni = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='individual-code', display_region='ni'
        )

        self.post_request_individual_code_confirm_name_address_en = \
            self.app.router['RequestCommonConfirmNameAddress:post'].url_for(request_type='individual-code',
                                                                            display_region='en')
        self.post_request_individual_code_confirm_name_address_cy = \
            self.app.router['RequestCommonConfirmNameAddress:post'].url_for(request_type='individual-code',
                                                                            display_region='cy')
        self.post_request_individual_code_confirm_name_address_ni = \
            self.app.router['RequestCommonConfirmNameAddress:post'].url_for(request_type='individual-code',
                                                                            display_region='ni')

        # Start Request Paper Form

        # URLs

        self.get_request_paper_form_enter_address_en = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='paper-form'
        )
        self.get_request_paper_form_enter_address_cy = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='paper-form'
        )
        self.get_request_paper_form_enter_address_ni = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='paper-form'
        )
        self.post_request_paper_form_enter_address_en = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='paper-form'
        )
        self.post_request_paper_form_enter_address_cy = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='paper-form'
        )
        self.post_request_paper_form_enter_address_ni = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='paper-form'
        )

        self.get_request_paper_form_select_address_en = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='paper-form'
        )
        self.get_request_paper_form_select_address_cy = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='paper-form'
        )
        self.get_request_paper_form_select_address_ni = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='paper-form'
        )
        self.post_request_paper_form_select_address_en = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='paper-form'
        )
        self.post_request_paper_form_select_address_cy = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='paper-form'
        )
        self.post_request_paper_form_select_address_ni = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='paper-form'
        )

        self.get_request_paper_form_confirm_address_en = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='paper-form'
        )
        self.get_request_paper_form_confirm_address_cy = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='paper-form'
        )
        self.get_request_paper_form_confirm_address_ni = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='paper-form'
        )
        self.post_request_paper_form_confirm_address_en = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='paper-form'
        )
        self.post_request_paper_form_confirm_address_cy = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='paper-form'
        )
        self.post_request_paper_form_confirm_address_ni = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='paper-form'
        )

        self.post_request_paper_form_resident_or_manager_en = self.app.router['CommonCEMangerQuestion:post'].url_for(
            display_region='en', user_journey='requests', sub_user_journey='paper-form'
        )
        self.post_request_paper_form_resident_or_manager_cy = self.app.router['CommonCEMangerQuestion:post'].url_for(
            display_region='cy', user_journey='requests', sub_user_journey='paper-form'
        )
        self.post_request_paper_form_resident_or_manager_ni = self.app.router['CommonCEMangerQuestion:post'].url_for(
            display_region='ni', user_journey='requests', sub_user_journey='paper-form'
        )

        self.post_request_paper_form_enter_name_en = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='paper-form', display_region='en'
        )
        self.post_request_paper_form_enter_name_cy = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='paper-form', display_region='cy'
        )
        self.post_request_paper_form_enter_name_ni = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='paper-form', display_region='ni'
        )

        self.post_request_paper_form_confirm_name_address_en = \
            self.app.router['RequestCommonConfirmNameAddress:post'].url_for(request_type='paper-form',
                                                                            display_region='en')
        self.post_request_paper_form_confirm_name_address_cy = \
            self.app.router['RequestCommonConfirmNameAddress:post'].url_for(request_type='paper-form',
                                                                            display_region='cy')
        self.post_request_paper_form_confirm_name_address_ni = \
            self.app.router['RequestCommonConfirmNameAddress:post'].url_for(request_type='paper-form',
                                                                            display_region='ni')

        # Content

        self.content_request_form_enter_address_secondary_en = \
            'To send a paper questionnaire, we need your address'
        # TODO: add welsh translation
        self.content_request_form_enter_address_secondary_cy = \
            'To send a paper questionnaire, we need your address'

        self.content_request_form_sent_post_title_en = \
            'A paper questionnaire will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        self.content_request_form_sent_post_title_large_print_en = \
            'A large-print paper questionnaire will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        self.content_request_form_sent_post_secondary_en = \
            'This should arrive soon for you to complete your census'
        # TODO: add welsh translation
        self.content_request_form_sent_post_title_cy = \
            'A paper questionnaire will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        # TODO: add welsh translation
        self.content_request_form_sent_post_title_large_print_cy = \
            'A large-print paper questionnaire will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        # TODO Add Welsh Translation
        self.content_request_form_sent_post_secondary_cy = \
            'This should arrive soon for you to complete your census'

        self.content_request_form_confirm_name_address_title_en = \
            'Do you want to send a paper questionnaire to this address?'
        self.content_request_form_confirm_name_address_option_yes_en = 'Yes, send the questionnaire by post'
        self.content_request_form_confirm_name_address_option_no_en = 'No, cancel and return'
        self.content_request_form_confirm_name_address_large_print_checkbox_en = 'I need a large-print questionnaire'

        # TODO Add Welsh Translation
        self.content_request_form_confirm_name_address_title_cy = \
            'Do you want to send a paper questionnaire to this address?'
        # TODO Add Welsh Translation
        self.content_request_form_confirm_name_address_option_yes_cy = 'Yes, send the questionnaire by post'
        # TODO Add Welsh Translation
        self.content_request_form_confirm_name_address_option_no_cy = 'No, cancel and return'
        # TODO Add Welsh Translation
        self.content_request_form_confirm_name_address_large_print_checkbox_cy = 'I need a large-print questionnaire'

        self.content_request_form_manager_title_en = 'We cannot send census forms to managers by post'
        # TODO Add Welsh Translation
        self.content_request_form_manager_title_cy = 'We cannot send census forms to managers by post'

        self.content_request_form_request_cancelled_title_en = 'Your request for a paper form has been cancelled'
        # TODO Add Welsh Translation
        self.content_request_form_request_cancelled_title_cy = 'Your request for a paper form has been cancelled'

        # Start Support Centre Pages

        # URLs

        self.get_support_centre_enter_postcode_en = self.app.router['SupportCentreEnterPostcode:get'].url_for(
            display_region='en'
        )
        self.get_support_centre_enter_postcode_cy = self.app.router['SupportCentreEnterPostcode:get'].url_for(
            display_region='cy'
        )
        self.post_support_centre_enter_postcode_en = self.app.router['SupportCentreEnterPostcode:post'].url_for(
            display_region='en'
        )
        self.post_support_centre_enter_postcode_cy = self.app.router['SupportCentreEnterPostcode:post'].url_for(
            display_region='cy'
        )
        self.get_support_centre_list_of_centres_postcode_invalid_en = \
            self.app.router['SupportCentreListCentres:get'].url_for(
                display_region='en', postcode=self.postcode_invalid)
        self.get_support_centre_list_of_centres_postcode_invalid_cy = \
            self.app.router['SupportCentreListCentres:get'].url_for(
                display_region='cy', postcode=self.postcode_invalid)
        self.get_support_centre_list_of_centres_postcode_valid_en = \
            self.app.router['SupportCentreListCentres:get'].url_for(
                display_region='en', postcode=self.postcode_valid)
        self.get_support_centre_list_of_centres_postcode_valid_cy = \
            self.app.router['SupportCentreListCentres:get'].url_for(
                display_region='cy', postcode=self.postcode_valid)

        # Contents

        self.content_support_centre_enter_postcode_title_en = 'Find a support centre'
        self.content_support_centre_enter_postcode_secondary_en = \
            'To find your nearest support centre, we need your postcode.'
        self.content_support_centre_enter_postcode_error_empty_en = 'You have not entered a postcode'
        self.content_support_centre_enter_postcode_error_invalid_en = 'The postcode is not a valid UK postcode'
        self.content_support_centre_enter_postcode_title_cy = "Chwilio am ganolfan gymorth"
        self.content_support_centre_enter_postcode_secondary_cy = \
            "Er mwyn chwilio am eich canolfan gymorth agosaf, bydd angen i ni gael eich cod post."
        # TODO Add Welsh Translation
        self.content_support_centre_enter_postcode_error_empty_cy = 'You have not entered a postcode'
        # TODO Add Welsh Translation
        self.content_support_centre_enter_postcode_error_invalid_cy = 'The postcode is not a valid UK postcode'

        self.content_support_centre_list_of_centres_result_one_google_url = \
            'https://www.google.com/maps/search/?api=1&query=53.380582,-1.466986'

        self.content_support_centre_list_of_centres_title_en = 'Support centres near ' + self.postcode_valid
        self.content_support_centre_list_of_centres_result_one_location_name_en = 'Sheffield Central Library'
        self.content_support_centre_list_of_centres_result_two_location_name_en = 'University of Sheffield'
        self.content_support_centre_list_of_centres_result_one_distance_away_en = \
            '<span class="u-mb-s tag">1.3 miles away</span>'
        self.content_support_centre_list_of_centres_result_one_address_en = \
            '<p>Surrey Street<br> Sheffield<br>S1 1XZ</p>'
        self.content_support_centre_list_of_centres_result_one_telephone_en = \
            'Telephone: <span>+44 (0)11 4273 4712</span>'
        self.content_support_centre_list_of_centres_result_one_email_en = \
            'Email: <a href="mailto:test@email.com">test@email.com</a>'
        self.content_support_centre_list_of_centres_result_open_monday_en = 'Monday &ndash;&nbsp;10:30am to 5:15pm'
        self.content_support_centre_list_of_centres_result_open_tuesday_en = 'Tuesday &ndash;&nbsp;10am to 5pm'
        self.content_support_centre_list_of_centres_result_open_wednesday_en = 'Wednesday &ndash;&nbsp;10am to 5pm'
        self.content_support_centre_list_of_centres_result_open_thursday_en = 'Thursday &ndash;&nbsp;10am to 5pm'
        self.content_support_centre_list_of_centres_result_open_friday_en = 'Friday &ndash;&nbsp;10am to 5pm'
        self.content_support_centre_list_of_centres_result_open_saturday_en = 'Saturday &ndash;&nbsp;10am to 1pm'
        self.content_support_centre_list_of_centres_result_open_sunday_en = 'Sunday &ndash;&nbsp;10am to 1pm'
        self.content_support_centre_list_of_centres_result_open_census_saturday_en = \
            'Census Saturday, 20 March &ndash;&nbsp;10am to 4pm'
        self.content_support_centre_list_of_centres_result_open_census_day_en = \
            'Census Day, 21 March &ndash;&nbsp;10am to 4pm'
        self.content_support_centre_list_of_centres_result_open_good_friday_en = \
            'Good Friday, 2 April &ndash;&nbsp;10am to 5pm'
        self.content_support_centre_list_of_centres_result_open_easter_monday_en = \
            'Easter Monday, 5 April &ndash;&nbsp;10am to 5pm'
        self.content_support_centre_list_of_centres_result_open_may_bank_holiday_en = \
            'May Bank Holiday, 3 May &ndash;&nbsp;10am to 5pm'
        self.content_support_centre_list_of_centres_result_closed_monday_en = 'Monday &ndash;&nbsp;Closed'
        self.content_support_centre_list_of_centres_result_closed_tuesday_en = 'Tuesday &ndash;&nbsp;Closed'
        self.content_support_centre_list_of_centres_result_closed_wednesday_en = 'Wednesday &ndash;&nbsp;Closed'
        self.content_support_centre_list_of_centres_result_closed_thursday_en = 'Thursday &ndash;&nbsp;Closed'
        self.content_support_centre_list_of_centres_result_closed_friday_en = 'Friday &ndash;&nbsp;Closed'
        self.content_support_centre_list_of_centres_result_closed_saturday_en = 'Saturday &ndash;&nbsp;Closed'
        self.content_support_centre_list_of_centres_result_closed_sunday_en = 'Sunday &ndash;&nbsp;Closed'
        self.content_support_centre_list_of_centres_result_closed_census_saturday_en = \
            'Census Saturday, 20 March &ndash;&nbsp;Closed'
        self.content_support_centre_list_of_centres_result_closed_census_day_en = \
            'Census Day, 21 March &ndash;&nbsp;Closed'
        self.content_support_centre_list_of_centres_result_closed_good_friday_en = \
            'Good Friday, 2 April &ndash;&nbsp;Closed'
        self.content_support_centre_list_of_centres_result_closed_easter_monday_en = \
            'Easter Monday, 5 April &ndash;&nbsp;Closed'
        self.content_support_centre_list_of_centres_result_closed_may_bank_holiday_en = \
            'May Bank Holiday, 3 May &ndash;&nbsp;Closed'

        self.content_support_centre_list_of_centres_result_one_public_parking_en = \
            'Car park, including disabled parking'
        self.content_support_centre_list_of_centres_result_two_public_parking_en = 'Disabled parking'
        self.content_support_centre_list_of_centres_result_three_public_parking_en = 'Car park'
        self.content_support_centre_list_of_centres_result_one_level_access_en = 'Level access into building entrance'
        self.content_support_centre_list_of_centres_result_one_wheelchair_access_en = 'Wheelchair access'
        self.content_support_centre_list_of_centres_result_one_disability_aware_en = 'Staff are disability aware'
        self.content_support_centre_list_of_centres_result_one_hearing_loop_en = 'Hearing loop system'

        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_title_cy = 'Support centres near ' + self.postcode_valid
        self.content_support_centre_list_of_centres_result_one_location_name_cy = 'Welsh Sheffield Central Library'
        self.content_support_centre_list_of_centres_result_two_location_name_cy = 'Welsh University of Sheffield'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_one_distance_away_cy = \
            '<span class="u-mb-s tag">1.3 miles away</span>'
        self.content_support_centre_list_of_centres_result_one_address_cy = \
            '<p>Welsh Street<br> Sheffield<br>S1 1XZ</p>'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_one_telephone_cy = \
            'Telephone: <span>+44 (0)11 4273 4712</span>'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_one_email_cy = \
            'Email: <a href="mailto:test@email.com">test@email.com</a>'

        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_monday_cy = \
            'Monday &ndash;&nbsp;10:30am tan 5:15pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_tuesday_cy = \
            'Tuesday &ndash;&nbsp;10am tan 5pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_wednesday_cy = \
            'Wednesday &ndash;&nbsp;10am tan 5pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_thursday_cy = 'Thursday &ndash;&nbsp;10am tan 5pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_friday_cy = 'Friday &ndash;&nbsp;10am tan 5pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_saturday_cy = 'Saturday &ndash;&nbsp;10am tan 1pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_sunday_cy = 'Sunday &ndash;&nbsp;10am tan 1pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_census_saturday_cy = \
            'Census Saturday, 20 March &ndash;&nbsp;10am tan 4pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_census_day_cy = \
            'Census Day, 21 March &ndash;&nbsp;10am tan 4pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_good_friday_cy = \
            'Good Friday, 2 April &ndash;&nbsp;10am tan 5pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_easter_monday_cy = \
            'Easter Monday, 5 April &ndash;&nbsp;10am tan 5pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_open_may_bank_holiday_cy = \
            'May Bank Holiday, 3 May &ndash;&nbsp;10am tan 5pm'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_monday_cy = 'Monday &ndash;&nbsp;Closed'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_tuesday_cy = 'Tuesday &ndash;&nbsp;Closed'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_wednesday_cy = 'Wednesday &ndash;&nbsp;Closed'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_thursday_cy = 'Thursday &ndash;&nbsp;Closed'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_friday_cy = 'Friday &ndash;&nbsp;Closed'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_saturday_cy = 'Saturday &ndash;&nbsp;Closed'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_sunday_cy = 'Sunday &ndash;&nbsp;Closed'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_census_saturday_cy = \
            'Census Saturday, 20 March &ndash;&nbsp;Closed'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_census_day_cy = \
            'Census Day, 21 March &ndash;&nbsp;Closed'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_good_friday_cy = \
            'Good Friday, 2 April &ndash;&nbsp;Closed'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_easter_monday_cy = \
            'Easter Monday, 5 April &ndash;&nbsp;Closed'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_closed_may_bank_holiday_cy = \
            'May Bank Holiday, 3 May &ndash;&nbsp;Closed'

        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_one_public_parking_cy = \
            'Car park, including disabled parking'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_two_public_parking_cy = 'Disabled parking'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_three_public_parking_cy = 'Car park'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_one_level_access_cy = 'Level access into building entrance'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_one_wheelchair_access_cy = 'Wheelchair access'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_one_disability_aware_cy = 'Staff are disability aware'
        # TODO Add Welsh Translation
        self.content_support_centre_list_of_centres_result_one_hearing_loop_cy = 'Hearing loop system'

        # Test Data

        self.support_centre_enter_postcode_input_valid = {
            'form-enter-address-postcode': self.postcode_valid, 'action[save_continue]': '',
        }

        self.support_centre_enter_postcode_input_invalid = {
            'form-enter-address-postcode': self.postcode_invalid, 'action[save_continue]': '',
        }

        self.support_centre_enter_postcode_input_empty = {
            'form-enter-address-postcode': self.postcode_empty, 'action[save_continue]': '',
        }

        with open('tests/test_data/ad_lookup/multiple_return.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ad_multiple_return = f

        with open('tests/test_data/ad_lookup/single_return.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ad_single_return = f

        with open('tests/test_data/ad_lookup/no_match_return.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ad_no_match_return = f

        self.ad_lookup_url = f'{ad_look_up_svc_url}/centres/postcode?postcode={self.postcode_valid}&limit=10'

        # yapf: enable
