from sqlalchemy import DateTime, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    status = Column(String)
    date_created = Column(DateTime(timezone=True), default=func.now())
    date_updated = Column(DateTime(timezone=True), default=None, onupdate=func.now())

    courses = relationship("Course", back_populates="lecturer")
    logs = relationship("Log", back_populates="user")
    participations = relationship("Participant", back_populates="student")
    # approved_logs = relationship("Log", back_populates="approver")


class Course(Base):
    __tablename__ = "Courses"

    id = Column(Integer, primary_key=True, index=True)
    course_tag = Column(Integer)
    course_name = Column(String)
    start_time = Column(DateTime(timezone=True))
    duration_in_minutes = Column(Integer)
    session_number = Column(Integer)
    secret_key = Column(String)
    session_number = Column(Integer)
    secret_key = Column(String)
    status = Column(String)
    date_created = Column(DateTime(timezone=True), default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    lecturer_id = Column(Integer, ForeignKey("Users.id"))
    room_id = Column(Integer, ForeignKey("Rooms.id"))

    lecturer = relationship("User", back_populates="courses")
    room = relationship("Room", back_populates="courses")
    participants = relationship("Participant", back_populates="course")
    logs = relationship("Log", back_populates="course")

class Room(Base):
    __tablename__ = "Rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String)
    building = Column(String)
    floor = Column(String)
    capacity = Column(Integer)
    status = Column(String)
    date_created = Column(DateTime(timezone=True), default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())

    courses = relationship("Course", back_populates="room")

class Participant(Base):
    __tablename__ = "Participants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    course_tag = Column(Integer, ForeignKey("Courses.course_tag"))
    status = Column(String)

    course = relationship("Course", back_populates="participants")
    student = relationship("User", back_populates="participations")

class Log(Base):
    __tablename__ = "Logs"

    id = Column(Integer, primary_key=True, index=True)
    log_time = Column(DateTime(timezone=True))
    approved_time = Column(DateTime(timezone=True))
    approver_id = Column(Integer)
    date_created = Column(DateTime(timezone=True), default=func.now())
    course_id = Column(Integer, ForeignKey("Courses.id"))
    user_id = Column(Integer, ForeignKey("Users.id"))
    # approver_id = Column(Integer, ForeignKey("Users.id"))

    course = relationship("Course", back_populates="logs")
    user = relationship("User", back_populates="logs")
    # approver = relationship("User", back_populates="approved_logs")
