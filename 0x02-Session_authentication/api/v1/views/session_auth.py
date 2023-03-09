#!/usr/bin/env python3
""" Module of Session auth views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    POST /api/v1/auth_session/login
    """
    email = request.form.get('email')
    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    userList = User().search({"email": email})
    if len(userList) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not userList[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    user = userList[0]
    from api.v1.app import auth

    user_session = auth.create_session(user.id)
    resp = jsonify(user.to_json())
    resp.set_cookie(os.getenv('SESSION_NAME'), user_session)

    return resp
