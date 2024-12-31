from typing import TypedDict

class TypedTask(TypedDict):
    id: int
    image_url: str
    title: str
    topic: str
    task: str
    answer: str
    tags: str
