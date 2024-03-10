#!/usr/bin/python3
"""
    Returns login and sign up pages as well as api test flights
                                                                """
from api.ports import app_ports
from models import storage
from models.user import User
from flask import request, abort, make_response, jsonify
from flask import render_template
from uuid import uuid4


@app_ports.route('/sign_up', methods=['GET'], strict_slashes=False)
def ports_sign_up():
    """
        Returns the sign up page upon request
                                                """
    return render_template('sign-up.html', uuid=uuid4())

@app_ports.route('/login', methods=['GET'], strict_slashes=False)
def ports_login():
    """
        Returns login page upon request
                                        """
    return render_template('login-page.html', uuid=uuid4())

@app_ports.route('/users/login', strict_slashes=False, methods=['POST'])
def user_login():
    """
        Returns User obj if User_id sent is registered
                                                        """
    if not request.get_json():
        abort(404)

    user_data = request.get_json()

    if not user_data.get('user_id'):
        abort(404)

    user_objs = storage.user_login(user_data.get('user_id'))

    if not user_objs:
        abort(404)

    return render_template('user-page.html', user_object=user_objs[0], uuid=uuid4())
