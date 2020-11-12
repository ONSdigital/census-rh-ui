from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from .helpers import TestHelpers


# noinspection PyTypeChecker
class TestStartHandlersTransient(TestHelpers):
    user_journey = 'start'
    sub_user_journey = 'transient'

    @unittest_run_loop
    async def test_transient_accommodation_type_empty_ew_e(self):
        display_region = 'en'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.transient_uac_json_e)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST',
                                      self.post_start_en,
                                      allow_redirects=True,
                                      data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/transient/enter-town-name'")

        await self.check_post_start_transient_enter_town_name_valid(
            self.get_url_from_class('StartTransientEnterTownName', 'post', display_region), display_region)
        await self.check_post_start_transient_accommodation_type_no_selection(
            self.get_url_from_class('StartTransientAccommodationType', 'post', display_region), display_region)
