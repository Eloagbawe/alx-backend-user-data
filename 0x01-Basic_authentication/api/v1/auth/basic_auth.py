#!/usr/bin/env python3
"""This file contains the BasicAuth class"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """The Basic Auth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """This method returns the Base64 part of
        the Authorization header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split("Basic ", 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """This method returns the decoded value of a
        Base64 string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            auth_str = base64.b64decode(base64_authorization_header)
            return auth_str.decode('utf-8')
        except Exception:
            return None
