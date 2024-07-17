#!/usr/bin/env python3
"""
a simple flask app authentication
"""
from flask import Flask, Response, abort, jsonify, redirect, request

from auth import Auth

app = Flask(__file__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """
    welcome page i guess
    """
    return jsonify(message="Bienvenue")


@app.route("/users", methods=["POST"])
def register_user():
    """
    regist user to the application
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        AUTH.register_user(email=email, password=password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """
    authenticate user login credential
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return abort(422)

    user_cred = AUTH.valid_login(email, password)
    if not user_cred:
        return abort(401)
    resp = jsonify({"email": email, "message": "logged in"})
    user_session = AUTH.create_session(email)
    if user_session:
        resp.set_cookie("session_id", user_session)
    return resp


@app.route("/sessions", methods=["DELETE"])
def logout():
    """logout user and rediret back to homepage"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return abort(403)

    AUTH.destroy_session(user_id=user.id)
    return redirect("/")


@app.route('/profile', methods=["GET"])
def profile():
    session_id = request.cookies.get("session_id")
    if not session_id:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return abort(403)

    return jsonify({"email": user.email}), 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
