from typing import TYPE_CHECKING, Dict, List, Union, Callable

import requests
from requests.auth import AuthBase

from sdk.request.decorators import request_handler
from sdk.request.exceptions import APIException

if TYPE_CHECKING:
    from sdk.modules.posts import PostData, CommentData
    from sdk.modules.todos import TodoData


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["authorization"] = "Bearer " + self.token
        return request


class APIRequestBase:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, model, resource: str, token: str, query_params=None):
        self._model = model
        self._resource = resource
        self._auth = BearerAuth(token)
        self._params = query_params


class APIRequestRetrieveMixin:

    def retrieve(
        self, model_id: int, raise_on_failure=False
    ) -> Union["PostData", "TodoData", "CommentData", None]:
        print(f"{self.BASE_URL}/{self._resource}/{model_id}")
        response = requests.get(
            f"{self.BASE_URL}/{self._resource}/{model_id}",
            auth=self._auth,
            params=self._params,
        )
        if response.status_code != 200:
            if raise_on_failure:
                raise APIException("something went wrong")
            return None
        data = response.json()
        return self._model(**data)


class APIRequestAllMixin:

    def list(
        self, raise_on_failure=False
    ) -> List[Union["PostData", "TodoData", "CommentData", None]]:
        print(f"{self.BASE_URL}/{self._resource}/")
        response = requests.get(
            f"{self.BASE_URL}/{self._resource}/", auth=self._auth, params=self._params
        )
        if response.status_code != 200:
            if raise_on_failure:
                raise APIException("something went wrong")
            return []
        data = response.json()
        return [self._model(**item) for item in data]


class APIRequestReadOnly(APIRequestBase, APIRequestAllMixin, APIRequestRetrieveMixin):
    pass


class APIRequest(APIRequestReadOnly):

    def create(
        self, payload: Dict, raise_on_failure=False
    ) -> Union["PostData", "TodoData", "CommentData"]:
        response = requests.post(
            f"{self.BASE_URL}/{self._resource}/", data=payload, auth=self._auth
        )
        if response.status_code != 201:
            if raise_on_failure:
                raise APIException("something went wrong")
            return None
        data = response.json()
        return self._model(**data)

    def update(self):
        pass

    def delete(self):
        pass

    def partial_update(self):
        pass
