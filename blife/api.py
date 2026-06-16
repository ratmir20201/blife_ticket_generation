from datetime import date

import requests

from config import settings
from logger import logger


def add_task_in_blife(description: str):
    blife_url = settings.blife.url
    responsible_id = settings.blife.user_id
    group_id = settings.blife.group_id

    add_method = blife_url + "tasks.task.add.json"

    today = date.today()

    payload = {
        "fields": {
            "TITLE": f"Задача по исправлению ошибок АЦ на {today}",
            "DESCRIPTION": description,
            "RESPONSIBLE_ID": responsible_id,
            "GROUP_ID": group_id,
        }
    }

    try:
        response = requests.post(add_method, json=payload)

        if response.status_code not in (200, 201):
            logger.error(
                "Ошибка при создании задачи в blife. Статус код: %s",
                response.status_code,
            )
    except Exception as e:
        logger.error("Произошла непредвиденная ошибка при работе с API: %s", e)
