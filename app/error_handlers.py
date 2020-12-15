import aiohttp_jinja2 as jinja

from aiohttp import web
from aiohttp.client_exceptions import (ClientResponseError,
                                       ClientConnectorError,
                                       ClientConnectionError, ContentTypeError)

from .exceptions import (ExerciseClosedError, InactiveCaseError,
                         InvalidEqPayLoad,
                         SessionTimeout,
                         TooManyRequests, TooManyRequestsWebForm)
from structlog import get_logger

from .utils import View

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

            index_resource = request.app.router['Start:get']

            if path_starts_with('/ni'):
                display_region = 'ni'
            elif path_starts_with('/cy'):
                display_region = 'cy'
            else:
                display_region = 'en'

            if request.path + '/' == index_resource.canonical.replace('{display_region}', display_region):
                logger.debug('redirecting to index', path=request.path)
                raise web.HTTPMovedPermanently(index_resource.url_for(display_region=display_region))
            return await not_found_error(request)
        except web.HTTPForbidden:
            return await forbidden(request)
        except SessionTimeout as ex:
            return await session_timeout(request, ex.user_journey, ex.sub_user_journey)
        except TooManyRequests as ex:
            return await too_many_requests(request, ex.sub_user_journey)
        except TooManyRequestsWebForm:
            return await too_many_requests_web_form(request)
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
        except KeyError as error:
            return await key_error(request, error)
        except ClientResponseError:
            return await response_error(request)
        # TODO fallthrough error here

    return middleware_handler


async def inactive_case(request, case_type):
    logger.warn('attempt to use an inactive access code')
    attributes = check_display_region(request)
    attributes['case_type'] = case_type
    return jinja.render_template('start-expired.html', request, attributes)


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


async def key_error(request, error):
    logger.error('required value ' + str(error) + ' missing', missing_key=error)
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
    return jinja.render_template('start-timeout.html', request, attributes, status=403)


async def too_many_requests(request, sub_user_journey: str):
    attributes = check_display_region(request)
    attributes['sub_user_journey'] = sub_user_journey
    return jinja.render_template('request-too-many-requests.html', request, attributes, status=429)


async def too_many_requests_web_form(request):
    attributes = check_display_region(request)
    return jinja.render_template('web-form-too-many-requests.html', request, attributes, status=429)


async def session_timeout(request, user_journey: str, sub_user_journey: str):
    attributes = check_display_region(request)
    if user_journey == 'start':
        return jinja.render_template('start-timeout.html', request, attributes, status=403)
    else:
        attributes['user_journey'] = user_journey
        attributes['sub_user_journey'] = sub_user_journey
        return jinja.render_template('request-timeout.html', request, attributes, status=403)


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
        'page_title': 'Error',
        'page_url': View.gen_page_url(request)
    }

    if path_starts_with('/ni'):
        attributes = {
            **base_attributes,
            'display_region': 'ni',
        }
    elif path_starts_with('/cy'):
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
