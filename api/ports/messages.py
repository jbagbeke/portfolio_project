#!/usr/bin/python3
"""
    Handles API requests to the Message class
                                            """
from api.ports import app_ports
from models import storage
from models.message import Message
from models.user import User
from models.recipient import Recipient
from flask import request, abort, make_response, jsonify
 

"""def create_recipient_object(user_id, message_id, receiver_number,
                            message_obj, user_obj):
        Creates A recipient Instance
                                    
    new_recipient = Recipient(user_id=user_id, message_id=message_id,
                              receiver_number=receiver_number, message=message_obj,
                              user=user_obj)
    return new_recipient"""

@app_ports.route('/messages/<message_id>', methods=['GET'], strict_slashes=False)
def ports_messages_get(message_id):
    """
        Retrieves a Message based On Id provided
        If not found returns None
                                            """
    if not storage.get(Message, message_id):
        abort(404)

    message_obj = storage.get(Message, message_id)

    return jsonify({'status': 'OK', 'object': message_obj.to_dict()})

@app_ports.route('/messages/create', methods=['POST'], strict_slashes=False)
def ports_messages_create():
    """
        Creates a new Message object and saves it to the DataBase
                                                                """
    if not request.get_json():
        abort(404)
    
    request_data = request.get_json()

    if not request_data.get('user_id') or not request_data.get('body'):
        return jsonify({'error': 'Invalid Details'})

    if not request_data.get('receiver_number'):
        return jsonify({'error': 'Invalid Details'})

    user_id = request_data.get('user_id')

    if not storage.get(User, user_id):
        abort(404)

    receiver_number = request_data.get('receiver_number')
    message_body = request_data.get('body')
    
    user_object = storage.get(User, user_id)
    message_object = Message(user_id=user_id, body=message_body,
                             user=user_object)

    recipient_object = Recipient(user_id=user_id, message_id=message_object.id,
                              receiver_number=receiver_number, message=message_object,
                              user=user_object)

    print("USER:\n", user_object.to_dict())
    print("\nMessage", message_object.to_dict())
    print("\nRecipient", recipient_object.to_dict())

    storage.new(message_object)
    storage.new(recipient_object)
    storage.save()

    return {'status': 'OK', 'object': message_object.to_dict()}

@app_ports.route('/messages/updates', methods=['POST'], strict_slashes=False)
def ports_messages_updates():
    """
        Updates attributes of a Message Object
                                    """
    if not request.get_json():
        abort(404)
    
    request_data = request.get_json()

    if not request_data.get('message_id'):
        abort(404)

    message_id = request_data.get('message_id')

    if not storage.get(Message, message_id):
        abort(404)

    message_object = storage.get(Message, message_id)

    message_body = request_data.get('body', None)

    if message_body:
        message_object.body = message_body
        storage.save()
    
    return jsonify({'status': 'OK', 'object': message_object.to_dict()})

@app_ports.route('/messages/delete/<message_id>', methods=['POST'], strict_slashes=False)
def ports_messages_delete(message_id):
    """
        Deletes a Message Object from the Database
                                                """
    if not storage.get(Message, message_id):
        abort(404)

    message_object = storage.get(Message, message_id)

    storage.delete(message_object)
    storage.save()

    return make_response(jsonify({'status': 'OK'}), 204)
