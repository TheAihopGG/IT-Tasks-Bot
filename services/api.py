import requests
import json
from data.settings import API_URL
from services.typed_dicts import TypedTask

def get_task(id: int) -> (TypedTask | None):
    """Requests to api and gets task"""
    response = requests.get(f"{API_URL}get_task/?id={id}")

    if response.ok:
        return json.loads(response.content)

    else:
        return None


def get_tasks_ids() -> (list[int] | None):
    """Requests to api and gets ids"""
    response = requests.get(f"{API_URL}get_tasks_ids/")

    if response.ok:
        return json.loads(response.content)["ids"]
    
    else:
        return None
