#!/usr/bin/env python3
from bcrypt import gensalt, hashpw
from sqlalchemy.orm.exc import NoResultFound

"""
handle user authorization
"""

from db import DB


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str):

        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists.")

        except NoResultFound:
            hashed_password = _hash_password(password)
            self._db.add_user(
                email=email, hashed_password=hashed_password.decode()
            )


def _hash_password(password: str) -> bytes:
    """
    hash user given password
    """
    salts = gensalt()
    return hashpw(password.encode(), salt=salts)
