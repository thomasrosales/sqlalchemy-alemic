import asyncio
from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from sdk.modules.posts import CommentData, PostData
    from sdk.modules.todos import TodoData


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
