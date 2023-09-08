from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
import crud.rooms_crud as crud, crud.users_crud as u_crud, models, schemas, dependency as d, auth
from database import engine

models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
    responses={404: {"description": "Not found"}},
)


# Create room
@router.post("/", response_model=schemas.Room, status_code=201)
async def create_room(
        room: schemas.RoomCreate,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_room = crud.get_room_by_room_name(db, room=room)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_room:
        raise HTTPException(status_code=400, detail="Room unavailable!")
    return crud.create_room(db=db, room=room)


# Get all rooms
@router.get("/", response_model=List[schemas.Room])
async def read_rooms(
        skip: int = 0,
        limit: int = 100,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):

    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return rooms


# Get room by id
@router.get("/{room_id}", response_model=schemas.Room)
async def read_room_by_id(
        room_id: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_room = crud.get_room(db, room_id=room_id)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


# Update room
@router.patch("/{room_id}", response_model=schemas.Room)
async def update_room(
        room_id: int,
        room: schemas.RoomUpdate,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_room = crud.get_room(db, room_id=room_id)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return crud.update_room(db=db, room=room, room_id=room_id)


# Delete room
@router.delete("/{room_id}", status_code=204)
async def delete_room(
        room_id: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_room = crud.get_room(db, room_id=room_id)
    db_user = u_crud.get_user_by_username(db=db, username=token_data.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return crud.delete_room(db=db, room_id=room_id)
