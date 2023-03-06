#!/usr/bin/env python3
"""This file contains the Auth class"""
from typing import List, TypeVar
from flask import Request


class Auth():
    """The Auth Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """The require_auth method"""
        return False

    def authorization_header(self, request=None) -> str:
        """The authorization_header method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """The current_user method"""
        return None
