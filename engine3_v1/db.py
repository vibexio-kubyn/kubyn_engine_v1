import pymysql
import os
import logging

logger = logging.getLogger(__name__)

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "kubyn"),
        password=os.getenv("DB_PASSWORD", "Venkat@3929"),
        database=os.getenv("DB_NAME", "kubyn"),
        port=int(os.getenv("DB_PORT", "3306")),
        cursorclass=pymysql.cursors.DictCursor
    )

def fetch_one(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchone()
    except Exception:
        logger.exception("fetch_one failed")
        raise
    finally:
        conn.close()

def fetch_all(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    except Exception:
        logger.exception("fetch_all failed")
        raise
    finally:
        conn.close()

def execute(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
        conn.commit()
    except Exception:
        conn.rollback()
        logger.exception("execute failed, transaction rolled back")
        raise
    finally:
        conn.close()
