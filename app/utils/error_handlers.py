# utils/error_handlers.py

from webargs.flaskparser import abort
from marshmallow import ValidationError

def handle_validation_error(err, status_code):
    """Handle validation errors and return a JSON response with the error details."""
    if isinstance(err, ValidationError):
        abort(status_code, errors=err.messages)