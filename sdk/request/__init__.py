import asyncio
from typing import TYPE_CHECKING, Dict, List, Union

import requests
from aiohttp import ClientSession
from loguru import logger
from requests.auth import AuthBase

from core.enums import Constants
from sdk.request.decorators import request_handler
from sdk.request.exceptions import ApiError

if TYPE_CHECKING:
    from sdk.modules.posts import CommentData, PostData
    from sdk.modules.todos import TodoData


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["authorization"] = "Bearer " + self.token
        return request


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
            url = url.replace("api", "apis")
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


class APIRequestRetrieveMixin:

    async def retrieve(
        self, model_id: int, raise_on_failure=False
    ) -> Union["PostData", "TodoData", "CommentData", None]:
        data_json = self._fetch_data_sync(
            f"{self.APPLICATION_URLS[self._application]}/{self._resource}/{model_id}",
            raise_on_failure,
        )
        data = data_json["data"] if "data" in data_json else data_json
        return self._model(**data)


class APIRequestAllMixin:

    async def list(
        self, raise_on_failure=False
    ) -> List[Union["PostData", "TodoData", "CommentData", None]]:
        url = f"{self.APPLICATION_URLS[self._application]}/{self._resource}/"
        data_json = self._fetch_data_sync(url, raise_on_failure)
        if isinstance(data_json, dict):
            total_pages = data_json.get("total_pages")
            tasks = set()
            async_response = []

            if total_pages > 1:
                for page_count in range(1, total_pages):
                    params = self._params
                    params.update({"page": page_count + 1})
                    tasks.add(
                        asyncio.create_task(
                            self._fetch_data(url, params, raise_on_failure)
                        )
                    )

                async_response = await asyncio.gather(*tasks)

            data = data_json["data"]
            for ar in async_response:
                if ar:
                    data.extend(ar["data"])
        else:
            data = data_json

        return [self._model(**item) for item in data]


class APIRequestReadOnly(APIRequestBase, APIRequestAllMixin, APIRequestRetrieveMixin):
    pass


class APIRequest(APIRequestReadOnly):

    def create(
        self, payload: Dict, raise_on_failure=False
    ) -> Union["PostData", "TodoData", "CommentData"]:
        response = requests.post(
            f"{self.APPLICATION_URLS[self._application]}/{self._resource}/", data=payload, auth=self._auth
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
