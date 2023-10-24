from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from passlib.context import CryptContext

from core.UserApp.schema import UserCreate

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
ACCESS_SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c" # tmp
REFRESH_SECRET_KEY = "4fb2fce7a6b079e1c014390315ed372dd6edb1c5d972cbb74a2904135132c03c" # tmp
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


USERS = [
    {
        'id': 1,
        'username': "antifly55",
        "password": pwd_context.hash("3141592a"),
        'email': "antifly55@naver.com",
        'message': "안녕하세요. ",
        "image_url": "http://mte.com"
    }
]

REFRESH_TOKENS_DB = dict()


def make_tokens(username):
    # make access token
    data = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, ACCESS_SECRET_KEY, algorithm=ALGORITHM)

    # make refresh token
    data = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    refresh_token = jwt.encode(data, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token


def create_user(user_create: UserCreate):

    USERS.append({
        'id': 2,
        'username': user_create.username,
        'password': pwd_context.hash(user_create.password1),
        'email': user_create.email,
        'message': "default",
        'image_url': "default"
    })

def get_existing_user(username: str, email: str):
    for user in USERS:
        if user['username'] == username or user['email'] == email:
            return user

def get_user(username: str):
    for user in USERS:
        if user['username'] == username:
            return user

def verify_refresh_token(refresh_token: str):
    db_refresh_token = REFRESH_TOKENS_DB['username']
    if refresh_token != db_refresh_token:
        return False
    # TODO: if refresh token is not valid -> return False
    return True

def get_refresh_token(username: str):
    if username not in REFRESH_TOKENS_DB.keys():
        return None
    return REFRESH_TOKENS_DB[username]

def delete_refresh_token(username: str):
    del REFRESH_TOKENS_DB[username]

def update_refresh_token(username: str, refresh_token: str):
    REFRESH_TOKENS_DB[username] = refresh_token

def update_password(username: str, password: str):
    for user in USERS:
        if user['username']==username:
            user['password'] = pwd_context.hash(password)
            break

def delete_user(username: str):
    for idx in range(len(USERS)):
        if USERS[idx]['username']==username:
            USERS.pop(idx)
            break