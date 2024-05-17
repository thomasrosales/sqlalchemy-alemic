from dataclasses import dataclass
from typing import Dict, Optional

from core.enums import Constants
from sdk.request import APIRequest


@dataclass
class TodoData:
    title: str
    completed: bool
    userId: int
    id: Optional[int] = None

    def to_payload(self) -> Dict:
        return {"title": self.title, "completed": self.completed, "userId": self.userId}


class Todos(APIRequest):

    RESOURCE = "todos"
    MODEL = TodoData

    def __init__(self, token):
        super().__init__(Constants.BASE_URL, self.MODEL, self.RESOURCE, token)
