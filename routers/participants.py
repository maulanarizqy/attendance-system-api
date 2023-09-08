from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
import models, schemas,\
       crud.participants_crud as crud,\
       crud.courses_crud as c_crud,\
       crud.users_crud as u_crud,\
       crud.logs_crud as l_crud,\
       dependency as d,\
       auth
from database import engine
from pydantic import parse_obj_as


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/participants",
    tags=["participants"],
    responses={404: {"description": "Not found"}},
)


# Create participant
@router.post("/", response_model=List[schemas.Participant], status_code=201)
async def create_participant(
        participants: List[schemas.ParticipantCreate],
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    participant_list = list()
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for participant in participants:
        db_courses = c_crud.get_course_by_tag(db, course_tag=participant.course_tag)
        db_user = u_crud.get_user(db, user_id=participant.user_id)
        db_participant = crud.get_participants_by_user_id(db=db, user_id=participant.user_id)

        if not db_courses:
            raise HTTPException(status_code=400, detail="Course unavailable!")
        if db_user is None:
            raise HTTPException(status_code=400, detail="User unavailable!")
        if db_user.role is not "student":
            raise HTTPException(status_code=400, detail="User is not student!")
        if db_participant:
            raise HTTPException(status_code=400, detail="User is already participant!")
        

        for course in db_courses:
            log = schemas.LogCreate (
                course_id = course.id,
                user_id = participant.user_id
            )
            l_crud.create_log(db=db, log=log)
    
        create_participant = crud.create_participant(db=db, participant=participant)
        participant_list.append(create_participant)
    
    participant_list_response = parse_obj_as(List[schemas.Participant], participant_list)
    return participant_list_response


# Get all participants
@router.get("/", response_model=List[schemas.Participant])
async def read_participants(
        skip: int = 0,
        limit: int = 100,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):

    participants = crud.get_participants(db, skip=skip, limit=limit)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return participants


# # Get participants by course id
# @router.get("/course/{course_id}", response_model=List[schemas.Participant])
# async def read_participants_by_course(course_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(d.get_db)):
#     participants = crud.get_participants_by_course_id(db=db ,course_id=course_id, skip=skip, limit=limit)
#     return participants


# Get participant by id
@router.get("/{participant_id}", response_model=schemas.Participant)
async def read_participant_by_id(
        participant_id: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_participant = crud.get_participant(db, participant_id=participant_id)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    return db_participant


# Update participant
@router.patch("/{participant_id}", response_model=schemas.Participant)
async def update_participant(
        participant_id: int,
        participant: schemas.ParticipantUpdate,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_participant = crud.get_participant(db, participant_id=participant_id)
    db_course = c_crud.get_course(db, course_id=participant.course_id)
    db_user = u_crud.get_user(db, user_id=participant.user_id)
    db_username = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_username is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    if db_course is None:
        raise HTTPException(status_code=400, detail="Course unavailable!")
    if db_user is None:
        raise HTTPException(status_code=400, detail="User unavailable!")
    
    return crud.update_participant(db=db, participant=participant, participant_id=participant_id)


# Delete participant
@router.delete("/{participant_id}", status_code=204)
async def delete_participant(
        participant_id: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_participant = crud.get_participant(db, participant_id=participant_id)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    return crud.delete_participant(db=db, participant_id=participant_id)
