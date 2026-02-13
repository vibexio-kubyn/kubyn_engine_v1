import pymysql
import logging
from config import MYSQL_CONFIG

logger = logging.getLogger("engine2-db")


def get_connection():
    """
    Create and return a new DB connection.
    """
    try:
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["database"],
            port=MYSQL_CONFIG.get("port", 3306),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        return conn
    except pymysql.Error as e:
        logger.error(f"DB connection failed: {e}")
        logger.error(f"Host: {MYSQL_CONFIG['host']}, User: {MYSQL_CONFIG['user']}, DB: {MYSQL_CONFIG['database']}")
        raise

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

    except pymysql.Error as e:
        logger.error(f"DB fetch_all failed - SQL Error: {e}")
        logger.error(f"Query: {query}")
        logger.error(f"Params: {params}")
        raise
    except Exception as e:
        logger.exception(f"DB fetch_all failed - Unexpected error: {e}")
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

    except pymysql.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"DB execute failed - SQL Error: {e}")
        logger.error(f"Query: {query}")
        logger.error(f"Params: {params}")
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        logger.exception(f"DB execute failed - Unexpected error: {e}")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
