from typing import TYPE_CHECKING, Dict, Union

import requests
from aiohttp import ClientSession
from loguru import logger

from core.enums import Constants
from sdk.request.decorators import request_handler
from sdk.request.exceptions import ApiError

if TYPE_CHECKING:
    from sdk.modules.posts import CommentData, PostData
    from sdk.modules.todos import TodoData

from .auth import BearerAuth
from .mixins import APIRequestAllMixin, APIRequestRetrieveMixin


class APIRequestBase:
    APPLICATION_URLS = {
        Constants.BASE_URL: "https://jsonplaceholder.typicode.com",
        Constants.BASE_USERS: "https://reqres.in/api",
    }

    def _set_query_params(self, query_params):
        params = {"page": 1, "per_page": 5}
        if query_params is None:
            query_params = {}
        params.update(query_params)
        return params

    def __init__(
        self, application, model, resource: str, token: str, query_params=None
    ):
        self._application = application
        self._model = model
        self._resource = resource
        self._auth = BearerAuth(token)
        self._params = self._set_query_params(query_params)

    async def _fetch_data(self, url, params, raise_on_failure):
        async with ClientSession() as session:
            headers = {"Authorization": f"Basic  {self._auth.token}"}
            async with session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    if raise_on_failure:
                        raise ApiError(response.status, response.reason)
                    logger.error(response.reason)
                    return []
                return await response.json()

    def _fetch_data_sync(self, url, raise_on_failure):
        response = requests.get(url, auth=self._auth, params=self._params)
        if response.status_code != 200:
            if raise_on_failure:
                raise ApiError(response.status_code, str(response.text))
            logger.error(response.text)
            return []

        return response.json()


class APIRequestReadOnly(APIRequestBase, APIRequestAllMixin, APIRequestRetrieveMixin):
    pass


class APIRequest(APIRequestReadOnly):

    def create(
        self, payload: Dict, raise_on_failure=False
    ) -> Union["PostData", "TodoData", "CommentData"]:
        response = requests.post(
            f"{self.APPLICATION_URLS[self._application]}/{self._resource}/",
            data=payload,
            auth=self._auth,
        )
        if response.status_code != 201:
            if raise_on_failure:
                raise ApiError(response.status_code, response.text)
            return None
        data = response.json()
        return self._model(**data)

    def update(self):
        pass

    def delete(self):
        pass

    def partial_update(self):
        pass
