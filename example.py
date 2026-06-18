from asyncio import run
from os import getenv
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from pasarguard_panel_api import AsyncPasarguard, NewUser

async def main():
    load_dotenv()

    pg = AsyncPasarguard(
        getenv("url"),
        getenv("user"),
        getenv("password")
    )

    # firstly, lets auth and get our session token
    await pg.auth()

    # get all users list
    users = await pg.get_users(
        limit=10,
        sort="-created_at",
        load_sub=True,
        offset=0,
        is_protocol=False
    )
    print(users)

    # create new user
    info = await pg.get_general_info() # to get default proxy method from panel
    user = await pg.add_user(
        NewUser(
            username="new_user",
            group_ids=[7], # your group id, that could be obtained from groups
            expire=datetime.now(timezone.utc) + timedelta(weeks=1),
            proxy_settings={
                "vless":{},
                "shadowsocks":{"method":info.default_method}
            }
        )
    )

    print(user) # user that we added

    # edit existing user
    user.expire += timedelta(weeks=1) # lets add one more week to user's subscription
    edited_user = await pg.modify_user(user)

    print(edited_user)

    # get system info (like perfomance stats, memory usage)
    stats = await pg.get_system_info()

    print(stats)

    # get only one user from search
    user = await pg.get_user("new") # since the username starts with 'new', it will be returned

    print(user)

run(main())
