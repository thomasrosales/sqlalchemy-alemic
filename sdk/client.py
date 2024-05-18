from environs import Env

from sdk.modules.posts import Posts
from sdk.modules.todos import Todos
from sdk.modules.users import Users
from sdk.request import APIConfig

env = Env()
env.read_env()


class Client:

    def __init__(self, *args, sdk_token=None, **kwargs):
        self.token = sdk_token or env.str("SDK_TOKEN")
        if not self.token:
            raise ValueError("Authorization is required")

        self._config = APIConfig(token=self.token)
        self._posts = Posts()
        self._todos = Todos()
        self._users = Users()

    @property
    def posts(self) -> Posts:
        return self._posts

    @property
    def todos(self) -> Todos:
        return self._todos

    @property
    def users(self) -> Users:
        return self._users


client = Client()
