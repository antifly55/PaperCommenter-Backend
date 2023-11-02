from datetime import datetime

from pymysql.cursors import Cursor

from core.PaperApp.schema import PaperCreate

def get_paper_list(db: Cursor, skip: int = 0, limit: int = 10):
    db.execute(f"SELECT * FROM paper ORDER BY id desc LIMIT {limit} OFFSET {skip}")
    _paper_list = db.fetchall()

    paper_list = []
    for row_data in _paper_list:
        paper_list.append(row_data)

    total = len(paper_list)
    return total, paper_list

def get_paper_by_slug(db: Cursor, slug: str):
    db.execute(f"SELECT * FROM paper WHERE slug='{slug}'")
    paper = db.fetchone()

    return paper

def create_paper(db: Cursor, paper_create: PaperCreate, user_id: int):

    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # Auto Increment ID
    paper_info = "(user_id, slug, title, authors, publish_year, publisher, site_url, paper_url, create_datetime, like_count, comment_count)"
    paper_values = f"({user_id}, '{paper_create.slug}', '{paper_create.title}', '{paper_create.authors}', {paper_create.publish_year}, '{paper_create.publisher}', \
        '{paper_create.site_url}', '{paper_create.paper_url}', '{now}', 0, 0)"

    db.execute(f"INSERT INTO paper {paper_info} VALUES {paper_values}")
    db.connection.commit()

def delete_paper(db: Cursor, paper_id: int):
    db.execute(f"DELETE FROM paper WHERE id={paper_id}")
    db.connection.commit()