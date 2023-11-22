import pymysql

from common.parse_env import get_config_variables


HOST, PORT, USER, PASSWORD, DB, CHARSET = get_config_variables('DB',\
    fields=['host', 'port', 'user', 'password', 'db', 'charset'])


# TODO: apply Connection Pooling, separate dictcursor and cursor
conn = pymysql.connect(host=HOST, port=int(PORT), user=USER, password=PASSWORD, db=DB, charset=CHARSET)

def get_db():
    db = conn.cursor(pymysql.cursors.DictCursor)
    try:
        yield db
    finally:
        db.close()