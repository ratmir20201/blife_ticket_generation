def parse_logs(logs_list: list[tuple[str, str]]):
    errors_list: list[tuple[str, str]] = []

    for log in logs_list:
        log_field, jobname = log

        if "Error connecting to database" in log_field:
            pass
