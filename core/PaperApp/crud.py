from datetime import datetime

from pymysql.cursors import Cursor

from core.PaperApp.schema import PaperCreate

def get_paper_list(db: Cursor,
                   skip: int = 0,
                   limit: int = 10):
    db.execute(f"SELECT * FROM paper ORDER BY id desc LIMIT {limit} OFFSET {skip}")
    _paper_list = db.fetchall()

    paper_list = []
    for row_data in _paper_list:
        paper_list.append(row_data)

    total = len(paper_list)
    return total, paper_list

def get_paper_by_slug(db: Cursor,
                      slug: str):
    db.execute(f"SELECT * FROM paper WHERE slug='{slug}'")
    paper = db.fetchone()

    return paper

def create_paper(db: Cursor,
                 paper_create: PaperCreate,
                 user_id: int):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # Auto Increment ID
    paper_info = "(user_id, slug, title, authors, publish_year, publisher, site_url, paper_url, create_datetime, like_count, comment_count)"
    paper_values = f"({user_id}, '{paper_create.slug}', '{paper_create.title}', '{paper_create.authors}', {paper_create.publish_year}, '{paper_create.publisher}', \
        '{paper_create.site_url}', '{paper_create.paper_url}', '{now}', 0, 0)"

    db.execute(f"INSERT INTO paper {paper_info} VALUES {paper_values}")
    db.connection.commit()

def delete_paper(db: Cursor,
                 paper_id: int):
    db.execute(f"DELETE FROM paper WHERE id={paper_id}")
    db.connection.commit()

def get_paper_like(db: Cursor,
                   paper_id: int,
                   user_id: int):
    db.execute(f"SELECT * FROM paper_like WHERE paper_id={paper_id} and user_id={user_id}")
    paper_like = db.fetchone()

    return paper_like

def like_paper(db: Cursor,
               paper_id: int,
               user_id: int):
    db.execute(f"INSERT INTO paper_like (paper_id, user_id) VALUES ({paper_id}, {user_id})")
    db.connection.commit()

def withdraw_like_paper(db: Cursor,
                        paper_id: int,
                        user_id: int):
    db.execute(f"DELETE FROM paper_like WHERE paper_id={paper_id} and user_id={user_id}")
    db.connection.commit()

def get_paper_rating(db: Cursor,
                     paper_id: int,
                     user_id: int):
    db.execute(f"SELECT * FROM paper_rating WHERE paper_id={paper_id} and user_id={user_id}")
    paper_rating = db.fetchone()

    return paper_rating

def rating_paper(db: Cursor,
                 paper_id: int,
                 user_id: int,
                 rating: int):
    rating = min(max(rating, 1), 5)
    db.execute(f"INSERT INTO paper_rating (paper_id, user_id, rating) VALUES ({paper_id}, {user_id}, {rating})")
    db.connection.commit()

def withdraw_rating_paper(db: Cursor,
                          paper_id: int,
                          user_id: int):
    db.execute(f"DELETE FROM paper_rating WHERE paper_id={paper_id} and user_id={user_id}")
    db.connection.commit()

def update_rating_paper(db: Cursor,
                        paper_id: int,
                        user_id: int,
                        rating: int):
    db.execute(f"UPDATE paper_rating SET rating={rating} WHERE paper_id={paper_id} and user_id={user_id}")
    db.connection.commit()