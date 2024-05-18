import asyncio
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from core.enums import Constants
from sdk.modules.decorators import insert_api_module_attribute
from sdk.request import APIListAllMixin, APIRequest, APIRequestBase


@dataclass
class CommentData:
    name: str
    email: str
    body: str
    postId: int
    id: Optional[int] = None


class Comments(APIRequestBase, APIListAllMixin):

    RESOURCE = "posts/{0}/comments"
    MODEL = CommentData

    def __init__(self, related_instance_id=None):
        resource = self.RESOURCE.format(related_instance_id)
        super().__init__(Constants.BASE_URL, self.MODEL, resource)

    def all(self, raise_on_failure=False) -> List[Union[CommentData, None]]:
        return asyncio.run(super().all(raise_on_failure))


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
    RESOURCE = "posts"
    MODEL = PostData

    def __init__(self):
        super().__init__(Constants.BASE_URL, self.MODEL, self.RESOURCE)

    @insert_api_module_attribute("_comments", Comments)
    def retrieve(self, model_id: int, raise_on_failure=False) -> Union[PostData, None]:
        return super().retrieve(model_id, raise_on_failure)

    @insert_api_module_attribute("_comments", Comments)
    def all(self, raise_on_failure=False) -> List[Union[PostData, None]]:
        return super().all(raise_on_failure)


class PostsReadOnly(APIRequestBase, APIListAllMixin):
    RESOURCE = "posts"
    MODEL = PostData

    def __init__(self, related_instance_id=None):
        super().__init__(
            Constants.BASE_URL,
            self.MODEL,
            self.RESOURCE,
            query_params={"userId": related_instance_id},
        )

    @insert_api_module_attribute("_comments", Comments)
    def all(self, raise_on_failure=False) -> List[Union[PostData, None]]:
        return super().all(raise_on_failure)
