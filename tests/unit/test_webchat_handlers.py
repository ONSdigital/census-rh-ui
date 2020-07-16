import datetime

from unittest import mock

from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app import (WEBCHAT_MISSING_QUERY_MSG,
                 WEBCHAT_MISSING_COUNTRY_MSG,
                 WEBCHAT_MISSING_NAME_MSG,
                 WEBCHAT_MISSING_QUERY_MSG_CY,
                 WEBCHAT_MISSING_COUNTRY_MSG_CY,
                 WEBCHAT_MISSING_NAME_MSG_CY)
from app.webchat_handlers import WebChat

from . import RHTestCase


class TestWebChatHandlers(RHTestCase):
    def test_check_open_weekday_open_census_weekend(self):
        mocked_now = datetime.datetime(2019, 10, 12, 9, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertTrue(WebChat.check_open())

    def test_check_open_weekday_closed_census_weekend(self):
        mocked_now = datetime.datetime(2019, 10, 13, 6, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    def test_check_open_weekday_open(self):
        mocked_now = datetime.datetime(2019, 6, 17, 9, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertTrue(WebChat.check_open())

    def test_check_open_weekday_closed_am(self):
        mocked_now = datetime.datetime(2019, 6, 16, 4, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    def test_check_open_weekday_closed_pm(self):
        mocked_now = datetime.datetime(2019, 6, 16, 21, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    def test_check_open_saturday_open(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertTrue(WebChat.check_open())

    def test_check_open_saturday_closed(self):
        mocked_now = datetime.datetime(2019, 6, 15, 16, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    def test_check_open_sunday_closed(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now
            self.assertFalse(WebChat.check_open())

    @unittest_run_loop
    async def test_get_webchat_open_en(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            response = await self.client.request('GET', self.get_webchat_en)
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Enter your name', contents)
            self.assertEqual(contents.count('radio__input'), 10)
            self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_webchat_open_cy(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            response = await self.client.request('GET', self.get_webchat_cy)
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Nodwch eich enw', contents)
            self.assertEqual(contents.count('radio__input'), 10)
            self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_webchat_open_ni(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            response = await self.client.request('GET', self.get_webchat_ni)
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Enter your name', contents)
            self.assertEqual(contents.count('radio__input'), 10)
            self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_en(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request('GET',
                                                     self.get_webchat_en)

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_cy(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request('GET',
                                                     self.get_webchat_cy)

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('Gwyliau Banc', contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_ni(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request('GET',
                                                     self.get_webchat_ni)

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_query_en(self):
        form_data = self.webchat_form_data.copy()
        del form_data['query']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_webchat_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'form submission error')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_QUERY_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_query_cy(self):
        form_data = self.webchat_form_data.copy()
        del form_data['query']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_webchat_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'form submission error')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_QUERY_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_query_ni(self):
        form_data = self.webchat_form_data.copy()
        del form_data['query']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_webchat_ni,
                                                 data=form_data)
        self.assertLogEvent(cm, 'form submission error')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_QUERY_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_country_en(self):
        form_data = self.webchat_form_data.copy()
        del form_data['country']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_webchat_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'form submission error')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_COUNTRY_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_country_cy(self):
        form_data = self.webchat_form_data.copy()
        del form_data['country']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_webchat_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'form submission error')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_COUNTRY_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_country_ni(self):
        form_data = self.webchat_form_data.copy()
        del form_data['country']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_webchat_ni,
                                                 data=form_data)
        self.assertLogEvent(cm, 'form submission error')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_COUNTRY_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_name_en(self):
        form_data = self.webchat_form_data.copy()
        del form_data['screen_name']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_webchat_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'form submission error')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_NAME_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_name_cy(self):
        form_data = self.webchat_form_data.copy()
        del form_data['screen_name']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_webchat_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'form submission error')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_NAME_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_name_ni(self):
        form_data = self.webchat_form_data.copy()
        del form_data['screen_name']

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_webchat_ni,
                                                 data=form_data)
        self.assertLogEvent(cm, 'form submission error')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertMessagePanel(WEBCHAT_MISSING_NAME_MSG, contents)

    @unittest_run_loop
    async def test_post_webchat_open_en(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_en,
                                                     allow_redirects=False,
                                                     data=self.webchat_form_data)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received POST on endpoint 'en/web-chat'")
            self.assertLogEvent(cm, "date/time check")

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('iframe', contents)
            self.assertIn('Web Chat', contents)

    @unittest_run_loop
    async def test_post_webchat_open_cy(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_cy,
                                                     allow_redirects=False,
                                                     data=self.webchat_form_data)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/web-chat'")
            self.assertLogEvent(cm, "date/time check")

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('iframe', contents)
            self.assertIn('Gwe-sgwrs', contents)

    @unittest_run_loop
    async def test_post_webchat_open_ni(self):
        mocked_now = datetime.datetime(2019, 6, 15, 9, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_ni,
                                                     allow_redirects=False,
                                                     data=self.webchat_form_data)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/web-chat'")
            self.assertLogEvent(cm, "date/time check")

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn('iframe', contents)
            self.assertIn('Web Chat', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_en(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request(
                    'POST',
                    self.post_webchat_en,
                    allow_redirects=False,
                    data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn('Bank Holidays', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_cy(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request(
                    'POST',
                    self.post_webchat_cy,
                    allow_redirects=False,
                    data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('Gwyliau Banc', contents)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_ni(self):
        mocked_now = datetime.datetime(2019, 6, 16, 16, 30, 00, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now') as mocked_get_now:
            mocked_get_now.return_value = mocked_now

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request(
                    'POST',
                    self.post_webchat_ni,
                    allow_redirects=False,
                    data=self.webchat_form_data)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn('Bank Holidays', contents)
