import json
import datetime

from unittest import mock
from urllib.parse import urlsplit, parse_qs

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app import (
    BAD_CODE_MSG, INVALID_CODE_MSG, WEBCHAT_MISSING_QUERY_MSG, WEBCHAT_MISSING_COUNTRY_MSG, WEBCHAT_MISSING_NAME_MSG,
    POSTCODE_INVALID_MSG,
    BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY, WEBCHAT_MISSING_QUERY_MSG_CY, WEBCHAT_MISSING_COUNTRY_MSG_CY,
    WEBCHAT_MISSING_NAME_MSG_CY, POSTCODE_INVALID_MSG_CY)
from app.exceptions import InactiveCaseError, InvalidEqPayLoad
from app.handlers import IndexEN, IndexCY, IndexNI, WebChat


from . import RHTestCase, build_eq_raises, skip_encrypt


class TestHandlers(RHTestCase):

    @unittest_run_loop
    async def test_get_index_en(self):
        response = await self.client.request("GET", self.get_index_en)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('Enter the 16 character code printed on the letter', contents)
        self.assertIn(self.ons_logo_en, contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_index_cy(self):
        response = await self.client.request("GET", self.get_index_cy)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('Rhowch y cod 16 nod sydd', contents)
        self.assertIn(self.ons_logo_cy, contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_index_ni(self):
        response = await self.client.request("GET", self.get_index_ni)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('Enter the 16 character code printed on the letter', contents)
        self.assertIn(self.nisra_logo, contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_post_index_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)

            response = await self.client.request("POST", self.post_index_en, allow_redirects=False, data=self.form_data)

        self.assertEqual(response.status, 302)
        self.assertIn('/start/address-confirmation', response.headers['Location'])

    @unittest_run_loop
    async def test_post_index_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)

            response = await self.client.request("POST", self.post_index_cy, allow_redirects=False, data=self.form_data)

        self.assertEqual(response.status, 302)
        self.assertIn('/dechrau/cadarnhad-o-gyfeiriad', response.headers['Location'])

    @unittest_run_loop
    async def test_post_index_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)

            response = await self.client.request("POST", self.post_index_ni, allow_redirects=False, data=self.form_data)

        self.assertEqual(response.status, 302)
        self.assertIn('/ni/start/address-confirmation', response.headers['Location'])

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_en_region_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-ENG'
            eq_payload['language_code'] = 'en'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_en}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_en}"

            response = await self.client.request("POST", self.post_index_en, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_en, allow_redirects=False,
                                                     data=self.address_confirmation_data)

            self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_cy_region_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-WLS'
            eq_payload['language_code'] = 'cy'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_cy}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_cy}"

            response = await self.client.request("POST", self.post_index_cy, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/dechrau/cadarnhad-o-gyfeiriad', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                     data=self.address_confirmation_data)

            self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_ni_region_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-ENG'
            eq_payload['language_code'] = 'en'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_ni}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_ni}"

            response = await self.client.request("POST", self.post_index_ni, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_en, allow_redirects=False,
                                                     data=self.address_confirmation_data)

            self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_en_region_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_en}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_en}"

            response = await self.client.request("POST", self.post_index_en, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_en, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/start/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_en, allow_redirects=False,
                                                         data=self.language_options_ni_eng_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_cy_region_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_cy}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_cy}"

            response = await self.client.request("POST", self.post_index_cy, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/dechrau/cadarnhad-o-gyfeiriad', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/dechrau/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_cy, allow_redirects=False,
                                                         data=self.language_options_ni_eng_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_ni_region_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_ni}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_ni}"

            response = await self.client.request("POST", self.post_index_ni, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_ni, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_ni, allow_redirects=False,
                                                         data=self.language_options_ni_eng_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_en_language_choice_ul_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'eo'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_en}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_en}"

            response = await self.client.request("POST", self.post_index_en, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_en, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/start/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_en, allow_redirects=False,
                                                     data=self.language_options_ni_not_eng_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/start/select-language', response.headers['Location'])

                response = await self.client.request("POST", self.post_select_language_en, allow_redirects=False,
                                                         data=self.select_language_ni_ul_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_cy_language_choice_ul_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'eo'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_cy}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_cy}"

            response = await self.client.request("POST", self.post_index_cy, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/dechrau/cadarnhad-o-gyfeiriad', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/dechrau/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_cy, allow_redirects=False,
                                                     data=self.language_options_ni_not_eng_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/dechrau/select-language', response.headers['Location'])

                response = await self.client.request("POST", self.post_select_language_cy, allow_redirects=False,
                                                         data=self.select_language_ni_ul_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_ni_language_choice_ul_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'eo'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_ni}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_ni}"

            response = await self.client.request("POST", self.post_index_ni, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_ni, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_ni, allow_redirects=False,
                                                     data=self.language_options_ni_not_eng_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/select-language', response.headers['Location'])

                response = await self.client.request("POST", self.post_select_language_ni, allow_redirects=False,
                                                         data=self.select_language_ni_ul_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_en_language_choice_ga_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'ga'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_en}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_en}"

            response = await self.client.request("POST", self.post_index_en, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_ni, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/start/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_ni, allow_redirects=False,
                                                     data=self.language_options_ni_not_eng_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/start/select-language', response.headers['Location'])

                response = await self.client.request("POST", self.post_select_language_ni, allow_redirects=False,
                                                         data=self.select_language_ni_ga_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_cy_language_choice_ga_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'ga'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_cy}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_cy}"

            response = await self.client.request("POST", self.post_index_cy, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/dechrau/cadarnhad-o-gyfeiriad', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/dechrau/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_cy, allow_redirects=False,
                                                     data=self.language_options_ni_not_eng_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/dechrau/select-language', response.headers['Location'])

                response = await self.client.request("POST", self.post_select_language_cy, allow_redirects=False,
                                                         data=self.select_language_ni_ga_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_ni_language_choice_ga_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'ga'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_ni}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_ni}"

            response = await self.client.request("POST", self.post_index_ni, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_ni, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_ni, allow_redirects=False,
                                                     data=self.language_options_ni_not_eng_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/select-language', response.headers['Location'])

                response = await self.client.request("POST", self.post_select_language_ni, allow_redirects=False,
                                                         data=self.select_language_ni_ga_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_en_language_choice_en_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_en}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_en}"

            response = await self.client.request("POST", self.post_index_en, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_ni, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/start/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_ni, allow_redirects=False,
                                                     data=self.language_options_ni_not_eng_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/start/select-language', response.headers['Location'])

                response = await self.client.request("POST", self.post_select_language_ni, allow_redirects=False,
                                                         data=self.select_language_ni_en_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_cy_language_choice_en_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_cy}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_cy}"

            response = await self.client.request("POST", self.post_index_cy, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/dechrau/cadarnhad-o-gyfeiriad', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/dechrau/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_cy, allow_redirects=False,
                                                     data=self.language_options_ni_not_eng_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/dechrau/select-language', response.headers['Location'])

                response = await self.client.request("POST", self.post_select_language_cy, allow_redirects=False,
                                                         data=self.select_language_ni_en_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_ni_language_choice_en_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_ni}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_ni}"

            response = await self.client.request("POST", self.post_index_ni, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_ni, allow_redirects=False,
                                                     data=self.address_confirmation_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/language-options', response.headers['Location'])

                response = await self.client.request("POST", self.post_language_options_ni, allow_redirects=False,
                                                     data=self.language_options_ni_not_eng_data)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/select-language', response.headers['Location'])

                response = await self.client.request("POST", self.post_select_language_ni, allow_redirects=False,
                                                         data=self.select_language_ni_en_data)

                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_address_edit_with_build_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.put(self.rhsvc_modify_address + self.case_id + '/address', payload=self.modify_address_data)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_en}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_en}"

            response = await self.client.request("POST", self.post_index_en, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_en, allow_redirects=False,
                                                     data=self.address_confirmation_data_edit)
                self.assertEqual(response.status, 302)

                response = await self.client.request("POST", self.post_address_edit_en, allow_redirects=False,
                                                     data=self.address_edit_data)

                self.assertLogLine(logs_home, 'Raising address modification call')
                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_address_edit_with_build_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.put(self.rhsvc_modify_address + self.case_id + '/address', payload=self.modify_address_data)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-WLS'
            eq_payload['language_code'] = 'cy'
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_cy}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_cy}"

            response = await self.client.request("POST", self.post_index_cy, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                     data=self.address_confirmation_data_edit)
                self.assertEqual(response.status, 302)

                response = await self.client.request("POST", self.post_address_edit_cy, allow_redirects=False,
                                                     data=self.address_edit_data)

                self.assertLogLine(logs_home, 'Raising address modification call')
                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_address_edit_with_build_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.put(self.rhsvc_modify_address + self.case_id + '/address', payload=self.modify_address_data)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['account_service_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_url_ni}"
            eq_payload['account_service_log_out_url'] = \
                f"{self.app['ACCOUNT_SERVICE_URL']}{self.app['URL_PATH_PREFIX']}{self.account_service_log_out_url_ni}"

            response = await self.client.request("POST", self.post_index_ni, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request("POST", self.post_address_confirmation_ni, allow_redirects=False,
                                                     data=self.address_confirmation_data_edit)
                self.assertEqual(response.status, 302)

                response = await self.client.request("POST", self.post_address_edit_ni, allow_redirects=False,
                                                     data=self.address_edit_data)

                self.assertLogLine(logs_home, 'Raising address modification call')
                self.assertLogLine(logs_home, 'Redirecting to eQ')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']), redirected_url)  # outputs url on fail
        _, _, _, query, *_ = urlsplit(redirected_url)  # we only care about the query string
        token = json.loads(parse_qs(query)['token'][0])  # convert token to dict
        self.assertEqual(eq_payload.keys(), token.keys())  # fail early if payload keys differ
        for key in eq_payload.keys():
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue  # skip uuid / time generated values
            self.assertEqual(eq_payload[key], token[key], key)  # outputs failed key as msg

    @build_eq_raises
    @unittest_run_loop
    async def test_post_index_build_raises_InvalidEqPayLoad_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request("POST", self.post_index_en, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request("POST", self.post_address_confirmation_en, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Service failed to build eQ payload")

        # then error handler catches exception and renders error.html
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @build_eq_raises
    @unittest_run_loop
    async def test_post_index_build_raises_InvalidEqPayLoad_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request("POST", self.post_index_cy, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/dechrau/cadarnhad-o-gyfeiriad', response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Service failed to build eQ payload")

        # then error handler catches exception and renders error.html
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @build_eq_raises
    @unittest_run_loop
    async def test_post_index_build_raises_InvalidEqPayLoad_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request("POST", self.post_index_ni, allow_redirects=False, data=self.form_data)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/address-confirmation', response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request("POST", self.post_address_confirmation_ni, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Service failed to build eQ payload")

        # then error handler catches exception and renders error.html
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_invalid_blank_en(self):
        form_data = self.form_data.copy()
        del form_data['uac']

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index_en, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_invalid_blank_cy(self):
        form_data = self.form_data.copy()
        del form_data['uac']

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index_cy, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(BAD_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_index_invalid_blank_ni(self):
        form_data = self.form_data.copy()
        del form_data['uac']

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index_ni, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_url_en(self):
        form_data = self.form_data.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index_en, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_url_cy(self):
        form_data = self.form_data.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index_cy, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(BAD_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_url_ni(self):
        form_data = self.form_data.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index_ni, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_random_en(self):
        form_data = self.form_data.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index_en, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_random_cy(self):
        form_data = self.form_data.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index_cy, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(BAD_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_random_ni(self):
        form_data = self.form_data.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_index_ni, data=form_data)
        self.assertLogLine(cm, "Attempt to use a malformed access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_uac_active_missing_en(self):
        uac_json = self.uac_json.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an inactive access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Your unique access code has expired', contents)

    @unittest_run_loop
    async def test_post_index_uac_active_missing_cy(self):
        uac_json = self.uac_json_cy.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an inactive access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Mae eich cod mynediad unigryw wedi dod i ben', contents)

    @unittest_run_loop
    async def test_post_index_uac_active_missing_ni(self):
        uac_json = self.uac_json_ni.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_ni, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an inactive access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Your unique access code has expired', contents)

    @unittest_run_loop
    async def test_post_index_uac_inactive_en(self):
        uac_json = self.uac_json.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an inactive access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Your unique access code has expired', contents)

    @unittest_run_loop
    async def test_post_index_uac_inactive_cy(self):
        uac_json = self.uac_json_cy.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an inactive access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Mae eich cod mynediad unigryw wedi dod i ben', contents)

    @unittest_run_loop
    async def test_post_index_uac_inactive_ni(self):
        uac_json = self.uac_json_ni.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_ni, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an inactive access code")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Your unique access code has expired', contents)

    @unittest_run_loop
    async def test_post_index_uac_case_status_not_found_en(self):
        uac_json = self.uac_json.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertLogLine(cm, "Service failed to build eQ payload")

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_uac_case_status_not_found_cy(self):
        uac_json = self.uac_json_cy.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertLogLine(cm, "Service failed to build eQ payload")


        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_uac_case_status_not_found_ni(self):
        uac_json = self.uac_json_ni.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_ni, data=self.form_data)
            self.assertLogLine(cm, "Service failed to build eQ payload")

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_connection_error_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertLogLine(cm, "Client failed to connect", url=self.rhsvc_url)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_connection_error_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertLogLine(cm, "Client failed to connect", url=self.rhsvc_url)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_connection_error_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index_ni, data=self.form_data)
            self.assertLogLine(cm, "Client failed to connect", url=self.rhsvc_url)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_500_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_500_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index_ni, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_503_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_503_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_index_ni, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_404_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an invalid access code", client_ip=None)

        self.assertEqual(response.status, 401)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(INVALID_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_404_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an invalid access code", client_ip=None)

        self.assertEqual(response.status, 401)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(INVALID_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_404_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request("POST", self.post_index_ni, data=self.form_data)
            self.assertLogLine(cm, "Attempt to use an invalid access code", client_ip=None)

        self.assertEqual(response.status, 401)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(INVALID_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_403_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_403_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_403_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_ni, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_401_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_401_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_ni, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_400_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_400_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_400_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_index_ni, data=self.form_data)
            self.assertLogLine(cm, "Error in response", status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_address_confirmation_survey_launched_connection_error_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched, exception=ClientConnectionError('Failed'))

            response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_address_confirmation_en, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Client failed to connect", url=self.rhsvc_url_surveylaunched)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_address_confirmation_survey_launched_connection_error_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.post(self.rhsvc_url_surveylaunched, exception=ClientConnectionError('Failed'))

            response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Client failed to connect", url=self.rhsvc_url_surveylaunched)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_401_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched, status=401)

            response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_address_confirmation_en, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Error in response", status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.post(self.rhsvc_url_surveylaunched, status=401)

            response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Error in response", status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_404_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched, status=404)

            response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertEqual(response.status, 200)

            response = await self.client.request("POST", self.post_address_confirmation_en, allow_redirects=False,
                                                 data=self.address_confirmation_data)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_404_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.post(self.rhsvc_url_surveylaunched, status=404)

            response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertEqual(response.status, 200)

            response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                 data=self.address_confirmation_data)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_500_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json)
            mocked.post(self.rhsvc_url_surveylaunched, status=500)

            response = await self.client.request("POST", self.post_index_en, data=self.form_data)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_address_confirmation_en, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Error in response", status_code=500)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.post(self.rhsvc_url_surveylaunched, status=500)

            response = await self.client.request("POST", self.post_index_cy, data=self.form_data)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                     data=self.address_confirmation_data)
            self.assertLogLine(cm, "Error in response", status_code=500)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)
            self.assertIn(self.ons_logo_cy, contents)

    def test_check_open_weekday_open_census_weekend(self):
        mocked_now = datetime.datetime(2019, 10, 12, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertTrue(WebChat.check_open())

    def test_check_open_weekday_closed_census_weekend(self):
        mocked_now = datetime.datetime(2019, 10, 13, 6, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    def test_check_open_weekday_open(self):
        mocked_now = datetime.datetime(2019, 6, 17, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertTrue(WebChat.check_open())

    def test_check_open_weekday_closed(self):
        mocked_now = datetime.datetime(2019, 6, 16, 19, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    def test_check_open_saturday_open(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertTrue(WebChat.check_open())

    def test_check_open_saturday_closed(self):
        mocked_now = datetime.datetime(2019, 6, 15, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    def test_check_open_sunday_closed(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    @unittest_run_loop
    async def test_get_webchat_open_en(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            response = await self.client.request("GET", self.get_webchat_en)
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Enter your name', contents)
            self.assertEqual(contents.count('radio__input'), 10)
            self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_webchat_open_cy(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            response = await self.client.request("GET", self.get_webchat_cy)
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Nodwch eich enw', contents)
            self.assertEqual(contents.count('radio__input'), 10)
            self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_webchat_open_ni(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            response = await self.client.request("GET", self.get_webchat_ni)
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Enter your name', contents)
            self.assertEqual(contents.count('radio__input'), 10)
            self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_en(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request("GET", self.get_webchat_en)

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_cy(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request("GET", self.get_webchat_cy)

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Gwyliau Banc', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_ni(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request("GET", self.get_webchat_ni)

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_clientconnectionerror_en(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, exception=ClientConnectionError('Failed'))

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("GET", self.get_webchat_en)
                self.assertLogLine(cm, "Client failed to connect")
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_clientconnectionerror_cy(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, exception=ClientConnectionError('Failed'))

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("GET", self.get_webchat_cy)
                self.assertLogLine(cm, "Client failed to connect")
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Gwyliau Banc', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_clientconnectionerror_ni(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, exception=ClientConnectionError('Failed'))

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("GET", self.get_webchat_ni)
                self.assertLogLine(cm, "Client failed to connect")
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_500_en(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=500)

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("GET", self.get_webchat_en)

                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_500_cy(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=500)

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("GET", self.get_webchat_cy)

                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Gwyliau Banc', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_500_ni(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=500)

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("GET", self.get_webchat_ni)

                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_query_en(self):
        form_data = self.webchat_form_data.copy()
        del form_data['query']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat_en, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_QUERY_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_query_cy(self):
        form_data = self.webchat_form_data.copy()
        del form_data['query']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat_cy, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_QUERY_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_query_ni(self):
        form_data = self.webchat_form_data.copy()
        del form_data['query']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat_ni, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_QUERY_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_country_en(self):
        form_data = self.webchat_form_data.copy()
        del form_data['country']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat_en, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_COUNTRY_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_country_cy(self):
        form_data = self.webchat_form_data.copy()
        del form_data['country']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat_cy, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_COUNTRY_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_country_ni(self):
        form_data = self.webchat_form_data.copy()
        del form_data['country']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat_ni, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_COUNTRY_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_name_en(self):
        form_data = self.webchat_form_data.copy()
        del form_data['screen_name']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat_en, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_NAME_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_name_cy(self):
        form_data = self.webchat_form_data.copy()
        del form_data['screen_name']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat_cy, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_NAME_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_name_ni(self):
        form_data = self.webchat_form_data.copy()
        del form_data['screen_name']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request("POST", self.post_webchat_ni, data=form_data)
        self.assertLogLine(cm, "Form submission error")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_NAME_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_open_en(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            response = await self.client.request("POST", self.post_webchat_en, allow_redirects=False,
                                                 data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('iframe', contents)

    @unittest_run_loop
    async def test_post_webchat_open_cy(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            response = await self.client.request("POST", self.post_webchat_cy, allow_redirects=False,
                                                 data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('iframe', contents)

    @unittest_run_loop
    async def test_post_webchat_open_ni(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            response = await self.client.request("POST", self.post_webchat_ni, allow_redirects=False,
                                                 data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('iframe', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_en(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request("POST", self.post_webchat_en, allow_redirects=False,
                                                     data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_cy(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request("POST", self.post_webchat_cy, allow_redirects=False,
                                                     data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Gwyliau Banc', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_ni(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request("POST", self.post_webchat_ni, allow_redirects=False,
                                                     data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_clientconnectionerror_en(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, exception=ClientConnectionError('Failed'))

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("POST", self.post_webchat_en, allow_redirects=False,
                                                         data=self.webchat_form_data)
                self.assertLogLine(cm, "Client failed to connect")
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_clientconnectionerror_cy(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, exception=ClientConnectionError('Failed'))

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("POST", self.post_webchat_cy, allow_redirects=False,
                                                         data=self.webchat_form_data)
                self.assertLogLine(cm, "Client failed to connect")
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Gwyliau Banc', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_clientconnectionerror_ni(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, exception=ClientConnectionError('Failed'))

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("POST", self.post_webchat_ni, allow_redirects=False,
                                                         data=self.webchat_form_data)
                self.assertLogLine(cm, "Client failed to connect")
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_500_en(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=500)

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("POST", self.post_webchat_en, allow_redirects=False,
                                                         data=self.webchat_form_data)
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_500_cy(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=500)

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("POST", self.post_webchat_cy, allow_redirects=False,
                                                         data=self.webchat_form_data)
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Gwyliau Banc', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_500_ni(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=500)

                with self.assertLogs('respondent-home', 'ERROR') as cm:
                    response = await self.client.request("POST", self.post_webchat_ni, allow_redirects=False,
                                                         data=self.webchat_form_data)
                self.assertLogLine(cm, "Failed to send WebChat Closed")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Bank Holidays', contents)

    def test_uac_hash_en(self):
        # Given some post data
        post_data = {'uac': 'w4nw wpph jjpt p7fn', 'action[save_continue]': ''}

        # When join_uac is called
        result = IndexEN.uac_hash(post_data)

        # Then a single string built from the uac values is returned
        self.assertEqual(result, '8a9d5db4bbee34fd16e40aa2aaae52cfbdf1842559023614c30edb480ec252b4')

    def test_join_uac_cy(self):
        # Given some post data
        post_data = {'uac': 'w4nw wpph jjpt p7fn', 'action[save_continue]': ''}

        # When join_uac is called
        result = IndexCY.uac_hash(post_data)

        # Then a single string built from the uac values is returned
        self.assertEqual(result, '8a9d5db4bbee34fd16e40aa2aaae52cfbdf1842559023614c30edb480ec252b4')

    def test_join_uac_ni(self):
        # Given some post data
        post_data = {'uac': 'w4nw wpph jjpt p7fn', 'action[save_continue]': ''}

        # When join_uac is called
        result = IndexNI.uac_hash(post_data)

        # Then a single string built from the uac values is returned
        self.assertEqual(result, '8a9d5db4bbee34fd16e40aa2aaae52cfbdf1842559023614c30edb480ec252b4')

    def test_join_uac_missing_en(self):
        # Given some missing post data
        post_data = {'uac': '', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            IndexEN.uac_hash(post_data)
        # Then a TypeError is raised

    def test_join_uac_missing_cy(self):
        # Given some missing post data
        post_data = {'uac': '', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            IndexCY.uac_hash(post_data)
        # Then a TypeError is raised

    def test_join_uac_missing_ni(self):
        # Given some missing post data
        post_data = {'uac': '', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            IndexNI.uac_hash(post_data)
        # Then a TypeError is raised

    def test_join_uac_some_missing_en(self):
        # Given some missing post data
        post_data = {'uac': '123456781234', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            IndexEN.uac_hash(post_data)
        # Then a TypeError is raised

    def test_join_uac_some_missing_cy(self):
        # Given some missing post data
        post_data = {'uac': '123456781234', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            IndexCY.uac_hash(post_data)
        # Then a TypeError is raised

    def test_join_uac_some_missing_ni(self):
        # Given some missing post data
        post_data = {'uac': '123456781234', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            IndexNI.uac_hash(post_data)
        # Then a TypeError is raised

    def test_validate_case_en(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'OK'}

        # When validate_case is called
        IndexEN.validate_case(case_json)

        # Nothing happens

    def test_validate_case_cy(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'OK'}

        # When validate_case is called
        IndexCY.validate_case(case_json)

        # Nothing happens

    def test_validate_case_ni(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'OK'}

        # When validate_case is called
        IndexNI.validate_case(case_json)

        # Nothing happens

    def test_validate_case_inactive_en(self):
        # Given a dict with an active key and value
        case_json = {'active': False, 'caseStatus': 'OK'}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            IndexEN.validate_case(case_json)

        # Then an InactiveCaseError is raised

    def test_validate_case_inactive_cy(self):
        # Given a dict with an active key and value
        case_json = {'active': False, 'caseStatus': 'OK'}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            IndexCY.validate_case(case_json)

        # Then an InactiveCaseError is raised

    def test_validate_case_inactive_ni(self):
        # Given a dict with an active key and value
        case_json = {'active': False, 'caseStatus': 'OK'}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            IndexNI.validate_case(case_json)

        # Then an InactiveCaseError is raised

    def test_validate_caseStatus_notfound_en(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'NOT_FOUND'}

        # When validate_case is called
        with self.assertRaises(InvalidEqPayLoad):
            IndexEN.validate_case(case_json)

        # Then an InvalidEqPayload is raised

    def test_validate_caseStatus_notfound_cy(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'NOT_FOUND'}

        # When validate_case is called
        with self.assertRaises(InvalidEqPayLoad):
            IndexCY.validate_case(case_json)

        # Then an InvalidEqPayload is raised

    def test_validate_caseStatus_notfound_ni(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'NOT_FOUND'}

        # When validate_case is called
        with self.assertRaises(InvalidEqPayLoad):
            IndexNI.validate_case(case_json)

        # Then an InvalidEqPayload is raised

    def test_validate_case_empty_en(self):
        # Given an empty dict
        case_json = {}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            IndexEN.validate_case(case_json)

        # Then an InactiveCaseError is raised

    def test_validate_case_empty_cy(self):
        # Given an empty dict
        case_json = {}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            IndexCY.validate_case(case_json)

        # Then an InactiveCaseError is raised

    def test_validate_case_empty_ni(self):
        # Given an empty dict
        case_json = {}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            IndexNI.validate_case(case_json)

        # Then an InactiveCaseError is raised

    @unittest_run_loop
    async def test_get_request_access_code_hh_en(self):
        response = await self.client.request("GET", self.get_requestcode_household_en)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Request a new access code', contents)
        self.assertIn('You will need to provide:', contents)

    @unittest_run_loop
    async def test_get_request_access_code_hh_cy(self):
        response = await self.client.request("GET", self.get_requestcode_household_cy)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Gofyn am god mynediad newydd', contents)
        self.assertIn('Bydd angen i chi ddarparu:', contents)

    @unittest_run_loop
    async def test_get_request_access_code_hh_ni(self):
        response = await self.client.request("GET", self.get_requestcode_household_ni)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Request a new access code', contents)
        self.assertIn('You will need to provide:', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hh_en(self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_requestcode_enter_address_hh_en,
                                                 data=self.request_code_form_data_invalid)
        self.assertLogLine(cm, "Attempt to use an invalid postcode")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hh_cy(self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_requestcode_enter_address_hh_cy,
                                                 data=self.request_code_form_data_invalid)
        self.assertLogLine(cm, "Attempt to use an invalid postcode")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hh_ni(self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_requestcode_enter_address_hh_ni,
                                                 data=self.request_code_form_data_invalid)
        self.assertLogLine(cm, "Attempt to use an invalid postcode")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hh_en(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_en,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Valid postcode")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hh_cy(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_cy,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Valid postcode")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Dewiswch eich cyfeiriad', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hh_ni(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_ni,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Valid postcode")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hh_en(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_en,
                                                     data=self.request_code_form_data_valid)
                self.assertLogLine(cm, "Valid postcode")

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('We cannot find your address', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hh_cy(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_cy,
                                                     data=self.request_code_form_data_valid)
                self.assertLogLine(cm, "Valid postcode")

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn("Allwn ni ddim dod o hyd", contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hh_ni(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_ni,
                                                     data=self.request_code_form_data_valid)
                self.assertLogLine(cm, "Valid postcode")

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('We cannot find your address', contents)

    # Commented out as session not maintaining the new data between pages - to be revisited.
    # @unittest_run_loop
    # async def test_get_request_code_confirm_address_hh(self):
    #
    #     with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
    #         mocked_get_ai_postcode.return_value = self.ai_postcode_results
    #
    #         with self.assertLogs('respondent-home', 'INFO') as cm:
    #             response = await self.client.request("POST", self.post_requestcode_hh, data=self.request_code_form_data_valid)
    #             self.assertLogLine(cm, "Valid postcode")
    #
    #             self.assertEqual(response.status, 200)
    #             self.assertIn('1 Gate Reach', str(await response.content.read()))
    #
    #             with self.assertLogs('respondent-home', 'INFO') as cm:
    #                 response = await self.client.request("POST", self.post_requestcode_selectaddress,
    #                                                      data=self.post_requestcode_address_confirmation_data)
    #                 self.assertLogLine(cm, "Session updated")
    #                 self.assertEqual(response.status, 200)

    @unittest_run_loop
    async def test_get_request_access_code_hi_en(self):
        response = await self.client.request("GET", self.get_requestcode_individual_en)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Request an individual access code', contents)
        self.assertIn('You will need to provide:', contents)

    @unittest_run_loop
    async def test_get_request_access_code_hi_cy(self):
        response = await self.client.request("GET", self.get_requestcode_individual_cy)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Gofyn am god mynediad unigryw', contents)
        self.assertIn('Bydd angen i chi ddarparu:', contents)

    @unittest_run_loop
    async def test_get_request_access_code_hi_ni(self):
        response = await self.client.request("GET", self.get_requestcode_individual_ni)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Request an individual access code', contents)
        self.assertIn('You will need to provide:', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_address_hi_en(self):
        response = await self.client.request("GET", self.get_requestcode_enter_address_hi_en)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('What is your postcode?', contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('UK postcode', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_address_hi_cy(self):
        response = await self.client.request("GET", self.get_requestcode_enter_address_hi_cy)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Beth yw eich cod post?', contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('Cod post yn y Deyrnas Unedig', contents)

    @unittest_run_loop
    async def test_get_request_access_code_enter_address_hi_ni(self):
        response = await self.client.request("GET", self.get_requestcode_enter_address_hi_ni)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('What is your postcode?', contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('UK postcode', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hi_en(self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_requestcode_enter_address_hi_en,
                                                 data=self.request_code_form_data_invalid)
        self.assertLogLine(cm, "Attempt to use an invalid postcode")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hi_cy(self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_requestcode_enter_address_hi_cy,
                                                 data=self.request_code_form_data_invalid)
        self.assertLogLine(cm, "Attempt to use an invalid postcode")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_hi_ni(self):

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request("POST", self.post_requestcode_enter_address_hi_ni,
                                                 data=self.request_code_form_data_invalid)
        self.assertLogLine(cm, "Attempt to use an invalid postcode")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(POSTCODE_INVALID_MSG, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hi_en(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hi_en,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Valid postcode")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hi_cy(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hi_cy,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Valid postcode")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn('Dewiswch eich cyfeiriad', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_good_postcode_hi_ni(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hi_ni,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Valid postcode")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn('Select your address', str(resp_content))
            self.assertIn('1 Gate Reach', str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hi_en(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hi_en,
                                                     data=self.request_code_form_data_valid)
                self.assertLogLine(cm, "Valid postcode")

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_en, contents)
                self.assertIn('We cannot find your address', contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hi_cy(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hi_cy,
                                                     data=self.request_code_form_data_valid)
                self.assertLogLine(cm, "Valid postcode")

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.ons_logo_cy, contents)
                self.assertIn("Allwn ni ddim dod o hyd", contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_hi_ni(self):
        with mock.patch('app.handlers.RequestCodeCommon.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hi_ni,
                                                     data=self.request_code_form_data_valid)
                self.assertLogLine(cm, "Valid postcode")

                self.assertEqual(response.status, 200)
                contents = str(await response.content.read())
                self.assertIn(self.nisra_logo, contents)
                self.assertIn('We cannot find your address', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_en,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Client failed to connect", url=self.addressindexsvc_url + self.postcode_valid)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_cy,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Client failed to connect", url=self.addressindexsvc_url + self.postcode_valid)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_ni,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Client failed to connect", url=self.addressindexsvc_url + self.postcode_valid)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_en,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_cy,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_ni,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_en,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_cy,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_ni,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_en,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_cy,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_ni,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_en,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_cy,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_ni,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_hh_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_en,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_hh_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_cy,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn("Mae\\\'n flin gennym, aeth rhywbeth o\\\'i le", contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_hh_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request("POST", self.post_requestcode_enter_address_hh_ni,
                                                     data=self.request_code_form_data_valid)
            self.assertLogLine(cm, "Error in response", status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_get_address_confirmation_direct_access_en(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.get_address_confirmation_en, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Enter the 16 character code printed on the letter', contents)

    @unittest_run_loop
    async def test_get_address_confirmation_direct_access_cy(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.get_address_confirmation_cy, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Rhowch y cod 16 nod sydd', contents)

    @unittest_run_loop
    async def test_get_address_confirmation_direct_access_ni(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.get_address_confirmation_ni, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Enter the 16 character code printed on the letter', contents)

    @unittest_run_loop
    async def test_post_address_confirmation_direct_access_en(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("POST", self.post_address_confirmation_en, allow_redirects=False,
                                                 data=self.address_confirmation_data)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Enter the 16 character code printed on the letter', contents)

    @unittest_run_loop
    async def test_post_address_confirmation_direct_access_cy(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("POST", self.post_address_confirmation_cy, allow_redirects=False,
                                                 data=self.address_confirmation_data)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Rhowch y cod 16 nod sydd', contents)

    @unittest_run_loop
    async def test_post_address_confirmation_direct_access_ni(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("POST", self.post_address_confirmation_ni, allow_redirects=False,
                                                 data=self.address_confirmation_data)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Enter the 16 character code printed on the letter', contents)

    @unittest_run_loop
    async def test_get_address_edit_direct_access_en(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.get_address_edit_en, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Enter the 16 character code printed on the letter', contents)

    @unittest_run_loop
    async def test_get_address_edit_direct_access_cy(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.get_address_edit_cy, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Rhowch y cod 16 nod sydd', contents)

    @unittest_run_loop
    async def test_get_address_edit_direct_access_ni(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.get_address_edit_ni, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Enter the 16 character code printed on the letter', contents)

    @unittest_run_loop
    async def test_post_address_edit_direct_access_en(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.post_address_edit_en, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Enter the 16 character code printed on the letter', contents)

    @unittest_run_loop
    async def test_post_address_edit_direct_access_cy(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.post_address_edit_cy, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Rhowch y cod 16 nod sydd', contents)

    @unittest_run_loop
    async def test_post_address_edit_direct_access_ni(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request("GET", self.post_address_edit_ni, allow_redirects=False)
        self.assertLogLine(cm, "Permission denied")
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Enter the 16 character code printed on the letter', contents)
