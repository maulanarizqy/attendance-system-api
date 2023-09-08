from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, validator


class LogBase(BaseModel):
    course_id: int
    user_id: int


class LogCreate(LogBase):
    pass


class Log(LogBase):
    id: int
    log_time: Union[datetime, None] = None
    approved_time: Union[datetime, None] = None
    approver_id: Union[int, None] = None
    # date_created: datetime

    class Config:
        orm_mode = True


class LogRecord(BaseModel):
    log_time: datetime


class LogApprove(BaseModel):
    approved_time: datetime
    approver_id: int


class RoomBase(BaseModel):
    building: str
    floor: str
    room_name: str
    capacity: int


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int
    status: Union[str, None] = None
    # date_created: datetime
    # date_updated: Union[datetime, None] = None
    # courses: List[Course] = []

    class Config:
        orm_mode = True


class RoomUpdate(BaseModel):
    building: Union[str, None] = None
    floor: Union[str, None] = None
    room_name: Union[str, None] = None
    capacity: Union[int, None] = None
    status: Union[str, None] = None


class RoomSearch(BaseModel):
    building: Union[str, None] = None
    floor: Union[str, None] = None
    room_name: Union[str, None] = None


class UserBase(BaseModel):
    name: str
    username: str
    role: str    


class UserCreate(UserBase):
    password: str

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v
    
    @validator('role')
    def role_validation(cls, v):
        if v == "student":
            return v
        if v == "lecturer":
            return v
        if v == "admin":
            return v
        raise ValueError("Role is not defined")


class User(UserBase):
    id: int    
    status: Union[str, None]
    # date_created: datetime
    # date_updated: Union[datetime, None] = None
    # courses: List[Course] = []
    # logs: List[Log] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Union[str, None] = None
    username: Union[str, None] = None
    role: Union[str, None] = None
    password: Union[str, None] = None

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v
    
    @validator('role')
    def role_validation(cls, v):
        if v == "student":
            return v
        if v == "lecturer":
            return v
        if v == "admin":
            return v
        raise ValueError("Role is not defined")
    

class ParticipantBase(BaseModel):
    user_id: int
    course_tag: int


class ParticipantCreate(ParticipantBase):
    pass


class Participant(ParticipantBase):
    id: int
    status: str
    student: Union[User, None] = None

    class Config:
        orm_mode = True


class ParticipantUpdate(BaseModel):
    course_id: Union[int, None] = None
    user_id: Union[int, None] = None
    status: Union[str, None] = None
    

class CourseBase(BaseModel):
    course_name: str
    start_time: datetime
    duration_in_minutes: int


class CourseCreate(CourseBase):
    number_of_sessions: int


class Course(CourseBase):
    id: int
    course_tag: int
    session_number: int
    status: Union[str, None] = None
    # date_created: datetime
    # date_updated: Union[datetime, None] = None
    lecturer: Union[User, None] = None
    room: Union[Room, None] = None
    # participants: List[Participant] = []
    # logs: List[Log] = []

    class Config:
        orm_mode = True


class CourseUpdate(BaseModel):
    course_name: Union[str, None] = None
    start_time: Union[datetime, None] = None
    duration_in_minutes: Union[int, None] = None


class CourseOTP(BaseModel):
    id: int
    course_name: str
    course_tag: int
    session_number: int
    start_time: datetime
    duration_in_minutes: int
    one_time_code: int


class CourseAssignLecturer(BaseModel):
    user_id: int
    course_tag: int


class CourseSetRoom(BaseModel):
    room_id: int
    course_tag: int
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


