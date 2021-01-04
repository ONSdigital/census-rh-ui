async def ga_ua_id_processor(request):
    return {'gtm_cont_id': request.app['GTM_CONTAINER_ID'], 'gtm_auth': request.app['GTM_AUTH']}
