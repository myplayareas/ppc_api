from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime

from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default='')
    username = Column(String, default='')
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    image = Column(String, default='')
    is_active = Column(Boolean, default=True)
    repositories = relationship("Repository", back_populates="owner")

class Repository(Base):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    analysis_date = Column(DateTime, default=datetime.datetime.utcnow)
    analysed = Column(Integer, default=1)
    owner_id = Column(Integer, ForeignKey("users.id") )
    owner = relationship("User", back_populates="repositories")
