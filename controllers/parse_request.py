from flask import request
import json


def get_request_data():
    """
    Get keys & values from request (Note that this method should parse requests with content type "application/x-www-form-urlencoded")
    """

    if request.content_type.startswith('application/x-www-form-'):
        data = request.form.to_dict()
        return data
