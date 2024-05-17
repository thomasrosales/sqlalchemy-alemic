from dataclasses import dataclass
from typing import Optional, Dict

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

    resource = "todos"
    model = TodoData

    def __init__(self, token):
        super().__init__(self.model, self.resource, token)
