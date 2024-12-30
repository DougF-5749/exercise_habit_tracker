# The file that sqlalchemy (the orm) uses to create the tables in ther MySQL database
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    ForeignKey,
    )
from lib.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    password = Column(String(500))
    # profile_picture = Column(String(250))
    date_created = Column(DateTime, default=datetime.datetime.now)
    
    # Allows you to see all ExerciseSession recorded by this User
    exercise_sessions = relationship("ExerciseSession", back_populates="recorder")

class ExerciseSession(Base):
    __tablename__ = "exercise_sessions"
    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Allows you to access the User who recorded this session
    recorder = relationship("User", back_populates="exercise_sessions")