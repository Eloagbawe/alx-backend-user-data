#!/usr/bin/env python3
"""This file contains the SessionExpAuth class """
from datetime import datetime, timedelta

from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAut(SessionAuth):
    """The SessionExpAuth Class"""

    def __init__(self):
        """initialization"""
        session_duration = os.getenv('SESSION_DURATION')
        try:
            duration = int(session_duration)
        except Exception:
            duration = 0

        # if session_duration:
        #     try:
        #         duration = int(session_duration)
        #     except Exception:
        #         duration = 0
        # else:
        #     duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """create_session"""
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
        """user_id_for_session_id"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if session_dict.get('created_at') is None:
            return None
        created_at = session_dict.get('created_at')
        duration = created_at + timedelta(seconds=self.session_duration)

        if duration < datetime.now():
            return None
        return session_dict.get('user_id')
