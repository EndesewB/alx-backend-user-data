#!/usr/bin/env python3
"""
Module for UserSession model
"""
from sqlalchemy import Column, String, ForeignKey
from models.base import Base


class UserSession(Base):
    """UserSession class inherits from Base
    """
    __tablename__ = 'user_sessions'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    session_id = Column(String(60), nullable=False)

    def __init__(self, *args: list, **kwargs: dict):
        """Initialization of UserSession instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.session_id = kwargs.get('session_id', '')
