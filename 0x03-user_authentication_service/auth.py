#!/usr/bin/env python3
import uuid
from typing import Optional

from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy.orm.exc import NoResultFound

from user import User

"""
handle user authorization into application
"""

from db import DB


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> None:
        """
        register user into the application
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists.")

        except NoResultFound:
            hashed_password = _hash_password(password)
            self._db.add_user(
                email=email, hashed_password=hashed_password.decode()
            )

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate user credential into the application
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if not user:
            return False
        return checkpw(password.encode(), user.hashed_password.encode())

    def create_session(self, email: str) -> Optional[str]:
        """
        create user session token
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = __generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            return
        if not user:
            return
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        find users by the provided session id
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        reset user session id to None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return
        return


def _hash_password(password: str) -> bytes:
    """
    hash user given password
    """
    salts = gensalt()
    return hashpw(password.encode(), salt=salts)


def __generate_uuid() -> str:
    """
    generate a uuid value
    """
    return str(uuid.uuid4())
