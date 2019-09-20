import aiohttp_jinja2 as jinja
import traceback

from aiohttp import web
from aiohttp.client_exceptions import (ClientResponseError,
                                       ClientConnectorError,
                                       ClientConnectionError, ContentTypeError)

from .exceptions import (ExerciseClosedError, InactiveCaseError,
                         InvalidEqPayLoad)
from structlog import get_logger

logger = get_logger('respondent-home')


def create_error_middleware(overrides):
    @web.middleware
    async def middleware_handler(request, handler):
        try:
            resp = await handler(request)
            override = overrides.get(resp.status)
            return await override(request) if override else resp
        except web.HTTPNotFound:
            path_prefix = request.app['URL_PATH_PREFIX']

            def path_starts_with(suffix):
                return request.path.startswith(path_prefix + suffix)

            if path_starts_with('/ni'):
                index_resource = request.app.router['IndexNI:get']
            elif path_starts_with('/dechrau') or path_starts_with('/cy'):
                index_resource = request.app.router['IndexCY:get']
            else:
                index_resource = request.app.router['IndexEN:get']

            if request.path + '/' == index_resource.canonical:
                logger.debug('redirecting to index', path=request.path)
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
        except KeyError:
            return await key_error(request)
        except ClientResponseError:
            return await response_error(request)
        # TODO fallthrough error here

    return middleware_handler


async def inactive_case(request, case_type):
    logger.warn('attempt to use an inactive access code')
    attributes = check_display_region(request)
    attributes['case_type'] = case_type
    return jinja.render_template('expired.html', request, attributes)


async def ce_closed(request, collex_id):
    logger.warn('attempt to access collection exercise that has already ended',
                collex_id=collex_id)
    attributes = check_display_region(request)
    return jinja.render_template('closed.html', request, attributes)


async def eq_error(request, message: str):
    logger.error('service failed to build eq payload', exception=message)
    attributes = check_display_region(request)
    return jinja.render_template('error.html', request, attributes, status=500)


async def connection_error(request, message: str):
    logger.error('service connection error', exception=message)
    attributes = check_display_region(request)
    return jinja.render_template('error.html', request, attributes, status=500)


async def payload_error(request, url: str):
    logger.error('service failed to return expected json payload', url=url)
    attributes = check_display_region(request)
    return jinja.render_template('error.html', request, attributes, status=500)


async def key_error(request):
    logger.error('required value missing')
    attributes = check_display_region(request)
    return jinja.render_template('error.html', request, attributes, status=500)


async def response_error(request):
    attributes = check_display_region(request)
    return jinja.render_template('error.html', request, attributes, status=500)


async def not_found_error(request):
    attributes = check_display_region(request)
    return jinja.render_template('404.html', request, attributes, status=404)


async def forbidden(request):
    attributes = check_display_region(request)
    return jinja.render_template('index.html', request, attributes, status=403)


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

    def path_starts_with(suffix):
        return request.path.startswith(path_prefix + suffix)

    domain_url_en = request.app['DOMAIN_URL_PROTOCOL'] + request.app[
        'DOMAIN_URL_EN']
    domain_url_cy = request.app['DOMAIN_URL_PROTOCOL'] + request.app[
        'DOMAIN_URL_CY']

    base_attributes = {
        'domain_url_en': domain_url_en,
        'domain_url_cy': domain_url_cy,
        'page_title': 'Error'
    }

    if path_starts_with('/ni'):
        attributes = {
            **base_attributes,
            'display_region': 'ni',
        }
    elif any([
            path_starts_with('/dechrau'),
            path_starts_with('/gwe-sgwrs'),
            path_starts_with('/gofyn-am-god-mynediad'),
            path_starts_with('/cy')
    ]):
        attributes = {
            **base_attributes,
            'display_region': 'cy',
            'locale': 'cy',
        }
    else:
        attributes = {
            **base_attributes,
            'display_region': 'en',
        }

    return attributes
