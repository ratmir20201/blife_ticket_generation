from pentaho_repo.connection import get_postgres_connection

"""
select log_field from public.r_job_log 
where jobname = 'STAGE_DO' and logdate::date = '2026-05-15';
"""


def get_error():
    with get_postgres_connection() as conn:
        cursor = conn.cursor()
        cursor.execute()
