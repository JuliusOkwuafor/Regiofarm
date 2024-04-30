from django.http import JsonResponse
from .response import get_response


def error_404(request, exception):
    message = "The endpoint is not found"
    gresponse = get_response(message=message)
    response = JsonResponse(data=gresponse)
    response.status_code = 404
    return response


def error_500(request):
    message = "An error occured it from us"
    gresponse = get_response(message=message, code=50000)
    response = JsonResponse(data=gresponse)
    response.status_code = 500
    return response
