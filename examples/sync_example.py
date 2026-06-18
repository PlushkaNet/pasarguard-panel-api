from os import getenv
from dotenv import load_dotenv
from pasarguard_panel_api import Pasarguard, NewUser, Status

load_dotenv() # load environment variables from .env file

# initialize Pasarguard object
pg = Pasarguard(
    getenv("host"), # Pasarguard panel URL
    getenv("user"),
    getenv("password")
)

pg.auth() # request an auth token

# get available groups
groups = pg.get_groups()
print(f"Total groups: {groups.total}") # how many groups are there

# groups fields:
# groups.total  - total groups
# groups.groups - complete list of Group (from pasarguard_panel_api import Group)

# add user
user = pg.add_user(
    NewUser(
        username="username1",
        status=Status.ACTIVE,
        group_ids=[groups.groups[0].id] # assign to the first available group
    )
)

print(user.subscription_url) # prints subscription URL (e.g., /sub/ia9Akdcn2usaJs)
print(user.admin.username) # print user's administrator name

# modify user
user.status = Status.DISABLED
also_user = pg.modify_user(user)

assert user.id == also_user.id

# get system information (like panel health, etc)
sys_info = pg.get_system_info()

print(sys_info.online_users) # how many users are online
