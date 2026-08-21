import vertica_python

from config import settings

QIC_BLIFE_SQL = """
SELECT MAX(PERIOD) FROM STAGE_DO.BLIFE_SMART_PROCESS
WHERE PACKAGE_ID = (SELECT MAX(PACKAGE_ID) FROM STAGE_DO.BLIFE_SMART_PROCESS)
	AND FORM_NAME = 'QIC освоение';
"""


def get_max_blife_qic_period():
    with vertica_python.connect(**settings.db.conn_info) as conn:
        cursor = conn.cursor()
        cursor.execute(QIC_BLIFE_SQL)

        result = cursor.fetchone()
        max_period = result[0]

        return max_period


if __name__ == "__main__":
    print(get_max_blife_qic_period())
