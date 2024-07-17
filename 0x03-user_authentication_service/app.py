#!/usr/bin/env python3
"""
a simple flask app authentication
"""
from flask import Flask, jsonify, request

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
        if request.headers.get('content_type') == "application/json":
            email = request.json.get("email")
            password = request.json.get("password")
        else:
            email = request.form.get('email')
            password = request.form.get('password')
        AUTH.register_user(email=email, password=password)
    except ValueError:
        return jsonify(message="email already registered"), 400

    return jsonify({"email": email, "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
