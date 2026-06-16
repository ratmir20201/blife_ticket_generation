from datetime import date

from blife.api import add_task_in_blife
from blife.message import make_message_description_for_blife
from config import LOGS_DIR
from pentaho_repo.logs import get_logs_with_errors
from utils import make_log_file, clear_log_directory

errors_list = get_logs_with_errors()

message, description = make_message_description_for_blife(errors_list)

print(message, description)

try:
    today = date.today()
    filename = "log_" + today.strftime("%Y%m%d") + ".txt"
    file_path = LOGS_DIR / filename

    make_log_file(file_path, message)
    add_task_in_blife(description)
finally:
    clear_log_directory()
