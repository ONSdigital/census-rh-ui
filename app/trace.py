from aiohttp import web
from aiohttp_session import get_session
from uuid import uuid4


def get_trace(headers):
    try:
        trace, span = headers.get("X-Cloud-Trace-Context").split("/")
    except (ValueError, AttributeError):
        return None
    return trace


@web.middleware
async def trace_middleware(request, handler):
    request['trace'] = get_trace(request.headers)
    request['client_ip'] = request.headers.get('X-Forwarded-For')
    session = await get_session(request)
    if 'client_id' in session:
        request['client_id'] = session['client_id']
    else:
        session['client_id'] = request['client_id'] = str(uuid4())
    return await handler(request)
