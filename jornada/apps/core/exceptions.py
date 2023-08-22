import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ValidationError

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    if isinstance(exc, ValidationError):
        # logs detail data from the exception being handled
        logging.error(f"Original error detail and callstack: {exc}")
        return Response({'status': 400, 'error': 'Bad Request', 'messsages': exc.messages}, status=400)

    if isinstance(exc, Exception):
        # logs detail data from the exception being handled
        logging.error(f"Original error detail and callstack: {exc}")
        return Response({'status': 400, 'error': 'Bad Request', 'messsages': str(exc)}, status=400)
    
    # returns response as handled normally by the framework
    return response

def get_error_message(error):
    if hasattr(error, 'message'):
        return error.message
    if hasattr(error, 'messages'):
        print(f"{type(error.messages)=}")
        if isinstance(error.messages, list):
            return ', '.join(error.messages)
        if isinstance(error.messages, dict):
            return ', '.join(error.messages.values())
        return str(error.messages)
    return str(error)