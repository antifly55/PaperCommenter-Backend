import pymysql
import configparser

properties = configparser.ConfigParser()
properties.read('config.ini')

properties_DB = properties['DB']

HOST = properties_DB['host']
PORT = int(properties_DB['port'])
USER = properties_DB['user']
PASSWORD = properties_DB['password']
DB = properties_DB['db']
CHARSET = properties_DB['charset']


# TODO: apply Connection Pooling, separate dictcursor and cursor
conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB, charset=CHARSET)

def get_db():
    db = conn.cursor(pymysql.cursors.DictCursor)
    try:
        yield db
    finally:
        db.close()