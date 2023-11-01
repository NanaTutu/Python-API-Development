from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = 'posts'
    id=Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable= False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    # username = Column(String(256), unique=True, index=True, nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    password = Column(String(256), nullable=False)
    # is_active = Column(Boolean(), default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    