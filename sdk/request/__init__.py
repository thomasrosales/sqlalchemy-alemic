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
from .mixins import APICreateMixin, APIListAllMixin, APIRetrieveMixin


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
                if 200 <= response.status < 300:
                    return await response.json()
                if raise_on_failure:
                    raise ApiError(response.status, response.reason)
                logger.error(response.reason)
                return []

    async def _create_model(self, url, data, params, raise_on_failure):
        async with ClientSession() as session:
            headers = {"Authorization": f"Basic  {self._auth.token}"}
            async with session.post(
                url, headers=headers, params=params, data=data
            ) as response:
                if 200 <= response.status < 300:
                    return await response.json()
                if raise_on_failure:
                    raise ApiError(response.status, response.reason)
                logger.error(response.reason)
                return None

    def _fetch_data_sync(self, url, raise_on_failure, single=False):
        response = requests.get(url, auth=self._auth, params=self._params)
        if 200 <= response.status_code < 300:
            return response.json()
        if raise_on_failure:
            raise ApiError(response.status_code, str(response.text))
        logger.error(response.text)
        return {} if single else []


class APIRequestReadOnly(APIRequestBase, APIListAllMixin, APIRetrieveMixin):
    pass


class APIRequest(APIRequestReadOnly, APICreateMixin):

    def update(self):
        pass

    def delete(self):
        pass

    def partial_update(self):
        pass
