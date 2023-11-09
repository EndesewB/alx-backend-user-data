#!/usr/bin/env python3
"""
Module for SessionDBAuth class
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from uuid import uuid4


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class inherits from SessionExpAuth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id=None):
        """Create a new UserSession and return the session ID
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        new_user_session = UserSession(user_id=user_id, session_id=session_id)
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': new_user_session.created_at
        }

        new_user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the User ID based on session ID from the database
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

    def destroy_session(self, request=None):
        """Destroy the UserSession based on the Session ID from the request cookie
        """
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False

        user_session = UserSession.get(session_cookie)
        if not user_session:
            return False

        user_session.delete()
        del self.user_id_by_session_id[session_cookie]
        return True
