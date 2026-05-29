from blife.message import make_message_for_blife
from pentaho_repo.logs import get_logs_with_errors

errors_list = get_logs_with_errors()

message = make_message_for_blife(errors_list)

print(message)
