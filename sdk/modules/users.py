from dataclasses import dataclass
from typing import List, Optional, Union

from core.enums import Constants
from sdk.modules.decorators import insert_api_module_attribute
from sdk.modules.posts import Posts, PostsReadOnly
from sdk.request import APIRequest


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
    id: Optional[int] = None
    address: AddressData = None
    company: CompanyData = None
    name: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None

    def __post_init__(self):
        self._posts = None

    @property
    def posts(self) -> Posts:
        return self._posts


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
