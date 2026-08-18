import requests

from config import settings
from logger import logger


def add_task_in_blife(title: str, description: str, responsible_id: int):
    blife_url = settings.blife.url
    group_id = settings.blife.group_id

    add_method = blife_url + "tasks.task.add.json"

    payload = {
        "fields": {
            "TITLE": title,
            "DESCRIPTION": description,
            "RESPONSIBLE_ID": responsible_id,
            "GROUP_ID": group_id,
        }
    }

    try:
        response = requests.post(add_method, json=payload)

        json_data = response.json()
        result = json_data.get("result")
        task = result.get("task")
        task_id = task.get("id")

        if response.status_code not in (200, 201):
            logger.error(
                "Ошибка при создании задачи в blife. Статус код: %s",
                response.status_code,
            )

        return task_id
    except Exception as e:
        logger.error("Произошла непредвиденная ошибка при работе с API: %s", e)
        return None


def add_file_on_disk(file_path: str):
    blife_url = settings.blife.url
    upload_file_method = blife_url + "disk.folder.uploadfile.json"

    data = {"id": str(settings.blife.folder_id)}

    try:
        with open(file_path, "rb") as f:
            files = {"file": f}

            response = requests.post(
                upload_file_method,
                data=data,
                files=files,
            )

            if response.status_code not in (200, 201):
                logger.error(
                    "Ошибка при создании загрузки файла на диск blife. Статус код: %s",
                    response.status_code,
                )

            json_data = response.json()
            result = json_data.get("result")
            upload_url = result.get("uploadUrl")

            file_id = add_file_by_upload_url(upload_url, file_path)
            return file_id
    except Exception as e:
        logger.error("Произошла непредвиденная ошибка при работе с API: %s", e)
        return None


def add_file_by_upload_url(upload_url: str, file_path: str):
    with open(file_path, "rb") as f:
        files = {"file": f}

        response = requests.post(upload_url, files=files)

        json_data = response.json()
        result = json_data.get("result")
        file_id = result.get("ID")

        return file_id


def attach_file_to_task(task_id: int, file_id: int):
    blife_url = settings.blife.url

    attach_method = blife_url + "tasks.task.files.attach.json"
    payload = {"taskId": task_id, "fileId": file_id}
    try:
        response = requests.post(attach_method, json=payload)

        if response.status_code not in (200, 201):
            logger.error(
                "Ошибка при прикреплении файла к задаче blife. Статус код: %s",
                response.status_code,
            )
    except Exception as e:
        logger.error("Произошла непредвиденная ошибка при работе с API: %s", e)
