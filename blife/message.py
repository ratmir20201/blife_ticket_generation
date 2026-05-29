def make_message_for_blife(logs_list: list[tuple[str, str]]):
    message = ""

    for log in logs_list:
        log_field, jobname = log

        if "Error connecting to database" in log_field:
            message += f"Ошибка с подключением к источнику в {jobname}"
        else:
            message += f"Ошибка в {jobname}"

        message += f"\nЛОГ: \n{log_field}\n\n\n"
