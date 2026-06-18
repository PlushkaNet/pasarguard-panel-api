from os import getenv
from dotenv import load_dotenv
from pasarguard_panel_api import Pasarguard, NewUser, Status

load_dotenv() # load environment variables from .env file

# initialize Pasarguard object
pg = Pasarguard(
    getenv("host"),    # str
    getenv("user"),    # str
    getenv("password") # str
)

pg.auth() # request an auth token

# get our groups for users
groups = pg.get_groups()
print(f"Total groups: {groups.total}") # how many groups are there

# add user
user = pg.add_user(
    NewUser(
        username="username1",
        status=Status.ACTIVE,
        group_ids=[groups.groups[0].id] # create in first group
    )
)

print(user.subscription_url) # print user's subscription url in format /sub/...
print(user.admin) # print user's administator (pydantic representation)

# modify user
user.status = Status.DISABLED
also_user = pg.modify_user(user)

assert user.id == also_user.id

# get system information (like panel health, etc)
sys_info = pg.get_system_info()

print(sys_info.online_users) # how many users are online
