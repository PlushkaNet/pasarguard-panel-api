from pasarguard_panel_api import AsyncPasarguard, NewUser
from dotenv import load_dotenv
from os import getenv
from datetime import timedelta, datetime, timezone
load_dotenv()

pg = AsyncPasarguard(getenv("host"), getenv("user"), getenv("password"))

async def main():
    await pg.auth()

    info = await pg.get_general_info()
    print(info.model_dump())

    systeminfo = await pg.get_system_info()
    print(systeminfo.model_dump())

    groups = await pg.get_groups()
    print(groups.model_dump())

    users = await pg.get_users(
        limit=10, sort="-created_at",
        load_sub=True, offset=0,
        is_protocol=False
    )
    print(users.model_dump())

    users = await pg.get_users(
        limit=10, sort="-created_at",
        load_sub=False, offset=0,
        is_protocol=False
    )
    print(users.model_dump())

    await pg.add_user(
        NewUser(
            username="new_user",
            group_ids=[groups.groups[0]], # your group id, that could be obtained from groups
            expire=datetime.now(timezone.utc),
            proxy_settings={
                "vless":{},
                "shadowsocks":{"method":info.default_method}
            }
        )
    )

    user = await pg.get_user("new_user")
    if user:
        user.expire += timedelta(weeks=1)
        user = await pg.modify_user(user)
        print(user.model_dump())

from asyncio import run
run(main())
