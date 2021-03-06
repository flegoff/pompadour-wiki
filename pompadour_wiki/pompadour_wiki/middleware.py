class UnsetAcceptLanguageHeaderMiddleware(object):
    """
        Remove HTTP_ACCEPT_LANGUAGE header in order to use value
        defined in settings.py
    """

    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del(request.META['HTTP_ACCEPT_LANGUAGE'])
