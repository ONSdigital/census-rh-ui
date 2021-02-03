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

        self.aims_postcode_limit = '250'

        self.get_info = self.app.router['Info:get'].url_for()

        # Common

        # Test Data

        self.postcode_valid = 'EX2 6GA'
        self.postcode_invalid = 'ZZ99 9ZZ'
        self.postcode_no_results = 'GU34 6DU'
        self.postcode_empty = ''
        self.adlocation = '1234567890'

        self.common_form_data_empty = {}

        self.content_common_invalid_mobile_error_en = \
            'Enter a UK mobile number in a valid format, for example, 07700 900345 or +44 7700 900345'
        # TODO: add welsh translation
        self.content_common_invalid_mobile_error_cy = \
            'Enter a UK mobile number in a valid format, for example, 07700 900345 or +44 7700 900345'

        self.common_select_address_input_valid = {
            'form-pick-address': '10023122451', 'action[save_continue]': '',
        }

        self.common_select_address_input_not_listed = {
            'form-pick-address': 'xxxx', 'action[save_continue]': '',
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

        with open('tests/test_data/address_index/uprn_valid_hh.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_hh = f

        with open('tests/test_data/address_index/uprn_valid_spg.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_spg = f

        with open('tests/test_data/address_index/uprn_valid_ce.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_ce = f

        with open('tests/test_data/address_index/uprn_england.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_england = f

        with open('tests/test_data/address_index/uprn_wales.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_wales = f

        with open('tests/test_data/address_index/uprn_northern_ireland.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_northern_ireland = f

        with open('tests/test_data/address_index/uprn_northern_ireland_ce.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_northern_ireland_ce = f

        with open('tests/test_data/address_index/uprn_scotland.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_scotland = f

        with open('tests/test_data/address_index/uprn_censusaddresstype_na.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_censusaddresstype_na = f

        with open('tests/test_data/address_index/uprn_censusaddresstype_na_ni.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_censusaddresstype_na_ni = f

        # Content
        self.ons_logo_en = '/img/ons-logo-pos-en.svg'
        self.ons_logo_cy = '/img/ons-logo-pos-cy.svg'
        self.nisra_logo = '/img/nisra-logo-en.svg'

        self.content_call_centre_number_ew = '0800 141 2021'
        self.content_call_centre_number_cy = '0800 169 2021'
        self.content_call_centre_number_ni = '0800 328 2021'

        self.content_common_address_in_northern_ireland_page_title_en = \
            '<title>Address not part of census for England and Wales - Census 2021</title>'
        self.content_common_address_in_northern_ireland_en = \
            'This address is not part of the census for England and Wales'
        # TODO: add welsh translation
        self.content_common_address_in_northern_ireland_page_title_cy = \
            '<title>Address not part of census for England and Wales - Cyfrifiad 2021</title>'
        self.content_common_address_in_northern_ireland_cy = \
            "Nid yw\\\'r cyfeiriad hwn yn rhan o\\\'r cyfrifiad yng Nghymru a Lloegr"

        self.content_common_address_not_in_northern_ireland_page_title = \
            '<title>Address not part of census for Northern Ireland - Census 2021</title>'
        self.content_common_address_not_in_northern_ireland = \
            'This address is not part of the census for Northern Ireland'
        self.content_common_address_in_england_secondary = \
            'You have selected an address in England.'
        self.content_common_address_in_wales_secondary = \
            'You have selected an address in Wales.'

        self.content_common_address_in_scotland_page_title_en = \
            '<title>Address not part of census for England and Wales - Census 2021</title>'
        self.content_common_address_in_scotland_en = 'This address is not part of the census for England and Wales'
        # TODO: add welsh translation
        self.content_common_address_in_scotland_page_title_cy = \
            '<title>Address not part of census for England and Wales - Cyfrifiad 2021</title>'
        self.content_common_address_in_scotland_cy = \
            "Nid yw\\\'r cyfeiriad hwn yn rhan o\\\'r cyfrifiad yng Nghymru a Lloegr"
        self.content_common_address_in_scotland_page_title_ni = \
            '<title>Address not part of census for Northern Ireland - Census 2021</title>'
        self.content_common_address_in_scotland_ni = 'This address is not part of the census for Northern Ireland'

        self.content_common_enter_address_error_en = 'Enter a valid UK postcode'
        # TODO Add Welsh Translation
        self.content_common_enter_address_error_cy = "Enter a valid UK postcode"

        self.content_common_enter_address_error_empty_en = 'Enter a postcode'
        # TODO Add Welsh Translation
        self.content_common_enter_address_error_empty_cy = "Enter a postcode"

        self.content_common_select_address_page_title_en = '<title>Select address - Census 2021</title>'
        self.content_common_select_address_page_title_error_en = '<title>Error: Select address - Census 2021</title>'
        self.content_common_select_address_title_en = 'Select your address'
        self.content_common_select_address_error_en = 'Select an address'
        self.content_common_select_address_value_en = '1 Gate Reach'
        self.content_common_select_address_no_results_en = 'We cannot find your address'
        self.content_common_select_address_page_title_cy = '<title>Dewis cyfeiriad - Cyfrifiad 2021</title>'
        self.content_common_select_address_page_title_error_cy = '<title>Gwall: Dewis cyfeiriad - Cyfrifiad 2021</title>'
        self.content_common_select_address_title_cy = 'Dewiswch eich cyfeiriad'
        self.content_common_select_address_error_cy = 'Dewiswch gyfeiriad'
        self.content_common_select_address_value_cy = '1 Gate Reach'
        self.content_common_select_address_no_results_cy = 'Allwn ni ddim dod o hyd'

        self.content_common_confirm_address_page_title_en = '<title>Confirm address - Census 2021</title>'
        self.content_common_confirm_address_page_title_error_en = '<title>Error: Confirm address - Census 2021</title>'
        self.content_common_confirm_address_title_en = 'Is this the correct address?'
        self.content_common_confirm_address_error_en = 'Select an answer'
        self.content_common_confirm_address_value_yes_en = 'Yes, this is the correct address'
        self.content_common_confirm_address_value_no_en = 'No, search for address again'
        self.content_common_confirm_address_page_title_cy = '<title>Cadarnhau cyfeiriad - Cyfrifiad 2021</title>'
        self.content_common_confirm_address_page_title_error_cy = \
            '<title>Gwall: Cadarnhau cyfeiriad - Cyfrifiad 2021</title>'
        self.content_common_confirm_address_title_cy = "Ai hwn yw\\\'r cyfeiriad cywir?"
        # TODO: add welsh translation
        self.content_common_confirm_address_error_cy = "Select an answer"
        self.content_common_confirm_address_value_yes_cy = "Ie, hwn yw\\\'r cyfeiriad cywir"
        self.content_common_confirm_address_value_no_cy = "Na, rwyf am chwilio am fy nghyfeiriad eto"

        self.content_common_ce_room_number_text = 'Room A8'
        self.content_common_ce_room_number_add_link_en = 'Add flat or room number'
        self.content_common_ce_room_number_change_link_en = 'Change flat or room number'
        self.content_common_enter_room_number_page_title_en = \
            '<title>Enter flat or room number - Census 2021</title>'
        self.content_common_enter_room_number_page_title_error_en = \
            '<title>Error: Enter flat or room number - Census 2021</title>'
        self.content_common_enter_room_number_title_en = 'What is your flat or room number?'
        self.content_common_enter_room_number_empty_en = 'Enter your flat or room number'
        self.content_common_enter_room_number_over_length_en = \
            'You have entered too many characters. Enter up to 10 characters'
        self.content_common_ce_room_number_add_link_cy = "Ychwanegu rhif fflat neu ystafell"
        self.content_common_ce_room_number_change_link_cy = "Newid rhif fflat neu ystafell"
        self.content_common_enter_room_number_page_title_cy = \
            '<title>Nodi rhif fflat neu ystafell - Cyfrifiad 2021</title>'
        self.content_common_enter_room_number_page_title_error_cy = \
            '<title>Gwall: Nodi rhif fflat neu ystafell - Cyfrifiad 2021</title>'
        self.content_common_enter_room_number_title_cy = "Beth yw rhif eich fflat neu ystafell?"
        # TODO: add welsh translation
        self.content_common_enter_room_number_empty_cy = 'Enter your flat or room number'
        # TODO: add welsh translation
        self.content_common_enter_room_number_over_length_cy = \
            'You have entered too many characters. Enter up to 10 characters'

        self.common_room_number_input_valid = {
            'form-enter-room-number': self.content_common_ce_room_number_text, 'action[save_continue]': '',
        }
        self.common_room_number_input_empty = {
            'form-enter-room-number': '', 'action[save_continue]': '',
        }
        self.common_room_number_input_over_length = {
            'form-enter-room-number': 'Room A8, Flat 47', 'action[save_continue]': '',
        }

        self.content_common_register_address_title_en = \
            'Register an address'
        self.content_common_register_address_title_cy = \
            "Cofrestru cyfeiriad"
        self.content_common_register_address_text_en = \
            'If you can\\xe2\\x80\\x99t find your address, it may not be registered on our system.'
        self.content_common_register_address_text_cy = \
            "Os na allwch chi ddod o hyd i\\\'ch cyfeiriad, mae\\\'n bosibl nad yw wedi\\\'i gofrestru ar ein system."
        self.content_common_call_contact_centre_address_linking_en = \
            'There is an issue linking your address via the website.'
        self.content_common_call_contact_centre_address_linking_cy = \
            "Mae problem wrth newid eich cyfeiriad drwy\\\'r wefan."
        self.content_common_call_contact_centre_change_address_en = \
            'There is an issue changing your address via the website.'
        self.content_common_call_contact_centre_change_address_cy = \
            "Mae problem wrth newid eich cyfeiriad drwy\\\'r wefan."

        self.content_common_call_contact_centre_title_en = 'You need to call the Census customer contact centre'
        self.content_common_call_contact_centre_title_cy = \
            "Mae angen i chi ffonio canolfan gyswllt cwsmeriaid y cyfrifiad"

        self.content_common_call_contact_centre_unable_to_match_address_en = \
            'There is an issue processing your address via the website.'
        self.content_common_call_contact_centre_unable_to_match_address_cy = \
            "Mae problem wrth newid eich cyfeiriad drwy\\\'r wefan."

        self.content_common_500_error_en = 'Sorry, something went wrong'
        self.content_common_500_error_cy = "Mae\\'n flin gennym, aeth rhywbeth o\\'i le"

        self.content_common_404_error_title_en = 'Page not found'
        self.content_common_404_error_secondary_en = 'If you entered a web address, check it is correct.'
        self.content_common_404_error_title_cy = "Heb ddod o hyd i\\\'r dudalen"
        self.content_common_404_error_secondary_cy = \
            "Os gwnaethoch nodi cyfeiriad gwefan, gwnewch yn si\\xc5\\xb5r ei fod yn gywir."

        self.content_common_timeout_en = 'Your session has timed out due to inactivity'
        self.content_common_timeout_cy = 'Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch'

        self.content_common_429_error_eq_launch_title_en = \
            'Sorry, there was a problem starting your census'
        self.content_common_429_error_uac_title_en = \
            'You have reached the maximum number of access codes you can request online'
        self.content_common_429_error_paper_questionnaire_title_en = \
            'You have reached the maximum number of paper questionnaires you can request online'
        self.content_common_429_error_continuation_questionnaire_title_en = \
            'You have reached the maximum number of continuation questionnaires you can request online'
        # TODO: add welsh translation
        self.content_common_429_error_eq_launch_title_cy = \
            'Sorry, there was a problem starting your census'
        self.content_common_429_error_uac_title_cy = \
            "Rydych chi wedi cyrraedd y nifer fwyaf o godau mynediad y gallwch ofyn amdanynt ar lein"
        self.content_common_429_error_paper_questionnaire_title_cy = \
            "Rydych chi wedi cyrraedd y nifer fwyaf o holiaduron papur y gallwch ofyn amdanynt ar lein"
        # TODO: add welsh translation
        self.content_common_429_error_continuation_questionnaire_title_cy = \
            'You have reached the maximum number of continuation questionnaires you can request online'

        self.content_common_resident_or_manager_page_title_en = \
            '<title>Confirm resident or manager - Census 2021</title>'
        self.content_common_resident_or_manager_page_title_error_en = \
            '<title>Error: Confirm resident or manager - Census 2021</title>'
        self.content_common_resident_or_manager_title_en = 'Are you a resident or manager of this establishment?'
        self.content_common_resident_or_manager_option_resident_en = 'Resident'
        self.content_common_resident_or_manager_description_resident_en = \
            'Residents are responsible for answering the census questions about themselves'
        self.content_common_resident_or_manager_option_manager_en = 'Manager'
        self.content_common_resident_or_manager_description_manager_en = \
            'A manager is responsible for answering the census questions about this establishment'
        self.content_common_resident_or_manager_error_en = 'Select an answer'
        self.content_common_resident_or_manager_page_title_cy = \
            '<title>Cadarnhau preswylydd neu reolwr - Cyfrifiad 2021</title>'
        self.content_common_resident_or_manager_page_title_error_cy = \
            '<title>Gwall: Cadarnhau preswylydd neu reolwr - Cyfrifiad 2021</title>'
        self.content_common_resident_or_manager_title_cy = "Ai preswylydd neu reolwr ydych chi yn y sefydliad hwn?"
        self.content_common_resident_or_manager_option_resident_cy = "Preswylydd"
        self.content_common_resident_or_manager_description_resident_cy = \
            "Mae preswylwyr yn gyfrifol am ateb cwestiynau\\\'r cyfrifiad amdanyn nhw eu hunain"
        self.content_common_resident_or_manager_option_manager_cy = "Rheolwr"
        self.content_common_resident_or_manager_description_manager_cy = \
            "Mae rheolwr yn gyfrifol am ateb cwestiynau\\\'r cyfrifiad am y sefydliad hwn"
        # TODO: add welsh translation
        self.content_common_resident_or_manager_error_cy = 'Select an answer'

        self.content_common_nisra_ce_manager_title = 'You need to visit the Communal Establishment Manager Portal'

        # End Common

        # Start Journey

        # Content

        self.content_start_exit_button_en = 'href="/en/start/exit/"'
        self.content_start_exit_button_cy = 'href="/cy/start/exit/"'
        self.content_start_exit_button_ni = 'href="/ni/start/exit/"'

        self.content_start_title_en = 'Start census'
        self.content_start_uac_title_en = 'Enter your 16-character access code'
        self.content_start_title_cy = "Dechrau\\\'r cyfrifiad"
        self.content_start_uac_title_cy = "Rhowch god mynediad eich cartref, sy\\\'n cynnwys 16 o nodau"

        self.content_start_uac_expired_en = 'This access code has already been used'
        self.content_start_uac_expired_cy = "Mae\\\'r cod mynediad hwn eisoes wedi cael ei ddefnyddio"

        self.content_start_code_for_northern_ireland_title_en = \
            'This access code is not part of the census for England and Wales'
        # TODO: add welsh translation
        self.content_start_code_for_northern_ireland_title_cy = \
            'This access code is not part of the census for England and Wales'
        self.content_start_code_not_for_northern_ireland_title = \
            'This access code is not part of the census for Northern Ireland'
        self.content_start_code_for_england_and_wales_secondary = \
            'You have entered an access code for the census in England and Wales.'

        self.content_start_confirm_address_page_title_en = '<title>Confirm address - Census 2021</title>'
        self.content_start_confirm_address_page_title_error_en = '<title>Error: Confirm address - Census 2021</title>'
        self.content_start_confirm_address_title_en = 'Is this the correct address?'
        self.content_start_confirm_address_option_yes_en = 'Yes, this is the correct address'
        self.content_start_confirm_address_option_no_en = 'No, this is not the correct address'
        self.content_start_confirm_address_error_en = 'Select an answer'
        self.content_start_confirm_address_page_title_cy = '<title>Cadarnhau cyfeiriad - Cyfrifiad 2021</title>'
        self.content_start_confirm_address_page_title_error_cy = \
            '<title>Gwall: Cadarnhau cyfeiriad - Cyfrifiad 2021</title>'
        self.content_start_confirm_address_title_cy = "Ai hwn yw\\\'r cyfeiriad cywir?"
        self.content_start_confirm_address_option_yes_cy = "Ie, hwn yw\\\'r cyfeiriad cywir"
        self.content_start_confirm_address_option_no_cy = "Na, nid hwn yw\\\'r cyfeiriad cywir"
        # TODO: add welsh translation
        self.content_start_confirm_address_error_cy = 'Select an answer'
        self.content_start_confirm_address_region_warning_cy = \
            'Mae eich cyfeiriad yn Lloegr, felly dim ond yn Saesneg y gallwch chi gwblhau eich cyfrifiad'

        self.content_start_ni_language_options_page_title = \
            '<title>Confirm English or other language - Census 2021</title>'
        self.content_start_ni_language_options_page_title_error = \
            '<title>Error: Confirm English or other language - Census 2021</title>'
        self.content_start_ni_language_options_title = 'Would you like to complete the census in English?'
        self.content_start_ni_language_options_error = 'Select a language option'
        self.content_start_ni_language_options_option_yes = 'Yes, continue in English'

        self.content_start_ni_select_language_page_title = '<title>Choose language - Census 2021</title>'
        self.content_start_ni_select_language_page_title_error = \
            '<title>Error: Choose language - Census 2021</title>'
        self.content_start_ni_select_language_title = 'Choose your language'
        self.content_start_ni_select_language_error = 'Select a language option'
        self.content_start_ni_select_language_option = 'Continue in English'
        self.content_start_ni_select_language_switch_back = 'You can change your language back to English at any time.'

        self.content_signed_out_page_title_en = '<title>Progress saved - Census 2021</title>'
        self.content_signed_out_title_en = 'Your progress has been saved'
        # TODO: add welsh translation
        self.content_signed_out_page_title_cy = '<title>Progress saved - Cyfrifiad 2021</title>'
        self.content_signed_out_title_cy = 'Mae eich cynnydd wedi cael ei gadw'

        self.content_start_forbidden_title_en = 'Sorry, there is a problem'
        self.content_start_timeout_forbidden_link_text_en = 'enter your 16-character access code'
        # TODO: add welsh translation
        self.content_start_forbidden_title_cy = 'Sorry, there is a problem'
        # TODO: add welsh translation
        self.content_start_timeout_forbidden_link_text_cy = 'enter your 16-character access code'

        # End Start Journey

        # Session Timeout

        self.content_timeout_title_en = 'Your session has timed out due to inactivity'
        self.content_timeout_title_cy = 'Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch'
        self.content_timeout_secondary_en = 'To protect your information we have timed you out'
        self.content_start_timeout_secondary_cy = \
            'Er mwyn diogelu eich gwybodaeth, mae eich sesiwn wedi cyrraedd y terfyn amser'
        # Welsh translation for start but not yet request timeout page though identical text. Babel not run since change
        self.content_request_timeout_secondary_cy = \
            'To protect your information we have timed you out'
        self.content_request_timeout_restart_en = 're-enter your postcode'
        self.content_request_timeout_restart_cy = 'nodi eich cod post eto'

        # End Session Timeout

        self.get_start_en = self.app.router['Start:get'].url_for(display_region='en')
        self.get_start_adlocation_valid_en = self.app.router['Start:get'].url_for(display_region='en').with_query(
            {"adlocation": self.adlocation})
        self.get_start_adlocation_invalid_en = self.app.router['Start:get'].url_for(display_region='en').with_query(
            {"adlocation": "invalid"})
        self.post_start_en = self.app.router['Start:post'].url_for(display_region='en')
        self.get_start_confirm_address_en = self.app.router['StartConfirmAddress:get'].url_for(display_region='en')
        self.post_start_confirm_address_en = self.app.router['StartConfirmAddress:post'].url_for(display_region='en')

        self.get_start_cy = self.app.router['Start:get'].url_for(display_region='cy')
        self.get_start_adlocation_valid_cy = self.app.router['Start:get'].url_for(display_region='cy').with_query(
            {"adlocation": self.adlocation})
        self.get_start_adlocation_invalid_cy = self.app.router['Start:get'].url_for(display_region='cy').with_query(
            {"adlocation": "invalid"})
        self.post_start_cy = self.app.router['Start:post'].url_for(display_region='cy')
        self.get_start_confirm_address_cy = self.app.router['StartConfirmAddress:get'].url_for(display_region='cy')
        self.post_start_confirm_address_cy = self.app.router['StartConfirmAddress:post'].url_for(display_region='cy')

        self.get_start_ni = self.app.router['Start:get'].url_for(display_region='ni')
        self.get_start_adlocation_valid_ni = self.app.router['Start:get'].url_for(display_region='ni').with_query(
            {"adlocation": self.adlocation})
        self.get_start_adlocation_invalid_ni = self.app.router['Start:get'].url_for(display_region='ni').with_query(
            {"adlocation": "invalid"})
        self.post_start_ni = self.app.router['Start:post'].url_for(display_region='ni')
        self.get_start_confirm_address_ni = self.app.router['StartConfirmAddress:get'].url_for(display_region='ni')
        self.post_start_confirm_address_ni = self.app.router['StartConfirmAddress:post'].url_for(display_region='ni')

        self.get_start_language_options_ni = self.app.router['StartNILanguageOptions:get'].url_for()
        self.post_start_language_options_ni = self.app.router['StartNILanguageOptions:post'].url_for()
        self.get_start_select_language_ni = self.app.router['StartNISelectLanguage:get'].url_for()
        self.post_start_select_language_ni = self.app.router['StartNISelectLanguage:post'].url_for()

        self.get_signed_out_en = self.app.router['SignedOut:get'].url_for(display_region='en')
        self.get_signed_out_cy = self.app.router['SignedOut:get'].url_for(display_region='cy')
        self.get_signed_out_ni = self.app.router['SignedOut:get'].url_for(display_region='ni')

        self.case_id = self.uac_json_e['caseId']
        self.collection_exercise_id = self.uac_json_e['collectionExerciseId']
        self.eq_id = 'census'
        self.survey = 'CENSUS'
        self.form_type = self.uac_json_e['formType']
        self.jti = str(uuid.uuid4())
        self.uac_code = ''.join([str(n) for n in range(13)])
        self.uac1, self.uac2, self.uac3, self.uac4 = \
            self.uac_code[:4], self.uac_code[4:8], self.uac_code[8:12], self.uac_code[12:]
        self.period_id = '2021'
        self.uac = 'w4nwwpphjjptp7fn'
        self.uac_ce4 = 'ce4fghtykjuiplku'
        self.uacHash = self.uac_json_e['uacHash']
        self.uprn = self.uac_json_e['address']['uprn']
        self.response_id = '111000000092a445af12905967d'
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
            'display_address':
                self.uac_json_e['address']['addressLine1'] + ', ' + self.uac_json_e['address']['addressLine2'],
            'response_id': self.response_id,
            'account_service_url': f'{account_svc_url}{url_path_prefix}/start/',
            'account_service_log_out_url': f'{account_svc_url}{url_path_prefix}/signed-out/',
            'channel': self.channel,
            'user_id': '',
            'questionnaire_id': self.questionnaire_id,
            'eq_id': self.eq_id,
            'period_id': self.period_id,
            'form_type': self.form_type,
            'survey': self.survey
        }

        self.account_service_url = '/start/'
        self.account_service_log_out_url = '/signed-out/'

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
            'uac': self.uac, 'adlocation': self.adlocation, 'action[save_continue]': '',
        }

        self.start_data_ce4 = {
            'uac': self.uac_ce4, 'action[save_continue]': '',
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
        self.address_index_epoch_param = f'?limit={self.aims_postcode_limit}&epoch={aims_epoch}'
        self.address_index_epoch_param_test = f'?limit={self.aims_postcode_limit}&epoch=test'

        self.selected_uprn = '10023122451'
        self.selected_uprn_ni = '187748262'

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

        self.request_code_select_how_to_receive_data_sms = {
            'form-select-method': 'sms', 'action[save_continue]': ''
        }

        self.request_code_select_how_to_receive_data_post = {
            'form-select-method': 'post', 'action[save_continue]': ''
        }

        self.request_code_select_how_to_receive_data_invalid = {
            'form-select-method': 'invalid', 'action[save_continue]': ''
        }

        self.request_code_enter_mobile_form_data_valid = {
            'request-mobile-number': self.mobile_valid, 'action[save_continue]': '',
        }

        self.request_code_enter_mobile_form_data_invalid = {
            'request-mobile-number': self.mobile_invalid_short, 'action[save_continue]': '',
        }

        self.request_code_enter_mobile_form_data_empty = {
            'request-mobile-number': '', 'action[save_continue]': '',
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

        self.request_common_enter_name_form_data_long_surname = {
            'name_first_name': 'Bob', 'name_last_name': 'Bobbington-Fortesque-Smythe',
            'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_no_first = {
            'name_last_name': 'Bobbington', 'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_no_last = {
            'name_first_name': 'Bob', 'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_overlong_firstname = {
            'name_first_name': 'Robert Albert Everest Reginald Bartholomew', 'name_last_name': 'Bobbington',
            'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_overlong_lastname = {
            'name_first_name': 'Bob', 'name_last_name': 'Bobbington-Browning Fortesque-Smythe',
            'action[save_continue]': '',
        }

        self.request_common_confirm_send_by_post_data_yes = {
            'request-name-address-confirmation': 'yes', 'action[save_continue]': ''
        }

        self.request_common_confirm_send_by_post_data_yes_large_print = {
            'request-name-address-confirmation': 'yes',
            'request-name-address-large-print': 'large-print',
            'action[save_continue]': ''
        }

        self.request_common_confirm_send_by_post_data_no = {
            'request-name-address-confirmation': 'no', 'action[save_continue]': ''
        }

        self.request_common_confirm_send_by_post_data_invalid = {
            'request-name-address-confirmation': 'invalid', 'action[save_continue]': ''
        }

        self.content_request_individual_page_title_en = '<title>Request individual access code - Census 2021</title>'
        self.content_request_individual_title_en = 'Request an individual access code'
        self.content_request_individual_secondary_en = 'You can choose to receive your new access code by text or post.'
        self.content_request_individual_page_title_cy = '<title>Gofyn am god mynediad unigol - Cyfrifiad 2021</title>'
        self.content_request_individual_title_cy = "Gofyn am god mynediad unigol"
        self.content_request_individual_secondary_cy = \
            "Gallwch chi ddewis cael eich cod mynediad newydd drwy neges destun neu drwy\\\'r post."

        self.content_request_individual_questionnaire_page_title_en = \
            '<title>Request individual paper questionnaire - Census 2021</title>'
        self.content_request_individual_questionnaire_title_en = 'Request an individual paper questionnaire'
        # TODO: add welsh translation
        self.content_request_individual_questionnaire_page_title_cy = \
            '<title>Request individual paper questionnaire - Cyfrifiad 2021</title>'
        self.content_request_individual_questionnaire_title_cy = "Gofyn am holiadur papur i unigolion"
        self.content_request_individual_questionnaire_secondary_en = \
            'An individual paper questionnaire lets you answer your census questions separately from the people ' \
            'you live with, so they can\\xe2\\x80\\x99t see your answers.'
        self.content_request_individual_questionnaire_secondary_cy = \
            "Mae holiadur papur i unigolion yn eich galluogi chi i ateb eich cwestiynau ar gyfer y cyfrifiad " \
            "ar wah\\xc3\\xa2n i\\\'r bobl rydych chi\\\'n byw gyda nhw, fel na allant weld eich atebion."

        self.content_request_enter_address_page_title_en = '<title>Enter address - Census 2021</title>'
        self.content_request_enter_address_page_title_error_en = '<title>Error: Enter address - Census 2021</title>'
        self.content_request_enter_address_title_en = 'What is your postcode?'
        self.content_request_access_code_enter_address_secondary_en = \
            'To request an access code, we need your address'
        self.content_request_individual_code_enter_address_secondary_en = \
            'To request an individual access code, we need your address'
        self.content_request_enter_address_page_title_cy = '<title>Nodi cyfeiriad - Cyfrifiad 2021</title>'
        self.content_request_enter_address_page_title_error_cy = '<title>Gwall: Nodi cyfeiriad - Cyfrifiad 2021</title>'
        self.content_request_enter_address_title_cy = 'Beth yw eich cod post?'
        self.content_request_access_code_enter_address_secondary_cy = \
            "I ofyn am god mynediad, bydd angen eich cyfeiriad arnom"
        self.content_request_individual_code_enter_address_secondary_cy = \
            'To request an individual access code, we need your address'

        self.content_request_code_select_how_to_receive_individual_response_question_en = \
            'Need to answer separately from your household?'
        self.content_request_code_select_how_to_receive_error_en = 'Select an answer'
        self.content_request_code_select_how_to_receive_secondary_en = 'Select how to send access code'
        self.content_request_code_select_how_to_receive_option_text_en = 'Text message'
        self.content_request_code_select_how_to_receive_option_post_en = 'Post'
        self.content_request_code_select_how_to_receive_option_post_hint_en = \
            'We can only send access codes to the registered household address'
        self.content_request_code_select_how_to_receive_option_post_hint_individual_en = \
            'An unbranded envelope can be addressed to you at the registered household address'
        self.content_request_code_select_how_to_receive_option_post_hint_ce_en = \
            'We can only send access codes to the registered address'
        self.content_request_code_select_how_to_receive_option_post_hint_ce_individual_en = \
            'An unbranded envelope can be addressed to you at the registered address'

        self.content_request_code_select_how_to_receive_individual_response_question_cy = \
            "Angen ateb ar wahân i aelodau eich cartref?"
        # TODO Add Welsh Translation
        self.content_request_code_select_how_to_receive_error_cy = "Select an answer"
        self.content_request_code_select_how_to_receive_secondary_cy = "Dewiswch sut i anfon y cod mynediad"
        self.content_request_code_select_how_to_receive_option_text_cy = "Neges destun"
        self.content_request_code_select_how_to_receive_option_post_cy = "Post"
        self.content_request_code_select_how_to_receive_option_post_hint_cy = \
            "Dim ond i gyfeiriad cofrestredig y cartref y gallwn anfon codau mynediad"
        # TODO Add Welsh Translation
        self.content_request_code_select_how_to_receive_option_post_hint_individual_cy = \
            'An unbranded envelope can be addressed to you at the registered household address'
        # TODO Add Welsh Translation
        self.content_request_code_select_how_to_receive_option_post_hint_ce_cy = \
            "We can only send access codes to the registered address"
        # TODO Add Welsh Translation
        self.content_request_code_select_how_to_receive_option_post_hint_ce_individual_cy = \
            'An unbranded envelope can be addressed to you at the registered address'

        self.content_request_code_select_how_to_receive_household_page_title_en = \
            '<title>Select how to receive household access code - Census 2021</title>'
        self.content_request_code_select_how_to_receive_household_page_title_error_en = \
            '<title>Error: Select how to receive household access code - Census 2021</title>'
        self.content_request_code_select_how_to_receive_household_title_en = \
            'How would you like to receive a new household access code?'
        self.content_request_code_select_how_to_receive_household_page_title_cy = \
            '<title>Dewis sut i gael cod mynediad y cartref - Cyfrifiad 2021</title>'
        self.content_request_code_select_how_to_receive_household_page_title_error_cy = \
            '<title>Gwall: Dewis sut i gael cod mynediad y cartref - Cyfrifiad 2021</title>'
        self.content_request_code_select_how_to_receive_household_title_cy = \
            "Sut hoffech chi gael cod mynediad newydd ar gyfer y cartref?"

        self.content_request_code_select_how_to_receive_individual_page_title_en = \
            '<title>Select how to receive individual access code - Census 2021</title>'
        self.content_request_code_select_how_to_receive_individual_page_title_error_en = \
            '<title>Error: Select how to receive individual access code - Census 2021</title>'
        self.content_request_code_select_how_to_receive_individual_title_en = \
            'How would you like to receive an individual access code?'
        self.content_request_code_select_how_to_receive_individual_page_title_cy = \
            '<title>Dewis sut i anfon cod mynediad unigol - Cyfrifiad 2021</title>'
        self.content_request_code_select_how_to_receive_individual_page_title_error_cy = \
            '<title>Gwall: Dewis sut i anfon cod mynediad unigol - Cyfrifiad 2021</title>'
        self.content_request_code_select_how_to_receive_individual_title_cy = \
            "Sut hoffech chi gael cod mynediad unigol?"

        self.content_request_code_select_how_to_receive_manager_page_title_en = \
            '<title>Select how to receive manager access code - Census 2021</title>'
        self.content_request_code_select_how_to_receive_manager_page_title_error_en = \
            '<title>Error: Select how to receive manager access code - Census 2021</title>'
        self.content_request_code_select_how_to_receive_manager_title_en = \
            'How would you like to receive a new manager access code?'
        self.content_request_code_select_how_to_receive_manager_page_title_cy = \
            '<title>Dewis sut i gael cod mynediad rheolwr - Cyfrifiad 2021</title>'
        self.content_request_code_select_how_to_receive_manager_page_title_error_cy = \
            '<title>Gwall: Dewis sut i gael cod mynediad rheolwr - Cyfrifiad 2021</title>'
        self.content_request_code_select_how_to_receive_manager_title_cy = \
            "Sut hoffech chi gael cod mynediad rheolwr newydd?"

        self.content_request_code_enter_mobile_page_title_en = '<title>Enter mobile number - Census 2021</title>'
        self.content_request_code_enter_mobile_page_title_error_en = \
            '<title>Error: Enter mobile number - Census 2021</title>'
        self.content_request_code_enter_mobile_title_en = 'What is your mobile number?'
        self.content_request_code_enter_mobile_error_empty_en = 'Enter your mobile number'
        self.content_request_code_enter_mobile_error_invalid_en = \
            'Enter a UK mobile number in a valid format, for example, 07700 900345 or +44 7700 900345'
        self.content_request_code_enter_mobile_secondary_en = \
            'This will not be stored and only used once to send the access code'
        self.content_request_code_enter_mobile_page_title_cy = \
            '<title>Nodi rhif ff\\xc3\\xb4n symudol - Cyfrifiad 2021</title>'
        self.content_request_code_enter_mobile_page_title_error_cy = \
            '<title>Gwall: Nodi rhif ff\\xc3\\xb4n symudol - Cyfrifiad 2021</title>'
        self.content_request_code_enter_mobile_title_cy = "Beth yw eich rhif symudol?"
        # TODO Add Welsh Translation
        self.content_request_code_enter_mobile_error_empty_cy = "Enter your mobile number"
        # TODO Add Welsh Translation
        self.content_request_code_enter_mobile_error_invalid_cy = \
            "Enter a UK mobile number in a valid format, for example, 07700 900345 or +44 7700 900345"
        self.content_request_code_enter_mobile_secondary_cy = \
            "Ni chaiff y rhif ei storio a dim ond unwaith i anfon y cod mynediad y caiff ei ddefnyddio"

        self.content_request_code_confirm_send_by_text_page_title_household_en = \
            '<title>Confirm to send household access code by text - Census 2021</title>'
        self.content_request_code_confirm_send_by_text_page_title_household_error_en = \
            '<title>Error: Confirm to send household access code by text - Census 2021</title>'
        self.content_request_code_confirm_send_by_text_page_title_manager_en = \
            '<title>Confirm to send manager access code by text - Census 2021</title>'
        self.content_request_code_confirm_send_by_text_page_title_manager_error_en = \
            '<title>Error: Confirm to send manager access code by text - Census 2021</title>'
        self.content_request_code_confirm_send_by_text_page_title_individual_en = \
            '<title>Confirm to send individual access code by text - Census 2021</title>'
        self.content_request_code_confirm_send_by_text_page_title_individual_error_en = \
            '<title>Error: Confirm to send individual access code by text - Census 2021</title>'
        self.content_request_code_confirm_send_by_text_title_en = 'Is this mobile number correct?'
        self.content_request_code_confirm_send_by_text_error_en = 'Select an answer'
        self.content_request_code_confirm_send_by_text_page_title_household_cy = \
            '<title>Cadarnhau i anfon cod mynediad y cartref drwy neges destun - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_text_page_title_household_error_cy = \
            '<title>Gwall: Cadarnhau i anfon cod mynediad y cartref drwy neges destun - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_text_page_title_manager_cy = \
            '<title>Cadarnhau i anfon cod mynediad rheolwr drwy neges destun - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_text_page_title_manager_error_cy = \
            '<title>Gwall: Cadarnhau i anfon cod mynediad rheolwr drwy neges destun - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_text_page_title_individual_cy = \
            '<title>Cadarnhau i anfon cod mynediad unigol drwy neges destun - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_text_page_title_individual_error_cy = \
            '<title>Gwall: Cadarnhau i anfon cod mynediad unigol drwy neges destun - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_text_title_cy = "Ydy\\xe2\\x80\\x99r rhif symudol hwn yn gywir?"
        # TODO Add Welsh Translation
        self.content_request_code_confirm_send_by_text_error_cy = "Select an answer"

        self.content_request_code_sent_by_text_page_title_household_en = \
            '<title>Household access code has been sent by text - Census 2021</title>'
        self.content_request_code_sent_by_text_page_title_individual_en = \
            '<title>Individual access code has been sent by text - Census 2021</title>'
        self.content_request_code_sent_by_text_page_title_manager_en = \
            '<title>Manager access code has been sent by text - Census 2021</title>'
        self.content_request_code_sent_by_text_title_en = 'A text has been sent to '
        self.content_request_code_sent_by_text_secondary_individual_en = \
            'The text message with an individual access code should arrive soon for you to start your census'
        self.content_request_code_sent_by_text_secondary_manager_en = \
            'The text message with a new manager access code should arrive soon for you to start the census'
        self.content_request_code_sent_by_text_secondary_household_en = \
            'The text message with a new household access code should arrive soon for you to start your census'
        self.content_request_code_sent_by_text_page_title_household_cy = \
            '<title>Mae cod mynediad y cartref wedi cael ei anfon drwy neges destun - Cyfrifiad 2021</title>'
        self.content_request_code_sent_by_text_page_title_individual_cy = \
            '<title>Mae cod mynediad unigol wedi cael ei anfon drwy neges destun - Cyfrifiad 2021</title>'
        self.content_request_code_sent_by_text_page_title_manager_cy = \
            '<title>Mae cod mynediad rheolwr wedi cael ei anfon drwy neges destun - Cyfrifiad 2021</title>'
        self.content_request_code_sent_by_text_title_cy = 'Mae neges destun wedi cael ei hanfon i '
        self.content_request_code_sent_by_text_secondary_individual_cy = \
            "Dylai\\xe2\\x80\\x99r neges destun yn cynnwys cod mynediad unigol gyrraedd yn fuan er mwyn " \
            "i chi ddechrau eich cyfrifiad"
        self.content_request_code_sent_by_text_secondary_manager_cy = \
            'The text message with a new manager access code should arrive soon for you to start the census'
        self.content_request_code_sent_by_text_secondary_household_cy = \
            "Dylai\\xe2\\x80\\x99r neges destun yn cynnwys cod mynediad newydd ar gyfer y cartref gyrraedd " \
            "yn fuan er mwyn i chi ddechrau eich cyfrifiad"

        self.content_request_code_household_page_title_en = \
            '<title>Request new household access code - Census 2021</title>'
        self.content_request_code_household_title_en = 'Request a new household access code'
        self.content_request_code_household_page_title_cy = \
            '<title>Gofyn am god mynediad newydd ar gyfer y cartref - Cyfrifiad 2021</title>'
        self.content_request_code_household_title_cy = "Gofyn am god mynediad newydd ar gyfer eich cartref"

        self.content_request_questionnaire_household_page_title_en = \
            '<title>Request household paper questionnaire - Census 2021</title>'
        self.content_request_questionnaire_household_title_en = 'Request a household paper questionnaire'
        # TODO Add Welsh Translation
        self.content_request_questionnaire_household_page_title_cy = \
            '<title>Request household paper questionnaire - Cyfrifiad 2021</title>'
        self.content_request_questionnaire_household_title_cy = "Gofyn am holiadur papur y cartref"

        self.content_request_questionnaire_people_in_household_title_en = 'How many people are in your household?'
        self.content_request_questionnaire_people_in_household_error_empty_en = \
            'Enter the number of people in your household'
        self.content_request_questionnaire_people_in_household_error_nan_en = 'Enter a number'
        self.content_request_questionnaire_people_in_household_error_number_less_en = \
            'Enter a number less than 31'
        self.content_request_questionnaire_people_in_household_title_cy = "Faint o bobl sydd yn eich cartref?"
        # TODO Add Welsh Translation
        self.content_request_questionnaire_people_in_household_error_empty_cy = \
            'Enter the number of people in your household'
        # TODO Add Welsh Translation
        self.content_request_questionnaire_people_in_household_error_nan_cy = 'Enter a number'
        # TODO: add welsh translation
        self.content_request_questionnaire_people_in_household_error_number_less_cy = \
            'Enter a number less than 31'

        self.content_request_common_enter_name_page_title_en = \
            '<title>Enter name - Census 2021</title>'
        self.content_request_common_enter_name_page_title_error_en = \
            '<title>Error: Enter name - Census 2021</title>'
        self.content_request_common_enter_name_title_en = 'What is your name?'
        self.content_request_common_enter_name_error_first_name_en = 'Enter your first name'
        self.content_request_common_enter_name_error_first_name_overlength_en = \
            "You have entered too many characters. Enter up to 35 characters"
        self.content_request_common_enter_name_error_last_name_en = 'Enter your last name'
        self.content_request_common_enter_name_error_last_name_overlength_en = \
            "You have entered too many characters. Enter up to 35 characters"
        self.content_request_common_enter_name_page_title_cy = \
            '<title>Nodi enw - Cyfrifiad 2021</title>'
        self.content_request_common_enter_name_page_title_error_cy = \
            '<title>Gwall: Nodi enw - Cyfrifiad 2021</title>'
        self.content_request_common_enter_name_title_cy = "Beth yw eich enw?"
        # TODO Add Welsh Translation
        self.content_request_common_enter_name_error_first_name_cy = "Enter your first name"
        # TODO Add Welsh Translation
        self.content_request_common_enter_name_error_first_name_overlength_cy = \
            "You have entered too many characters. Enter up to 35 characters"
        # TODO Add Welsh Translation
        self.content_request_common_enter_name_error_last_name_cy = 'Enter your last name'
        # TODO Add Welsh Translation
        self.content_request_common_enter_name_error_last_name_overlength_cy = \
            "You have entered too many characters. Enter up to 35 characters"

        self.content_request_code_confirm_send_by_post_page_title_individual_en = \
            '<title>Confirm to send individual access code by post - Census 2021</title>'
        self.content_request_code_confirm_send_by_post_page_title_error_individual_en = \
            '<title>Error: Confirm to send individual access code by post - Census 2021</title>'
        self.content_request_code_confirm_send_by_post_page_title_manager_en = \
            '<title>Confirm to send manager access code by post - Census 2021</title>'
        self.content_request_code_confirm_send_by_post_page_title_error_manager_en = \
            '<title>Error: Confirm to send manager access code by post - Census 2021</title>'
        self.content_request_code_confirm_send_by_post_page_title_household_en = \
            '<title>Confirm to send household access code by post - Census 2021</title>'
        self.content_request_code_confirm_send_by_post_page_title_error_household_en = \
            '<title>Error: Confirm to send household access code by post - Census 2021</title>'
        self.content_request_code_confirm_send_by_post_title_individual_en = \
            'Do you want to send an individual access code to this address?'
        self.content_request_code_confirm_send_by_post_title_manager_en = \
            'Do you want to send a new manager access code to this address?'
        self.content_request_code_confirm_send_by_post_title_household_en = \
            'Do you want to send a new household access code to this address?'
        self.content_request_common_confirm_send_by_post_error_en = 'Select an answer'
        self.content_request_code_confirm_send_by_post_individual_message_en = \
            'A letter with your individual access code will arrive in a brown unbranded envelope'
        self.content_request_questionnaire_confirm_send_by_post_individual_message_en = \
            'Your individual paper questionnaire will arrive in a white unbranded envelope'
        self.content_request_code_confirm_send_by_post_option_yes_en = 'Yes, send the access code by post'
        self.content_request_code_confirm_send_by_post_option_no_en = 'No, send it by text message'
        # TODO Add Welsh Translation
        self.content_request_code_confirm_send_by_post_page_title_individual_cy = \
            '<title>Cadarnhau i anfon cod mynediad unigol drwy&#39;r post - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_post_page_title_error_individual_cy = \
            '<title>Gwall: Cadarnhau i anfon cod mynediad unigol drwy&#39;r post - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_post_page_title_manager_cy = \
            '<title>Cadarnhau i anfon cod mynediad rheolwr drwy&#39;r post - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_post_page_title_error_manager_cy = \
            '<title>Gwall: Cadarnhau i anfon cod mynediad rheolwr drwy&#39;r post - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_post_page_title_household_cy = \
            '<title>Cadarnhau i anfon cod mynediad y cartref drwy&#39;r post - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_post_page_title_error_household_cy = \
            '<title>Gwall: Cadarnhau i anfon cod mynediad y cartref drwy&#39;r post - Cyfrifiad 2021</title>'
        self.content_request_code_confirm_send_by_post_title_individual_cy = \
            "Ydych chi am anfon cod mynediad unigol i\\\'r cyfeiriad hwn?"
        self.content_request_code_confirm_send_by_post_title_manager_cy = \
            "Ydych chi am anfon cod mynediad rheolwr newydd i\\\'r cyfeiriad hwn?"
        self.content_request_code_confirm_send_by_post_title_household_cy = \
            "Ydych chi am anfon cod mynediad newydd ar gyfer y cartref i\\\'r cyfeiriad hwn?"
        # TODO Add Welsh Translation
        self.content_request_common_confirm_send_by_post_error_cy = \
            "Select an answer"
        self.content_request_code_confirm_send_by_post_individual_message_cy = \
            "Bydd llythyr yn cynnwys cod mynediad unigol yn cyrraedd mewn amlen blaen frown"
        self.content_request_questionnaire_confirm_send_by_post_individual_message_cy = \
            "Bydd eich holiadur papur i unigolion yn cyrraedd mewn amlen blaen wen"
        self.content_request_code_confirm_send_by_post_option_yes_cy = "Ydw, anfonwch y cod mynediad drwy\\\'r post"
        # TODO Add Welsh Translation
        self.content_request_code_confirm_send_by_post_option_no_cy = 'No, send it by text message'

        self.content_request_code_sent_by_post_page_title_household_en = \
            '<title>Household access code will be sent by post - Census 2021</title>'
        self.content_request_code_sent_by_post_page_title_manager_en = \
            '<title>Manager access code will be sent by post - Census 2021</title>'
        self.content_request_code_sent_by_post_page_title_individual_en = \
            '<title>Individual access code will be sent by post - Census 2021</title>'
        self.content_request_code_sent_post_title_en = \
            'A letter will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        self.content_request_code_sent_post_title_ce_en = \
            'A letter will be sent to Bob Bobbington at Halls Of Residence, Cumbria College Of Art &amp; Design'
        self.content_request_code_sent_post_title_ce_with_room_en = \
            'A letter will be sent to Bob Bobbington, Room A8 at Halls Of Residence, ' \
            'Cumbria College Of Art &amp; Design'
        self.content_request_code_sent_post_title_ce_with_room_long_surname_en = \
            'A letter will be sent to Room A8 Bob Bobbington-Fortesque-Smythe ' \
            'at Halls Of Residence, Cumbria College Of Art &amp; Design'
        self.content_request_code_sent_post_secondary_individual_en = \
            'The letter with an individual access code should arrive soon for you to start the census'
        self.content_request_code_sent_post_secondary_manager_en = \
            'The letter with a new manager access code should arrive soon for you to start the census'
        self.content_request_code_sent_post_secondary_household_en = \
            'The letter with a new household access code should arrive soon for you to start the census'
        self.content_request_code_sent_by_post_page_title_household_cy = \
            '<title>Caiff cod mynediad y cartref ei anfon drwy&#39;r post - Cyfrifiad 2021</title>'
        self.content_request_code_sent_by_post_page_title_manager_cy = \
            '<title>Caiff cod mynediad rheolwr ei anfon drwy&#39;r post - Cyfrifiad 2021</title>'
        self.content_request_code_sent_by_post_page_title_individual_cy = \
            '<title>Caiff cod mynediad unigol ei anfon drwy&#39;r post - Cyfrifiad 2021</title>'
        self.content_request_code_sent_post_title_cy = \
            'Caiff llythyr ei anfon at Bob Bobbington yn 1 Gate Reach, Exeter'
        self.content_request_code_sent_post_title_ce_cy = \
            "Caiff llythyr ei anfon at Bob Bobbington yn Halls Of Residence, Cumbria College Of Art &amp; Design"
        self.content_request_code_sent_post_title_ce_with_room_cy = \
            "Caiff llythyr ei anfon at Bob Bobbington, Room A8 yn Halls Of Residence, " \
            "Cumbria College Of Art &amp; Design"
        self.content_request_code_sent_post_title_ce_with_room_long_surname_cy = \
            "Caiff llythyr ei anfon at Room A8 Bob Bobbington-Fortesque-Smythe " \
            "yn Halls Of Residence, Cumbria College Of Art &amp; Design"
        self.content_request_code_sent_post_secondary_individual_cy = \
            "Dylai\\xe2\\x80\\x99r llythyr yn cynnwys cod mynediad unigol gyrraedd yn fuan " \
            "er mwyn i chi ddechrau\\\'r cyfrifiad"
        self.content_request_code_sent_post_secondary_manager_cy = \
            "Dylai\\xe2\\x80\\x99r llythyr yn cynnwys cod mynediad rheolwr newydd gyrraedd yn fuan er " \
            "mwyn i chi ddechrau\\\'r cyfrifiad"
        self.content_request_code_sent_post_secondary_household_cy = \
            "Dylai\\xe2\\x80\\x99r llythyr yn cynnwys cod mynediad newydd ar gyfer y cartref gyrraedd " \
            "yn fuan er mwyn i chi ddechrau\\\'r cyfrifiad"
        self.content_request_code_sent_post_title_ni = \
            'A letter will be sent to Bob Bobbington at 27 Kings Road, Whitehead'

        self.content_request_contact_centre_en = 'You need to call the Census customer contact centre'
        # TODO: add welsh translation
        self.content_request_contact_centre_cy = 'You need to call the Census customer contact centre'

        self.content_request_timeout_error_en = 're-enter your postcode'
        self.content_request_timeout_error_cy = 'nodi eich cod post eto'

        # Unlinked/Link Address UACs

        # URLs
        self.get_start_link_address_enter_address_en = \
            self.app.router['CommonEnterAddress:get'].url_for(display_region='en', user_journey='start',
                                                              sub_user_journey='link-address')
        self.get_start_link_address_enter_address_cy = \
            self.app.router['CommonEnterAddress:get'].url_for(display_region='cy', user_journey='start',
                                                              sub_user_journey='link-address')
        self.get_start_link_address_enter_address_ni = \
            self.app.router['CommonEnterAddress:get'].url_for(display_region='ni', user_journey='start',
                                                              sub_user_journey='link-address')
        self.post_start_link_address_enter_address_en = \
            self.app.router['CommonEnterAddress:post'].url_for(display_region='en', user_journey='start',
                                                               sub_user_journey='link-address')
        self.post_start_link_address_enter_address_cy = \
            self.app.router['CommonEnterAddress:post'].url_for(display_region='cy', user_journey='start',
                                                               sub_user_journey='link-address')
        self.post_start_link_address_enter_address_ni = \
            self.app.router['CommonEnterAddress:post'].url_for(display_region='ni', user_journey='start',
                                                               sub_user_journey='link-address')

        self.get_start_link_address_select_address_en = \
            self.app.router['CommonSelectAddress:get'].url_for(display_region='en', user_journey='start',
                                                               sub_user_journey='link-address')
        self.get_start_link_address_select_address_cy = \
            self.app.router['CommonSelectAddress:get'].url_for(display_region='cy', user_journey='start',
                                                               sub_user_journey='link-address')
        self.get_start_link_address_select_address_ni = \
            self.app.router['CommonSelectAddress:get'].url_for(display_region='ni', user_journey='start',
                                                               sub_user_journey='link-address')
        self.post_start_link_address_select_address_en = \
            self.app.router['CommonSelectAddress:post'].url_for(display_region='en', user_journey='start',
                                                                sub_user_journey='link-address')
        self.post_start_link_address_select_address_cy = \
            self.app.router['CommonSelectAddress:post'].url_for(display_region='cy', user_journey='start',
                                                                sub_user_journey='link-address')
        self.post_start_link_address_select_address_ni = \
            self.app.router['CommonSelectAddress:post'].url_for(display_region='ni', user_journey='start',
                                                                sub_user_journey='link-address')

        self.get_start_link_address_confirm_address_en = \
            self.app.router['CommonConfirmAddress:get'].url_for(display_region='en', user_journey='start',
                                                                sub_user_journey='link-address')
        self.get_start_link_address_confirm_address_cy = \
            self.app.router['CommonConfirmAddress:get'].url_for(display_region='cy', user_journey='start',
                                                                sub_user_journey='link-address')
        self.get_start_link_address_confirm_address_ni = \
            self.app.router['CommonConfirmAddress:get'].url_for(display_region='ni', user_journey='start',
                                                                sub_user_journey='link-address')
        self.post_start_link_address_confirm_address_en = \
            self.app.router['CommonConfirmAddress:post'].url_for(display_region='en', user_journey='start',
                                                                 sub_user_journey='link-address')
        self.post_start_link_address_confirm_address_cy = \
            self.app.router['CommonConfirmAddress:post'].url_for(display_region='cy', user_journey='start',
                                                                 sub_user_journey='link-address')
        self.post_start_link_address_confirm_address_ni = \
            self.app.router['CommonConfirmAddress:post'].url_for(display_region='ni', user_journey='start',
                                                                 sub_user_journey='link-address')

        # Test Data
        with open('tests/test_data/rhsvc/uac_unlinked_e.json') as fp:
            self.link_address_uac_json_e = json.load(fp)
        with open('tests/test_data/rhsvc/uac_unlinked_w.json') as fp:
            self.link_address_uac_json_w = json.load(fp)
        with open('tests/test_data/rhsvc/uac_unlinked_n.json') as fp:
            self.link_address_uac_json_n = json.load(fp)

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
        self.content_start_link_address_enter_address_question_title_en = 'What is your postcode?'
        # TODO: add welsh translation
        self.content_start_link_address_enter_address_question_title_cy = 'Beth yw eich cod post?'

        self.content_link_address_timeout_error_en = 'enter your 16-character access code'
        # TODO: add welsh translation
        self.content_link_address_timeout_error_cy = 'enter your 16-character access code'

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

        self.content_start_change_address_timeout_error_en = 're-enter your access code'
        self.content_start_change_address_timeout_error_cy = 'nodi eich cod mynediad eto'

        # Start Request Access Code

        # URLs

        self.get_request_access_code_enter_address_en = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_access_code_enter_address_cy = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_access_code_enter_address_ni = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_enter_address_en = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_enter_address_cy = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_enter_address_ni = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )

        self.get_request_access_code_select_address_en = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_access_code_select_address_cy = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_access_code_select_address_ni = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_select_address_en = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_select_address_cy = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_select_address_ni = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )

        self.get_request_access_code_confirm_address_en = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_access_code_confirm_address_cy = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_access_code_confirm_address_ni = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_confirm_address_en = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_confirm_address_cy = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_confirm_address_ni = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )

        self.get_request_access_code_enter_room_number_en = self.app.router['CommonEnterRoomNumber:get'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_access_code_enter_room_number_cy = self.app.router['CommonEnterRoomNumber:get'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_access_code_enter_room_number_ni = self.app.router['CommonEnterRoomNumber:get'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_enter_room_number_en = self.app.router['CommonEnterRoomNumber:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_enter_room_number_cy = self.app.router['CommonEnterRoomNumber:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_enter_room_number_ni = self.app.router['CommonEnterRoomNumber:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )

        self.post_request_access_code_resident_or_manager_en = self.app.router['CommonCEMangerQuestion:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_resident_or_manager_cy = self.app.router['CommonCEMangerQuestion:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_resident_or_manager_ni = self.app.router['CommonCEMangerQuestion:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )

        self.get_request_access_code_select_how_to_receive_en = \
            self.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                request_type='access-code', display_region='en'
            )
        self.get_request_access_code_select_how_to_receive_cy = \
            self.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                request_type='access-code', display_region='cy'
            )
        self.get_request_access_code_select_how_to_receive_ni = \
            self.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                request_type='access-code', display_region='ni'
            )
        self.post_request_access_code_select_how_to_receive_en = \
            self.app.router['RequestCodeSelectHowToReceive:post'].url_for(
                request_type='access-code', display_region='en'
            )
        self.post_request_access_code_select_how_to_receive_cy = \
            self.app.router['RequestCodeSelectHowToReceive:post'].url_for(
                request_type='access-code', display_region='cy'
            )
        self.post_request_access_code_select_how_to_receive_ni = \
            self.app.router['RequestCodeSelectHowToReceive:post'].url_for(
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

        self.get_request_access_code_confirm_send_by_text_en = \
            self.app.router['RequestCodeConfirmSendByText:get'].url_for(request_type='access-code', display_region='en')
        self.get_request_access_code_confirm_send_by_text_cy = \
            self.app.router['RequestCodeConfirmSendByText:get'].url_for(request_type='access-code', display_region='cy')
        self.get_request_access_code_confirm_send_by_text_ni = \
            self.app.router['RequestCodeConfirmSendByText:get'].url_for(request_type='access-code', display_region='ni')
        self.post_request_access_code_confirm_send_by_text_en = \
            self.app.router['RequestCodeConfirmSendByText:post'].url_for(request_type='access-code',
                                                                         display_region='en')
        self.post_request_access_code_confirm_send_by_text_cy = \
            self.app.router['RequestCodeConfirmSendByText:post'].url_for(request_type='access-code',
                                                                         display_region='cy')
        self.post_request_access_code_confirm_send_by_text_ni = \
            self.app.router['RequestCodeConfirmSendByText:post'].url_for(request_type='access-code',
                                                                         display_region='ni')

        self.post_request_access_code_enter_name_en = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='access-code', display_region='en'
        )
        self.post_request_access_code_enter_name_cy = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.post_request_access_code_enter_name_ni = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='access-code', display_region='ni'
        )

        self.post_request_access_code_confirm_send_by_post_en = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='access-code',
                                                                           display_region='en')
        self.post_request_access_code_confirm_send_by_post_cy = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='access-code',
                                                                           display_region='cy')
        self.post_request_access_code_confirm_send_by_post_ni = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='access-code',
                                                                           display_region='ni')

        # Start Request Individual Code

        # URLs

        self.get_request_individual_code_en = self.app.router['RequestCodeIndividual:get'].url_for(
            request_type='access-code', display_region='en'
        )
        self.get_request_individual_code_cy = self.app.router['RequestCodeIndividual:get'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.get_request_individual_code_ni = self.app.router['RequestCodeIndividual:get'].url_for(
            request_type='access-code', display_region='ni'
        )

        self.get_request_individual_form_en = self.app.router['RequestIndividualForm:get'].url_for(
            request_type='paper-questionnaire', display_region='en'
        )
        self.get_request_individual_form_cy = self.app.router['RequestIndividualForm:get'].url_for(
            request_type='paper-questionnaire', display_region='cy'
        )
        self.get_request_individual_form_ni = self.app.router['RequestIndividualForm:get'].url_for(
            request_type='paper-questionnaire', display_region='ni'
        )

        self.post_request_individual_code_en = self.app.router['RequestCodeIndividual:post'].url_for(
            request_type='access-code', display_region='en'
        )
        self.post_request_individual_code_cy = self.app.router['RequestCodeIndividual:post'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.post_request_individual_code_ni = self.app.router['RequestCodeIndividual:post'].url_for(
            request_type='access-code', display_region='ni'
        )

        self.post_request_individual_form_en = self.app.router['RequestIndividualForm:post'].url_for(
            request_type='paper-questionnaire', display_region='en'
        )
        self.post_request_individual_form_cy = self.app.router['RequestIndividualForm:post'].url_for(
            request_type='paper-questionnaire', display_region='cy'
        )
        self.post_request_individual_form_ni = self.app.router['RequestIndividualForm:post'].url_for(
            request_type='paper-questionnaire', display_region='ni'
        )

        self.get_request_individual_code_enter_address_en = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_individual_code_enter_address_cy = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_individual_code_enter_address_ni = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_individual_code_enter_address_en = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_individual_code_enter_address_cy = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_individual_code_enter_address_ni = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )

        self.get_request_individual_code_select_address_en = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_individual_code_select_address_cy = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_individual_code_select_address_ni = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_individual_code_select_address_en = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_individual_code_select_address_cy = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_individual_code_select_address_ni = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )

        self.get_request_individual_code_confirm_address_en = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_individual_code_confirm_address_cy = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.get_request_individual_code_confirm_address_ni = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_individual_code_confirm_address_en = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_individual_code_confirm_address_cy = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_individual_code_confirm_address_ni = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )

        self.get_request_individual_code_select_how_to_receive_en = \
            self.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                request_type='access-code', display_region='en'
            )
        self.get_request_individual_code_select_how_to_receive_cy = \
            self.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                request_type='access-code', display_region='cy'
            )
        self.get_request_individual_code_select_how_to_receive_ni = \
            self.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                request_type='access-code', display_region='ni'
            )
        self.post_request_individual_code_select_how_to_receive_en = \
            self.app.router['RequestCodeSelectHowToReceive:post'].url_for(
                request_type='access-code', display_region='en'
            )
        self.post_request_individual_code_select_how_to_receive_cy = \
            self.app.router['RequestCodeSelectHowToReceive:post'].url_for(
                request_type='access-code', display_region='cy'
            )
        self.post_request_individual_code_select_how_to_receive_ni = \
            self.app.router['RequestCodeSelectHowToReceive:post'].url_for(
                request_type='access-code', display_region='ni'
            )

        self.get_request_individual_code_enter_mobile_en = self.app.router['RequestCodeEnterMobile:get'].url_for(
            request_type='access-code', display_region='en'
        )
        self.get_request_individual_code_enter_mobile_cy = self.app.router['RequestCodeEnterMobile:get'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.get_request_individual_code_enter_mobile_ni = self.app.router['RequestCodeEnterMobile:get'].url_for(
            request_type='access-code', display_region='ni'
        )
        self.post_request_individual_code_enter_mobile_en = self.app.router['RequestCodeEnterMobile:post'].url_for(
            request_type='access-code', display_region='en'
        )
        self.post_request_individual_code_enter_mobile_cy = self.app.router['RequestCodeEnterMobile:post'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.post_request_individual_code_enter_mobile_ni = self.app.router['RequestCodeEnterMobile:post'].url_for(
            request_type='access-code', display_region='ni'
        )

        self.get_request_individual_code_confirm_send_by_text_en = \
            self.app.router['RequestCodeConfirmSendByText:get'].url_for(request_type='access-code', display_region='en')
        self.get_request_individual_code_confirm_send_by_text_cy = \
            self.app.router['RequestCodeConfirmSendByText:get'].url_for(request_type='access-code', display_region='cy')
        self.get_request_individual_code_confirm_send_by_text_ni = \
            self.app.router['RequestCodeConfirmSendByText:get'].url_for(request_type='access-code', display_region='ni')
        self.post_request_individual_code_confirm_send_by_text_en = \
            self.app.router['RequestCodeConfirmSendByText:post'].url_for(request_type='access-code',
                                                                         display_region='en')
        self.post_request_individual_code_confirm_send_by_text_cy = \
            self.app.router['RequestCodeConfirmSendByText:post'].url_for(request_type='access-code',
                                                                         display_region='cy')
        self.post_request_individual_code_confirm_send_by_text_ni = \
            self.app.router['RequestCodeConfirmSendByText:post'].url_for(request_type='access-code',
                                                                         display_region='ni')

        self.post_request_individual_code_enter_name_en = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='access-code', display_region='en'
        )
        self.post_request_individual_code_enter_name_cy = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='access-code', display_region='cy'
        )
        self.post_request_individual_code_enter_name_ni = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='access-code', display_region='ni'
        )

        self.post_request_individual_form_enter_name_en = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='paper-questionnaire', display_region='en'
        )
        self.post_request_individual_form_enter_name_cy = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='paper-questionnaire', display_region='cy'
        )
        self.post_request_individual_form_enter_name_ni = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='paper-questionnaire', display_region='ni'
        )

        self.post_request_individual_code_confirm_send_by_post_en = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='access-code',
                                                                           display_region='en')
        self.post_request_individual_code_confirm_send_by_post_cy = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='access-code',
                                                                           display_region='cy')
        self.post_request_individual_code_confirm_send_by_post_ni = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='access-code',
                                                                           display_region='ni')

        self.post_request_individual_form_confirm_send_by_post_en = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='paper-questionnaire',
                                                                           display_region='en')
        self.post_request_individual_form_confirm_send_by_post_cy = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='paper-questionnaire',
                                                                           display_region='cy')
        self.post_request_individual_form_confirm_send_by_post_ni = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='paper-questionnaire',
                                                                           display_region='ni')

        # Start Request Paper Questionnaire

        # URLs

        self.get_request_paper_questionnaire_enter_address_en = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='en', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.get_request_paper_questionnaire_enter_address_cy = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.get_request_paper_questionnaire_enter_address_ni = self.app.router['CommonEnterAddress:get'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.post_request_paper_questionnaire_enter_address_en = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.post_request_paper_questionnaire_enter_address_cy = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.post_request_paper_questionnaire_enter_address_ni = self.app.router['CommonEnterAddress:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='paper-questionnaire'
        )

        self.get_request_paper_questionnaire_select_address_en = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='en', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.get_request_paper_questionnaire_select_address_cy = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.get_request_paper_questionnaire_select_address_ni = self.app.router['CommonSelectAddress:get'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.post_request_paper_questionnaire_select_address_en = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.post_request_paper_questionnaire_select_address_cy = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.post_request_paper_questionnaire_select_address_ni = self.app.router['CommonSelectAddress:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='paper-questionnaire'
        )

        self.get_request_paper_questionnaire_confirm_address_en = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='en', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.get_request_paper_questionnaire_confirm_address_cy = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.get_request_paper_questionnaire_confirm_address_ni = self.app.router['CommonConfirmAddress:get'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.post_request_paper_questionnaire_confirm_address_en = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.post_request_paper_questionnaire_confirm_address_cy = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='paper-questionnaire'
        )
        self.post_request_paper_questionnaire_confirm_address_ni = self.app.router['CommonConfirmAddress:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='paper-questionnaire'
        )

        self.get_request_paper_questionnaire_enter_room_number_en = \
            self.app.router['CommonEnterRoomNumber:get'].url_for(
                display_region='en', user_journey='request', sub_user_journey='paper-questionnaire'
            )
        self.get_request_paper_questionnaire_enter_room_number_cy = \
            self.app.router['CommonEnterRoomNumber:get'].url_for(
                display_region='cy', user_journey='request', sub_user_journey='paper-questionnaire'
            )
        self.get_request_paper_questionnaire_enter_room_number_ni = \
            self.app.router['CommonEnterRoomNumber:get'].url_for(
                display_region='ni', user_journey='request', sub_user_journey='paper-questionnaire'
            )
        self.post_request_paper_questionnaire_enter_room_number_en = \
            self.app.router['CommonEnterRoomNumber:post'].url_for(
                display_region='en', user_journey='request', sub_user_journey='paper-questionnaire'
            )
        self.post_request_paper_questionnaire_enter_room_number_cy = \
            self.app.router['CommonEnterRoomNumber:post'].url_for(
                display_region='cy', user_journey='request', sub_user_journey='paper-questionnaire'
            )
        self.post_request_paper_questionnaire_enter_room_number_ni = \
            self.app.router['CommonEnterRoomNumber:post'].url_for(
                display_region='ni', user_journey='request', sub_user_journey='paper-questionnaire'
            )

        self.post_request_access_code_household_en = self.app.router['RequestCodeHousehold:post'].url_for(
            display_region='en', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_household_cy = self.app.router['RequestCodeHousehold:post'].url_for(
            display_region='cy', user_journey='request', sub_user_journey='access-code'
        )
        self.post_request_access_code_household_ni = self.app.router['RequestCodeHousehold:post'].url_for(
            display_region='ni', user_journey='request', sub_user_journey='access-code'
        )

        self.post_request_paper_questionnaire_household_en = \
            self.app.router['RequestHouseholdForm:post'].url_for(
                display_region='en', user_journey='request', sub_user_journey='paper-questionnaire'
            )
        self.post_request_paper_questionnaire_household_cy = \
            self.app.router['RequestHouseholdForm:post'].url_for(
                display_region='cy', user_journey='request', sub_user_journey='paper-questionnaire'
            )
        self.post_request_paper_questionnaire_household_ni = \
            self.app.router['RequestHouseholdForm:post'].url_for(
                display_region='ni', user_journey='request', sub_user_journey='paper-questionnaire'
            )

        self.post_request_paper_questionnaire_people_in_household_en = \
            self.app.router['RequestCommonPeopleInHousehold:post'].url_for(
                display_region='en', user_journey='request', request_type='paper-questionnaire'
            )
        self.post_request_paper_questionnaire_people_in_household_cy = \
            self.app.router['RequestCommonPeopleInHousehold:post'].url_for(
                display_region='cy', user_journey='request', request_type='paper-questionnaire'
            )
        self.post_request_paper_questionnaire_people_in_household_ni = \
            self.app.router['RequestCommonPeopleInHousehold:post'].url_for(
                display_region='ni', user_journey='request', request_type='paper-questionnaire'
            )

        self.post_request_paper_questionnaire_resident_or_manager_en = \
            self.app.router['CommonCEMangerQuestion:post'].url_for(
                display_region='en', user_journey='request', sub_user_journey='paper-questionnaire'
            )
        self.post_request_paper_questionnaire_resident_or_manager_cy = \
            self.app.router['CommonCEMangerQuestion:post'].url_for(
                display_region='cy', user_journey='request', sub_user_journey='paper-questionnaire'
            )
        self.post_request_paper_questionnaire_resident_or_manager_ni = \
            self.app.router['CommonCEMangerQuestion:post'].url_for(
                display_region='ni', user_journey='request', sub_user_journey='paper-questionnaire'
            )

        self.post_request_paper_questionnaire_enter_name_en = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='paper-questionnaire', display_region='en'
        )
        self.post_request_paper_questionnaire_enter_name_cy = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='paper-questionnaire', display_region='cy'
        )
        self.post_request_paper_questionnaire_enter_name_ni = self.app.router['RequestCommonEnterName:post'].url_for(
            request_type='paper-questionnaire', display_region='ni'
        )

        self.post_request_paper_questionnaire_confirm_send_by_post_en = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='paper-questionnaire',
                                                                           display_region='en')
        self.post_request_paper_questionnaire_confirm_send_by_post_cy = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='paper-questionnaire',
                                                                           display_region='cy')
        self.post_request_paper_questionnaire_confirm_send_by_post_ni = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='paper-questionnaire',
                                                                           display_region='ni')

        # Content

        self.content_request_paper_questionnaire_enter_address_secondary_en = \
            'To send a paper census questionnaire, we need your address'
        self.content_request_paper_questionnaire_enter_address_secondary_cy = \
            "I anfon holiadur papur y cyfrifiad, bydd angen eich cyfeiriad arnom"

        self.content_request_questionnaire_sent_post_page_title_en = \
            '<title>Household paper questionnaire will be sent - Census 2021</title>'
        self.content_request_questionnaire_sent_post_individual_page_title_en = \
            '<title>Individual paper questionnaire will be sent - Census 2021</title>'
        self.content_request_questionnaire_sent_post_page_title_large_print_en = \
            '<title>Large-print household paper questionnaire will be sent - Census 2021</title>'
        self.content_request_questionnaire_sent_post_individual_page_title_large_print_en = \
            '<title>Large-print individual paper questionnaire will be sent - Census 2021</title>'
        self.content_request_questionnaire_sent_post_title_en = \
            'A household paper questionnaire will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        self.content_request_questionnaire_sent_post_individual_title_en = \
            'An individual paper questionnaire will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        self.content_request_questionnaire_sent_post_title_large_print_en = \
            'A large-print household paper questionnaire will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        self.content_request_questionnaire_sent_post_individual_title_large_print_en = \
            'A large-print individual paper questionnaire will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        self.content_request_questionnaire_sent_post_title_ce_en = \
            'A household paper questionnaire will be sent to Bob Bobbington at Halls Of Residence, ' \
            'Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_post_individual_title_ce_en = \
            'An individual paper questionnaire will be sent to Bob Bobbington at Halls Of Residence, ' \
            'Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_post_title_ce_with_room_en = \
            'A household paper questionnaire will be sent to Bob Bobbington, Room A8 at Halls Of Residence, ' \
            'Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_indi_title_ce_room_en = \
            'An individual paper questionnaire will be sent to Bob Bobbington, Room A8 at Halls Of Residence, ' \
            'Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_title_ce_room_long_last_en = \
            'A household paper questionnaire will be sent to Bob Bobbington-Fortesque-Smythe, ' \
            'Room A8 at Halls Of Residence, Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_indi_title_ce_room_long_last_en = \
            'An individual paper questionnaire will be sent to Room A8 Bob Bobbington-Fortesque-Smythe ' \
            'at Halls Of Residence, Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_post_title_large_print_ce_en = \
            'A large-print household paper questionnaire will be sent to Bob Bobbington at Halls Of Residence, ' \
            'Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_post_individual_title_large_print_ce_en = \
            'A large-print individual paper questionnaire will be sent to Bob Bobbington at Halls Of Residence, ' \
            'Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_title_large_print_ce_room_en = \
            'A large-print household paper questionnaire will be sent to Bob Bobbington, ' \
            'Room A8 at Halls Of Residence, Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_indi_title_lp_ce_room_en = \
            'A large-print individual paper questionnaire will be sent to Bob Bobbington, ' \
            'Room A8 at Halls Of Residence, Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_post_title_lp_ce_with_room_long_last_en = \
            'A large-print household paper questionnaire will be sent to Bob Bobbington-Fortesque-Smythe, ' \
            'Room A8 at Halls Of Residence, Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_post_secondary_en = \
            'This should arrive soon for you to complete your census'

        # TODO: add welsh translation
        self.content_request_questionnaire_sent_post_page_title_cy = \
            '<title>Household paper questionnaire will be sent - Cyfrifiad 2021</title>'
        # TODO: add welsh translation
        self.content_request_questionnaire_sent_post_individual_page_title_cy = \
            '<title>Individual paper questionnaire will be sent - Cyfrifiad 2021</title>'
        # TODO: add welsh translation
        self.content_request_questionnaire_sent_post_page_title_large_print_cy = \
            '<title>Large-print household paper questionnaire will be sent - Cyfrifiad 2021</title>'
        # TODO: add welsh translation
        self.content_request_questionnaire_sent_post_individual_page_title_large_print_cy = \
            '<title>Large-print individual paper questionnaire will be sent - Cyfrifiad 2021</title>'
        self.content_request_questionnaire_sent_post_title_cy = \
            "Caiff holiadur papur y cartref ei anfon at Bob Bobbington yn 1 Gate Reach, Exeter"
        self.content_request_questionnaire_sent_post_individual_title_cy = \
            "Caiff holiadur papur i unigolion ei anfon at Bob Bobbington yn 1 Gate Reach, Exeter"
        self.content_request_questionnaire_sent_post_title_large_print_cy = \
            "Caiff copi print mawr o holiadur papur y cartref ei anfon at Bob Bobbington yn 1 Gate Reach, Exeter"
        self.content_request_questionnaire_sent_post_individual_title_large_print_cy = \
            "Caiff copi print mawr o\\\'r holiadur papur i unigolion ei anfon at Bob Bobbington yn 1 Gate Reach, Exeter"
        self.content_request_questionnaire_sent_post_title_ce_cy = \
            'Caiff holiadur papur y cartref ei anfon at Bob Bobbington yn Halls Of Residence, ' \
            'Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_post_individual_title_ce_cy = \
            'Caiff holiadur papur i unigolion ei anfon at Bob Bobbington yn Halls Of Residence, ' \
            'Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_title_ce_with_room_cy = \
            "Caiff holiadur papur y cartref ei anfon at Bob Bobbington, Room A8 yn Halls Of Residence, " \
            "Cumbria College Of Art &amp; Design"
        self.content_request_questionnaire_sent_individual_title_ce_with_room_cy = \
            'Caiff holiadur papur i unigolion ei anfon at Bob Bobbington, Room A8 yn Halls Of Residence, ' \
            'Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_title_ce_with_room_long_last_cy = \
            'Caiff holiadur papur y cartref ei anfon at Bob Bobbington-Fortesque-Smythe, ' \
            'Room A8 yn Halls Of Residence, Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_indi_title_ce_room_long_last_cy = \
            'Caiff holiadur papur i unigolion ei anfon at Room A8 Bob Bobbington-Fortesque-Smythe ' \
            'yn Halls Of Residence, Cumbria College Of Art &amp; Design'
        # TODO: add welsh translation
        self.content_request_questionnaire_sent_post_title_large_print_ce_cy = \
            'A large-print household paper questionnaire will be sent to Bob Bobbington at Halls Of Residence, ' \
            'Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_post_individual_title_large_print_ce_cy = \
            "Caiff copi print mawr o\\\'r holiadur papur i unigolion ei anfon at Bob Bobbington yn " \
            "Halls Of Residence, Cumbria College Of Art &amp; Design"
        # TODO: add welsh translation
        self.content_request_questionnaire_sent_title_lp_ce_room_cy = \
            "A large-print household paper questionnaire will be sent to Bob Bobbington, Room A8 at " \
            "Halls Of Residence, Cumbria College Of Art &amp; Design"
        self.content_request_questionnaire_sent_indi_title_lp_ce_room_cy = \
            "Caiff copi print mawr o\\\'r holiadur papur i unigolion ei anfon at Bob Bobbington, Room A8 yn " \
            "Halls Of Residence, Cumbria College Of Art &amp; Design"
        # TODO: add welsh translation
        self.content_request_questionnaire_sent_post_title_lp_ce_with_room_long_last_cy = \
            'A large-print household paper questionnaire will be sent to Bob Bobbington-Fortesque-Smythe, ' \
            'Room A8 at Halls Of Residence, Cumbria College Of Art &amp; Design'
        self.content_request_questionnaire_sent_post_secondary_cy = \
            "Dylai gyrraedd yn fuan er mwyn i chi gwblhau eich cyfrifiad"

        self.content_request_questionnaire_sent_post_title_ni = \
            'A household paper questionnaire will be sent to Bob Bobbington at 27 Kings Road, Whitehead'
        self.content_request_questionnaire_sent_post_individual_title_ni = \
            'An individual paper questionnaire will be sent to Bob Bobbington at 27 Kings Road, Whitehead'
        self.content_request_questionnaire_sent_post_title_large_print_ni = \
            'A large-print household paper questionnaire will be sent to Bob Bobbington at 27 Kings Road, Whitehead'
        self.content_request_questionnaire_sent_post_individual_title_large_print_ni = \
            'A large-print individual paper questionnaire will be sent to Bob Bobbington at 27 Kings Road, Whitehead'

        self.content_request_questionnaire_confirm_send_by_post_page_title_en = \
            '<title>Confirm to send household paper questionnaire - Census 2021</title>'
        self.content_request_questionnaire_confirm_send_by_post_page_title_error_en = \
            '<title>Error: Confirm to send household paper questionnaire - Census 2021</title>'
        self.content_request_questionnaire_confirm_send_by_post_title_en = \
            'Do you want to send a household paper questionnaire to this address?'
        self.content_request_questionnaire_confirm_send_by_post_individual_page_title_en = \
            '<title>Confirm to send individual paper questionnaire - Census 2021</title>'
        self.content_request_questionnaire_confirm_send_by_post_individual_page_title_error_en = \
            '<title>Error: Confirm to send individual paper questionnaire - Census 2021</title>'
        self.content_request_questionnaire_confirm_send_by_post_individual_title_en = \
            'Do you want to send an individual paper questionnaire to this address?'
        self.content_request_questionnaire_confirm_send_by_post_option_yes_en = 'Yes, send the questionnaire by post'
        self.content_request_questionnaire_confirm_send_by_post_option_no_en = 'No, cancel and return'
        self.content_request_questionnaire_confirm_send_by_post_large_print_checkbox_en = \
            'I need a large-print questionnaire'

        self.content_request_questionnaire_confirm_send_by_post_page_title_cy = \
            '<title>Cadarnhau i anfon copi papur o Holiadur y Cartref - Cyfrifiad 2021</title>'
        self.content_request_questionnaire_confirm_send_by_post_page_title_error_cy = \
            '<title>Gwall: Cadarnhau i anfon copi papur o Holiadur y Cartref - Cyfrifiad 2021</title>'
        self.content_request_questionnaire_confirm_send_by_post_title_cy = \
            "Ydych chi am anfon holiadur papur y cartref i\\\'r cyfeiriad hwn?"
        # TODO Add Welsh Translation
        self.content_request_questionnaire_confirm_send_by_post_individual_page_title_cy = \
            '<title>Confirm to send individual paper questionnaire - Cyfrifiad 2021</title>'
        # TODO Add Welsh Translation
        self.content_request_questionnaire_confirm_send_by_post_individual_page_title_error_cy = \
            '<title>Gwall: Confirm to send individual paper questionnaire - Cyfrifiad 2021</title>'
        self.content_request_questionnaire_confirm_send_by_post_individual_title_cy = \
            "Ydych chi am anfon holiadur papur i unigolion i\\\'r cyfeiriad hwn?"
        self.content_request_questionnaire_confirm_send_by_post_option_yes_cy = \
            "Ydw, anfonwch yr holiadur drwy\\\'r post"
        self.content_request_questionnaire_confirm_send_by_post_option_no_cy = "Nac ydw, rwyf am ganslo a dychwelyd"
        self.content_request_questionnaire_confirm_send_by_post_large_print_checkbox_cy = \
            'Mae angen holiadur print mawr arnaf'

        self.content_request_questionnaire_manager_title_en = \
            'We cannot send communal establishment paper questionnaires to managers'
        self.content_request_questionnaire_manager_title_cy = \
            "Ni allwn anfon holiaduron papur sefydliadau cymunedol at reolwyr"

        self.content_request_questionnaire_request_cancelled_title_en = \
            'Your request for a paper questionnaire has been cancelled'
        # TODO Add Welsh Translation
        self.content_request_questionnaire_request_cancelled_title_cy = \
            'Your request for a paper questionnaire has been cancelled'

        # Start Request Continuation Questionnaire

        # URLs

        self.get_request_continuation_questionnaire_enter_address_en = \
            self.app.router['CommonEnterAddress:get'].url_for(
                display_region='en', user_journey='request', sub_user_journey='continuation-questionnaire'
            )
        self.get_request_continuation_questionnaire_enter_address_cy = \
            self.app.router['CommonEnterAddress:get'].url_for(
                display_region='cy', user_journey='request', sub_user_journey='continuation-questionnaire'
            )
        self.get_request_continuation_questionnaire_enter_address_ni = \
            self.app.router['CommonEnterAddress:get'].url_for(
                display_region='ni', user_journey='request', sub_user_journey='continuation-questionnaire'
            )
        self.post_request_continuation_questionnaire_enter_address_en = \
            self.app.router['CommonEnterAddress:post'].url_for(
                display_region='en', user_journey='request', sub_user_journey='continuation-questionnaire'
            )
        self.post_request_continuation_questionnaire_enter_address_cy = \
            self.app.router['CommonEnterAddress:post'].url_for(
                display_region='cy', user_journey='request', sub_user_journey='continuation-questionnaire'
            )
        self.post_request_continuation_questionnaire_enter_address_ni = \
            self.app.router['CommonEnterAddress:post'].url_for(
                display_region='ni', user_journey='request', sub_user_journey='continuation-questionnaire'
            )

        self.post_request_continuation_questionnaire_select_address_en = \
            self.app.router['CommonSelectAddress:post'].url_for(
                display_region='en', user_journey='request', sub_user_journey='continuation-questionnaire'
            )
        self.post_request_continuation_questionnaire_select_address_cy = \
            self.app.router['CommonSelectAddress:post'].url_for(
                display_region='cy', user_journey='request', sub_user_journey='continuation-questionnaire'
            )
        self.post_request_continuation_questionnaire_select_address_ni = \
            self.app.router['CommonSelectAddress:post'].url_for(
                display_region='ni', user_journey='request', sub_user_journey='continuation-questionnaire'
            )

        self.post_request_continuation_questionnaire_confirm_address_en = \
            self.app.router['CommonConfirmAddress:post'].url_for(
                display_region='en', user_journey='request', sub_user_journey='continuation-questionnaire'
            )
        self.post_request_continuation_questionnaire_confirm_address_cy = \
            self.app.router['CommonConfirmAddress:post'].url_for(
                display_region='cy', user_journey='request', sub_user_journey='continuation-questionnaire'
            )
        self.post_request_continuation_questionnaire_confirm_address_ni = \
            self.app.router['CommonConfirmAddress:post'].url_for(
                display_region='ni', user_journey='request', sub_user_journey='continuation-questionnaire'
            )

        self.post_request_continuation_questionnaire_people_in_household_en = \
            self.app.router['RequestCommonPeopleInHousehold:post'].url_for(
                display_region='en', user_journey='request', request_type='continuation-questionnaire'
            )
        self.post_request_continuation_questionnaire_people_in_household_cy = \
            self.app.router['RequestCommonPeopleInHousehold:post'].url_for(
                display_region='cy', user_journey='request', request_type='continuation-questionnaire'
            )
        self.post_request_continuation_questionnaire_people_in_household_ni = \
            self.app.router['RequestCommonPeopleInHousehold:post'].url_for(
                display_region='ni', user_journey='request', request_type='continuation-questionnaire'
            )

        self.post_request_continuation_questionnaire_enter_name_en = \
            self.app.router['RequestCommonEnterName:post'].url_for(
                request_type='continuation-questionnaire', display_region='en'
            )
        self.post_request_continuation_questionnaire_enter_name_cy = \
            self.app.router['RequestCommonEnterName:post'].url_for(
                request_type='continuation-questionnaire', display_region='cy'
            )
        self.post_request_continuation_questionnaire_enter_name_ni = \
            self.app.router['RequestCommonEnterName:post'].url_for(
                request_type='continuation-questionnaire', display_region='ni'
            )

        self.post_request_continuation_questionnaire_confirm_send_by_post_en = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='continuation-questionnaire',
                                                                           display_region='en')
        self.post_request_continuation_questionnaire_confirm_send_by_post_cy = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='continuation-questionnaire',
                                                                           display_region='cy')
        self.post_request_continuation_questionnaire_confirm_send_by_post_ni = \
            self.app.router['RequestCommonConfirmSendByPost:post'].url_for(request_type='continuation-questionnaire',
                                                                           display_region='ni')

        # Content

        self.content_request_continuation_questionnaire_enter_address_secondary_en = \
            'To send a continuation questionnaire, we need your address'
        # TODO: add welsh translation
        self.content_request_continuation_questionnaire_enter_address_secondary_cy = \
            'To send a continuation questionnaire, we need your address'

        self.content_request_continuation_questionnaire_not_a_household_title_en = \
            'This address is not a household address'
        self.content_request_continuation_questionnaire_not_a_household_secondary_en = \
            'Continuation questionnaires can only be requested for household addresses.'
        # TODO: add welsh translation
        self.content_request_continuation_questionnaire_not_a_household_title_cy = \
            'This address is not a household address'
        # TODO: add welsh translation
        self.content_request_continuation_questionnaire_not_a_household_secondary_cy = \
            'Continuation questionnaires can only be requested for household addresses.'

        self.content_request_continuation_questionnaire_people_in_household_error_number_greater_en = \
            'Enter a number greater than 5'
        # TODO: add welsh translation
        self.content_request_continuation_questionnaire_people_in_household_error_number_greater_cy = \
            'Enter a number greater than 5'
        self.content_request_continuation_questionnaire_people_in_household_error_number_greater_ni = \
            'Enter a number greater than 6'

        self.content_request_continuation_questionnaire_sent_post_page_title_en = \
            '<title>Continuation questionnaire will be sent - Census 2021</title>'
        self.content_request_continuation_questionnaire_sent_post_title_en = \
            'A continuation questionnaire will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        self.content_request_continuation_questionnaire_sent_post_secondary_en = \
            'This should arrive soon for you to complete your census'
        # TODO: add welsh translation
        self.content_request_continuation_questionnaire_sent_post_page_title_cy = \
            '<title>Continuation questionnaire will be sent - Cyfrifiad 2021</title>'
        # TODO: add welsh translation
        self.content_request_continuation_questionnaire_sent_post_title_cy = \
            'A continuation questionnaire will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        # TODO Add Welsh Translation
        self.content_request_continuation_questionnaire_sent_post_secondary_cy = \
            'This should arrive soon for you to complete your census'

        self.content_request_continuation_questionnaire_sent_post_title_ni = \
            'A continuation questionnaire will be sent to Bob Bobbington at 27 Kings Road, Whitehead'

        self.content_request_continuation_questionnaire_confirm_send_by_post_page_title_en = \
            '<title>Confirm to send continuation questionnaire - Census 2021</title>'
        self.content_request_continuation_questionnaire_confirm_send_by_post_page_title_error_en = \
            '<title>Error: Confirm to send continuation questionnaire - Census 2021</title>'
        self.content_request_continuation_questionnaire_confirm_send_by_post_title_en = \
            'Do you want to send a continuation questionnaire to this address?'
        self.content_request_continuation_questionnaire_confirm_send_by_post_page_title_cy = \
            '<title>Cadarnhau i anfon holiadur parhad - Cyfrifiad 2021</title>'
        self.content_request_continuation_questionnaire_confirm_send_by_post_page_title_error_cy = \
            '<title>Gwall: Cadarnhau i anfon holiadur parhad - Cyfrifiad 2021</title>'
        # TODO Add Welsh Translation
        self.content_request_continuation_questionnaire_confirm_send_by_post_title_cy = \
            'Do you want to send a continuation questionnaire to this address?'

        self.content_request_continuation_questionnaire_request_cancelled_title_en = \
            'Your request for a continuation questionnaire has been cancelled'
        # TODO Add Welsh Translation
        self.content_request_continuation_questionnaire_request_cancelled_title_cy = \
            'Your request for a continuation questionnaire has been cancelled'

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

        self.content_support_centre_enter_postcode_page_title_en = '<title>Find a support centre - Census 2021</title>'
        self.content_support_centre_enter_postcode_page_title_error_en = \
            '<title>Error: Find a support centre - Census 2021</title>'
        self.content_support_centre_enter_postcode_title_en = 'Find a support centre'
        self.content_support_centre_enter_postcode_secondary_en = \
            'To find your nearest support centre, we need your postcode.'
        self.content_support_centre_enter_postcode_error_empty_en = 'Enter a postcode'
        self.content_support_centre_enter_postcode_error_invalid_en = 'Enter a valid UK postcode'

        self.content_support_centre_enter_postcode_page_title_cy = \
            '<title>Chwilio am ganolfan gymorth - Cyfrifiad 2021</title>'
        self.content_support_centre_enter_postcode_page_title_error_cy = \
            '<title>Gwall: Chwilio am ganolfan gymorth - Cyfrifiad 2021</title>'
        self.content_support_centre_enter_postcode_title_cy = "Chwilio am ganolfan gymorth"
        self.content_support_centre_enter_postcode_secondary_cy = \
            "Er mwyn chwilio am eich canolfan gymorth agosaf, bydd angen i ni gael eich cod post."
        # TODO Add Welsh Translation
        self.content_support_centre_enter_postcode_error_empty_cy = 'Enter a postcode'
        # TODO Add Welsh Translation
        self.content_support_centre_enter_postcode_error_invalid_cy = "Enter a valid UK postcode"

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

        self.content_support_centre_list_of_centres_title_cy = 'Canolfannau cymorth gerllaw ' + self.postcode_valid
        self.content_support_centre_list_of_centres_result_one_location_name_cy = 'Welsh Sheffield Central Library'
        self.content_support_centre_list_of_centres_result_two_location_name_cy = 'Welsh University of Sheffield'
        self.content_support_centre_list_of_centres_result_one_distance_away_cy = \
            '<span class="u-mb-s tag">1.3 milltir i ffwrdd</span>'
        self.content_support_centre_list_of_centres_result_one_address_cy = \
            '<p>Welsh Street<br> Sheffield<br>S1 1XZ</p>'
        self.content_support_centre_list_of_centres_result_one_telephone_cy = \
            "Ff\\xc3\\xb4n: <span>+44 (0)11 4273 4712</span>"
        self.content_support_centre_list_of_centres_result_one_email_cy = \
            'E-bost: <a href="mailto:test@email.com">test@email.com</a>'

        self.content_support_centre_list_of_centres_result_open_monday_cy = \
            'Dydd Llun &ndash;&nbsp;10:30am tan 5:15pm'
        self.content_support_centre_list_of_centres_result_open_tuesday_cy = \
            'Dydd Mawrth &ndash;&nbsp;10am tan 5pm'
        self.content_support_centre_list_of_centres_result_open_wednesday_cy = \
            'Dydd Mercher &ndash;&nbsp;10am tan 5pm'
        self.content_support_centre_list_of_centres_result_open_thursday_cy = 'Dydd Iau &ndash;&nbsp;10am tan 5pm'
        self.content_support_centre_list_of_centres_result_open_friday_cy = 'Dydd Gwener &ndash;&nbsp;10am tan 5pm'
        self.content_support_centre_list_of_centres_result_open_saturday_cy = 'Dydd Sadwrn &ndash;&nbsp;10am tan 1pm'
        self.content_support_centre_list_of_centres_result_open_sunday_cy = 'Dydd Sul &ndash;&nbsp;10am tan 1pm'
        self.content_support_centre_list_of_centres_result_open_census_saturday_cy = \
            'Dydd Sadwrn y Cyfrifiad, 20 Mawrth &ndash;&nbsp;10am tan 4pm'
        self.content_support_centre_list_of_centres_result_open_census_day_cy = \
            'Diwrnod y Cyfrifiad, 21 Mawrth &ndash;&nbsp;10am tan 4pm'
        self.content_support_centre_list_of_centres_result_open_good_friday_cy = \
            'Dydd Gwener y Groglith, 2 Ebrill &ndash;&nbsp;10am tan 5pm'
        self.content_support_centre_list_of_centres_result_open_easter_monday_cy = \
            'Dydd Llun y Pasg, 5 Ebrill &ndash;&nbsp;10am tan 5pm'
        self.content_support_centre_list_of_centres_result_open_may_bank_holiday_cy = \
            "G\\xc5\\xb5yl Banc Calan Mai, 3 Mai &ndash;&nbsp;10am tan 5pm"
        self.content_support_centre_list_of_centres_result_closed_monday_cy = 'Dydd Llun &ndash;&nbsp;Ar gau'
        self.content_support_centre_list_of_centres_result_closed_tuesday_cy = 'Dydd Mawrth &ndash;&nbsp;Ar gau'
        self.content_support_centre_list_of_centres_result_closed_wednesday_cy = 'Dydd Mercher &ndash;&nbsp;Ar gau'
        self.content_support_centre_list_of_centres_result_closed_thursday_cy = 'Dydd Iau &ndash;&nbsp;Ar gau'
        self.content_support_centre_list_of_centres_result_closed_friday_cy = 'Dydd Gwener &ndash;&nbsp;Ar gau'
        self.content_support_centre_list_of_centres_result_closed_saturday_cy = 'Dydd Sadwrn &ndash;&nbsp;Ar gau'
        self.content_support_centre_list_of_centres_result_closed_sunday_cy = 'Dydd Sul &ndash;&nbsp;Ar gau'
        self.content_support_centre_list_of_centres_result_closed_census_saturday_cy = \
            'Dydd Sadwrn y Cyfrifiad, 20 Mawrth &ndash;&nbsp;Ar gau'
        self.content_support_centre_list_of_centres_result_closed_census_day_cy = \
            'Diwrnod y Cyfrifiad, 21 Mawrth &ndash;&nbsp;Ar gau'
        self.content_support_centre_list_of_centres_result_closed_good_friday_cy = \
            'Dydd Gwener y Groglith, 2 Ebrill &ndash;&nbsp;Ar gau'
        self.content_support_centre_list_of_centres_result_closed_easter_monday_cy = \
            'Dydd Llun y Pasg, 5 Ebrill &ndash;&nbsp;Ar gau'
        self.content_support_centre_list_of_centres_result_closed_may_bank_holiday_cy = \
            "G\\xc5\\xb5yl Banc Calan Mai, 3 Mai &ndash;&nbsp;Ar gau"

        self.content_support_centre_list_of_centres_result_one_public_parking_cy = \
            'Maes parcio, gan gynnwys parcio anabl'
        self.content_support_centre_list_of_centres_result_two_public_parking_cy = "Parcio anabl"
        self.content_support_centre_list_of_centres_result_three_public_parking_cy = 'Maes parcio'
        self.content_support_centre_list_of_centres_result_one_level_access_cy = \
            "Mynediad gwastad i mewn i\\\'r adeilad"
        self.content_support_centre_list_of_centres_result_one_wheelchair_access_cy = 'Mynediad i gadeiriau olwyn'
        self.content_support_centre_list_of_centres_result_one_disability_aware_cy = \
            'Staff yn meddu ar ymwybyddiaeth o anableddau'
        self.content_support_centre_list_of_centres_result_one_hearing_loop_cy = 'System dolen glywed'

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

        # Start Web Form

        self.get_webform_en = self.app.router['WebForm:get'].url_for(display_region='en')
        self.get_webform_cy = self.app.router['WebForm:get'].url_for(display_region='cy')
        self.get_webform_ni = self.app.router['WebForm:get'].url_for(display_region='ni')
        self.post_webform_en = self.app.router['WebForm:post'].url_for(display_region='en')
        self.post_webform_cy = self.app.router['WebForm:post'].url_for(display_region='cy')
        self.post_webform_ni = self.app.router['WebForm:post'].url_for(display_region='ni')

        self.webform_form_data = {
            'name': 'Bob Bobbington',
            'email': 'bob.bobbington@theinternet.co.uk',
            'description': 'Hello this is Bob',
            'category': 'MISSING_INFORMATION',
            'country': 'E'
        }

        self.rhsvc_url_web_form = (
            f'{rh_svc_url}/webform'
        )

        self.content_web_form_page_title_en = '<title>Web form - Census 2021</title>'
        self.content_web_form_page_title_error_en = '<title>Error: Web form - Census 2021</title>'
        self.content_web_form_title_en = 'Web form'
        self.content_web_form_warning_en = 'Information about what we do with your personal data is available in our'
        # TODO Add Welsh Translation
        self.content_web_form_page_title_cy = '<title>Web form - Cyfrifiad 2021</title>'
        # TODO Add Welsh Translation
        self.content_web_form_page_title_error_cy = '<title>Gwall: Web form - Cyfrifiad 2021</title>'
        # TODO Add Welsh Translation
        self.content_web_form_title_cy = 'Web form'
        # TODO Add Welsh Translation
        self.content_web_form_warning_cy = 'Information about what we do with your personal data is available in our'

        self.content_web_form_success_page_title_en = '<title>Thank you for contacting us - Census 2021</title>'
        self.content_web_form_success_title_en = 'Thank you for contacting us'
        self.content_web_form_success_confirmation_en = 'Your message has been sent'
        self.content_web_form_success_secondary_en = 'We will respond to you within 2 working days'
        self.content_web_form_success_page_title_cy = '<title>Diolch am gysylltu \\xc3\\xa2 ni - Cyfrifiad 2021</title>'
        self.content_web_form_success_title_cy = 'Diolch am gysylltu \\xc3\\xa2 ni'
        # TODO Add Welsh Translation
        self.content_web_form_success_confirmation_cy = 'Your message has been sent'
        # TODO Add Welsh Translation
        self.content_web_form_success_secondary_cy = 'We will respond to you within 2 working days'

        self.content_web_form_error_429_title_en = 'You have reached the maximum number web form submissions'
        # TODO Add Welsh Translation
        self.content_web_form_error_429_title_cy = 'You have reached the maximum number web form submissions'

        # Transient

        # Content

        self.content_start_transient_enter_town_name_page_title_en = \
            '<title>Nearest town or city - Census 2021</title>'
        self.content_start_transient_enter_town_name_page_title_error_en = \
            '<title>Error: Nearest town or city - Census 2021</title>'
        self.content_start_transient_enter_town_name_pre_census_day_title_en = \
            'What is the nearest town or city to where you will be living on Sunday 21 March 2021?'
        self.content_start_transient_enter_town_name_post_census_day_title_en = \
            'What is the nearest town or city to where you were living on Sunday 21 March 2021?'
        self.content_start_transient_enter_town_name_error_en = "Enter your nearest town or city"
        # TODO Add Welsh Translation
        self.content_start_transient_enter_town_name_page_title_cy = \
            '<title>Nearest town or city - Cyfrifiad 2021</title>'
        # TODO Add Welsh Translation
        self.content_start_transient_enter_town_name_page_title_error_cy = \
            '<title>Gwall: Nearest town or city - Cyfrifiad 2021</title>'
        # TODO Add Welsh Translation
        self.content_start_transient_enter_town_name_pre_census_day_title_cy = \
            'What is the nearest town or city to where you will be living on Sunday 21 March 2021?'
        # TODO Add Welsh Translation
        self.content_start_transient_enter_town_name_post_census_day_title_cy = \
            'What is the nearest town or city to where you were living on Sunday 21 March 2021?'
        # TODO Add Welsh Translation
        self.content_start_transient_enter_town_name_error_cy = "Enter your nearest town or city"

        self.content_start_transient_accommodation_type_page_title_en = \
            "<title>Select type of accommodation - Census 2021</title>"
        self.content_start_transient_accommodation_type_page_title_error_en = \
            "<title>Error: Select type of accommodation - Census 2021</title>"
        self.content_start_transient_accommodation_type_title_en = \
            "Which of the following best describes your type of accommodation?"
        self.content_start_transient_accommodation_type_error_en = "Select an answer"
        self.content_start_transient_accommodation_type_value_barge_en = "Barge or boat"
        self.content_start_transient_accommodation_type_value_caravan_en = "Caravan or live-in vehicle"
        self.content_start_transient_accommodation_type_value_tent_en = "Tent or temporary structure"
        self.content_start_transient_accommodation_type_page_title_cy = \
            "<title>Dewis math o lety - Cyfrifiad 2021</title>"
        self.content_start_transient_accommodation_type_page_title_error_cy = \
            "<title>Gwall: Dewis math o lety - Cyfrifiad 2021</title>"
        self.content_start_transient_accommodation_type_title_cy = \
            "Pa un o\\xe2\\x80\\x99r canlynol sy\\xe2\\x80\\x99n disgrifio eich math o gartref orau?"
        # TODO Add Welsh Translation
        self.content_start_transient_accommodation_type_error_cy = "Select an answer"
        self.content_start_transient_accommodation_type_value_barge_cy = "Bad neu gwch"
        self.content_start_transient_accommodation_type_value_caravan_cy = "Caraf\\xc3\\xa1n neu gerbyd preswyl"
        self.content_start_transient_accommodation_type_value_tent_cy = "Pabell neu strwythur dros dro"

        # Test Data
        self.data_start_transient_town_name = 'Fareham'
        self.start_transient_town_name_input_valid = {
            'form-enter-town-name': self.data_start_transient_town_name, 'action[save_continue]': '',
        }
        self.start_transient_town_name_input_empty = {
            'form-enter-town-name': '', 'action[save_continue]': '',
        }

        self.start_transient_accommodation_type_input_barge_en = {
            'accommodation-type': 'Barge or boat', 'action[save_continue]': '',
        }
        self.start_transient_accommodation_type_input_caravan_en = {
            'accommodation-type': 'Caravan or live-in vehicle', 'action[save_continue]': '',
        }
        self.start_transient_accommodation_type_input_tent_en = {
            'accommodation-type': 'Tent or temporary structure', 'action[save_continue]': '',
        }
        # TODO Add Welsh Translation
        self.start_transient_accommodation_type_input_barge_cy = {
            'accommodation-type': 'Bad neu gwch', 'action[save_continue]': '',
        }
        # TODO Add Welsh Translation
        self.start_transient_accommodation_type_input_caravan_cy = {
            'accommodation-type': 'Caraf\\xc3\\xa1n neu gerbyd preswyl', 'action[save_continue]': '',
        }
        # TODO Add Welsh Translation
        self.start_transient_accommodation_type_input_tent_cy = {
            'accommodation-type': 'Pabell neu strwythur dros dro', 'action[save_continue]': '',
        }

        with open('tests/test_data/rhsvc/uac_transient_e.json') as fp:
            self.transient_uac_json_e = json.load(fp)
        with open('tests/test_data/rhsvc/uac_transient_w.json') as fp:
            self.transient_uac_json_w = json.load(fp)
        with open('tests/test_data/rhsvc/uac_transient_n.json') as fp:
            self.transient_uac_json_n = json.load(fp)

        # yapf: enable

    # URL functions
    def get_url_from_class(self, class_name, method_type, display_region=None, query=None):
        if display_region:
            if query:
                url = self.app.router[class_name + ':' + method_type].url_for(display_region=display_region).\
                    with_query(query)
            else:
                url = self.app.router[class_name + ':' + method_type].url_for(display_region=display_region)
        else:
            if query:
                url = self.app.router[class_name + ':' + method_type].url_for().with_query(query)
            else:
                url = self.app.router[class_name + ':' + method_type].url_for()
        return url
