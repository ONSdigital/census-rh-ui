import functools
from unittest import mock

from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app.eq import EqPayloadConstructor, format_date, parse_date
#from app.eq import EqPayloadConstructor, build_response_id, format_date, parse_date
from app.exceptions import ExerciseClosedError, InvalidEqPayLoad

from . import RHTestCase


class TestEq(RHTestCase):

    def test_create_eq_constructor(self):
        self.assertIsInstance(EqPayloadConstructor(
            self.uac_json, self.uac_json['address'], self.app), EqPayloadConstructor)

    def test_create_eq_constructor_missing_case_id(self):
        uac_json = self.uac_json.copy()
        del uac_json['caseId']

        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqPayloadConstructor(uac_json, self.uac_json['address'], self.app )
        self.assertIn('No case id in supplied case JSON', ex.exception.message)

    def test_create_eq_constructor_missing_ce_id(self):
        uac_json = self.uac_json.copy()
        del uac_json["collectionExerciseId"]

        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqPayloadConstructor(uac_json, self.uac_json['address'], self.app )
        self.assertIn(f'No collection id in supplied case JSON', ex.exception.message)

    def test_create_eq_constructor_missing_questionnaire_id(self):
        uac_json = self.uac_json.copy()
        del uac_json["questionnaireId"]

        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqPayloadConstructor(uac_json, self.uac_json['address'], self.app)
            self.assertIn(f'No questionnaireId in supplied case JSON', ex.exception.message)

    def test_create_eq_constructor_missing_case_type(self):
        uac_json = self.uac_json.copy()
        del uac_json["caseType"]

        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqPayloadConstructor(uac_json, self.uac_json['address'], self.app)
            self.assertIn(f'No case type in supplied case JSON', ex.exception.message)

    def test_create_eq_constructor_missing_uprn(self):
        uac_json = self.uac_json.copy()
        del uac_json["address"]["uprn"]

        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqPayloadConstructor(uac_json, self.uac_json['address'], self.app)
            self.assertIn(f'Could not retrieve address uprn from case JSON', ex.exception.message)

    @unittest_run_loop
    async def test_build(self):
        self.maxDiff = None  # for full payload comparison when running this test
        with mock.patch('app.eq.uuid4') as mocked_uuid4, mock.patch('app.eq.time.time') as mocked_time:
            # NB: has to be mocked after setup but before import
            mocked_time.return_value = self.eq_payload['iat']
            mocked_uuid4.return_value = self.jti

            with aioresponses() as mocked:
                mocked.get(self.collection_instrument_url, payload=self.collection_instrument_json)
                mocked.get(self.collection_exercise_url, payload=self.collection_exercise_json)
                mocked.get(self.collection_exercise_events_url, payload=self.collection_exercise_events_json)

                with self.assertLogs('app.eq', 'DEBUG') as cm:
                    payload = await EqPayloadConstructor(
                        self.case_json, self.sample_unit_attributes, self.app, self.iac_code).build()
                self.assertLogLine(cm, 'Creating payload for JWT', case_id=self.case_id, tx_id=self.jti)

        mocked_uuid4.assert_called()
        mocked_time.assert_called()
        self.assertEqual(payload, self.eq_payload)

    @unittest_run_loop
    async def test_build_raises_InvalidEqPayLoad_bad_ci_type(self):
        ci_json = self.collection_instrument_json.copy()
        ci_json['type'] = 'not_eq'

        from app import eq  # NB: local import to avoid overwriting the patched version for some tests

        with aioresponses() as mocked:
            mocked.get(self.collection_instrument_url, payload=ci_json)

            with self.assertRaises(InvalidEqPayLoad) as ex:
                await eq.EqPayloadConstructor(
                    self.case_json, self.sample_unit_attributes, self.app, self.iac_code).build()
            self.assertIn(f"Collection instrument {self.collection_instrument_id} type is not EQ", ex.exception.message)

    @unittest_run_loop
    async def test_build_raises_InvalidEqPayLoad_missing_ci_type(self):
        ci_json = self.collection_instrument_json.copy()
        del ci_json['type']

        with aioresponses() as mocked:
            mocked.get(self.collection_instrument_url, payload=ci_json)

            with self.assertRaises(InvalidEqPayLoad) as ex:
                await EqPayloadConstructor(self.case_json, self.sample_unit_attributes, self.app, self.iac_code).build()
            self.assertIn(f"No Collection Instrument type for {self.collection_instrument_id}", ex.exception.message)

    @unittest_run_loop
    async def test_build_raises_InvalidEqPayLoad_missing_classifiers(self):
        ci_json = self.collection_instrument_json.copy()
        del ci_json['classifiers']

        with aioresponses() as mocked:
            mocked.get(self.collection_instrument_url, payload=ci_json)

            with self.assertRaises(InvalidEqPayLoad) as ex:
                await EqPayloadConstructor(self.case_json, self.sample_unit_attributes, self.app, self.iac_code).build()
            self.assertIn(f"Could not retrieve classifiers for case {self.case_id}", ex.exception.message)

    @unittest_run_loop
    async def test_build_raises_InvalidEqPayLoad_missing_eq_id(self):
        ci_json = self.collection_instrument_json.copy()
        del ci_json['classifiers']['eq_id']

        with aioresponses() as mocked:
            mocked.get(self.collection_instrument_url, payload=ci_json)

            with self.assertRaises(InvalidEqPayLoad) as ex:
                await EqPayloadConstructor(self.case_json, self.sample_unit_attributes, self.app, self.iac_code).build()
            self.assertIn(f"Could not retrieve eq_id for case {self.case_id}", ex.exception.message)

    @unittest_run_loop
    async def test_build_raises_InvalidEqPayLoad_missing_form_type(self):
        ci_json = self.collection_instrument_json.copy()
        del ci_json['classifiers']['form_type']

        with aioresponses() as mocked:
            mocked.get(self.collection_instrument_url, payload=ci_json)

            with self.assertRaises(InvalidEqPayLoad) as ex:
                await EqPayloadConstructor(self.case_json, self.sample_unit_attributes, self.app, self.iac_code).build()
            self.assertIn(f"Could not retrieve form_type for eq_id {self.eq_id}", ex.exception.message)

    @unittest_run_loop
    async def test_build_raises_InvalidEqPayLoad_missing_exerciseRef(self):
        ce_json = self.collection_exercise_json.copy()
        del ce_json['exerciseRef']

        with aioresponses() as mocked:
            mocked.get(self.collection_instrument_url, payload=self.collection_instrument_json)
            mocked.get(self.collection_exercise_url, payload=ce_json)

            with self.assertRaises(InvalidEqPayLoad) as ex:
                await EqPayloadConstructor(self.case_json, self.sample_unit_attributes, self.app, self.iac_code).build()
            self.assertIn(f"Could not retrieve period id for case {self.case_id}", ex.exception.message)

    @unittest_run_loop
    async def test_build_raises_InvalidEqPayLoad_missing_exercise_id(self):
        ce_json = self.collection_exercise_json.copy()
        del ce_json['id']

        with aioresponses() as mocked:
            mocked.get(self.collection_instrument_url, payload=self.collection_instrument_json)
            mocked.get(self.collection_exercise_url, payload=ce_json)

            with self.assertRaises(InvalidEqPayLoad) as ex:
                await EqPayloadConstructor(self.case_json, self.sample_unit_attributes, self.app, self.iac_code).build()
            self.assertIn(f"Could not retrieve ce id for case {self.case_id}", ex.exception.message)

    @unittest_run_loop
    async def test_build_raises_InvalidEqPayLoad_missing_country_code(self):
        sample_json = self.sample_attributes_json.copy()
        del sample_json['attributes']['COUNTRY']

        with aioresponses() as mocked:
            mocked.get(self.collection_instrument_url, payload=self.collection_instrument_json)
            mocked.get(self.collection_exercise_url, payload=self.collection_exercise_json)
            mocked.get(self.collection_exercise_events_url, payload=self.collection_exercise_events_json)

            with self.assertRaises(InvalidEqPayLoad) as ex:
                await EqPayloadConstructor(self.case_json, self.sample_unit_attributes, self.app, self.iac_code).build()
            self.assertIn(f"Could not retrieve country_code for case {self.case_id}", ex.exception.message)

    @unittest_run_loop
    async def test_build_raises_InvalidEqPayLoad_missing_attributes(self):

        from app import eq  # NB: local import to avoid overwriting the patched version for some tests

        with aioresponses() as mocked:
            mocked.get(self.collection_instrument_url, payload=self.collection_instrument_json)
            mocked.get(self.collection_exercise_url, payload=self.collection_exercise_json)
            mocked.get(self.collection_exercise_events_url, payload=self.collection_exercise_events_json)

            with self.assertRaises(InvalidEqPayLoad) as ex:
                await eq.EqPayloadConstructor(
                    self.case_json, None, self.app, self.iac_code).build()
            self.assertIn('Attributes is empty', ex.exception.message)

    def test_caps_to_snake(self):
        from app import eq

        result = eq.EqPayloadConstructor.caps_to_snake('TEST_CASE')
        self.assertEqual(result, 'test_case')

    def test_caps_to_snake_numbers(self):
        from app import eq

        result = eq.EqPayloadConstructor.caps_to_snake('ADDRESS_LINE1')
        self.assertEqual(result, 'address_line1')

    def test_caps_to_snake_empty(self):
        from app import eq

        result = eq.EqPayloadConstructor.caps_to_snake('')
        self.assertEqual(result, '')

    def test_build_display_address(self):
        from app import eq

        result = eq.EqPayloadConstructor.build_display_address(self.uac_json['address'])
        self.assertEqual(result, self.eq_payload['display_address'])

    def test_build_display_address_raises(self):
        from app import eq

        attributes = {}

        with self.assertRaises(InvalidEqPayLoad) as ex:
            eq.EqPayloadConstructor.build_display_address(attributes)
            self.assertIn("Displayable address not in sample attributes", ex.exception.message)

    def test_build_display_address_prems(self):
        from app import eq

        for attributes, expected in [
            ({
                 "addressLine1": "A House",
                 "addressLine2": "",
             }, "A House"),
            ({
                 "addressLine1": "",
                 "addressLine2": "A Second House",
             }, "A Second House"),
            ({
                 "addressLine1": "A House",
                 "addressLine2": "On The Second Hill",
             }, "A House, On The Second Hill"),
            ({
                 "addressLine1": "Another House",
                 "addressLine2": "",
                 "addressLine3": "",
                 "townName": "",
                 "postcode": "AA1 2BB"
             }, "Another House, AA1 2BB"),
            ({
                 "addressLine1": "Another House",
                 "addressLine2": "",
                 "addressLine3": "",
                 "townName": "In Brizzle",
                 "postcode": ""
             }, "Another House, In Brizzle"),
            ({
                 "addressLine1": "Another House",
                 "addressLine2": "",
                 "addressLine3": "In The Shire",
                 "townName": "",
                 "postcode": ""
             }, "Another House, In The Shire"),
        ]:
            self.assertEqual(eq.EqPayloadConstructor.build_display_address(attributes), expected)

    def test_correct_iso8601_date_format(self):
        # Given a valid date
        date = '2007-01-25T12:00:00Z'

        # When format_date is called
        result = format_date(parse_date(date))

        # Then the date is formatted correctly
        self.assertEqual(result, '2007-01-25')

    def test_invalid_iso8601_date_format(self):
        # Given a valid date
        date = 'invalid_date'

        # When parse_date is called
        with self.assertRaises(InvalidEqPayLoad) as e:
            parse_date(date)

        # Then the date is formatted correctly
        self.assertEqual(e.exception.message, 'Unable to parse invalid_date')

    def test_incorrect_date_format(self):
        # Given an invalid date
        date = 'invalid_date'

        # When format_date is called
        with self.assertRaises(InvalidEqPayLoad) as e:
            format_date(date)

        # Then an InvalidEqPayLoad is raised
        self.assertEqual(e.exception.message, 'Unable to format invalid_date')







