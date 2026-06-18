# pasarguard-panel-api

## ✨ Sync & async simple python module for interacting with Pasarguard panel API
Uses httpx and pydantic for validation

### 🔥 Features
- Token autorenew

## Installation using git
```
pip install git+https://github.com/PlushkaNet/pasarguard-panel-api.git
```

## 🔑 Auth into Pasarguard panel (sync):
```
from os import getenv
from pasarguard_panel_api import Pasarguard
from dotenv import load_dotenv

load_dotenv() # load out environment first

pg = Pasarguard(
    getenv("host"),
    getenv("user"),
    getenv("password")
)

pg.auth()
```
## ✨ Async example:
```
from os import getenv
import asyncio
from pasarguard_panel_api import AsyncPasarguard
from dotenv import load_dotenv

load_dotenv() # load out environment first

pg = Pasarguard(
    getenv("host"),
    getenv("user"),
    getenv("password")
)

async def main():
    await pg.auth()

asyncio.run(main())
```
As you can see, API for sync and async operations is common
## 👤 Create new user (sync)
```
from pasarguard_panel_api import NewUser, Status

# auth goes here

# first let's get avaliable groups
groups = pg.get_groups()

user = pg.add_user(
    NewUser(
        username="new-user",
        status=Status.ACTIVE, # enum for convenient use
        group_ids=[groups.groups[0].id] # just first group from avaliable
    )
)

print(user.subscription_url)
```
## ✨ Async example (almost the same)
```
from pasarguard_panel_api import NewUser, Status

# auth goes here

# first let's get avaliable groups
groups = await pg.get_groups()

user = await pg.add_user(
    NewUser(
        username="new-user",
        status=Status.ACTIVE, # enum for convenient use
        group_ids=[groups.groups[0].id] # just first group from avaliable
    )
)

print(user.subscription_url)
```
## 🔎 Search users (sync)
```
# auth goes here

# get only one user
user = pg.get_user("some-username")
print(user)

# or get list of search entries
users = pg.get_users(limit=10) # only 10 users
print(users)
```
## ✏️ Modify user (sync)
```
# auth goes here

from pasarguard_panel_api import Status

user = pg.get_user("some-username") # get any user
assert user is not None # check that user exists
user.status = Status.DISABLED # disable user
modified_user = pg.modify_user(user) # modify user
print(modified_user)
```
**Async example is almost the same**

### 📚 For more examples, check [examples](./examples/) directory

## Short about
**What this SDK does**: It gives you a fast, simple way to interact with Pasarguard's user management endpoints, without the bloat of a full-feature implementation. The code is kept lean and readable. This is a **minimal** wrapper — not a complete API coverage.

## ✏️ Contributing
If you want to contribute, report a bug, or suggest feature, feel free to open issues and pull requests

## ❤️ Special thanks for Pasarguard team for the wonderful panel that makes proxy managment easier!