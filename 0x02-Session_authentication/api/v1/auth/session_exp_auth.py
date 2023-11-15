#!/usr/bin/env python3
"""
Module for authentication using Session exp auth
"""

from datetime import datetime, timedelta
from os import getenv

from .session_auth import SessionAuth
from models.user import User
from uuid import uuid4


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class inherits from SessionAuth
    """

    def __init__(self):
        """Initialize SessionExpAuth instance
        """
        super().__init__()
        # Overload the __init__ method to set session_duration
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id: str = None) -> str:
        """Create a new UserSession with session expiration and return the session ID
        """
        # Overload the create_session method
        session_id = super().create_session(user_id)
        if session_id:
            # Ensure user_id_by_session_id[session_id] is a dictionary
            self.user_id_by_session_id.setdefault(session_id, {})['created_at'] = datetime.now()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return the User ID based on session ID with session expiration
        """
        # Overload the user_id_for_session_id method
        if not super().user_id_for_session_id(session_id):
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dict['user_id']
        if 'created_at' not in session_dict:
            return None
        expiration_time = session_dict['created_at'] + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None
        return session_dict['user_id']
