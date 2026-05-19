from parser import parse_logs
from pentaho_repo.logs import get_logs_with_errors

errors_list = get_logs_with_errors()
parse_logs(errors_list)
