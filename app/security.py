import random
import string
import hashlib

from aiohttp import web
from aiohttp_session import get_session, Session
from aiohttp.web import HTTPForbidden

from structlog import get_logger

from .session import get_existing_session

CSP = {
    'default-src': [
        "'self'",
        'https://cdn.census.gov.uk',
    ],
    'font-src': [
        "'self'",
        'data:',
        'https://fonts.gstatic.com',
        'https://cdn.census.gov.uk',
    ],
    'script-src': [
        "'self'",
        'https://www.googletagmanager.com',
        "'unsafe-inline'",
        "'unsafe-eval'",
        'https://cdn.census.gov.uk',
    ],
    'style-src': [
        "'self'",
        'https://tagmanager.google.com',
        'https://fonts.googleapis.com',
        "'unsafe-inline'",
        'https://cdn.census.gov.uk'
    ],
    'connect-src': [
        "'self'",
        'https://cdn.census.gov.uk',
        'https://www.google-analytics.com'
    ],
    'frame-src': [
        'https://www.googletagmanager.com',
        'https://www.timeforstorm.com'
    ],
    'img-src': [
        "'self'",
        'data:',
        'https://www.google-analytics.com',
        'https://ssl.gstatic.com',
        'https://www.gstatic.com',
        'https://cdn.census.gov.uk'
    ],
}


def _format_csp(csp_dict):
    return ' '.join([
        f"{section} {' '.join(content)};"
        for section, content in csp_dict.items()
    ])


DEFAULT_RESPONSE_HEADERS = {
    'Strict-Transport-Security': 'max-age=31536000 includeSubDomains',
    # 'Content-Security-Policy': _format_csp(CSP),
    'Content-Security-Policy': CSP,
    'X-Content-Security-Policy': CSP,
    'X-XSS-Protection': '1; mode=block',
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
}

ADD_NONCE_SECTIONS = [
    'script-src',
]

SESSION_KEY = 'identity'

rnd = random.SystemRandom()

logger = get_logger('respondent-home')


def get_random_string(length):
    allowed_chars = (string.ascii_lowercase + string.ascii_uppercase +
                     string.digits)
    return ''.join(rnd.choice(allowed_chars) for _ in range(length))


@web.middleware
async def nonce_middleware(request, handler):
    request.csp_nonce = get_random_string(16)
    return await handler(request)


async def on_prepare(request: web.BaseRequest, response: web.StreamResponse):
    for header, value in DEFAULT_RESPONSE_HEADERS.items():
        if isinstance(value, dict):
            value = '; '.join([
                f"{section} {' '.join(content)} 'nonce-{request.csp_nonce}'"
                if section in ADD_NONCE_SECTIONS else
                f"{section} {' '.join(content)}"
                for section, content in value.items()
            ])
        elif not isinstance(value, str):
            value = ' '.join(value)
        response.headers[header] = value


async def context_processor(request):
    return {
        'cspNonce': request.csp_nonce,
    }


async def get_permitted_session(request) -> Session:
    """
    Check request permission.
    Raise HTTPForbidden if existing session and not previously remembered, else return session.
    """
    session = await get_existing_session(request, 'start')
    try:
        identity = session[SESSION_KEY]
        logger.info('permission granted',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    identity=identity,
                    url=request.rel_url.human_repr())
        return session
    except KeyError:
        logger.warn('permission denied',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    url=request.rel_url.human_repr())
        raise HTTPForbidden


async def forget(request):
    """
    Forget identity.
    Modify session to remove previously remembered identity.
    """
    session = await get_session(request)
    try:
        identity = session[SESSION_KEY]
        session.pop(SESSION_KEY, None)
        logger.info('identity forgotten',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    identity=identity)
    except KeyError:
        logger.warn('identity not previously remembered',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    url=request.rel_url.human_repr())


async def remember(identity, request):
    """
    Remember identity.
    Modify session with remembered identity.
    """
    session = await get_session(request)
    session[SESSION_KEY] = identity
    logger.info('identity remembered',
                client_ip=request['client_ip'],
                client_id=request['client_id'],
                trace=request['trace'],
                identity=identity)


async def invalidate(request):
    """
    Invalidate open session.
    """
    session = await get_session(request)
    try:
        session.invalidate()
        logger.info('session invalidated',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'])
    except KeyError:
        logger.warn('session already invalidated',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'])


def get_sha256_hash(uac: str):
    return hashlib.sha256(uac.encode()).hexdigest()
