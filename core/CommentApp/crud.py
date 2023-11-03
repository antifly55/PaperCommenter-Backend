from datetime import datetime

import hashlib

from pymysql.cursors import Cursor

import core.CommentApp.schema as comment_schema


def make_hashed_identifier(identifier):
    return hashlib.md5(f"-".join(identifier).encode()).hexdigest()

def get_comment_by_hashed_identifier(db: Cursor,
                                     hashed_identifier: str):
    db.execute(f"SELECT * FROM comment WHERE hashed_identifier='{hashed_identifier}'")
    comment = db.fetchone()

    return comment

def get_comment_list(db: Cursor,
                     comment_read: comment_schema.comment_read,
                     paper_id: int):
    
    skip = comment_read.page * comment_read.size
    limit = comment_read.size

    db.execute(f"SELECT * FROM comment WHERE paper_id={paper_id} ORDER BY id desc LIMIT {limit} OFFSET {skip}")
    _comment_list = db.fetchall()

    comment_list = []
    for row_data in _comment_list:
        comment_list.append(row_data)

    total = len(comment_list)

    return total, comment_list

def create_comment(db: Cursor,
                   paper_id: int,
                   user_id: int,
                   username: str,
                   content: str):

    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    hashed_identifier = make_hashed_identifier(identifier=[paper_id, user_id, username, content, now])

    # Auto Increment ID
    comment_info = "(paper_id, user_id, hashed_identifier, username, content, create_datetime, like_count)"
    comment_values = f"({paper_id}, {user_id}, '{hashed_identifier}', '{username}', '{content}', '{now}', 0)"

    db.execute(f"INSERT INTO comment {comment_info} VALUES {comment_values}")
    db.connection.commit()

def update_comment(db: Cursor,
                   comment_id: int,
                   content: str):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    db.execute(f"UPDATE comment SET content='{content}', modify_datetime='{now}' WHERE id={comment_id}")
    db.connection.commit()

def delete_comment(db: Cursor,
                   comment_id: int):
    db.execute(f"DELETE FROM comment WHERE id={comment_id}")
    db.connection.commit()