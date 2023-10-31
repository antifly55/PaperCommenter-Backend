from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from passlib.context import CryptContext

from pymysql.cursors import Cursor

from core.UserApp.schema import User, UserCreate

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24
ACCESS_SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c" # tmp
REFRESH_SECRET_KEY = "4fb2fce7a6b079e1c014390315ed372dd6edb1c5d972cbb74a2904135132c03c" # tmp
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


REFRESH_TOKENS_DB = dict()


def make_tokens(user: User):
    # make access token
    data = {
        "sub": user["username"],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, ACCESS_SECRET_KEY, algorithm=ALGORITHM)

    # make refresh token
    data = {
        "sub": user["username"],
        "exp": datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    }
    refresh_token = jwt.encode(data, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token


def get_user_by_username(db: Cursor, username: str):
    pass

def get_user_by_token(db: Cursor, token: str):
    pass

def create_user(db: Cursor, user_create: UserCreate):
    pass

def delete_user(db: Cursor, user_id: int):
    pass

def update_password(db: Cursor, user_id: int, password: str):
    pass

def get_refresh_token(user_id: int):
    pass

def update_refresh_token(user_id: int, refresh_token: str):
    pass

def delete_refresh_token(user_id: int):
    pass