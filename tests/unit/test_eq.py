from unittest import mock
from aiohttp.test_utils import unittest_run_loop
from app.eq import EqPayloadConstructor
from app.exceptions import InvalidEqPayLoad

from . import RHTestCase


class TestEq(RHTestCase):

    def test_create_eq_constructor(self):
        self.assertIsInstance(EqPayloadConstructor(
            self.uac_json, self.uac_json['address'], self.app, None), EqPayloadConstructor)

    def test_create_eq_constructor_missing_case_id(self):
        uac_json = self.uac_json.copy()
        del uac_json['caseId']

        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqPayloadConstructor(uac_json, self.uac_json['address'], self.app, None)
        self.assertIn('No case id in supplied case JSON', ex.exception.message)

    def test_create_eq_constructor_missing_ce_id(self):
        uac_json = self.uac_json.copy()
        del uac_json["collectionExerciseId"]

        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqPayloadConstructor(uac_json, self.uac_json['address'], self.app, None)
        self.assertIn(f'No collection id in supplied case JSON', ex.exception.message)

    def test_create_eq_constructor_missing_questionnaire_id(self):
        uac_json = self.uac_json.copy()
        del uac_json["questionnaireId"]

        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqPayloadConstructor(uac_json, self.uac_json['address'], self.app, None)
            self.assertIn(f'No questionnaireId in supplied case JSON', ex.exception.message)

    def test_create_eq_constructor_missing_case_type(self):
        uac_json = self.uac_json.copy()
        del uac_json["caseType"]

        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqPayloadConstructor(uac_json, self.uac_json['address'], self.app, None)
            self.assertIn(f'No case type in supplied case JSON', ex.exception.message)

    def test_create_eq_constructor_missing_uprn(self):
        uac_json = self.uac_json.copy()
        del uac_json["address"]["uprn"]

        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqPayloadConstructor(uac_json, self.uac_json['address'], self.app, None)
            self.assertIn(f'Could not retrieve address uprn from case JSON', ex.exception.message)

    @unittest_run_loop
    async def test_build(self):
        with mock.patch('app.eq.uuid4') as mocked_uuid4, mock.patch('app.eq.time.time') as mocked_time:
            # NB: has to be mocked after setup but before import
            mocked_time.return_value = self.eq_payload['iat']
            mocked_uuid4.return_value = self.jti

            with self.assertLogs('app.eq', 'DEBUG') as cm:
                payload = await EqPayloadConstructor(
                    self.uac_json, self.uac_json['address'], self.app, None).build()
            self.assertLogLine(cm, 'Creating payload for JWT', case_id=self.case_id, tx_id=self.jti)

        mocked_uuid4.assert_called()
        mocked_time.assert_called()
        self.assertEqual(payload, self.eq_payload)

    @unittest_run_loop
    async def test_build_assisted_digital(self):
        eq_payload = self.eq_payload.copy()
        eq_payload['channel'] = 'ad'
        eq_payload['user_id'] = '1000007'
        with mock.patch('app.eq.uuid4') as mocked_uuid4, mock.patch('app.eq.time.time') as mocked_time:
            # NB: has to be mocked after setup but before import
            mocked_time.return_value = self.eq_payload['iat']
            mocked_uuid4.return_value = self.jti

            with self.assertLogs('app.eq', 'DEBUG') as cm:
                payload = await EqPayloadConstructor(
                    self.uac_json, self.uac_json['address'], self.app, eq_payload['user_id']).build()
            self.assertLogLine(cm, 'Creating payload for JWT', case_id=self.case_id, tx_id=self.jti)

        mocked_uuid4.assert_called()
        mocked_time.assert_called()
        self.assertEqual(payload, eq_payload)

    @unittest_run_loop
    async def test_build_raises_InvalidEqPayLoad_missing_attributes(self):

        from app import eq  # NB: local import to avoid overwriting the patched version for some tests

        with self.assertRaises(InvalidEqPayLoad) as ex:
            await eq.EqPayloadConstructor(
                self.uac_json, None, self.app, None).build()
        self.assertIn('Attributes is empty', ex.exception.message)

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


