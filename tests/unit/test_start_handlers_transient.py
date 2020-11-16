from aiohttp.test_utils import unittest_run_loop

from . import skip_encrypt

from .helpers import TestHelpers


# noinspection PyTypeChecker
class TestStartHandlersTransient(TestHelpers):
    user_journey = 'start'
    sub_user_journey = 'transient'

    async def check_start_transient_happy_path(self, display_region, region, selection, adlocation=False):
        await self.check_get_start(display_region, adlocation)
        await self.check_post_start_transient(display_region, region, after_census_day=False, adlocation=adlocation)
        await self.check_post_start_transient_enter_town_name_valid(display_region)
        await self.check_post_start_transient_accommodation_type_selection(
            display_region, selection, region, adlocation)

    async def check_start_transient_ni_language_option_yes(self, selection, adlocation=False):
        display_region = 'ni'
        await self.check_get_start(display_region, adlocation)
        await self.check_post_start_transient(display_region, 'N', after_census_day=False, adlocation=adlocation)
        await self.check_post_start_transient_enter_town_name_valid(display_region)
        await self.check_post_start_transient_accommodation_type_selection_ni(selection)
        await self.check_post_start_transient_ni_language_options_yes(selection, adlocation)

    async def check_start_transient_ni_language_option_empty(self, selection):
        display_region = 'ni'
        await self.check_get_start(display_region)
        await self.check_post_start_transient(display_region, 'N', after_census_day=False)
        await self.check_post_start_transient_enter_town_name_valid(display_region)
        await self.check_post_start_transient_accommodation_type_selection_ni(selection)
        await self.check_post_start_transient_ni_language_options_no_selection()

    async def check_start_transient_ni_select_language_option_no_selection(self, selection):
        display_region = 'ni'
        await self.check_get_start(display_region)
        await self.check_post_start_transient(display_region, 'N', after_census_day=False)
        await self.check_post_start_transient_enter_town_name_valid(display_region)
        await self.check_post_start_transient_accommodation_type_selection_ni(selection)
        await self.check_post_start_transient_ni_language_options_no()
        await self.check_post_start_transient_ni_select_language_no_selection()

    async def check_start_transient_ni_select_language_option_language_selection(self, selection,
                                                                                 language_selection, adlocation=False):
        display_region = 'ni'
        await self.check_get_start(display_region)
        await self.check_post_start_transient(display_region, 'N', after_census_day=False, adlocation=adlocation)
        await self.check_post_start_transient_enter_town_name_valid(display_region)
        await self.check_post_start_transient_accommodation_type_selection_ni(selection)
        await self.check_post_start_transient_ni_language_options_no()
        await self.check_post_start_transient_ni_select_language(selection, language_selection, adlocation)

    async def check_start_transient_town_name_after_census_day(self, display_region, region):
        await self.check_get_start(display_region, adlocation=False)
        await self.check_post_start_transient(display_region, region, after_census_day=True)

    async def check_start_transient_town_name_before_census_day(self, display_region, region):
        await self.check_get_start(display_region, adlocation=False)
        await self.check_post_start_transient(display_region, region, after_census_day=False)

    async def check_start_transient_town_name_empty(self, display_region, region):
        await self.check_get_start(display_region, adlocation=False)
        await self.check_post_start_transient(display_region, region)
        await self.check_post_start_transient_enter_town_name_empty(display_region)

    async def check_start_transient_accommodation_type_empty(self, display_region, region):
        await self.check_get_start(display_region, adlocation=False)
        await self.check_post_start_transient(display_region, region)
        await self.check_post_start_transient_enter_town_name_valid(display_region)
        await self.check_post_start_transient_accommodation_type_no_selection(display_region)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_barge_ew_e(self):
        await self.check_start_transient_happy_path('en', 'E', 'barge', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_barge_ew_w(self):
        await self.check_start_transient_happy_path('en', 'W', 'barge', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_barge_cy(self):
        await self.check_start_transient_happy_path('cy', 'W', 'barge', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_caravan_ew_e(self):
        await self.check_start_transient_happy_path('en', 'E', 'caravan', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_caravan_ew_w(self):
        await self.check_start_transient_happy_path('en', 'W', 'caravan', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_caravan_cy(self):
        await self.check_start_transient_happy_path('cy', 'W', 'caravan', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_tent_ew_e(self):
        await self.check_start_transient_happy_path('en', 'E', 'tent', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_tent_ew_w(self):
        await self.check_start_transient_happy_path('en', 'W', 'tent', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_tent_cy(self):
        await self.check_start_transient_happy_path('cy', 'W', 'tent', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_barge_with_adlocation_ew_e(self):
        await self.check_start_transient_happy_path('en', 'E', 'barge', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_barge_with_adlocation_ew_w(self):
        await self.check_start_transient_happy_path('en', 'W', 'barge', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_barge_with_adlocation_cy(self):
        await self.check_start_transient_happy_path('cy', 'W', 'barge', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_caravan_with_adlocation_ew_e(self):
        await self.check_start_transient_happy_path('en', 'E', 'caravan', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_caravan_with_adlocation_ew_w(self):
        await self.check_start_transient_happy_path('en', 'W', 'caravan', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_caravan_with_adlocation_cy(self):
        await self.check_start_transient_happy_path('cy', 'W', 'caravan', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_tent_with_adlocation_ew_e(self):
        await self.check_start_transient_happy_path('en', 'E', 'tent', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_tent_with_adlocation_ew_w(self):
        await self.check_start_transient_happy_path('en', 'W', 'tent', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_happy_path_tent_with_adlocation_cy(self):
        await self.check_start_transient_happy_path('cy', 'W', 'tent', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_barge(self):
        await self.check_start_transient_ni_language_option_yes('barge', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_caravan(self):
        await self.check_start_transient_ni_language_option_yes('caravan', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_tent(self):
        await self.check_start_transient_ni_language_option_yes('tent', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_barge_with_adlocation(self):
        await self.check_start_transient_ni_language_option_yes('barge', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_caravan_with_adlocation(self):
        await self.check_start_transient_ni_language_option_yes('barge', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_tent_with_adlocation(self):
        await self.check_start_transient_ni_language_option_yes('tent', adlocation=True)

    @unittest_run_loop
    async def test_transient_ni_language_options_empty_barge(self):
        await self.check_start_transient_ni_language_option_empty('barge')

    @unittest_run_loop
    async def test_transient_ni_language_options_empty_caravan(self):
        await self.check_start_transient_ni_language_option_empty('caravan')

    @unittest_run_loop
    async def test_transient_ni_language_options_empty_tent(self):
        await self.check_start_transient_ni_language_option_empty('tent')

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_barge_ga(self):
        await self.check_start_transient_ni_select_language_option_language_selection('barge', 'ga', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_barge_ul(self):
        await self.check_start_transient_ni_select_language_option_language_selection('barge', 'ul', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_barge_en(self):
        await self.check_start_transient_ni_select_language_option_language_selection('barge', 'en', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_caravan_ga(self):
        await self.check_start_transient_ni_select_language_option_language_selection('caravan', 'ga', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_caravan_ul(self):
        await self.check_start_transient_ni_select_language_option_language_selection('caravan', 'ul', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_caravan_en(self):
        await self.check_start_transient_ni_select_language_option_language_selection('caravan', 'en', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_tent_ga(self):
        await self.check_start_transient_ni_select_language_option_language_selection('tent', 'ga', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_tent_ul(self):
        await self.check_start_transient_ni_select_language_option_language_selection('tent', 'ul', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_tent_en(self):
        await self.check_start_transient_ni_select_language_option_language_selection('tent', 'en', adlocation=False)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_barge_with_adlocation_ga(self):
        await self.check_start_transient_ni_select_language_option_language_selection('barge', 'ga', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_barge_with_adlocation_ul(self):
        await self.check_start_transient_ni_select_language_option_language_selection('barge', 'ul', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_barge_with_adlocation_en(self):
        await self.check_start_transient_ni_select_language_option_language_selection('barge', 'en', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_caravan_with_adlocation_ga(self):
        await self.check_start_transient_ni_select_language_option_language_selection('caravan', 'ga', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_caravan_with_adlocation_ul(self):
        await self.check_start_transient_ni_select_language_option_language_selection('caravan', 'ul', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_caravan_with_adlocation_en(self):
        await self.check_start_transient_ni_select_language_option_language_selection('caravan', 'en', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_tent_with_adlocation_ga(self):
        await self.check_start_transient_ni_select_language_option_language_selection('tent', 'ga', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_tent_with_adlocation_ul(self):
        await self.check_start_transient_ni_select_language_option_language_selection('tent', 'ul', adlocation=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_transient_ni_language_options_option_yes_tent_with_adlocation_en(self):
        await self.check_start_transient_ni_select_language_option_language_selection('tent', 'en', adlocation=True)

    @unittest_run_loop
    async def test_transient_ni_select_language_option_empty_barge(self):
        await self.check_start_transient_ni_select_language_option_no_selection('barge')

    @unittest_run_loop
    async def test_transient_ni_select_language_option_empty_caravan(self):
        await self.check_start_transient_ni_select_language_option_no_selection('caravan')

    @unittest_run_loop
    async def test_transient_ni_select_language_option_empty_tent(self):
        await self.check_start_transient_ni_select_language_option_no_selection('tent')

    @unittest_run_loop
    async def test_transient_town_name_after_census_day_ew_e(self):
        await self.check_start_transient_town_name_empty('en', 'E')

    @unittest_run_loop
    async def test_transient_town_name_after_census_day_ew_w(self):
        await self.check_start_transient_town_name_empty('en', 'W')

    @unittest_run_loop
    async def test_transient_town_name_after_census_day_cy(self):
        await self.check_start_transient_town_name_empty('cy', 'W')

    @unittest_run_loop
    async def test_transient_town_name_after_census_day_ni(self):
        await self.check_start_transient_town_name_empty('ni', 'N')

    @unittest_run_loop
    async def test_transient_town_name_before_census_day_ew_e(self):
        await self.check_start_transient_town_name_empty('en', 'E')

    @unittest_run_loop
    async def test_transient_town_name_before_census_day_ew_w(self):
        await self.check_start_transient_town_name_empty('en', 'W')

    @unittest_run_loop
    async def test_transient_town_name_before_census_day_cy(self):
        await self.check_start_transient_town_name_empty('cy', 'W')

    @unittest_run_loop
    async def test_transient_town_name_before_census_day_ni(self):
        await self.check_start_transient_town_name_empty('ni', 'N')

    @unittest_run_loop
    async def test_transient_town_name_empty_ew_e(self):
        await self.check_start_transient_town_name_empty('en', 'E')

    @unittest_run_loop
    async def test_transient_town_name_empty_ew_w(self):
        await self.check_start_transient_town_name_empty('en', 'W')

    @unittest_run_loop
    async def test_transient_town_name_empty_cy(self):
        await self.check_start_transient_town_name_empty('cy', 'W')

    @unittest_run_loop
    async def test_transient_town_name_empty_ni(self):
        await self.check_start_transient_town_name_empty('ni', 'N')

    @unittest_run_loop
    async def test_transient_accommodation_type_empty_ew_e(self):
        await self.check_start_transient_accommodation_type_empty('en', 'E')

    @unittest_run_loop
    async def test_transient_accommodation_type_empty_ew_w(self):
        await self.check_start_transient_accommodation_type_empty('en', 'W')

    @unittest_run_loop
    async def test_transient_accommodation_type_empty_cy(self):
        await self.check_start_transient_accommodation_type_empty('cy', 'W')

    @unittest_run_loop
    async def test_transient_accommodation_type_empty_ni(self):
        await self.check_start_transient_accommodation_type_empty('ni', 'N')
