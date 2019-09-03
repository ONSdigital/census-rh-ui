import logging

import aiohttp_jinja2
from aiohttp import web
from aiohttp.client_exceptions import (
    ClientResponseError, ClientConnectorError, ClientConnectionError, ContentTypeError)
from structlog import wrap_logger

from .exceptions import ExerciseClosedError, InactiveCaseError, InvalidEqPayLoad


logger = wrap_logger(logging.getLogger("respondent-home"))


def create_error_middleware(overrides):

    @web.middleware
    async def middleware_handler(request, handler):
        try:
            resp = await handler(request)
            override = overrides.get(resp.status)
            return await override(request) if override else resp
        except web.HTTPNotFound:
            path_prefix = request.app['URL_PATH_PREFIX']
            if request.path.startswith(path_prefix + '/ni'):
                index_resource = request.app.router['IndexNI:get']
            elif request.path.startswith(path_prefix + '/dechrau') or request.path.startswith(path_prefix + '/cy'):
                index_resource = request.app.router['IndexCY:get']
            else:
                index_resource = request.app.router['IndexEN:get']

            if request.path + '/' == index_resource.canonical:
                logger.debug('Redirecting to index', path=request.path)
                raise web.HTTPMovedPermanently(index_resource.url_for())
            return await not_found_error(request)
        except web.HTTPForbidden:
            return await forbidden(request)
        except InactiveCaseError as ex:
            return await inactive_case(request, ex.case_type)
        except ExerciseClosedError as ex:
            return await ce_closed(request, ex.collection_exercise_id)
        except InvalidEqPayLoad as ex:
            return await eq_error(request, ex.message)
        except ClientConnectionError as ex:
            return await connection_error(request, ex.args[0])
        except ClientConnectorError as ex:
            return await connection_error(request, ex.os_error.strerror)
        except ContentTypeError as ex:
            return await payload_error(request, str(ex.request_info.url))
        except ClientResponseError:
            return await response_error(request)

    return middleware_handler


async def inactive_case(request, case_type):
    logger.warn("Attempt to use an inactive access code")
    attributes = check_display_region(request)
    attributes['case_type'] = case_type
    return aiohttp_jinja2.render_template("expired.html", request, attributes)


async def ce_closed(request, collex_id):
    logger.warn("Attempt to access collection exercise that has already ended", collex_id=collex_id)
    attributes = check_display_region(request)
    return aiohttp_jinja2.render_template("closed.html", request, attributes)


async def eq_error(request, message: str):
    logger.error("Service failed to build eQ payload", message=message)
    attributes = check_display_region(request)
    return aiohttp_jinja2.render_template("error.html", request, attributes, status=500)


async def connection_error(request, message: str):
    logger.error("Service connection error", message=message)
    attributes = check_display_region(request)
    return aiohttp_jinja2.render_template("error.html", request, attributes, status=500)


async def payload_error(request, url: str):
    logger.error("Service failed to return expected JSON payload", url=url)
    attributes = check_display_region(request)
    return aiohttp_jinja2.render_template("error.html", request, attributes, status=500)


async def response_error(request):
    attributes = check_display_region(request)
    return aiohttp_jinja2.render_template("error.html", request, attributes, status=500)


async def not_found_error(request):
    attributes = check_display_region(request)
    return aiohttp_jinja2.render_template("404.html", request, attributes, status=404)


async def forbidden(request):
    attributes = check_display_region(request)
    return aiohttp_jinja2.render_template("index.html", request, attributes, status=403)


def setup(app):
    overrides = {
        500: response_error,
        503: response_error,
        404: not_found_error,
    }
    error_middleware = create_error_middleware(overrides)
    app.middlewares.append(error_middleware)


def check_display_region(request):
    path_prefix = request.app['URL_PATH_PREFIX']
    if request.url.path.startswith(path_prefix + '/ni'):
        attributes = {'display_region': 'ni'}
    elif request.url.path.startswith(path_prefix + '/dechrau') or request.url.path.startswith(path_prefix + '/cy'):
        attributes = {'display_region': 'cy', 'locale': 'cy'}
    else:
        attributes = {'display_region': 'en'}

    return attributes
