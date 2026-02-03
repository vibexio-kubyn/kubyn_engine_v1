# db.py

import pymysql
import logging
from config import MYSQL_CONFIG

logger = logging.getLogger("engine2-db")


def get_connection():
    """
    Create and return a new DB connection.
    """
    return pymysql.connect(
        host=MYSQL_CONFIG["host"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        database=MYSQL_CONFIG["database"],
        port=MYSQL_CONFIG.get("port", 3306),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )

def fetch_all(query, params=None):
    """
    Execute SELECT query and return all rows.
    """
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, params or ())
        return cur.fetchall()

    except Exception:
        logger.exception("DB fetch_all failed")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def execute(query, params=None):
    """
    Execute INSERT / UPDATE / DELETE query.
    Returns number of affected rows.
    """
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, params or ())
        conn.commit()
        return cur.rowcount

    except Exception:
        if conn:
            conn.rollback()
        logger.exception("DB execute failed")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
