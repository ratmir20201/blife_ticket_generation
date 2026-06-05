def make_message_description_for_blife(logs_list: list[tuple[str, str]]):
    message = ""
    description = ""

    for log in logs_list:
        log_field, jobname = log

        if "Error connecting to database" in log_field:
            error = f"Ошибка с подключением к источнику в {jobname}"
            message += error
            description += error
        else:
            error = f"Ошибка в {jobname}"
            message += error
            description += error

        message += f"\nЛОГ: \n{log_field}\n\n\n"

    return message, description
