from app.utils import ProcessPostcode, ProcessMobileNumber, InvalidDataError, InvalidDataErrorWelsh, FlashMessage, View

from . import RHTestCase
import datetime

from unittest import mock


class TestUtils(RHTestCase):

    def test_validate_postcode_valid(self):
        postcode = 'PO15 5RR'
        locale = 'en'

        # When validate_postcode is called
        ProcessPostcode.validate_postcode(postcode, locale)
        # Nothing happens

    def test_validate_postcode_empty(self):
        postcode = ''
        locale = 'en'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Enter a postcode',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_not_alphanumeric(self):
        postcode = '?<>:{}'
        locale = 'en'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Enter a valid UK postcode',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_short(self):
        postcode = 'PO15'
        locale = 'en'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Enter a valid UK postcode',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_long(self):
        postcode = 'PO15 5RRR'
        locale = 'en'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Enter a valid UK postcode',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_invalid(self):
        postcode = 'ZZ99 9ZZ'
        locale = 'en'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Enter a valid UK postcode',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_valid_cy(self):
        postcode = 'PO15 5RR'
        locale = 'cy'

        # When validate_postcode is called
        ProcessPostcode.validate_postcode(postcode, locale)
        # Nothing happens

    def test_validate_postcode_empty_cy(self):
        postcode = ''
        locale = 'cy'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Rhowch god post',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_not_alphanumeric_cy(self):
        postcode = '?<>:{}'
        locale = 'cy'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Rhowch god post dilys yn y Deyrnas Unedig',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_short_cy(self):
        postcode = 'PO15'
        locale = 'cy'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Rhowch god post dilys yn y Deyrnas Unedig',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_long_cy(self):
        postcode = 'PO15 5RRR'
        locale = 'cy'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Rhowch god post dilys yn y Deyrnas Unedig',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_invalid_cy(self):
        postcode = 'ZZ99 9ZZ'
        locale = 'cy'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Rhowch god post dilys yn y Deyrnas Unedig',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_valid(self):
        mobile_number = '070 1234 5678'
        locale = 'en'

        # When validate_uk_mobile_phone_number is called
        ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Nothing happens

    def test_validate_uk_mobile_phone_number_short(self):
        mobile_number = '070 1234'
        locale = 'en'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_en,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_long(self):
        mobile_number = '070 1234 5678 9012 3456 7890'
        locale = 'en'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_en,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_not_mobile(self):
        mobile_number = '020 1234 5678'
        locale = 'en'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_en,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_not_numeric(self):
        mobile_number = 'gdsjkghjdsghjsd'
        locale = 'en'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_en,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_valid_cy(self):
        mobile_number = '070 1234 5678'
        locale = 'cy'

        # When validate_uk_mobile_phone_number is called
        ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Nothing happens

    def test_validate_uk_mobile_phone_number_short_cy(self):
        mobile_number = '070 1234'
        locale = 'cy'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_cy,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_long_cy(self):
        mobile_number = '070 1234 5678 9012 3456 7890'
        locale = 'cy'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_cy,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_not_mobile_cy(self):
        mobile_number = '020 1234 5678'
        locale = 'cy'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_cy,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_not_numeric_cy(self):
        mobile_number = 'gdsjkghjdsghjsd'
        locale = 'cy'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_cy,
            str(cm.exception)
        )
        # With the correct message

    def test_generate_flash_message(self):
        built = FlashMessage.generate_flash_message('Test message', 'LEVEL', 'MESSAGE_TYPE', 'field')
        expected = {'text': 'Test message', 'level': 'LEVEL', 'type': 'MESSAGE_TYPE', 'field': 'field'}
        self.assertEqual(built, expected)

    def test_get_call_centre_number(self):
        built_ew = View.get_call_centre_number('en')
        built_cy = View.get_call_centre_number('cy')
        built_ni = View.get_call_centre_number('ni')
        expected_ew = '0800 141 2021'
        expected_cy = '0800 169 2021'
        expected_ni = '0800 328 2021'
        self.assertEqual(built_ew, expected_ew)
        self.assertEqual(built_cy, expected_cy)
        self.assertEqual(built_ni, expected_ni)

    def after_census_day(self, year, month=None, day=None, hour=0, minute=0, second=0):
        mocked_now_utc = datetime.datetime(year, month, day, hour, minute, second, 0)
        with mock.patch('app.utils.View.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = mocked_now_utc
            self.assertTrue(View.check_if_after_census_day())

    def before_census_day(self, year, month=None, day=None, hour=0, minute=0, second=0):
        mocked_now_utc = datetime.datetime(year, month, day, hour, minute, second, 0)
        with mock.patch('app.utils.View.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = mocked_now_utc
            self.assertFalse(View.check_if_after_census_day())

    def test_check_before_after_census_day(self):
        self.after_census_day(2021, 3, 22)
        self.before_census_day(2021, 3, 21)
        self.before_census_day(2021, 3, 20)

    def test_client_ip_valid(self):
        valid_request = {'client_ip': '192.168.0.0, 35.190.0.0, 35.191.10.0'}
        spoofed_request = {'client_ip': '200.30.20.10, 192.168.0.0, 35.190.0.0, 35.191.10.0'}
        spoofed_request_ipv6 = \
            {'client_ip': '2001:db8:3333:4444:CCCC:DDDD:EEEE:FFFF, 192.168.0.0, 35.190.0.0, 35.191.10.0'}
        unknown_request = {'client_ip': 'unknown, 192.168.0.0, 35.190.0.0, 35.191.10.0'}
        expected_valid = '192.168.0.0'
        self.assertEqual(View.single_client_ip(valid_request), expected_valid)
        self.assertEqual(View.single_client_ip(spoofed_request), expected_valid)
        self.assertEqual(View.single_client_ip(spoofed_request_ipv6), expected_valid)
        self.assertEqual(View.single_client_ip(unknown_request), expected_valid)

    def test_client_ip_invalid_single(self):
        request = {'client_id': '36be6b97-b4de-4718-8a74-8b27fb03ca8c', 'trace': '105445aa7843bc8bf206b12000100000'}
        single_ip_request = {'client_ip': '35.191.10.0'}
        single_ip_request.update(request)
        expected_empty = ''
        with self.assertLogs('respondent-home', 'WARN') as cm:
            self.assertEqual(View.single_client_ip(single_ip_request), expected_empty)
            self.assertLogEvent(cm, 'clientIP failed validation. Provided IP - ' + single_ip_request['client_ip'],
                                client_id=request['client_id'], trace=request['trace'])

    def test_client_ip_invalid_ipv6(self):
        request = {'client_id': '36be6b97-b4de-4718-8a74-8b27fb03ca8c', 'trace': '105445aa7843bc8bf206b12000100000'}
        invalid_request_ipv6 = {'client_ip': '2001:db8:3333:4444:CCCC:DDDD:EEEE:FFFF, 35.190.0.0, 35.191.10.0'}
        invalid_request_ipv6.update(request)
        expected_empty = ''
        with self.assertLogs('respondent-home', 'WARN') as cm:
            self.assertEqual(View.single_client_ip(invalid_request_ipv6), expected_empty)
            self.assertLogEvent(cm, 'clientIP failed validation. Provided IP - ' + invalid_request_ipv6['client_ip'],
                                client_id=request['client_id'], trace=request['trace'])
