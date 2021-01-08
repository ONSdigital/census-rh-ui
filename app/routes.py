from aiohttp_utils.routing import add_resource_context

from .webchat_handlers import webchat_routes
from .web_form_handlers import web_form_routes
from .request_handlers import request_routes
from .start_handlers import start_routes
from .handlers import static_routes
from .common_handlers import common_routes
from .support_centre_handlers import support_centre_routes


def setup(app, url_path_prefix):
    """Set up routes as resources so we can use the `Index:get` notation for URL lookup."""

    combined_routes = [*request_routes, *start_routes, *static_routes, *web_form_routes,
                       *webchat_routes, *common_routes, *support_centre_routes]

    for route in combined_routes:
        use_prefix = route.kwargs.get('use_prefix', True)
        prefix = url_path_prefix if use_prefix else ''
        with add_resource_context(app,
                                  module='app.handlers',
                                  url_prefix=prefix) as new_route:
            new_route(route.path, route.handler())
