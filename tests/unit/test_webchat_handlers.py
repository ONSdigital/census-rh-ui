import datetime

from unittest import mock

from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app.webchat_handlers import WebChat

from . import RHTestCase


class TestWebChatHandlers(RHTestCase):

    def should_be_open(self, year, month=None, day=None, hour=0, minute=0, second=0):
        mocked_now_utc = datetime.datetime(year, month, day, hour, minute, second, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = mocked_now_utc
            self.assertTrue(WebChat.check_open())

    def should_be_closed(self, year, month=None, day=None, hour=0, minute=0, second=0):
        mocked_now_utc = datetime.datetime(year, month, day, hour, minute, second, 0)
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = mocked_now_utc
            self.assertFalse(WebChat.check_open())

    def test_check_open_census_saturday_open(self):
        self.should_be_open(2021, 3, 20, 16, 1)     # just after opening
        self.should_be_open(2021, 3, 20, 17, 30)    # mid evening
        self.should_be_open(2021, 3, 20, 19, 59)    # before closing

    def test_check_open_census_saturday_closed(self):
        self.should_be_closed(2021, 3, 20, 15, 59)  # just before opening
        self.should_be_closed(2021, 3, 20, 20, 1)   # just after closing

    def test_check_open_census_sunday_open(self):
        self.should_be_open(2021, 3, 21, 16, 1)     # just after opening
        self.should_be_open(2021, 3, 21, 17, 30)    # mid evening
        self.should_be_open(2021, 3, 21, 19, 59)    # before closing

    def test_check_open_census_sunday_closed(self):
        self.should_be_closed(2021, 3, 21, 15, 59)  # just before opening
        self.should_be_closed(2021, 3, 21, 20, 1)   # just after closing

    def test_check_open_weekday_open(self):
        self.should_be_open(2019, 6, 17, 11, 30)    # 2019 BST summer
        self.should_be_open(2020, 8, 12, 7, 1)     # 2020 BST summer just after opening
        self.should_be_open(2020, 8, 12, 18, 59)    # 2020 BST summer just before closing
        self.should_be_open(2020, 11, 10, 8, 1)    # 2020 GMT winter just after opening
        self.should_be_open(2020, 11, 10, 19, 59)   # 2020 GMT winter just before closing
        self.should_be_open(2021, 3, 26, 8, 1)     # 2021 GMT spring just after opening
        self.should_be_open(2021, 3, 26, 17, 30)    # 2021 GMT spring mid evening
        self.should_be_open(2021, 3, 26, 19, 59)    # 2021 GMT spring just before closing
        self.should_be_open(2021, 3, 29, 7, 1)     # 2021 BST summer just after opening
        self.should_be_open(2021, 3, 29, 18, 30)    # 2021 BST summer mid evening
        self.should_be_open(2021, 3, 29, 18, 59)    # 2021 BST summer just before closing

    def test_check_open_weekday_closed(self):
        self.should_be_closed(2019, 6, 16, 10, 30)  # 2019 BST summer before opening
        self.should_be_closed(2019, 6, 16, 19, 30)  # 2019 BST summer after closing
        self.should_be_closed(2020, 8, 12, 6, 59)  # 2020 BST summer just before opening
        self.should_be_closed(2020, 8, 12, 19, 1)   # 2020 BST summer just after closing
        self.should_be_closed(2020, 11, 10, 7, 59) # 2020 GMT winter just before opening
        self.should_be_closed(2020, 11, 10, 20, 1)  # 2020 GMT winter just after closing
        self.should_be_closed(2021, 3, 26, 7, 59)  # 2021 GMT spring just before opening
        self.should_be_closed(2021, 3, 26, 20, 1)   # 2021 GMT spring just after closing
        self.should_be_closed(2021, 3, 29, 6, 59)  # 2021 BST summer just before opening
        self.should_be_closed(2021, 3, 29, 19, 1)   # 2021 BST summer just after closing

    def test_check_open_saturday_open(self):
        self.should_be_open(2019, 6, 15, 9, 30)     # 2019 BST summer
        self.should_be_open(2020, 8, 15, 7, 1)      # 2020 BST summer just after opening
        self.should_be_open(2020, 8, 15, 11, 59)    # 2020 BST summer just before closing
        self.should_be_open(2020, 11, 14, 8, 1)     # 2020 GMT winter just after opening
        self.should_be_open(2020, 11, 14, 12, 59)   # 2020 GMT winter just before closing
        self.should_be_open(2021, 3, 27, 8, 1)      # 2021 GMT spring just after opening
        self.should_be_open(2021, 3, 27, 10, 30)    # 2021 GMT spring mid morning
        self.should_be_open(2021, 3, 27, 12, 59)    # 2021 GMT spring just before closing
        self.should_be_open(2021, 4, 3, 7, 1)       # 2021 BST summer just after opening
        self.should_be_open(2021, 4, 3, 9, 30)      # 2021 BST summer mid morning
        self.should_be_open(2021, 4, 3, 11, 59)     # 2021 BST summer just before closing

    def test_check_open_saturday_closed(self):
        self.should_be_closed(2019, 6, 15, 16, 30)  # 2019 BST summer
        self.should_be_closed(2020, 8, 15, 6, 59)   # 2020 BST summer just before opening
        self.should_be_closed(2020, 8, 15, 12, 1)   # 2020 BST summer just after closing
        self.should_be_closed(2020, 11, 14, 7, 59)  # 2020 GMT winter just before opening
        self.should_be_closed(2020, 11, 14, 13, 1)  # 2020 GMT winter just after closing
        self.should_be_closed(2021, 3, 27, 7, 59)   # 2021 GMT spring just before opening
        self.should_be_closed(2021, 3, 27, 13, 1)   # 2021 GMT spring just after closing
        self.should_be_closed(2021, 4, 3, 6, 59)    # 2021 BST summer just before opening
        self.should_be_closed(2021, 4, 3, 12, 1)    # 2021 BST summer just after closing

    def test_check_open_sunday_closed(self):
        self.should_be_closed(2019, 6, 16, 16, 30)      # 2019 BST summer
        self.should_be_closed(2020, 8, 16, 11, 30)      # 2020 BST summer
        self.should_be_closed(2020, 11, 15, 11, 30)     # 2020 GMT winter
        self.should_be_closed(2021, 3, 28, 11, 30)      # 2021 GMT spring
        self.should_be_closed(2021, 4, 4, 11, 30)       # 2021 BST summer

    def test_check_open_bank_holidays_closed(self):
        self.should_be_closed(2021, 4, 2, 10, 30)       # 2021 Good Friday
        self.should_be_closed(2021, 4, 5, 10, 30)       # 2021 Easter Monday
        self.should_be_closed(2021, 5, 3, 10, 30)       # 2021 Mayday bank holiday
        self.should_be_closed(2021, 5, 31, 10, 30)      # 2021 Spring bank holiday

    async def should_respond_open_to_get(self, path, logo, name_prompt, mocked_now_utc):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = mocked_now_utc

            response = await self.client.request('GET', path)
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(logo, contents)
            self.assertIn(name_prompt, contents)
            self.assertEqual(contents.count('radio__input'), 9)
            self.assertIn('type="submit"', contents)

    @unittest_run_loop
    async def test_get_webchat_open_en(self):
        mocked_now_utc = datetime.datetime(2019, 6, 15, 9, 30)
        await self.should_respond_open_to_get(self.get_webchat_en, self.ons_logo_en, 'Enter your name', mocked_now_utc)

    @unittest_run_loop
    async def test_get_webchat_open_en_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 15, 1)
        await self.should_respond_open_to_get(self.get_webchat_en, self.ons_logo_en, 'Enter your name', mocked_now_utc)

    @unittest_run_loop
    async def test_get_webchat_open_cy(self):
        mocked_now_utc = datetime.datetime(2019, 6, 15, 9, 30)
        await self.should_respond_open_to_get(self.get_webchat_cy, self.ons_logo_cy, 'Nodwch eich enw', mocked_now_utc)

    @unittest_run_loop
    async def test_get_webchat_open_cy_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 15, 1)
        await self.should_respond_open_to_get(self.get_webchat_cy, self.ons_logo_cy, 'Nodwch eich enw', mocked_now_utc)

    @unittest_run_loop
    async def test_get_webchat_open_ni(self):
        mocked_now_utc = datetime.datetime(2019, 6, 15, 9, 30)
        await self.should_respond_open_to_get(self.get_webchat_ni, self.nisra_logo, 'Enter your name', mocked_now_utc)

    @unittest_run_loop
    async def test_get_webchat_open_ni_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 15, 1)
        await self.should_respond_open_to_get(self.get_webchat_ni, self.nisra_logo, 'Enter your name', mocked_now_utc)

    async def should_respond_not_open_to_get(self, path, logo, reason, mocked_now_utc):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = mocked_now_utc

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request('GET', path)

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(logo, contents)
            self.assertIn(reason, contents)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_en(self):
        mocked_now_utc = datetime.datetime(2019, 6, 16, 16, 30)
        await self.should_respond_not_open_to_get(self.get_webchat_en, self.ons_logo_en,
                                                  'Web chat is now closed',
                                                  mocked_now_utc)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_en_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 19, 1)
        await self.should_respond_not_open_to_get(self.get_webchat_en, self.ons_logo_en,
                                                  'Web chat is now closed',
                                                  mocked_now_utc)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_cy(self):
        mocked_now_utc = datetime.datetime(2019, 6, 16, 16, 30)
        await self.should_respond_not_open_to_get(self.get_webchat_cy, self.ons_logo_cy,
                                                  "Mae gwe-sgwrs nawr ar gau",
                                                  mocked_now_utc)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_cy_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 19, 1)
        await self.should_respond_not_open_to_get(self.get_webchat_cy, self.ons_logo_cy,
                                                  "Mae gwe-sgwrs nawr ar gau",
                                                  mocked_now_utc)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_ni(self):
        mocked_now_utc = datetime.datetime(2019, 6, 16, 16, 30)
        await self.should_respond_not_open_to_get(self.get_webchat_ni, self.nisra_logo,
                                                  'Web chat is now closed',
                                                  mocked_now_utc)

    @unittest_run_loop
    async def test_get_webchat_not_open_200_ni_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 19, 1)
        await self.should_respond_not_open_to_get(self.get_webchat_ni, self.nisra_logo,
                                                  "Web chat is now closed",
                                                  mocked_now_utc)

    @unittest_run_loop
    async def test_post_webchat_incomplete_query_en(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_en.copy()
            del form_data['query']

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_en,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_webchat_form_page_title_error_en, contents)
            self.assertIn(self.content_webchat_form_title_en, contents)
            self.assertIn(self.content_common_error_panel_answer_en, contents)
            self.assertIn(self.content_common_error_select_an_option_en, contents)
            self.assertIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertIn(self.content_webchat_error_selected_country_en, contents)
            self.assertNotIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_query_cy(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_cy.copy()
            del form_data['query']

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_cy,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_webchat_form_page_title_error_cy, contents)
            self.assertIn(self.content_webchat_form_title_cy, contents)
            self.assertIn(self.content_common_error_panel_answer_cy, contents)
            self.assertIn(self.content_common_error_select_an_option_cy, contents)
            self.assertIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertIn(self.content_webchat_error_selected_country_cy, contents)
            self.assertNotIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_query_ni(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_ni.copy()
            del form_data['query']

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_ni,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_webchat_form_page_title_error_en, contents)
            self.assertIn(self.content_webchat_form_title_en, contents)
            self.assertIn(self.content_common_error_panel_answer_en, contents)
            self.assertIn(self.content_common_error_select_an_option_en, contents)
            self.assertIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertIn(self.content_webchat_error_selected_country_ni, contents)
            self.assertNotIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_country_en(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_en.copy()
            del form_data['country']

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_en,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_webchat_form_page_title_error_en, contents)
            self.assertIn(self.content_webchat_form_title_en, contents)
            self.assertIn(self.content_common_error_panel_answer_en, contents)
            self.assertIn(self.content_common_error_select_an_option_en, contents)
            self.assertIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertNotIn(self.content_webchat_error_selected_country_en, contents)
            self.assertIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_country_cy(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_cy.copy()
            del form_data['country']

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_cy,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_webchat_form_page_title_error_cy, contents)
            self.assertIn(self.content_webchat_form_title_cy, contents)
            self.assertIn(self.content_common_error_panel_answer_cy, contents)
            self.assertIn(self.content_common_error_select_an_option_cy, contents)
            self.assertIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertNotIn(self.content_webchat_error_selected_country_cy, contents)
            self.assertIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_country_ni(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_ni.copy()
            del form_data['country']

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_ni,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_webchat_form_page_title_error_en, contents)
            self.assertIn(self.content_webchat_form_title_en, contents)
            self.assertIn(self.content_common_error_panel_answer_en, contents)
            self.assertIn(self.content_common_error_select_an_option_en, contents)
            self.assertIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertNotIn(self.content_webchat_error_selected_country_ni, contents)
            self.assertIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_name_en(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_en.copy()
            del form_data['screen_name']

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_en,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_webchat_form_page_title_error_en, contents)
            self.assertIn(self.content_webchat_form_title_en, contents)
            self.assertIn(self.content_common_error_panel_answer_en, contents)
            self.assertIn(self.content_webchat_error_enter_your_name_en, contents)
            self.assertNotIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertIn(self.content_webchat_error_selected_country_en, contents)
            self.assertIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_name_cy(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_cy.copy()
            del form_data['screen_name']

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_cy,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_webchat_form_page_title_error_cy, contents)
            self.assertIn(self.content_webchat_form_title_cy, contents)
            self.assertIn(self.content_common_error_panel_answer_cy, contents)
            self.assertIn(self.content_webchat_error_enter_your_name_cy, contents)
            self.assertNotIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertIn(self.content_webchat_error_selected_country_cy, contents)
            self.assertIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_incomplete_name_ni(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_ni.copy()
            del form_data['screen_name']

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_ni,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_webchat_form_page_title_error_en, contents)
            self.assertIn(self.content_webchat_form_title_en, contents)
            self.assertIn(self.content_common_error_panel_answer_en, contents)
            self.assertIn(self.content_webchat_error_enter_your_name_en, contents)
            self.assertNotIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertIn(self.content_webchat_error_selected_country_ni, contents)
            self.assertIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_name_only_space_en(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_en.copy()
            form_data['screen_name'] = ' '

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_en,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_webchat_form_page_title_error_en, contents)
            self.assertIn(self.content_webchat_form_title_en, contents)
            self.assertIn(self.content_common_error_panel_answer_en, contents)
            self.assertIn(self.content_webchat_error_enter_your_name_en, contents)
            self.assertNotIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertIn(self.content_webchat_error_selected_country_en, contents)
            self.assertIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_name_only_space_cy(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_cy.copy()
            form_data['screen_name'] = ' '

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_cy,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_webchat_form_page_title_error_cy, contents)
            self.assertIn(self.content_webchat_form_title_cy, contents)
            self.assertIn(self.content_common_error_panel_answer_cy, contents)
            self.assertIn(self.content_webchat_error_enter_your_name_cy, contents)
            self.assertNotIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertIn(self.content_webchat_error_selected_country_cy, contents)
            self.assertIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_name_only_space_ni(self):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = datetime.datetime(2019, 6, 15, 9, 30)
            form_data = self.webchat_form_data_ni.copy()
            form_data['screen_name'] = ' '

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_webchat_ni,
                                                     data=form_data)
            self.assertLogEvent(cm, 'form submission error')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_webchat_form_page_title_error_en, contents)
            self.assertIn(self.content_webchat_form_title_en, contents)
            self.assertIn(self.content_common_error_panel_answer_en, contents)
            self.assertIn(self.content_webchat_error_enter_your_name_en, contents)
            self.assertNotIn(self.content_webchat_error_selected_screen_name, contents)
            self.assertIn(self.content_webchat_error_selected_country_ni, contents)
            self.assertIn(self.content_webchat_error_selected_query, contents)

    @unittest_run_loop
    async def test_post_webchat_open_en(self):
        mocked_now_utc = datetime.datetime(2019, 6, 15, 9, 30)
        await self.should_be_open_to_post(self.post_webchat_en, 'Web Chat', self.ons_logo_en, mocked_now_utc,
                                          'en/web-chat', self.webchat_form_data_en)

    @unittest_run_loop
    async def test_post_webchat_open_en_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 7, 1)
        await self.should_be_open_to_post(self.post_webchat_en, 'Web Chat', self.ons_logo_en, mocked_now_utc,
                                          'en/web-chat', self.webchat_form_data_en)

    @unittest_run_loop
    async def test_post_webchat_open_cy(self):
        mocked_now_utc = datetime.datetime(2019, 6, 15, 9, 30)
        await self.should_be_open_to_post(self.post_webchat_cy, 'Gwe-sgwrs', self.ons_logo_cy, mocked_now_utc,
                                          'cy/web-chat', self.webchat_form_data_cy)

    @unittest_run_loop
    async def test_post_webchat_open_cy_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 7, 1)
        await self.should_be_open_to_post(self.post_webchat_cy, 'Gwe-sgwrs', self.ons_logo_cy, mocked_now_utc,
                                          'cy/web-chat', self.webchat_form_data_cy)

    @unittest_run_loop
    async def test_post_webchat_open_ni(self):
        mocked_now_utc = datetime.datetime(2019, 6, 15, 9, 30)
        await self.should_be_open_to_post(self.post_webchat_ni, 'Web Chat', self.nisra_logo, mocked_now_utc,
                                          'ni/web-chat', self.webchat_form_data_ni)

    @unittest_run_loop
    async def test_post_webchat_open_ni_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 7, 1)
        await self.should_be_open_to_post(self.post_webchat_ni, 'Web Chat', self.nisra_logo, mocked_now_utc,
                                          'ni/web-chat', self.webchat_form_data_ni)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_en(self):
        mocked_now_utc = datetime.datetime(2019, 6, 16, 16, 30)
        await self.should_respond_not_open_to_post(self.post_webchat_en, 'Web chat is now closed',
                                                   self.ons_logo_en, mocked_now_utc, self.webchat_form_data_en)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_en_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 19, 1)
        await self.should_respond_not_open_to_post(self.post_webchat_en, 'Web chat is now closed',
                                                   self.ons_logo_en, mocked_now_utc, self.webchat_form_data_en)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_cy(self):
        mocked_now_utc = datetime.datetime(2019, 6, 16, 16, 30)
        await self.should_respond_not_open_to_post(self.post_webchat_cy, 'Mae gwe-sgwrs nawr ar gau',
                                                   self.ons_logo_cy, mocked_now_utc, self.webchat_form_data_cy)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_cy_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 19, 1)
        await self.should_respond_not_open_to_post(self.post_webchat_cy, 'Mae gwe-sgwrs nawr ar gau',
                                                   self.ons_logo_cy, mocked_now_utc, self.webchat_form_data_cy)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_ni(self):
        mocked_now_utc = datetime.datetime(2019, 6, 16, 16, 30)
        await self.should_respond_not_open_to_post(self.post_webchat_ni, 'Web chat is now closed',
                                                   self.nisra_logo, mocked_now_utc, self.webchat_form_data_ni)

    @unittest_run_loop
    async def test_post_webchat_not_open_200_ni_2021_bst(self):
        mocked_now_utc = datetime.datetime(2021, 3, 29, 19, 1)
        await self.should_respond_not_open_to_post(self.post_webchat_ni, 'Web chat is now closed',
                                                   self.nisra_logo, mocked_now_utc, self.webchat_form_data_ni)

    async def should_respond_not_open_to_post(self, path, reason, logo, mocked_now_utc, data):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = mocked_now_utc

            with aioresponses(passthrough=[str(self.server._root)]) as mocked:
                mocked.get(self.webchatsvc_url, status=200)

                response = await self.client.request(
                    'POST',
                    path,
                    allow_redirects=False,
                    data=data)

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(logo, contents)
        self.assertIn(reason, contents)

    async def should_be_open_to_post(self, path, reason, logo, mocked_now_utc, logged_endpoint, data):
        with mock.patch('app.webchat_handlers.WebChat.get_now_utc') as mocked_get_now_utc:
            mocked_get_now_utc.return_value = mocked_now_utc

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     path,
                                                     allow_redirects=False,
                                                     data=data)
            self.assertEqual(response.status, 200)
            self.assertLogEvent(cm, "received POST on endpoint '" + logged_endpoint + "'")
            self.assertLogEvent(cm, "date/time check")

            contents = str(await response.content.read())
            self.assertIn(logo, contents)
            self.assertIn('iframe', contents)
            self.assertIn(reason, contents)
