from typing import TYPE_CHECKING
from requests.auth import AuthBase


if TYPE_CHECKING:
    from sdk.request import APIConfig


class BearerAuth(AuthBase):
    def __init__(self, config: "APIConfig"):
        self.token = config.token

    def __call__(self, request):
        request.headers["authorization"] = "Bearer " + self.token
        return request
