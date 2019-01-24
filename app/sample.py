import logging

from aiohttp import ClientError
from aiohttp.web import Application
from structlog import wrap_logger


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
