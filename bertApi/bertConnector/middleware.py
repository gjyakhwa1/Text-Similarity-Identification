from django.http import HttpResponse


def simple_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if 4>5:
            return response
        return HttpResponse("Model Not loading", status=503)
    return middleware
