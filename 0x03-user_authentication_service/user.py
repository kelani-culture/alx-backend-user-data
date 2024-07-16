#!/user/bin/env python3
"""
User model table
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()

class User(Base):
    """
    User model table object oriented
    """
    __tablename__ = 'users'
    id: int = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250), nullable=True)
    reset_token: str = Column(String(250), nullable=True)