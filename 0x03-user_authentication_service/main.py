#!/usr/bin/env python3
"""
end to end user testing of endpoints 
"""
import requests
import requests.cookies

from auth import Auth

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """register user with password"""
    resp = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password}
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "email": "guillaume@holberton.io",
        "message": "user created",
    }


def log_in_wrong_password(email: str, password: str) -> None:
    """login user with wrong password"""
    resp = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert resp.status_code == 401


def profile_unlogged():
    """get user profile while not logged in"""
    resp = requests.get(f"{BASE_URL}/profile")
    assert resp.status_code == 403


def log_in(email: str, password: str) -> str:
    """login user with credential"""
    resp = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    resp_session = resp.cookies.get("session_id") or ""
    return resp_session


def profile_logged(session_id: str):
    """get user profile while logged in"""
    cookie = {"session_id": session_id}
    resp = requests.get(f"{BASE_URL}/profile", cookies=cookie)
    assert resp.status_code == 200
    assert resp.json() == {"email": EMAIL}


def log_out(session_id: str):
    """log user out of application"""
    cookie = {"session_id": session_id}
    resp = requests.delete(f"{BASE_URL}/sessions", cookies=cookie)
    assert resp.status_code == 200
    assert resp.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """get user password reset token"""
    resp = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert resp.status_code == 200
    assert all(key in resp.json() for key in ["email", "reset_token"])
    return resp.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str):
    """update user password"""
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    resp = requests.put(f"{BASE_URL}/reset_password", data=data)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
