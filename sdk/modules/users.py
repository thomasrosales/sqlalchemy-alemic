import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from core.enums import Constants
from sdk.modules.decorators import insert_api_module_attribute
from sdk.modules.posts import Posts, PostsReadOnly
from sdk.request import APIRequest

jobs = ["actress", "nurse", "butcher", "scientist", "plumber"]


def user_data_factory(name, job, id, createdAt):
    name = name.split(" ")
    if len(name) > 1:
        first_name, *_ = name
        *_, last_name = name
    else:
        first_name, last_name = name[0]
    email = f"{name}-{id}@fake.com"
    avatar = f"https://{name}.png"
    return UserData(
        first_name=first_name, last_name=last_name, email=email, id=id, avatar=avatar
    )


@dataclass
class CompanyData:
    name: str
    catchPhrase: str
    bs: str


@dataclass
class AddressData:
    street: str
    suite: str
    city: str
    zipcode: str
    geo: str
    id: Optional[int] = None


@dataclass
class UserData:
    email: int
    avatar: str
    first_name: str
    last_name: str
    id: Optional[int] = None

    def __post_init__(self):
        self._posts = None

    @property
    def posts(self) -> Posts:
        return self._posts

    def to_payload(self) -> Dict:
        return {
            "name": f"{self.last_name}, {self.first_name}",
            "job": random.choice(jobs),
        }


class Users(APIRequest):
    RESOURCE = "users"
    MODEL = UserData

    def __init__(self, token):
        self._token = token
        super().__init__(Constants.BASE_USERS, self.MODEL, self.RESOURCE, token)

    @insert_api_module_attribute("_posts", PostsReadOnly)
    def retrieve(self, model_id: int, raise_on_failure=False) -> Union[UserData, None]:
        return super().retrieve(model_id, raise_on_failure)

    @insert_api_module_attribute("_posts", PostsReadOnly)
    def all(self, raise_on_failure=False) -> List[Union[UserData, None]]:
        return super().all(raise_on_failure)

    def create_bulk(
        self,
        data_models: List["UserData"],
        return_model_factory=None,
        raise_on_failure=False,
    ) -> List["UserData"]:
        return super().create_bulk(
            data_models,
            return_model_factory=user_data_factory,
            raise_on_failure=raise_on_failure,
        )
