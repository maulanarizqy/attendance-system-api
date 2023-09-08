from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, APIRouter, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
import crud.users_crud as crud, models, schemas, dependency as d
from database import engine
from sqlalchemy.orm import Session
from pydantic import ValidationError
from fastapi.security import SecurityScopes


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "f23ad622f4aab94cb0b04232b98b499817bd52bafd7dfc168fb0634110286c9d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token", 
    # scopes={"student": "Student Role",
    #          "lecturer": "Lecturer Role",
    #          "admin": "Admin role"}
    # scopes={"me": "Read information about the current user.", "items": "Read items."}
)

router = APIRouter(tags=["auth"])


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(secret=password)


def authenticate_user(db: Session, username: str, password: str):
    user: models.User = crud.get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token_and_validate_scopes(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = schemas.TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    for scope in security_scopes.scopes:
        if scope in token_data.scopes:
            return token_data
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not enough permissions",
        headers={"WWW-Authenticate": authenticate_value},
    )


# def validate_scopes(security_scopes: SecurityScopes, token_data: schemas.TokenData = Depends(decode_jwt_token)):
#     scope_valid: bool
    
#     if security_scopes.scopes:
#         authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
#     else:
#         authenticate_value = "Bearer"

#     for scope in security_scopes.scopes:
#         if scope in token_data.scopes:
#             scope_valid = True
#             return scope_valid
        
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Not enough permissions",
#         headers={"WWW-Authenticate": authenticate_value},
#     )

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(d.get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": [user.role]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
