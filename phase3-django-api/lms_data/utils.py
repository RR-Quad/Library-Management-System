from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        # Wrap errors in a consistent format
        response.data = {
            "success": False,
            "errors": response.data
        }
        # Optional: add status code explicitly
        response.status_code = response.status_code
    else:
        # Handle unexpected errors
        response = Response(
            {"success": False, "errors": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response