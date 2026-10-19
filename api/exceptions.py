from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
import logging
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Let DRF handle its own exceptions first
    response = exception_handler(exc, context)
    if response is not None:
        return response

    # Django ValidationError from your service layer
    if isinstance(exc, DjangoValidationError):
        # Django ValidationError.messages is always a list
        return Response(
            {
                "error": {
                    "code": "validation_error",
                    "messages": exc.messages,
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # DRF ValidationError not caught by serializers
    if isinstance(exc, DRFValidationError):
        return Response(
            {
                "error": {
                    "code": "validation_error",
                    "detail": exc.detail,
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    logger.error("Unhandled exception", exc_info=exc)

    # Fallback: unexpected errors
    return Response(
        {
            "error": {
                "code": "server_error",
                "message": "Something went wrong.",
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
