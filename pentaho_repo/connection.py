from contextlib import contextmanager

import psycopg2

from config import settings


@contextmanager
def get_postgres_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=settings.pentaho_repo.name,
            user=settings.pentaho_repo.user,
            password=settings.pentaho_repo.password,
            host=settings.pentaho_repo.host,
            port=settings.pentaho_repo.port,
        )
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()
