from parser import parse_logs
from pentaho_repo.error import get_logs_with_errors

errors_list = get_logs_with_errors()
parse_logs(errors_list)
