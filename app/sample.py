import logging

from aiohttp import ClientError
from aiohttp.web import Application
from structlog import wrap_logger
from .exceptions import InvalidEqPayLoad

logger = wrap_logger(logging.getLogger(__name__))


async def get_sample_attributes(sample_unit_id: str, app: Application):
    url = f"{app['SAMPLE_URL']}/samples/" + sample_unit_id + "/attributes"
    logger.debug(f"Making GET request to {url}")
    async with app.http_session_pool.get(url, auth=app["SAMPLE_AUTH"]) as response:
        try:
            response.raise_for_status()
        except ClientError as ex:
            logger.error("Error retrieving sample attributes", sample_unit_id=sample_unit_id, url=str(response.url),
                         status_code=response.status)
            raise ex
        else:
            logger.debug("Successfully retrieved sample attributes", sample_unit_id=sample_unit_id,
                         url=str(response.url))
        return await response.json()


class Address(object):

    def __init__(self, sample_attributes: dict, case_id: str):
        sample_attributes = {k.lower(): v for k, v in sample_attributes.items()}
        try:
            self._address_line1 = sample_attributes["address_line1"]
        except KeyError:
            raise InvalidEqPayLoad(f"No address_line1 for case {case_id}")
        self._address_line2 = sample_attributes["address_line2"]
        self._town_name = sample_attributes["town_name"]
        self._locality = sample_attributes["locality"]
        self._postcode = sample_attributes["postcode"]

    def to_dict(self) -> dict:
        return {
            'address_line1': self._address_line1,
            'address_line2': self._address_line2,
            'town_name': self._town_name,
            'locality': self._locality,
            'postcode': self._postcode
        }
