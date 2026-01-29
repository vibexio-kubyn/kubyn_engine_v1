import pymysql
from config import MYSQL_CONFIG

def get_connection():
   return pymysql.connect(
       host=MYSQL_CONFIG["host"],
       user=MYSQL_CONFIG["user"],
       password=MYSQL_CONFIG["password"],
       database=MYSQL_CONFIG["database"],
       port=MYSQL_CONFIG.get("port", 3306),
       cursorclass=pymysql.cursors.DictCursor
   )

def fetch_all(query, params=None):
   conn = get_connection()
   cur = conn.cursor()
   cur.execute(query, params or ())
   rows = cur.fetchall()
   cur.close()
   conn.close()
   return rows

def execute(query, params=None):
   conn = get_connection()
   cur = conn.cursor()
   cur.execute(query, params or ())
   conn.commit()
   cur.close()
   conn.close()
