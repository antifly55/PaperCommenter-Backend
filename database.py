import pymysql
import configparser

properties = configparser.ConfigParser()
properties.read('config.ini')

properties_DB = properties['DB']

HOST = properties_DB['host']
USER = properties_DB['user']
PASSWORD = properties_DB['password']
DB = properties_DB['db']
CHARSET = properties_DB['charset']


conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset=CHARSET)

def get_db():
    db = conn.cursor()
    try:
        yield db
    finally:
        db.close()