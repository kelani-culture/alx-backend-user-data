#!/usr/bin/env python3
"""This module implements a function that hashes a
    password by returning its byte string . and a
    function to validate a password encryption"""
import bcrypt


def hash_password(password: str) -> bytes:
    """generates a sort and hash for a password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ did a password match a provided hashed password?
        """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)