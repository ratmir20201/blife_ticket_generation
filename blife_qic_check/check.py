from datetime import date

import vertica_python

from config import settings
from logger import logger

QIC_BLIFE_SQL = """
SELECT MAX(PERIOD) FROM STAGE_DO.BLIFE_SMART_PROCESS
WHERE PACKAGE_ID = (SELECT MAX(PACKAGE_ID) FROM STAGE_DO.BLIFE_SMART_PROCESS)
	AND FORM_NAME = 'QIC освоение';
"""


get_blife_smart_process_today_errors = """
select log_field, transname from (
  select log_field, logdate, transname, row_number() over(partition by transname order by logdate asc) as rn 
  from public.r_trans_log
  where transname = 'BLIFE_SMART_PROCESS'
      and logdate::date = %s
      and log_field ilike '%% ERROR %%'
) T
where T.rn = 1;
"""


def check_blife_smart_process_is_good() -> bool:
    today = date.today()
    logger.info("Запускается запрос на проверку BLIFE_SMART_PROCESS за %s", today)

    with vertica_python.connect(**settings.db.conn_info) as conn:
        cursor = conn.cursor()
        cursor.execute(get_blife_smart_process_today_errors)

        result = cursor.fetchone()

        if result is None:
            return True
        return False


def check_blife_qic_data():
    with vertica_python.connect(**settings.db.conn_info) as conn:
        cursor = conn.cursor()
        cursor.execute(QIC_BLIFE_SQL)

        result = cursor.fetchone()
