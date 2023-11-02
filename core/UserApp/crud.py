from datetime import timedelta, datetime

from jose import jwt, JWTError

from passlib.context import CryptContext

from pymysql.cursors import Cursor

from core.UserApp.schema import User, UserCreate

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c" # tmp
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


REFRESH_TOKENS_DB = dict()


def make_tokens(user: User):
    # make access token
    data = {
        "username": user["username"],
        "email": user["email"],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    # make refresh token
    data = {
        "username": user["username"],
        "email": user["email"],
        "exp": datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    }
    refresh_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token


def get_user_by_username(db: Cursor, username: str):
    db.execute(f"SELECT * FROM user WHERE username={username}")
    user = db.fetchone()

    return user

def get_user_by_token(db: Cursor, token: str):
    user_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return get_user_by_username(db=db, username=user_info['username'])

def create_user(db: Cursor, user_create: UserCreate):
    db.execute(f"INSERT INTO user (id, username, hashed_password, email, message, image_url) VALUES (1, {user_create.username}, {pwd_context.hash(user_create.password1)}, {user_create.email}, 'default', 'default');")
    db.connection.commit()

def delete_user(db: Cursor, user_id: int):
    db.execute(f"DELETE FROM user WHERE id={user_id}")
    db.connection.commit()

def update_password(db: Cursor, user_id: int, password: str):
    db.execute(f"UPDATE user SET hashed_password='{pwd_context.hash(password)}' WHERE id={user_id}")
    db.connection.commit()

def get_refresh_token(user_id: int):
    if user_id not in REFRESH_TOKENS_DB.keys():
        return None
    return REFRESH_TOKENS_DB[user_id]

def update_refresh_token(user_id: int, refresh_token: str):
    REFRESH_TOKENS_DB[user_id] = refresh_token

def delete_refresh_token(user_id: int):
    if user_id in REFRESH_TOKENS_DB.keys():
        del REFRESH_TOKENS_DB[user_id]