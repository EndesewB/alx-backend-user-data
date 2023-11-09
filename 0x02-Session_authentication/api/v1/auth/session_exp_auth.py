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
    """_summary_
    """

    def __init__(self):
        """_summary_
        """
        super().__init__()
        # Overload the __init__ method to set session_duration
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id: str = None) -> str:
        """_summary_

        Args:
            user_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        # Overload the create_session method
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id]['created_at'] = datetime.now()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """_summary_

        Args:
            session_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        # Overload the user_id_for_session_id method
        if not super().user_id_for_session_id(session_id):
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']
        if 'created_at' not in session_dict:
            return None
        expiration_time = session_dict['created_at'] + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None
        return session_dict['user_id']
