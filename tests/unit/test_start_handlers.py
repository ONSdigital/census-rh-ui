import json

from unittest import mock
from urllib.parse import urlsplit, parse_qs

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app import (BAD_CODE_MSG, INVALID_CODE_MSG,
                 BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY)
from app.exceptions import InactiveCaseError, InvalidEqPayLoad
from app.start_handlers import Start

from . import RHTestCase, build_eq_raises, skip_encrypt


class TestStartHandlers(RHTestCase):
    @unittest_run_loop
    async def test_get_index_en(self):
        response = await self.client.request('GET', self.get_start_en)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)
        self.assertIn(self.ons_logo_en, contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_index_cy(self):
        response = await self.client.request('GET', self.get_start_cy)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('Rhowch y cod 16 nod sydd', contents)
        self.assertIn(self.ons_logo_cy, contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_index_ni(self):
        response = await self.client.request('GET', self.get_start_ni)
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)
        self.assertIn(self.nisra_logo, contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_post_index_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/start/confirm-address',
                      response.headers['Location'])

    @unittest_run_loop
    async def test_post_index_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/cy/start/confirm-address/',
                      response.headers['Location'])

    @unittest_run_loop
    async def test_post_index_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/ni/start/confirm-address',
                      response.headers['Location'])

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_en_region_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-ENG'
            eq_payload['language_code'] = 'en'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/en'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/confirm-address',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)

            self.assertLogEvent(logs_home, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_ni_region_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload['account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload['account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/confirm-address',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_ni,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/language-options',
                              response.headers['Location'])

                response = await self.client.request(
                    'POST',
                    self.post_start_language_options_ni,
                    allow_redirects=False,
                    data=self.start_ni_language_option_data_yes)

                self.assertLogEvent(logs_home, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_ni_language_choice_ul_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'eo'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload['account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload['account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/confirm-address',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_ni,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/language-options',
                              response.headers['Location'])

                response = await self.client.request(
                    'POST',
                    self.post_start_language_options_ni,
                    allow_redirects=False,
                    data=self.start_ni_language_option_data_no)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/select-language',
                              response.headers['Location'])

                response = await self.client.request(
                    'POST',
                    self.post_start_select_language_ni,
                    allow_redirects=False,
                    data=self.start_ni_select_language_data_ul)

                self.assertLogEvent(logs_home, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_ni_language_choice_ga_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'ga'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload['account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload['account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/confirm-address',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_ni,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/language-options',
                              response.headers['Location'])

                response = await self.client.request(
                    'POST',
                    self.post_start_language_options_ni,
                    allow_redirects=False,
                    data=self.start_ni_language_option_data_no)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/select-language',
                              response.headers['Location'])

                response = await self.client.request(
                    'POST',
                    self.post_start_select_language_ni,
                    allow_redirects=False,
                    data=self.start_ni_select_language_data_ga)

                self.assertLogEvent(logs_home, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_with_build_ni_language_choice_en_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-NIR'
            eq_payload['language_code'] = 'en'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/confirm-address',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_ni,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/language-options',
                              response.headers['Location'])

                response = await self.client.request(
                    'POST',
                    self.post_start_language_options_ni,
                    allow_redirects=False,
                    data=self.start_ni_language_option_data_no)

                self.assertEqual(response.status, 302)
                self.assertIn('/ni/start/select-language',
                              response.headers['Location'])

                response = await self.client.request(
                    'POST',
                    self.post_start_select_language_ni,
                    allow_redirects=False,
                    data=self.start_ni_select_language_data_en)

                self.assertLogEvent(logs_home, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_address_edit_with_build_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)
            mocked.put(self.rhsvc_cases_url + self.case_id + '/address',
                       payload=self.start_modify_address_data)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/en'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_no)
                self.assertEqual(response.status, 302)

                response = await self.client.request(
                    'POST',
                    self.post_start_modify_address_en,
                    allow_redirects=False,
                    data=self.start_modify_address_data_valid)

                self.assertLogEvent(logs_home,
                                    'raising address modification call')
                self.assertLogEvent(logs_home, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_address_edit_with_build_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.put(self.rhsvc_cases_url + self.case_id + '/address',
                       payload=self.start_modify_address_data)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-WLS'
            eq_payload['language_code'] = 'cy'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/cy'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_no)
                self.assertEqual(response.status, 302)

                response = await self.client.request(
                    'POST',
                    self.post_start_modify_address_cy,
                    allow_redirects=False,
                    data=self.start_modify_address_data_valid)

                self.assertLogEvent(logs_home,
                                    'raising address modification call')
                self.assertLogEvent(logs_home, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_index_address_edit_with_build_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)
            mocked.put(self.rhsvc_cases_url + self.case_id + '/address',
                       payload=self.start_modify_address_data)
            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/ni'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)

            with self.assertLogs('respondent-home', 'DEBUG') as logs_home:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_ni,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_no)
                self.assertEqual(response.status, 302)

                response = await self.client.request(
                    'POST',
                    self.post_start_modify_address_ni,
                    allow_redirects=False,
                    data=self.start_modify_address_data_valid)

                self.assertLogEvent(logs_home,
                                    'raising address modification call')
                self.assertLogEvent(logs_home, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    @build_eq_raises
    @unittest_run_loop
    async def test_post_index_build_raises_InvalidEqPayLoad_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/confirm-address',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'service failed to build eq payload')

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

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/cy/start/confirm-address/',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        # then error handler catches exception and renders error.html
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @build_eq_raises
    @unittest_run_loop
    async def test_post_index_build_raises_InvalidEqPayLoad_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/confirm-address/',
                          response.headers['Location'])

            response = await self.client.request('POST',
                                                 self.post_start_confirm_address_ni,
                                                 allow_redirects=False,
                                                 data=self.start_confirm_address_data_yes)
            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/language-options/',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request(
                    'POST',
                    self.post_start_language_options_ni,
                    allow_redirects=False,
                    data=self.start_ni_language_option_data_yes)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        # then error handler catches exception and renders error.html
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_invalid_blank_en(self):
        form_data = self.start_data_valid.copy()
        del form_data['uac']

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_invalid_blank_cy(self):
        form_data = self.start_data_valid.copy()
        del form_data['uac']

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(BAD_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_index_invalid_blank_ni(self):
        form_data = self.start_data_valid.copy()
        del form_data['uac']

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_url_en(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_url_cy(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(BAD_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_url_ni(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_random_en(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_random_cy(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(BAD_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_index_invalid_text_random_ni(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_uac_active_missing_en(self):
        uac_json = self.uac_json_en.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

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
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

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
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Your unique access code has expired', contents)

    @unittest_run_loop
    async def test_post_index_uac_inactive_en(self):
        uac_json = self.uac_json_en.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

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
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

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
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Your unique access code has expired', contents)

    @unittest_run_loop
    async def test_post_index_uac_case_status_not_found_en(self):
        uac_json = self.uac_json_en.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'service failed to build eq payload')

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
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_uac_case_status_not_found_ni(self):
        uac_json = self.uac_json_ni.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_connection_error_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_connection_error_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_connection_error_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_500_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_500_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_503_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_503_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=503)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_404_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'attempt to use an invalid access code',
                                client_ip=None)

        self.assertEqual(response.status, 401)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(INVALID_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_404_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'attempt to use an invalid access code',
                                client_ip=None)

        self.assertEqual(response.status, 401)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(INVALID_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_404_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'attempt to use an invalid access code',
                                client_ip=None)

        self.assertEqual(response.status, 401)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(INVALID_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_403_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_403_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le",
                          contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_403_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_401_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le",
                          contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_401_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_400_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_index_get_uac_400_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le",
                          contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_index_get_uac_400_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_ni,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_address_confirmation_survey_launched_connection_error_en(
            self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)
            mocked.post(self.rhsvc_url_surveylaunched,
                        exception=ClientConnectionError('Failed'))

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url_surveylaunched)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Sorry, something went wrong', contents)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_address_confirmation_survey_launched_connection_error_cy(
            self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.post(self.rhsvc_url_surveylaunched,
                        exception=ClientConnectionError('Failed'))

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url_surveylaunched)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le", contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_401_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)
            mocked.post(self.rhsvc_url_surveylaunched, status=401)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.post(self.rhsvc_url_surveylaunched, status=401)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le",
                          contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_404_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)
            mocked.post(self.rhsvc_url_surveylaunched, status=404)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_404_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.post(self.rhsvc_url_surveylaunched, status=404)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                'POST',
                self.post_start_confirm_address_cy,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le",
                          contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_500_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)
            mocked.post(self.rhsvc_url_surveylaunched, status=500)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=500)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)
            mocked.post(self.rhsvc_url_surveylaunched, status=500)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=500)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le",
                          contents)
            self.assertIn(self.ons_logo_cy, contents)

    def test_uac_hash(self):
        # Given some post data
        post_data = {'uac': 'w4nw wpph jjpt p7fn', 'action[save_continue]': ''}

        # When join_uac is called
        result = Start.uac_hash(post_data['uac'])

        # Then a single string built from the uac values is returned
        self.assertEqual(result, '54598f02da027026a584fd0bc7176de55a3e6472f4b3c74f68d0ae7be206e17c')

    def test_join_uac_missing(self):
        # Given some missing post data
        post_data = {'uac': '', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            Start.uac_hash(post_data['uac'])
        # Then a TypeError is raised

    def test_join_uac_some_missing(self):
        # Given some missing post data
        post_data = {'uac': '123456781234', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            Start.uac_hash(post_data['uac'])
        # Then a TypeError is raised

    def test_validate_case(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'OK'}

        # When validate_case is called
        Start.validate_case(case_json)

        # Nothing happens

    def test_validate_case_inactive(self):
        # Given a dict with an active key and value
        case_json = {'active': False, 'caseStatus': 'OK'}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            Start.validate_case(case_json)

        # Then an InactiveCaseError is raised

    def test_validate_caseStatus_notfound(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'NOT_FOUND'}

        # When validate_case is called
        with self.assertRaises(InvalidEqPayLoad):
            Start.validate_case(case_json)

        # Then an InvalidEqPayload is raised

    def test_validate_case_empty(self):
        # Given an empty dict
        case_json = {}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            Start.validate_case(case_json)

        # Then an InactiveCaseError is raised

    @unittest_run_loop
    async def test_get_address_confirmation_direct_access_en(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request(
                'GET', self.get_start_confirm_address_en, allow_redirects=False)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)

    @unittest_run_loop
    async def test_get_address_confirmation_direct_access_cy(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request(
                'GET', self.get_start_confirm_address_cy, allow_redirects=False)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Rhowch y cod 16 nod sydd', contents)

    @unittest_run_loop
    async def test_get_address_confirmation_direct_access_ni(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request(
                'GET', self.get_start_confirm_address_ni, allow_redirects=False)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)

    @unittest_run_loop
    async def test_post_address_confirmation_direct_access_en(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)

    @unittest_run_loop
    async def test_post_address_confirmation_direct_access_cy(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request(
                'POST',
                self.post_start_confirm_address_cy,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Rhowch y cod 16 nod sydd', contents)

    @unittest_run_loop
    async def test_post_address_confirmation_direct_access_ni(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request(
                'POST',
                self.post_start_confirm_address_ni,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)

    @unittest_run_loop
    async def test_get_address_edit_direct_access_en(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request('GET',
                                                 self.get_start_modify_address_en,
                                                 allow_redirects=False)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)

    @unittest_run_loop
    async def test_get_address_edit_direct_access_cy(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request('GET',
                                                 self.get_start_modify_address_cy,
                                                 allow_redirects=False)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Rhowch y cod 16 nod sydd', contents)

    @unittest_run_loop
    async def test_get_address_edit_direct_access_ni(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request('GET',
                                                 self.get_start_modify_address_ni,
                                                 allow_redirects=False)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)

    @unittest_run_loop
    async def test_post_address_edit_direct_access_en(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request('GET',
                                                 self.post_start_modify_address_en,
                                                 allow_redirects=False)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)

    @unittest_run_loop
    async def test_post_address_edit_direct_access_cy(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request('GET',
                                                 self.post_start_modify_address_cy,
                                                 allow_redirects=False)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Rhowch y cod 16 nod sydd', contents)

    @unittest_run_loop
    async def test_post_address_edit_direct_access_ni(self):
        with self.assertLogs('respondent-home', 'WARN') as cm:
            response = await self.client.request('GET',
                                                 self.post_start_modify_address_ni,
                                                 allow_redirects=False)
        self.assertLogEvent(cm, 'permission denied')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)

    @unittest_run_loop
    async def test_post_start_address_confirm_empty_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 allow_redirects=False,
                                                 data=self.start_confirm_address_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Is this address correct?', contents)
            self.assertIn('Please check and confirm address', contents)

    @unittest_run_loop
    async def test_post_start_address_confirm_empty_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)

            await self.client.request('GET', self.get_start_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")

            await self.client.request('POST', self.post_start_cy, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_cy,
                                                 allow_redirects=False,
                                                 data=self.start_confirm_address_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn("Ydy\\\'r cyfeiriad hwn yn gywir?", contents)
            self.assertIn("Edrychwch eto ar y cyfeiriad a\\\'i gadarnhau.", contents)

    @unittest_run_loop
    async def test_post_start_address_confirm_empty_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_ni,
                                                 allow_redirects=False,
                                                 data=self.start_confirm_address_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Is this address correct?', contents)
            self.assertIn('Please check and confirm address', contents)

    @unittest_run_loop
    async def test_post_start_address_confirm_invalid_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 allow_redirects=False,
                                                 data=self.start_confirm_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Is this address correct?', contents)
            self.assertIn('Please check and confirm address', contents)

    @unittest_run_loop
    async def test_post_start_address_confirm_invalid_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)

            await self.client.request('GET', self.get_start_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")

            await self.client.request('POST', self.post_start_cy, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_cy,
                                                 allow_redirects=False,
                                                 data=self.start_confirm_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn("Ydy\\\'r cyfeiriad hwn yn gywir?", contents)
            self.assertIn("Edrychwch eto ar y cyfeiriad a\\\'i gadarnhau.", contents)

    @unittest_run_loop
    async def test_post_start_address_confirm_invalid_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_ni,
                                                 allow_redirects=False,
                                                 data=self.start_confirm_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Is this address correct?', contents)
            self.assertIn('Please check and confirm address', contents)

    @unittest_run_loop
    async def test_get_start_modify_address_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_confirm_address_en,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")

            response = await self.client.request('GET', self.get_start_modify_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/modify-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Change your address', contents)

    @unittest_run_loop
    async def test_get_start_modify_address_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)

            await self.client.request('GET', self.get_start_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")

            await self.client.request('POST', self.post_start_cy, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")

            await self.client.request('POST', self.post_start_confirm_address_cy,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start/confirm-address'")

            response = await self.client.request('GET', self.get_start_modify_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/modify-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Newid eich cyfeiriad', contents)

    @unittest_run_loop
    async def test_get_start_modify_address_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            response = await self.client.request('GET', self.get_start_modify_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/modify-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Change your address', contents)

    @unittest_run_loop
    async def test_post_start_modify_address_invalid_data_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_confirm_address_en,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")

            response = await self.client.request('POST', self.post_start_modify_address_en,
                                                 allow_redirects=False,
                                                 data=self.start_modify_address_data_incomplete)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/modify-address'")

            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "address-line-1 has no value")

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Change your address', contents)
            self.assertIn('Enter address to continue', contents)

    @unittest_run_loop
    async def test_post_start_modify_address_invalid_data_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)

            await self.client.request('GET', self.get_start_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")

            await self.client.request('POST', self.post_start_cy, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")

            await self.client.request('POST', self.post_start_confirm_address_cy,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start/confirm-address'")

            response = await self.client.request('POST', self.post_start_modify_address_cy,
                                                 allow_redirects=False,
                                                 data=self.start_modify_address_data_incomplete)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start/modify-address'")

            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "address-line-1 has no value")

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Newid eich cyfeiriad', contents)
            self.assertIn('Nodwch gyfeiriad i barhau', contents)

    @unittest_run_loop
    async def test_post_start_modify_address_invalid_data_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            response = await self.client.request('POST', self.post_start_modify_address_ni,
                                                 allow_redirects=False,
                                                 data=self.start_modify_address_data_incomplete)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/modify-address'")

            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "address-line-1 has no value")

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Change your address', contents)
            self.assertIn('Enter address to continue', contents)

    @unittest_run_loop
    async def test_get_start_modify_address_put_error_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.put(self.rhsvc_put_modify_address, payload={}, status=400)

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            response = await self.client.request('POST', self.post_start_modify_address_ni,
                                                 allow_redirects=False,
                                                 data=self.start_modify_address_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/modify-address'")

            self.assertLogEvent(cm, "error raising address modification call")

            self.assertEqual(response.status, 500)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Sorry, something went wrong', contents)

    @unittest_run_loop
    async def test_get_start_ni_language_options(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.put(self.rhsvc_put_modify_address, payload={})

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            await self.client.request('POST', self.post_start_modify_address_ni,
                                      allow_redirects=False,
                                      data=self.start_modify_address_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/modify-address'")

            response = await self.client.request('GET', self.get_start_language_options_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/language-options'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Would you like to complete the census in English?', contents)

    @unittest_run_loop
    async def test_post_start_ni_language_options_invalid(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.put(self.rhsvc_put_modify_address, payload={})

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            response = await self.client.request('POST', self.post_start_language_options_ni,
                                                 allow_redirects=False,
                                                 data=self.start_ni_language_option_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Would you like to complete the census in English?', contents)
            self.assertIn('Select a language option', contents)

    @unittest_run_loop
    async def test_post_start_ni_language_options_empty(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.put(self.rhsvc_put_modify_address, payload={})

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            response = await self.client.request('POST', self.post_start_language_options_ni,
                                                 allow_redirects=False,
                                                 data=self.start_ni_language_option_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Would you like to complete the census in English?', contents)
            self.assertIn('Select a language option', contents)

    @unittest_run_loop
    async def test_get_ni_select_language(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.put(self.rhsvc_put_modify_address, payload={})

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            response = await self.client.request('POST', self.post_start_language_options_ni,
                                                 allow_redirects=False,
                                                 data=self.start_ni_language_option_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")

            self.assertEqual(response.status, 302)
            self.assertIn('/ni/start/select-language', response.headers['Location'])

            response = await self.client.request('GET', self.get_start_select_language_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/ni-select-language'")

            contents = str(await response.content.read())
            self.assertIn('Choose your language', contents)
            self.assertIn('You can change your language back to English at any time.', contents)
            self.assertIn(self.nisra_logo, contents)

    @unittest_run_loop
    async def test_post_ni_select_language_empty(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.put(self.rhsvc_put_modify_address, payload={})

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            await self.client.request('POST', self.post_start_language_options_ni,
                                      allow_redirects=False,
                                      data=self.start_ni_language_option_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")

            response = await self.client.request('POST', self.post_start_select_language_ni,
                                                 allow_redirects=False,
                                                 data=self.start_ni_select_language_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/ni-select-language'")

            contents = str(await response.content.read())
            self.assertIn('Choose your language', contents)
            self.assertIn('Select a language option', contents)
            self.assertIn('You can change your language back to English at any time.', contents)
            self.assertIn(self.nisra_logo, contents)

    @unittest_run_loop
    async def test_post_ni_select_language_invalid(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)
            mocked.put(self.rhsvc_put_modify_address, payload={})

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start'")

            await self.client.request('POST', self.post_start_confirm_address_ni,
                                      allow_redirects=False,
                                      data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/confirm-address'")

            await self.client.request('POST', self.post_start_language_options_ni,
                                      allow_redirects=False,
                                      data=self.start_ni_language_option_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/language-options'")

            response = await self.client.request('POST', self.post_start_select_language_ni,
                                                 allow_redirects=False,
                                                 data=self.start_ni_select_language_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/start/ni-select-language'")

            contents = str(await response.content.read())
            self.assertIn('Choose your language', contents)
            self.assertIn('Select a language option', contents)
            self.assertIn('You can change your language back to English at any time.', contents)
            self.assertIn(self.nisra_logo, contents)

    @unittest_run_loop
    async def test_get_start_save_and_exit_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_save_and_exit_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/save-and-exit'")
            self.assertLogEvent(cm, "identity not previously remembered")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn('Your progress has been saved',
                          contents)
            self.assertIn(self.ons_logo_en, contents)

    @unittest_run_loop
    async def test_get_start_save_and_exit_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_save_and_exit_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/save-and-exit'")
            self.assertLogEvent(cm, "identity not previously remembered")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn('Mae eich cynnydd wedi cael ei gadw',
                          contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_get_start_save_and_exit_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_save_and_exit_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/save-and-exit'")
            self.assertLogEvent(cm, "identity not previously remembered")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn('Your progress has been saved',
                          contents)
            self.assertIn(self.nisra_logo, contents)

    @unittest_run_loop
    async def test_get_index_with_valid_adlocation_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_adlocation_valid_en)

        self.assertEqual(response.status, 200)
        self.assertLogEvent(cm, "assisted digital query parameter found")
        contents = str(await response.content.read())
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('type="submit"', contents)
        self.assertIn('type="hidden"', contents)
        self.assertIn('value="1234567890"', contents)

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid_with_adlocation)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/confirm-address',
                      response.headers['Location'])

    @unittest_run_loop
    async def test_get_index_with_invalid_adlocation_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_adlocation_invalid_en)

        self.assertEqual(response.status, 200)
        self.assertLogEvent(cm, "assisted digital query parameter not numeric - ignoring")
        contents = str(await response.content.read())
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('type="submit"', contents)
        self.assertNotIn('type="hidden"', contents)
        self.assertNotIn('value="invalid"', contents)

    @unittest_run_loop
    async def test_get_index_with_valid_adlocation_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_adlocation_valid_cy)

        self.assertEqual(response.status, 200)
        self.assertLogEvent(cm, "assisted digital query parameter found")
        contents = str(await response.content.read())
        self.assertIn('Rhowch y cod 16 nod sydd',
                      contents)
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('type="submit"', contents)
        self.assertIn('type="hidden"', contents)
        self.assertIn('value="1234567890"', contents)

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid_with_adlocation)

        self.assertEqual(response.status, 302)
        self.assertIn('/cy/start/confirm-address',
                      response.headers['Location'])

    @unittest_run_loop
    async def test_get_index_with_invalid_adlocation_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_adlocation_invalid_cy)

        self.assertEqual(response.status, 200)
        self.assertLogEvent(cm, "assisted digital query parameter not numeric - ignoring")
        contents = str(await response.content.read())
        self.assertIn('Rhowch y cod 16 nod sydd',
                      contents)
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('type="submit"', contents)
        self.assertNotIn('type="hidden"', contents)
        self.assertNotIn('value="invalid"', contents)

    @unittest_run_loop
    async def test_get_index_with_valid_adlocation_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_adlocation_valid_ni)

        self.assertEqual(response.status, 200)
        self.assertLogEvent(cm, "assisted digital query parameter found")
        contents = str(await response.content.read())
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('type="submit"', contents)
        self.assertIn('type="hidden"', contents)
        self.assertIn('value="1234567890"', contents)

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid_with_adlocation)

        self.assertEqual(response.status, 302)
        self.assertIn('/ni/start/confirm-address',
                      response.headers['Location'])

    @unittest_run_loop
    async def test_get_index_with_invalid_adlocation_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_start_adlocation_invalid_ni)

        self.assertEqual(response.status, 200)
        self.assertLogEvent(cm, "assisted digital query parameter not numeric - ignoring")
        contents = str(await response.content.read())
        self.assertIn('Enter the 16 character code printed on the letter',
                      contents)
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('type="submit"', contents)
        self.assertNotIn('type="hidden"', contents)
        self.assertNotIn('value="invalid"', contents)

    @unittest_run_loop
    async def test_get_change_of_region(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('GET', self.get_start_region_change_ni, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start/region-change'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Change of region', contents)

    @unittest_run_loop
    async def test_get_change_of_region_en_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            self.assertIn('/ni/start/region-change/', response.headers['Location'])

    @unittest_run_loop
    async def test_get_change_of_region_cy_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_ni)

            await self.client.request('GET', self.get_start_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/ni/start/region-change/',
                      response.headers['Location'])

    @unittest_run_loop
    async def test_get_change_of_region_cy_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)]) \
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)

            await self.client.request('GET', self.get_start_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/region-change/',
                      response.headers['Location'])

    @unittest_run_loop
    async def test_get_change_of_region_ni_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)]) \
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_cy)

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/region-change/',
                      response.headers['Location'])

    @unittest_run_loop
    async def test_get_change_of_region_ni_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)]) \
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_en)

            await self.client.request('GET', self.get_start_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/start'")

            response = await self.client.request('POST',
                                                 self.post_start_ni,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/region-change/',
                      response.headers['Location'])

    @skip_encrypt
    @unittest_run_loop
    async def test_unlinked_uac_happy_path_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.post_unlinked_uac') as mocked_post_unlinked_uac, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.unlinked_uac_json_en)
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_post_unlinked_uac.return_value = self.rhsvc_post_linked_uac_en

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-ENG'
            eq_payload['language_code'] = 'en'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/en'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = '10023122451'
            eq_payload['display_address'] = '1 Gate Reach, Exeter'

            response = await self.client.request('GET', self.get_start_en)
            self.assertEqual(200, response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=True,
                                                 data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")
            self.assertLogEvent(cm, "unlinked case")

            self.assertEqual(200, response.status)
            contents = str(await response.content.read())
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/unlinked/enter-address'")
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_start_unlinked_enter_address_title_en, contents)
            self.assertIn(self.content_start_unlinked_enter_address_secondary_en, contents)
            self.assertIn(self.content_start_unlinked_enter_address_question_title_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_start_unlinked_enter_address_en,
                    data=self.request_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/start/unlinked/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/unlinked/select-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_start_unlinked_select_address_title_en, str(resp_content))
            self.assertIn(self.content_start_unlinked_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_start_unlinked_select_address_en,
                    data=self.request_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/unlinked/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/unlinked/confirm-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_start_unlinked_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_start_unlinked_confirm_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_start_unlinked_confirm_address_en,
                    data=self.request_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/unlinked/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/unlinked/address-has-been-linked'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_start_unlinked_address_has_been_linked_title_en, str(resp_content))
            self.assertIn(self.content_start_unlinked_address_has_been_linked_secondary_en, str(resp_content))

            response = await self.client.request(
                'POST',
                self.post_start_unlinked_address_is_linked_en,
                allow_redirects=False,
                data=self.start_address_linked)

            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(response.status, 302)
        redirected_url = response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)
