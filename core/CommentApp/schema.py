import datetime

from pydantic import BaseModel

class Comment(BaseModel):
    username: str
    content: str

    create_datetime: datetime.datetime
    modify_datetime: datetime.datetime | None = None

    like_count: int

class CommentList(BaseModel):
    total: int = 0
    comment_list: list[Comment] = []