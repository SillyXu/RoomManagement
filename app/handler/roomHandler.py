# roomHandler.py
from flask import jsonify
from webargs.flaskparser import parser

def init_error_handlers(app):
    @parser.error_handler
    def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
        """webargs request parsing error handler"""
        status_code = error_status_code or 500
        return jsonify({'errors': err.messages}), status_code