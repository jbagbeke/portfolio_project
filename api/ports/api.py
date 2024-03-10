#!/usr/bin/python3
"""
    Handles API requests to the external APIs
                                            """
from models import storage
from models.user import User
from models.recipient import Recipient
from models.message import Message
from models.message_api import MessageAPI
from api.ports import app_ports
from flask import request, abort, jsonify, make_response 


@app_ports.route('/verify/number', methods=['POST'], strict_slashes=False)
def number_verification():
    """
        Performs number verification using external API
                                                        """
    if not request.get_json():
        abort(404)

    message_list = request.get_json()
    number_list = []
    
    number_list_tmp = message_list['recipients'].replace(',', ' ')
    number_list_tmp = number_list_tmp.replace('.', ' ')
    number_list_tmp = number_list_tmp.replace(';', ' ')
    number_list_tmp = number_list_tmp.split()

    for number in number_list_tmp:
        if number.startswith('+') and number[1:].isdigit():
            number_list.append(number)
        elif number.isdigit():
            number_list.append(str(number))

    number_verification = MessageAPI.verify_number_api(number_list)

    return jsonify(number_verification)

@app_ports.route('/message/generation', methods=['POST'], strict_slashes=False)
def message_api():
    """
        Handles AI message generation
                                    """
    if not request.get_json():
        print(request)
        abort(404)

    user_topic = request.get_json()
    message_topic = user_topic.get('topic')

    if not message_topic:
        abort(404)

    ai_messages = MessageAPI.open_ai(message_topic)

    return jsonify(ai_messages)

@app_ports.route('/message/send', methods=['POST'], strict_slashes=False)
def message_send():
    """
        Sends Message to specified recipients
                                            """
    if not request.get_json():
        abort(404)
        
    message_details = request.get_json()
    
    user_id = message_details.get('user_id')
    message_body = message_details.get('message') 
    number_list_tmp = message_details['recipients']
    
    recipient_list = []

    
    for number in number_list_tmp:
        if number.startswith('+') and number[1:].isdigit():
            recipient_list.append(number)
        elif number.isdigit():
            recipient_list.append(int(number))

    user_object = storage.get(User, user_id)

    message_response = MessageAPI.message_engine(str(message_body), recipient_list, user_object)

    return jsonify({'status': message_response})
