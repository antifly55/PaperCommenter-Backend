from datetime import datetime

from pymysql.cursors import Cursor


def get_comment_by_uuid(db: Cursor, comment_uuid: int):
    db.execute(f"SELECT * FROM comment WHERE uuid={comment_uuid}")
    comment = db.fetchone()

    return comment

def get_comment_list(db: Cursor, paper_id: int, skip: int = 0, limit: int = 10):
    db.execute(f"SELECT * FROM comment WHERE paper_id={paper_id} ORDER BY id desc LIMIT {limit} OFFSET {skip}")
    _comment_list = db.fetchall()

    comment_list = []
    for row_data in _comment_list:
        comment_list.append(row_data)

    total = len(comment_list)

    return total, comment_list

def create_comment(db: Cursor, paper_id: int, content: str):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    db.execute(f"INSERT INTO comment (id, paper_id, user_id, uuid, username, content, create_datetime, like_count) VALUES (1, 1, 1, 'string', 'string', '{now}', 0);")
    db.connection.commit()

def update_comment(db: Cursor, comment_id: int, content: str):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    db.execute(f"UPDATE comment SET content='{content}', modify_datetime='{now}' WHERE id={comment_id}")

def delete_comment(db: Cursor, comment_id: int):
    db.execute(f"DELETE FROM comment WHERE id={comment_id}")
    db.connection.commit()