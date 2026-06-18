from os import getenv
from dotenv import load_dotenv
from pasarguard_panel_api import Pasarguard, NewUser, Status

load_dotenv() # load environment variables from .env file

# initialize Pasarguard object
pg = Pasarguard(
    getenv("host"),
    getenv("user"),
    getenv("password")
)

# No manual authentication required:
# The client automatically obtains and renews tokens as needed.
# Just make your API calls — the client handles all auth logic behind the scenes

user = pg.get_user("asjdsajkdh") # user that doesn't exist
if user is None:
    print("user does not exist")

user = pg.get_user("username1") # user that exists
print(user.username)
print(user.id)
print(user.subscription_url)

users_result = pg.get_users(limit=10) # limit results to 10 users
print(len(users_result.users))