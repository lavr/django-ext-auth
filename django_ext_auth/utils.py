def get_real_ip(request):
    if 'HTTP_X_REAL_IP' in request.META:
        return request.META['HTTP_X_REAL_IP']
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
    return request.META.get('REMOTE_ADDR', None)

