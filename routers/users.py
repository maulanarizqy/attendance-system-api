from typing import List
from fastapi import Depends, APIRouter, HTTPException, status, Security
from sqlalchemy.orm import Session
import crud.users_crud as crud, models, schemas, dependency as d, auth
from database import engine


models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


async def get_current_user(
        token_data: schemas.TokenData = Depends(auth.decode_jwt_token_and_validate_scopes),
        db: Session = Depends(d.get_db)
    ):
    
    user: models.User = crud.get_user_by_username(db=db, username=token_data.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # if scope_validation is not True:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Not enough permissions",
    #     )
    return user


async def get_current_active_user(current_user: schemas.User = Security(get_current_user, scopes=["student", "lecturer", "admin"])):
    if current_user.status != "active":
        raise HTTPException(status_code=400, detail="User is " + current_user.status)
    return current_user


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
        user: schemas.UserCreate,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_user = crud.get_user_by_username(db=db, username=user.username)
    db_username = crud.get_user_by_username(db=db, username=token_data.username)

    if db_username is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username unavailable!")
    
    hashed_password = auth.get_password_hash(user.password)
    user.password = hashed_password
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
async def read_users(
        scope_validation: bool = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        skip: int = 0, limit: int = 100,
        db: Session = Depends(d.get_db)
    ):
    users = crud.get_users(db, skip=skip, limit=limit)
    if not scope_validation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return users


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.get("/@{username}", response_model=schemas.User)
async def read_user_by_username(
        username: str,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):
    
    db_user = crud.get_user_by_username(db, username=username)
    db_username = crud.get_user_by_username(db=db, username=token_data.username)

    if db_username is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
        user_id: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["student", "lecturer", "admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_user = crud.get_user(db, user_id=user_id)
    db_username = crud.get_user_by_username(db=db, username=token_data.username)

    if db_username is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.patch("/{user_id}", response_model=schemas.User)
async def update_user(
        user_id: int,
        user: schemas.UserUpdate,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_user = crud.get_user(db, user_id=user_id)
    db_username = crud.get_user_by_username(db=db, username=user.username)
    db_user_token = crud.get_user_by_username(db=db, username=token_data.username)

    if db_user_token is None:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username unavailable!")

    if user.password is not None:
        hashed_password = auth.get_password_hash(user.password)
        user.password = hashed_password

    return crud.update_user(db=db, user=user, user_id=user_id)


@router.delete("/{user_id}", status_code=204,)
async def delete_user(
        user_id: int,
        token_data: schemas.TokenData = Security(auth.decode_jwt_token_and_validate_scopes, scopes=["admin"]),
        db: Session = Depends(d.get_db)
    ):

    db_user = crud.get_user(db, user_id=user_id)
    db_username = crud.get_user_by_username(db=db, username=token_data.username)

    if db_username is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.delete_user(db=db, user_id=user_id)
