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

def get_current_user(access_token: str = Depends(oauth2_scheme),
                     db: Cursor = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="올바르지 않은 인증 정보입니다.",
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

    db_user = user_crud.get_user_by_username(db=db, username=form_data.username)
    if (not db_user) or (not user_crud.pwd_context.verify(form_data.password, db_user['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유저명이나 비밀번호가 올바르지 않습니다.",
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
            detail="비밀번호가 올바르지 않습니다.",
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
            detail="비밀번호가 올바르지 않습니다.",
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

@router.get("/profile", response_model=user_schema.Profile)
def get_profile(username: str,
                db: Cursor = Depends(get_db)):
    
    profile = user_crud.get_profile(db=db, username=username)
    if not profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    
    return profile

@router.put("/update/profile-image", status_code=status.HTTP_204_NO_CONTENT)
def update_profile_image(image_url: str,
                         db: Cursor = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    
    user_crud.update_profile_image(db=db, user_id=current_user['id'], image_url=image_url)

@router.put("/update/profile-message", status_code=status.HTTP_204_NO_CONTENT)
def update_profile_message(message: str,
                           db: Cursor = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    
    user_crud.update_profile_message(db=db, user_id=current_user['id'], message=message)

"""
TODO
- REFRESH_TOKEN_DB를 Redis와 연동
- 상태 코드 및 API 명세서 정리
"""