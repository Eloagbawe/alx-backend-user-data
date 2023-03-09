#!/usr/bin/env python3
"""This file contains the SessionExpAuth class """
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAut(SessionAuth):
    """The SessionExpAuth Class
    This class adds an expiration date to a Session ID
    """

    def __init__(self):
        """initialization of the SessionExpAuth Class"""
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """create_session
        Create a Session ID for a user_id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user_id_for_session_id
        Returns a user ID based on a session ID
        """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if 'created_at' not in session_dict.keys():
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        duration = created_at + timedelta(seconds=self.session_duration)

        if duration < datetime.now():
            return None
        return session_dict.get('user_id')
