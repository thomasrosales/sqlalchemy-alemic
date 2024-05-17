from sdk.modules.posts import Posts
from sdk.modules.todos import Todos
from sdk.modules.users import Users

from environs import Env


env = Env()
env.read_env()


class Client:

    def __init__(self, *args, sdk_token=None, **kwargs):
        self._token = sdk_token or env.str("SDK_TOKEN")
        if not self._token:
            raise ValueError("Authorization is required")

        self._posts = Posts(token=self._token)
        self._todos = Todos(token=self._token)
        self._users = Users(token=self._token)

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
