#!/usr/bin/python3
"""
    Handles API requests to the User class
                                            """
from api.ports import app_ports
from models import storage
from models.recipient import Recipient
from flask import abort, jsonify

@app_ports.route('/recipients/<recipient_id>', methods=['GET'], strict_slashes=False)
def ports_recipients_get(recipient_id):
    """
        Retrieves all recipients of a User based On Id provided
        If not found returns None
                                            """
    if not storage.get(Recipient, recipient_id):
        abort(404)

    recipient_obj = storage.get(Recipient, recipient_id)

    return jsonify({'status': 'OK', 'object': recipient_obj.to_dict()})
