from dataclasses import dataclass
from typing import Dict, Optional, Union, List

from sdk.modules.decorators import insert_api_module_attribute
from sdk.request import (
    APIRequest,
    APIRequestBase,
    APIRequestRetrieveMixin,
    APIRequestAllMixin,
)


@dataclass
class CommentData:
    name: str
    email: str
    body: str
    postId: int
    id: Optional[int] = None


class Comments(APIRequestBase, APIRequestAllMixin):

    resource = "posts/{0}/comments"
    model = CommentData

    def __init__(self, token, related_instance_id=None):
        resource = self.resource.format(related_instance_id)
        super().__init__(self.model, resource, token)


@dataclass
class PostData:
    title: str
    body: str
    userId: int
    id: Optional[int] = None

    def to_payload(self) -> Dict:
        return {"title": self.title, "body": self.body, "userId": self.userId}

    def __post_init__(self):
        self._comments = None

    @property
    def comments(self) -> Comments:
        return self._comments


class Posts(APIRequest):
    resource = "posts"
    model = PostData

    def __init__(self, token):
        self._token = token
        super().__init__(self.model, self.resource, self._token)

    @insert_api_module_attribute("_comments", Comments)
    def retrieve(self, model_id: int, raise_on_failure=False) -> Union[PostData, None]:
        return super().retrieve(model_id, raise_on_failure)

    @insert_api_module_attribute("_comments", Comments)
    def list(self, raise_on_failure=False) -> List[Union[PostData, None]]:
        return super().list(raise_on_failure)


class PostsReadOnly(APIRequestBase, APIRequestAllMixin):
    resource = "posts"
    model = PostData

    def __init__(self, token, related_instance_id=None):
        self._token = token
        super().__init__(
            self.model, self.resource, self._token, query_params={"userId": related_instance_id}
        )

    @insert_api_module_attribute("_comments", Comments)
    def list(self, raise_on_failure=False) -> List[Union[PostData, None]]:
        return super().list(raise_on_failure)
