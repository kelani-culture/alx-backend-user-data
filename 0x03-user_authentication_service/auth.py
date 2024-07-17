#!/usr/bin/env python3
from bcrypt import  hashpw, gensalt
"""
handle user authorization
"""


def _hash_password(password: str)-> bytes:
    """
    hash user given password
    """
    salts = gensalt()
    return hashpw(password.encode(), salt=salts)