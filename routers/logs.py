from typing import List
from datetime import datetime
import pytz
from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session
import crud.logs_crud as crud, models, schemas, auth, crud.courses_crud as c_crud, crud.users_crud as u_crud, dependency as d
from database import engine

models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/logs",
    tags=["logs"],
    responses={404: {"description": "Not found"}},
)


# Get all logs
@router.get("/", response_model=List[schemas.Log])
async def read_logs(
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(d.get_db)
    ):

    logs = crud.get_logs(db, skip=skip, limit=limit)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return logs


# Get logs by course
@router.get("/course/{course_id}", response_model=List[schemas.Log])
async def read_logs(
        course_id:int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(d.get_db)
    ):

    logs = crud.get_logs_by_course_id(db, course_id=course_id, skip=skip, limit=limit)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return logs


# Record log time
@router.get("/record", response_model=schemas.Log)
async def record_log(
        course_id: int,
        one_time_code: str,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student"]),
        db: Session = Depends(d.get_db)
    ):

    db_course = c_crud.get_course(db=db, course_id=course_id)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)
    db_log = crud.get_log_by_course_and_user(db=db, course_id=course_id, user_id=db_user.id)
    verify_code = d.verify_one_time_code(secret=db_course.secret_key, one_time_code=one_time_code)

    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if db_log.log_time is not None:
        raise HTTPException(status_code=404, detail="Log has been recorded")
    if verify_code is not True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One time code is not correct!")
    
    # Waktu Indonesia Barat (UTC+07:00)
    current_time = datetime.now(pytz.timezone('Asia/Jakarta'))

    log = {
        "log_time": current_time
    }
    

    return crud.record_log(db=db, log=log, log_id=db_log.id)


# Approve log time
@router.get("/approve", response_model=schemas.Log)
async def approve_log(
        log_id: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["lecturer"]),
        db: Session = Depends(d.get_db)
    ):

    db_log = crud.get_log(db=db, log_id=log_id)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)


    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if db_log.log_time is None:
        raise HTTPException(status_code=404, detail="Log has not been recorded")
    if db_log.approved_time is not None:
        raise HTTPException(status_code=404, detail="Log has been approved")
   
    # Waktu Indonesia Barat (UTC+07:00)
    current_time = datetime.now(pytz.timezone('Asia/Jakarta'))

    log = {
        "approved_time": current_time,
        "approver_id": db_user.id
    }
    

    return crud.approve_log(db=db, log=log, log_id=db_log.id)


# Get log by id
@router.get("/{log_id}", response_model=schemas.Log)
async def read_log_by_id(
        log_id: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_log = crud.get_log(db, log_id=log_id)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log
