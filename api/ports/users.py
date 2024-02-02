#!/usr/bin/python3
"""
    Handles API requests to the User class
                                            """
from api.ports import app_ports
from models import storage
from models.user import User
from flask import request, abort, make_response, jsonify

@app_ports.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def ports_users_get(user_id):
    """
        Retrieves a User based On Id provided
        If not found returns None
                                            """
    if not storage.get(User, user_id):
        abort(404)

    user_obj = storage.get(User, user_id)

    return jsonify({'status': 'OK', 'object': user_obj.to_dict()})


@app_ports.route('/users/create', methods=['POST'], strict_slashes=False)
def ports_users_create():
    """
        Creates a new User object and saves it to the DataBase
                                                                """
    if not request.get_json():
        abort(404)
    
    request_data = request.get_json()

    if not request_data.get('name') or not request_data.get('number'):
        abort(404)

    user_name = request_data.get('name')
    user_number = request_data.get('number')
    user_id = User._UserID()

    new_user_object = User(user_id=user_id, name=user_name, number=user_number)
    
    storage.new(new_user_object)
    storage.save()

    return jsonify({'status': 'OK', 'object': new_user_object.to_dict()})

@app_ports.route('/users/updates', methods=['POST'], strict_slashes=False)
def ports_users_updates():
    """
        Updates attributes of a User
                                    """
    if not request.get_json():
        abort(404)
    
    request_data = request.get_json()

    if not request_data.get('user_id'):
        abort(404)

    user_id = request_data.get('user_id')

    if not storage.get(User, user_id):
        abort(404)

    user_object = storage.get(User, user_id)

    user_name = request_data.get('name', None)
    user_number = request_data.get('number', None)
    valid = False

    if user_name:
        user_object.name = user_name
        valid = True
    
    if user_number:
        user_object.number = user_number
        valid = True

    if valid:
        storage.save()
    
    return jsonify({'status': 'OK', 'object': user_object.to_dict()})

@app_ports.route('/users/delete/<user_id>', methods=['POST'], strict_slashes=False)
def ports_users_delete(user_id):
    """
        Deletes a User Object from the Database
                                                """
    if not storage.get(User, user_id):
        abort(404)

    user_object = storage.get(User, user_id)

    storage.delete(user_object)
    storage.save()

    return make_response(jsonify({'status': 'OK'}), 204)
