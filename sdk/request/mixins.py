import asyncio
from typing import TYPE_CHECKING, List, Union

import requests

from sdk.request import ApiError

if TYPE_CHECKING:
    from sdk.modules.posts import CommentData, PostData
    from sdk.modules.todos import TodoData
    from sdk.modules.users import UserData


class APIRetrieveMixin:

    async def retrieve(
        self, model_id: int, raise_on_failure=False
    ) -> Union["PostData", "TodoData", "CommentData", None]:
        data_json = self._fetch_data_sync(
            f"{self._url}/{model_id}",
            raise_on_failure,
            single=True,
        )
        data = data_json["data"] if "data" in data_json else data_json
        return self._model(**data) if data else None


class APIListAllMixin:

    async def all(
        self, raise_on_failure=False
    ) -> List[Union["PostData", "TodoData", "CommentData", None]]:
        data_json = self._fetch_data_sync(self._url, raise_on_failure)
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
                            self._fetch_data(self._url, params, raise_on_failure)
                        )
                    )

                async_response = await asyncio.gather(*tasks)

            data = data_json["data"]
            for ar in async_response:
                if ar:
                    data.extend(ar["data"])
        else:
            data = data_json

        return [self._model(**item) for item in data if item is not None]


class APICreateMixin:

    async def _create_bulk(self, data_models, raise_on_failure=False):
        tasks = set()

        for model in data_models:
            data = model.to_payload()
            tasks.add(
                asyncio.create_task(
                    self._create_model(
                        self._url,
                        data,
                        self._params,
                        raise_on_failure,
                    )
                )
            )
        response = await asyncio.gather(*tasks)
        return response

    def create(
        self,
        model: Union["UserData", "PostData", "TodoData", "CommentData"],
        raise_on_failure=False,
    ) -> Union["UserData", "PostData", "TodoData", "CommentData", None]:
        response = requests.post(
            self._url,
            data=model.to_payload(),
            auth=self._auth,
        )
        if response.status_code != 201:
            if raise_on_failure:
                raise ApiError(response.status_code, response.text)
            return None
        data = response.json()
        return self._model(**data)

    def create_bulk(
        self,
        data_models: List[Union["UserData", "PostData", "TodoData", "CommentData"]],
        raise_on_failure=False,
        **kwargs,
    ) -> List[Union["UserData", "PostData", "TodoData", "CommentData"]]:
        model = kwargs.get("return_model_factory", self._model)
        response = asyncio.run(self._create_bulk(data_models, raise_on_failure))
        return [model(**item) for item in response if item is not None]
