from typing import List
from datetime import timedelta, date
from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
import crud.courses_crud as crud,\
       crud.users_crud as u_crud,\
       crud.rooms_crud as r_crud,\
       crud.courses_crud as c_crud,\
       models, schemas, dependency as d, auth
from database import engine
import random

models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    responses={404: {"description": "Not found"}},
)


# Create Courses
@router.post("/", response_model=List[schemas.Course], status_code=201)
async def create_courses(
        course: schemas.CourseCreate,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    course_tag = random.randint(1000, 2147483647)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if course.number_of_sessions > 20 or course.number_of_sessions < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Number of session should be between 1 and 20")
   
    if course.duration_in_minutes > 480 or course.duration_in_minutes < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duration should be between 1 and 480 minutes")

    for session_number in range(1, course.number_of_sessions+1):
        secret_key: str = d.random_string(32)
        crud.create_course(
            db=db,
            session_number=session_number,
            course_tag=course_tag,
            secret_key=secret_key,
            course=course
        )
        course.start_time = course.start_time + timedelta(days=7)

    response_courses = crud.get_course_by_tag(db=db, course_tag=course_tag)

    return response_courses


# Assign lecturer to course
@router.patch("/assign", response_model=List[schemas.Course])
async def assign_lecturer_to_course(
        lecturer: schemas.CourseAssignLecturer, 
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_username = u_crud.get_user_by_username(db=db, username=token_data.username)
    db_user = u_crud.get_user(db=db, user_id=lecturer.user_id)
    db_course = c_crud.get_course_by_tag(db=db, course_tag=lecturer.course_tag)

    if db_username is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.role != "lecturer":
        raise HTTPException(status_code=404, detail="User is not lecturer")
    
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return c_crud.assign_lecturer_course(db=db, lecturer_id = lecturer.user_id,course_tag=lecturer.course_tag)


# Set room on the course
@router.patch("/room", response_model=List[schemas.Course])
async def set_room_on_course(
        room: schemas.CourseSetRoom, 
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)
    db_room = r_crud.get_room(db=db, room_id=room.room_id)
    db_course = c_crud.get_course_by_tag(db=db, course_tag=room.course_tag)

    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return c_crud.set_course_room(db=db, room_id=room.room_id, course_tag=room.course_tag)


# Get all courses by date
@router.get("/date/{date}", response_model=List[schemas.Course])
async def read_courses_by_date(
        date: date = date.today(),
        skip: int = 0,
        limit: int = 100,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):

    courses = crud.get_courses_by_date(db, date=date, skip=skip, limit=limit)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses


# Get all courses
@router.get("/", response_model=List[schemas.Course])
async def read_courses(
        skip: int = 0,
        limit: int = 100,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):

    courses = crud.get_courses(db, skip=skip, limit=limit)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return courses


# Get code of course
@router.get("/code", response_model=schemas.CourseOTP)
async def get_course_one_time_code(
        course_id: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_course: schemas.Course = crud.get_course(db, course_id=course_id)
    one_time_code: str = d.generate_one_time_code(db_course.secret_key)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    response_code = {
        "id": db_course.id,
        "course_name": db_course.course_name,
        "course_tag": db_course.course_tag,
        "session_number": db_course.session_number,
        "start_time": db_course.start_time,
        "duration_in_minutes": db_course.duration_in_minutes,
        "one_time_code": one_time_code
    }
    return response_code


# Get courses by tag
@router.get("/tag/{course_tag}", response_model=List[schemas.Course])
async def read_course_by_tag(
        course_tag: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_courses = crud.get_course_by_tag(db, course_tag=course_tag)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_courses is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_courses


# Get course by id
@router.get("/{course_id}", response_model=schemas.Course)
async def read_course_by_id(
        course_id: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_course = crud.get_course(db, course_id=course_id)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


# Update course
@router.patch("/{course_id}", response_model=schemas.Course)
async def update_course(
        course_id: int,
        course: schemas.CourseUpdate,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_course = crud.get_course(db, course_id=course_id)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.update_course(db=db, course=course, course_id=course_id)


# Delete course
@router.delete("/{course_id}", status_code=204)
async def delete_course(
        course_id: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_course = crud.get_course(db, course_id=course_id)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.delete_course(db=db, course_id=course_id)
