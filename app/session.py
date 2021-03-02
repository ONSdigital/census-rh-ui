import time

from asyncio import get_event_loop
from aioredis import create_pool, RedisError
from aiohttp_session import session_middleware, Session, get_session
from aiohttp_session.redis_storage import RedisStorage
from structlog import get_logger
from .exceptions import SessionTimeout

logger = get_logger('respondent-home')

# Please see https://github.com/aio-libs/aiohttp-session/issues/344
# Anomalous behaviour can arise where you have a valid session cookie from the client as if a session was created by
# a previous request but cannot retrieve the session data in Redis, although the data will be in Redis. This behaviour
# was introduced with Pull Request: https://github.com/aio-libs/aiohttp-session/pull/331
# Monkey patch aiohttp_session Session.__init__ method to remove suspect behaviour.


def aiohttp_session_pr_331_rollback(self, identity, *, data, new,
                                    max_age=None):
    self._changed = False
    self._mapping = {}
    self._identity = identity if data != {} else None
    self._new = new
    self._new = new if data != {} else True
    self._max_age = max_age
    created = data.get('created', None) if data else None
    session_data = data.get('session', None) if data else None

    if self._new or created is None:
        self._created = int(time.time())
    else:
        self._created = created

    if session_data is not None:
        self._mapping.update(session_data)


def setup(app_config):
    # Monkey patch aiohttp_session.py Session.__init__ method to remove PR 331 as above
    Session.__init__ = aiohttp_session_pr_331_rollback

    loop = get_event_loop()
    redis_pool = loop.run_until_complete(
        make_redis_pool(app_config['REDIS_SERVER'], app_config['REDIS_PORT'], app_config['REDIS_POOL_MIN'], app_config['REDIS_POOL_MAX']))
    return session_middleware(
        RedisStorage(redis_pool,
                     cookie_name='RH_SESSION',
                     max_age=int(app_config['SESSION_AGE'])))


async def make_redis_pool(host, port, poolMin, poolMax):
    redis_address = (host, port)
    try:
        redis_pool = await create_pool(
            redis_address,
            create_connection_timeout=3,
            minsize=int(poolMin),
            maxsize=int(poolMax)
        )
        return redis_pool
    except (OSError, RedisError):
        logger.error('failed to create redis connection')


async def get_existing_session(request, user_journey, sub_user_journey=None) -> Session:
    session = await get_session(request)
    if not session.new:
        return session
    else:
        logger.warn('session timed out',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'])
        raise SessionTimeout(user_journey, sub_user_journey)


def get_session_value(request, session, key, user_journey, sub_user_journey=None):
    try:
        return session[key]
    except KeyError:
        logger.info(f'Failed to extract session key {key}',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'])
        raise SessionTimeout(user_journey, sub_user_journey)
