from pydantic import BaseModel, validator, EmailStr

class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr

    @validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @validator('password2')
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
    
class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    username: str

class User(BaseModel):
    id: int
    username: str
    email: str

class PasswordUpdate(BaseModel):
    prev_password: str
    new_password: str
    new_password2: str

    @validator('prev_password', 'new_password', 'new_password2')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @validator('new_password2')
    def passwords_match(cls, v, values):
        if 'new_password1' in values and v != values['new_password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
