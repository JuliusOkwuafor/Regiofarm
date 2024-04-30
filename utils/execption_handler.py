from django.http import JsonResponse
from rest_framework.views import exception_handler
from .response import get_response




def get_error_message(error_dict):
    field = next(iter(error_dict))
    response = error_dict[next(iter(error_dict))]
    if isinstance(response, dict):
        response = get_error_message(response)
    elif isinstance(response, list):
        response_message = response[0]
        if isinstance(response_message, dict):
            response = get_error_message(response_message)
        else:
            response = response[0]
    # print('my my my'+response)
    return response


def handle_exception(exc, context):
    error_response = exception_handler(exc, context)
    # print(f'context: {context},\nexception: {exc}')
    if error_response is not None:
        error = error_response.data

        if isinstance(error, list) and error:
            if isinstance(error[0], dict):
                error_response.data = get_response(message=get_error_message(error))

            elif isinstance(error[0], str):
                error_response.data = get_response(message=error[0])

        if isinstance(error, dict):
            error_response.data = get_response(message=get_error_message(error))
    # print(f'err_response:  {error_response}\n\n')
    return error_response
