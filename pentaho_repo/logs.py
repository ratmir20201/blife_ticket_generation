from datetime import date

from logger import logger
from pentaho_repo.connection import get_postgres_connection

get_current_day_job_logs = """
select log_field, jobname from (
  select log_field, logdate, jobname, row_number() over(partition by jobname order by logdate asc) as rn 
  from public.r_job_log 
  where jobname in ('STAGE_DO', 'HUBS', 'LINKS', 'SATELLITES', 'DI', 'DM_DAILY_MAIN', 'HR_REPORTS', 'BLIFE_MAIN', 'FRP_1C_WRAPPER_INNER', 'BLIFE_DI_ALL') 
      and logdate::date = %s
      and log_field ilike '%%ERROR%%'
) T
where T.rn = 1;
"""


get_current_day_transform_logs = """
select log_field, transname from (
  select log_field, logdate, transname, row_number() over(partition by transname order by logdate asc) as rn 
  from public.r_trans_log
  where transname in ('DI_EXCHANGE_RATES', 'AS_HUBS', 'AS_LINKS', 'AS_SATELLITES', 'DM_LOAN_PORTFOLIO_15', 'DM_LOAN_PORTFOLIO_18', 'DO_CONNECTION_CHECK', 'FRP_1C_ANALYSIS_MAP'
    'GetToniaData', 'TRANS_LOG') 
      and logdate::date = %s
      and log_field ilike '%%ERROR%%'
) T
where T.rn = 1;
"""

blife_main_sur_logs = """
select log_field, jobname
from public.r_job_log 
where jobname = 'BLIFE_MAIN_SUR'
    and logdate >= date_trunc('day', %s) - interval '1 day' + interval '7 hour'
    and logdate < date_trunc('day', %s) + interval '7 hour' + interval '25 minutes'
    and log_field ilike '%%ERROR%%'
"""


def get_logs_with_errors() -> list[tuple[str, str]]:
    today = date.today()
    logger.info("Запускаются запросы на проверку ошибок за %s", today)

    with get_postgres_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(get_current_day_job_logs, (today,))
        result_1 = cursor.fetchall()

        cursor.execute(get_current_day_transform_logs, (today,))
        result_2 = cursor.fetchall()

        cursor.execute(blife_main_sur_logs, (today, today))
        result_3 = cursor.fetchall()

        general_result = result_1 + result_2 + result_3

        return general_result
