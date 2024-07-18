#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.create_session(email))
# print(auth.create_session("unknown@email.com"))
token = auth.get_reset_password_token(email)
change_password = auth.update_password(token, 'mypasswordmwag')
print(auth.valid_login('bob@bob.com', 'mypasswordmwag'))