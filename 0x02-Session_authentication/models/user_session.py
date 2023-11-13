#!/usr/bin/env python3
"""
Module for UserSession model
"""
from sqlalchemy import Column, String, ForeignKey
from models.base import Base


class ForeignKey:
    """Class representing a foreign key in a database table.
    """
    
    def __init__(self, table, column, _table_key):
        """Initialize a ForeignKey instance.

        Args:
            table (str): The name of the referenced table.
            column (str): The name of the referenced column.
            _table_key (str): The key used to relate the tables.
        """
        self.table = table
        self.column = column
        self._table_key = _table_key

    def __repr__(self):
        """Return a string representation of the ForeignKey instance.
        """
        return f"ForeignKey(table={self.table}, column={self.column}, _table_key={self._table_key})"

    def _table_key(self):
        """Get the key used to relate the tables.

        Returns:
            str: The key used to relate the tables.
        """
        return self._table_key


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
