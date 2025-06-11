from psycopg2 import pool
import logging

logger = logging.getLogger(__name__)
DB_POOL = None

def init_db_pool(config: dict):
    global DB_POOL
    DB_POOL = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host=config.get("DB_HOST", "localhost"),
        port=config.get("DB_PORT", "5432"),
        dbname=config.get("DB_NAME"),
        user=config.get("DB_USER"),
        password=config.get("DB_PASSWORD")
    )
    logger.info("Database connection pool created.")

def close_db_pool():
    global DB_POOL
    if DB_POOL:
        DB_POOL.closeall()
        logger.info("Database connections closed.")

def run_query(query: str):
    conn = DB_POOL.getconn()
    try:
        cur = conn.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description] if cur.description else []
        rows = cur.fetchall() if cur.description else []
        cur.close()
        return columns, rows
    finally:
        DB_POOL.putconn(conn)