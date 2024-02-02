#!/usr/bin/python3
"""
    Handles API requests to the User class
                                            """
from api.ports import app_ports
from models import storage
from models.recipient import Recipient
from flask import abort

@app_ports.route('/recipients/<user_id>', methods=['GET'], strict_slashes=False)
def ports_recipients_get(user_id):
    """
        Retrieves all recipients of a User based On Id provided
        If not found returns None
                                            """
    if not storage.get(User, user_id):
        abort(404)

    user_obj = storage.get(User, user_id)
    recipients = user_obj.recipients

    recipient_list = [obj.to_dict() for obj in recipients]

    return jsonify({'status': 'OK', 'objects': recipient_list})
