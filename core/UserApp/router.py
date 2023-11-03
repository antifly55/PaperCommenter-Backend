from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from database import get_db
from pymysql.cursors import Cursor

import core.UserApp.crud as user_crud
import core.UserApp.schema as user_schema
from core.UserApp.schema import User

router = APIRouter(
    prefix="/api/user",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c" # tmp
ALGORITHM = "HS256"


def get_current_user(access_token: str = Depends(oauth2_scheme),
                     db: Cursor = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        db_user = user_crud.get_user_by_token(db=db, token=access_token)
        if db_user is None:
            raise credentials_exception
        return db_user
    except JWTError:
        raise credentials_exception


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(user_create: user_schema.UserCreate,
                db: Cursor = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db=db, username=user_create.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=user_create)

@router.post("/login", response_model=user_schema.Tokens)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Cursor = Depends(get_db)):

    # check user and password
    db_user = user_crud.get_user_by_username(db=db, username=form_data.username)
    if (not db_user) or (not user_crud.pwd_context.verify(form_data.password, db_user['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token = user_crud.make_tokens(user=db_user)
    user_crud.update_refresh_token(user_id=db_user['id'], refresh_token=refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "username": db_user['username']
    }

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: User = Depends(get_current_user)):
    user_crud.delete_refresh_token(user_id=current_user['id'])

@router.post("/update/password", status_code=status.HTTP_201_CREATED)
def update_password(password_update: user_schema.PasswordUpdate,
                    db: Cursor = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    if not user_crud.pwd_context.verify(password_update.prev_password, current_user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_crud.update_password(db=db, user_id=current_user['id'], password=password_update.new_password1)

@router.post("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(cur_password: str,
                db: Cursor = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    if not user_crud.pwd_context.verify(cur_password, current_user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_crud.delete_user(db=db, user_id=current_user['id'])

@router.post("/update/refresh", response_model=user_schema.Tokens)
def update_refresh_token(refresh_token: str = Depends(oauth2_scheme),
                         db: Cursor = Depends(get_db)):
    db_user = user_crud.get_user_by_token(db=db, token=refresh_token)
    db_refresh_token = user_crud.get_refresh_token(user_id=db_user['id'])
    if refresh_token == db_refresh_token:
        access_token, refresh_token = user_crud.make_tokens(user=db_user)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "username": db_user['username']
        }
    
"""
TODO
- get_profile, update_profile_image, update_profile_message 기능 구현
- REFRESH_TOKEN_DB를 Redis와 연동
- 상태 코드 및 API 명세서 정리
"""