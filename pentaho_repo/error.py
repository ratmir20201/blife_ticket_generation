from datetime import date

from pentaho_repo.connection import get_postgres_connection

get_current_day_logs = """
select log_field, jobname from (
	select log_field, logdate, jobname, row_number() over(partition by jobname order by logdate asc) as rn 
	from public.r_job_log 
	where jobname in ('STAGE_DO', 'DWH', 'DI', 'DM_DAILY_MAIN') 
	    and logdate::date = %s
) T
where T.rn = 1;
"""


def get_errors() -> list[tuple[str, str]]:
    with get_postgres_connection() as conn:
        cursor = conn.cursor()

        today = date.today()
        cursor.execute(get_current_day_logs, (today,))
        result = cursor.fetchall()

        return result


if __name__ == "__main__":
    get_errors()
