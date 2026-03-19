from pasarguard_api import AsyncPasarguard, NewUser
from asyncio import run
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, timezone, timedelta

async def main():
    load_dotenv()
    
    pg = AsyncPasarguard(
        getenv("url"),
        getenv("user"),
        getenv("password")
    )

    # firstly, lets auth and get our session token
    await pg.Auth()

    # getting all users list
    users = await pg.GetUsers(limit=10, sort="-created_at",
                              load_sub=True, offset=0,
                              is_protocol=False)
    print(users)

    # creating new user
    info = await pg.GetGeneralInfo()
    user = await pg.AddUser(
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

    # editing existing user
    user.expire += timedelta(weeks=1) # lets add one more week to user's subscription
    edited_user = await pg.ModifyUser(user)

    print(edited_user)

    # getting system info (like perfomance stats, memory usage)
    stats = await pg.GetSystemInfo()

    print(stats)

    # getting only one user from search
    user = await pg.GetUser("new") # our user starts with "new", so it will be returned

    print(user)

run(main())