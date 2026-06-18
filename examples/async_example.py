from os import getenv
import asyncio
from dotenv import load_dotenv
from pasarguard_panel_api import AsyncPasarguard, NewUser, Status

load_dotenv() # load environment variables from .env file

async def main():
    # initialize AsyncPasarguard object
    pg = AsyncPasarguard(
        getenv("host"), # Pasarguard panel URL
        getenv("user"),
        getenv("password")
    )

    await pg.auth() # request an auth token

    # groups fields:
    # groups.total  - total groups
    # groups.groups - complete list of Group (from pasarguard_panel_api import Group)

    # get available groups
    groups = await pg.get_groups()
    print(f"Total groups: {groups.total}") # how many groups are there

    # add user
    user = await pg.add_user(
        NewUser(
            username="username1",
            status=Status.ACTIVE,
            group_ids=[groups.groups[0].id] # assign to the first available group
        )
    )

    print(user.subscription_url) # prints subscription URL (e.g., /sub/ia9Akdcn2usaJs)
    print(user.admin.username) # print user's administator name

    # modify user
    user.status = Status.DISABLED
    also_user = await pg.modify_user(user)

    assert user.id == also_user.id # user is the same

    # get system information (like panel health, etc)
    sys_info = await pg.get_system_info()

    print(sys_info.online_users) # how many users are online

asyncio.run(main())
