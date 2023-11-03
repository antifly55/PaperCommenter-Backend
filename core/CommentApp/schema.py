import datetime

from pydantic import BaseModel

class Comment(BaseModel):
    username: str
    content: str
    hashed_identifier: str

    create_datetime: datetime.datetime
    modify_datetime: datetime.datetime | None = None

    like_count: int

class CommentList(BaseModel):
    total: int = 0
    comment_list: list[Comment] = []

class CommentRead(BaseModel):
    slug: str
    page: int = 0
    size: int = 10

class CommentCreate(BaseModel):
    slug: str
    content: str

class CommentUpdate(BaseModel):
    prev_hashed_identifier: str
    new_content: str