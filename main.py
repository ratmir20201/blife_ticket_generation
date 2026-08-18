from datetime import date, timedelta

from blife.api import add_task_in_blife, add_file_on_disk, attach_file_to_task
from blife.message import make_message_description_for_blife
from blife_qic_check.check import (
    get_max_blife_qic_period,
)
from config import LOGS_DIR, settings
from logger import logger
from pentaho_repo.logs import check_blife_smart_process_is_good, get_logs_with_errors
from utils import make_log_file, clear_log_directory

today = date.today()
yesterday = today - timedelta(days=1)


# Алгоритм для просмотра ошибок в целом всего регламента
errors_list = get_logs_with_errors()

if not errors_list:
    logger.info("Ошибок на %s нету", today)
else:
    logger.info("Найдены ошибки, создается задача в blife")
    message, description = make_message_description_for_blife(errors_list)

    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        filename = "log_" + today.strftime("%Y%m%d") + ".txt"
        file_path = LOGS_DIR / filename

        make_log_file(file_path, message)

        task_id = add_task_in_blife(
            title=f"Задача по исправлению ошибок в АЦ на {today}",
            description=description,
            responsible_id=settings.blife.a2_responsible_id,
        )

        file_id = add_file_on_disk(file_path)

        attach_file_to_task(task_id, file_id)
    finally:
        clear_log_directory()

# Алгоритм для просмотра недогружености в blife QIC
if today.weekday() == 4:
    if check_blife_smart_process_is_good():
        max_period = get_max_blife_qic_period()

        if max_period != yesterday:
            add_task_in_blife(
                title=f"Не загружены данные за {today} — QIC",
                description=f"""
                Добрый день!
                 
                Автоматизированной проверкой выявлено отсутствие данных от QIC (Освоение) за отчетную дату {yesterday}.
                """,
                responsible_id=settings.blife.holding_responsible_id,
            )
