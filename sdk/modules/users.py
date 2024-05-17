from dataclasses import dataclass
from typing import Optional, Union, List

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
    name: str
    username: str
    email: int
    phone: str
    website: str
    id: Optional[int] = None
    address: AddressData = None
    company: CompanyData = None

    def __post_init__(self):
        self._posts = None

    @property
    def posts(self) -> Posts:
        return self._posts


class Users(APIRequest):

    resource = "users"
    model = UserData

    def __init__(self, token):
        self._token = token
        super().__init__(self.model, self.resource, token)

    @insert_api_module_attribute("_posts", PostsReadOnly)
    def retrieve(self, model_id: int, raise_on_failure=False) -> Union[UserData, None]:
        return super().retrieve(model_id, raise_on_failure)

    @insert_api_module_attribute("_posts", PostsReadOnly)
    def list(self, raise_on_failure=False) -> List[Union[UserData, None]]:
        return super().list(raise_on_failure)
