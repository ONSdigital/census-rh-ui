import logging

from asyncio import get_event_loop
from aioredis import create_pool, RedisError
from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
from structlog import wrap_logger


logger = wrap_logger(logging.getLogger("respondent-home"))


def setup(app_config):
    loop = get_event_loop()
    redis_pool = loop.run_until_complete(make_redis_pool(app_config["REDIS_SERVER"], app_config["REDIS_PORT"]))
    return session_middleware(RedisStorage(redis_pool, cookie_name='RH_SESSION',
                                           max_age=int(app_config["ABSOLUTE_SESSION_AGE"])))


async def make_redis_pool(host, port):
    redis_address = (host, port)
    try:
        redis_pool = await create_pool(
            redis_address,
            create_connection_timeout=3,
        )
        return redis_pool
    except (OSError, RedisError):
        logger.error("Failed to create Redis connection")
