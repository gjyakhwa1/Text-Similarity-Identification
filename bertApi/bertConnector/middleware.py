from email.header import Header
from .helper import getCount
from django.http import HttpResponse


def simple_middleware(get_response):
    def middleware(request):
        if getCount() == 1:
            response = get_response(request)
            return response
        return HttpResponse("Model Not loading", status=503)
    return middleware
