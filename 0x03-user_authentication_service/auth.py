#!/usr/bin/env python3
"""
This contains the Auth Class
"""
from db import DB
from user import User
# from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.exc import NoResultFound

import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """The hash_password function"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """The register_user method"""

        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed_password = _hash_password(password).decode('utf-8')
            newUser = self._db.add_user(email=email,
                                        hashed_password=hashed_password)
            return newUser

    def valid_login(self, email: str, password: str) -> bool:
        """The valid_login function"""
        try:
            user = self._db.find_user_by(email=email)
            password_bytes = password.encode('utf-8')
            hashed_password_bytes = user.hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_password_bytes)
        except Exception:
            return False

    def _generate_uuid(self) -> str:
        """The Generate UUID function"""
        return str(uuid.uuid4())
