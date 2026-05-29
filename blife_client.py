import requests

WEBHOOK_URL = "https://test-blife.baiterek.gov.kz/rest/1/7hj3ccd81cl4gmcq/"


def add_task():
    pass


if __name__ == '__main__':
    response = requests.get(WEBHOOK_URL)
    print(response.json())