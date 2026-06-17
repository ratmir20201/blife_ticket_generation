from datetime import date

from blife.api import add_file_on_disk, add_task_in_blife, attach_file_to_task
from blife.message import make_message_description_for_blife
from config import LOGS_DIR
from logger import logger
from pentaho_repo.logs import get_logs_with_errors
from utils import make_log_file, clear_log_directory

errors_list = get_logs_with_errors()
today = date.today()

if not errors_list:
    logger.info("Ошибок на %s нету", today)
else:
    message, description = make_message_description_for_blife(errors_list)

    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        filename = "log_" + today.strftime("%Y%m%d") + ".txt"
        file_path = LOGS_DIR / filename

        make_log_file(file_path, message)
        task_id = add_task_in_blife(description)
        file_id = add_file_on_disk(file_path)

        attach_file_to_task(task_id, file_id)
    finally:
        clear_log_directory()
