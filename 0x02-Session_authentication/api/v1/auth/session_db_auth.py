#!/usr/bin/env python3
"""
Module for SessionDBAuth class
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv
from uuid import uuid4


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class inherits from SessionAuth
    """
    def __init__(self):
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """Create a new UserSession with session expiration and return the session ID
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        self.user_id_by_session_id[session_id]['created_at'] = datetime.now()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the User ID based on session ID with session expiration
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict['user_id']

        if 'created_at' not in session_dict:
            return None

        expiration_time = session_dict['created_at'] + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return session_dict['user_id']
