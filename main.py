from blife.api import add_task_in_blife
from blife.message import make_message_description_for_blife
from pentaho_repo.logs import get_logs_with_errors

errors_list = get_logs_with_errors()

message, description = make_message_description_for_blife(errors_list)

print(message)

add_task_in_blife(description)
