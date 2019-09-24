async def ga_ua_id_processor(request):
    return {'gtm_auth': request.app['GTM_AUTH'],
            'gtm_preview': request.app['GTM_PREVIEW'],
            'gtm_cookies_win': request.app['GTM_COOKIES_WIN']}
