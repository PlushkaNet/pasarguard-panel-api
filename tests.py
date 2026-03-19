from pasarguard_api import *
from dotenv import load_dotenv
from os import getenv
from datetime import timedelta, datetime, timezone
load_dotenv()

pg = AsyncPasarguard(getenv("url"), getenv("user"), getenv("password"))

async def main():
    await pg.Auth()
    info = await pg.GetGeneralInfo()
    print(info.model_dump())
    systeminfo = await pg.GetSystemInfo()
    print(systeminfo.model_dump())
    groups = await pg.GetGroups()
    print(groups.model_dump())
    users = await pg.GetUsers(
        limit=10, sort="-created_at",
        load_sub=True, offset=0,
        is_protocol=False
    )
    print(users.model_dump())
    users = await pg.GetUsers(
        limit=10, sort="-created_at",
        load_sub=False, offset=0,
        is_protocol=False
    )
    print(users.model_dump())
    user = await pg.AddUser(
        NewUser(
            username="new_user",
            group_ids=[7], # your group id, that could be obtained from groups
            expire=datetime.now(timezone.utc),
            proxy_settings={
                "vless":{},
                "shadowsocks":{"method":info.default_method}
            }
        )
    )
    user = await pg.GetUser("new_user")
    if user:
        user.expire += timedelta(weeks=1)
        user = await pg.ModifyUser(user)
        print(user.model_dump())

from asyncio import run
run(main())