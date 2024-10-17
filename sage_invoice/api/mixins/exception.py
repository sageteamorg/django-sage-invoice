import logging
import uuid

from django.utils.timezone import now
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    NotAcceptable,
    NotFound,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler

# Get the logger instance
logger = logging.getLogger(__name__)


class ErrorHandlingMixin:
    """
    Mixin to provide consistent error handling across APIs,
    including structured error responses, logging, and trace IDs.
    """

    def handle_exception(self, exc):
        """
        Override the default DRF exception handling to provide
        a structured error response with logging and trace IDs.
        """
        # Call the default DRF exception handler first to get the default response
        response = exception_handler(exc, self.get_exception_handler_context())

        # Generate a unique trace ID for this request
        trace_id = str(uuid.uuid4())

        # Path from the current request
        path = self.request.path if hasattr(self, "request") else "unknown"

        # Default error structure
        error_response = {
            "code": "SERVER_ERROR",
            "message": "An unexpected error occurred.",
            "details": [],
            "path": path,
            "traceId": trace_id,
            "timestamp": now().isoformat(),
        }

        # Handle specific exceptions for better detail
        if isinstance(exc, ValidationError):
            error_response["code"] = "VALIDATION_ERROR"
            error_response["message"] = "Invalid input parameters"
            error_response["details"] = [
                {"field": field, "message": msg[0] if isinstance(msg, list) else msg}
                for field, msg in exc.detail.items()
            ]
            status_code = status.HTTP_400_BAD_REQUEST

        elif isinstance(exc, NotFound):
            error_response["code"] = "NOT_FOUND"
            error_response["message"] = str(exc)
            status_code = status.HTTP_404_NOT_FOUND

        elif isinstance(exc, NotAcceptable):
            error_response["code"] = "NOT_ACCEPTABLE"
            error_response["message"] = str(exc)
            status_code = status.HTTP_406_NOT_ACCEPTABLE

        elif isinstance(exc, APIException):
            error_response["code"] = exc.get_codes() if exc.get_codes() else "API_ERROR"
            error_response["message"] = str(exc)
            status_code = exc.status_code

        else:
            # If response is None, this means DRF didn't handle the exception, so we do it ourselves.
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        # If DRF handled the exception, override its response data with the structured error
        if response is not None:
            response.data = error_response
            response.status_code = status_code
        else:
            # Create a custom response if DRF couldn't handle the exception
            response = Response(error_response, status=status_code)

        # Log the error details with trace ID for correlation
        logger.error(
            f"Error occurred [traceId={trace_id}] at {path}: {exc}", exc_info=True
        )

        return response

    def get_exception_handler_context(self):
        """
        This method returns the context that will be passed to the DRF exception
        handler.

        It's useful to provide additional request-related context (like view, request, args).
        """
        return {
            "view": self,
            "request": self.request,
        }
