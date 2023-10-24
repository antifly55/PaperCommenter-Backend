from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status


import core.UserApp.crud as user_crud
import core.UserApp.schema as user_schema

router = APIRouter(
    prefix="/api/user",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
ACCESS_SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c" # tmp
REFRESH_SECRET_KEY = "4fb2fce7a6b079e1c014390315ed372dd6edb1c5d972cbb74a2904135132c03c" # tmp
ALGORITHM = "HS256"


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(user_create: user_schema.UserCreate):
    user = user_crud.get_existing_user(username=user_create.username, email=user_create.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(user_create=user_create)

@router.post("/login", response_model=user_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    # check user and password
    user = user_crud.get_user(form_data.username)
    if not user or not user_crud.pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token = user_crud.make_tokens(user.username)
    user_crud.update_refresh_token(user, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "username": user.username
    }

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(access_token: str = Depends(oauth2_scheme)):
    # access token에서 user name get
    username = ''
    user_crud.delete_refresh_token(username=username)

@router.post("/update/password", status_code=status.HTTP_201_CREATED)
def update_password(prev_password: str,
                    new_password: str,
                    access_token: str = Depends(oauth2_scheme)):
    # access_token으로 유저 정보, 이전 패스워드 가져오기
    # prev_password와 이전 패스워드가 같은지 확인
    user_crud.update_password(username=username, password=new_password)

@router.post("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(password: str, access_token: str = Depends(oauth2_scheme)):
    # access token으로 유저정보 가져오기
    # password와 유저정보 패스워드가 같은지 확인
    user_crud.delete_user(username=username)

@router.post("/update/refresh", response_model=user_schema.Token)
def update_refresh_token(refresh_token: str = Depends(oauth2_scheme)):
    # refresh_token에서 유저 정보 알아내기
    db_refresh_token = user_crud.get_refresh_token(username=username)
    if refresh_token == db_refresh_token:
        access_token, refresh_token = user_crud.make_tokens(username=username)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "username": username
        }

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(username=username)
        if user is None:
            raise credentials_exception
        return user
    
"""
TODO
- get_current_user에서 pk만 반환해도 괜찮지 않을까?
- get_profile, update_profile_image, update_profile_message 기능 구현
- 실제 DB 연동
- REFRESH_TOKEN_DB를 Redis와 연동
- 상태 코드 및 API 명세서 정리
"""