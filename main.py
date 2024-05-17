from database.controllers import create_user, get_user_by_id
from sdk.client import Client, client

if __name__ == "__main__":
    users = client.users.all()
    print(users)
    post1 = client.posts.retrieve(1)
    print(post1)
    """
    spongebob = get_user_by_id(1)
    sandy = get_user_by_id(2)
    patrick = get_user_by_id(3)

    if not spongebob:
        spongebob = create_user(
            "Spongebob", "Squarepants", ["spongebob@sqlalchemy.org"]
        )

    if not sandy:
        sandy = create_user(
            name="sandy",
            last_name="Sandy Cheeks",
            emails=[
                "sandy@sqlalchemy.org",
                "sandy@squirrelpower.org",
            ],
        )

    if not patrick:
        patrick = create_user(name="patrick", last_name="Patrick Star", emails=[])

    print(spongebob)
    print(sandy)
    print(patrick)


    # users = client.users.list()
    user = client.users.retrieve(1, raise_on_failure=True)
    post = user.posts.list()[0]

    breakpoint()

    post3 = client.posts.retrieve(1000, raise_on_failure=True)

    post1 = client.posts.retrieve(1)
    post2 = client.posts.retrieve(4)
    print(post1.comments.list())
    print(post2.comments.list())

    # print(client.todos.retrieve(197))

    # post = PostData(body="ttt", userId=1, title="asd")
    # print(client.posts.create(post.to_payload()))
    """
