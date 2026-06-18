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

# we don't need to auth explicitly, because Pasarguard object will automatically
# perform auth if we didn't do it before

user = pg.get_user("asjdsajkdh") # user that doesn't exist
print(user)

user = pg.get_user("username1") # user that exists
print(user)

users = pg.get_users(limit=10) # get only 10 users
print(len(users.users))