# 📡 API reference

Both clients expose an identical interface. Method names below refer to
`Pasarguard` (sync) — for `AsyncPasarguard` the same names apply and must be
awaited. Return types are identical.

```python
from pasarguard_panel_api import Pasarguard, AsyncPasarguard
```

---

## Client constructor

### `Pasarguard(url: str, user: str, password: str)`

### `AsyncPasarguard(url: str, user: str, password: str)`

| Argument | Type | Description |
| --- | --- | --- |
| `url` | `str` | Panel base URL, e.g. `https://panel.example.com`. A trailing `/` is stripped. |
| `user` | `str` | Admin username. |
| `password` | `str` | Admin password. |

No network I/O happens in the constructor.

---

## Methods

### `auth() -> None`

Obtains an access token from `POST /api/admin/token` and stores it internally
for subsequent requests.

- **Raises:** `AuthorizationError` if credentials are rejected.

All subsequent methods work even if `auth()` was never called — the client
authenticates lazily before the first API request.

---

### `get_system_info() -> SystemInfo`

Queries `GET /api/system`.

Returns panel runtime statistics: version, uptime, memory/disk/CPU usage,
user counters (total, online, active, on-hold, disabled, expired, limited)
and aggregate bandwidth.

---

### `get_general_info() -> GeneralSettings`

Queries `GET /api/settings/general`.

Returns general panel settings such as the default proxy method
(`default_method`) and flow (`default_flow`). Useful when building
`proxy_settings` for a new user.

---

### `get_groups() -> Groups`

Queries `GET /api/groups?all=true`.

Returns all user groups and their `id`s. Group IDs are required when creating
users (`NewUser.group_ids`).

---

### `get_users(**filters) -> Users`

Queries `GET /api/users`.

Search users with optional filters. The filters are forwarded to the panel as
query parameters:

| Keyword | Type | Default | Meaning |
| --- | --- | --- | --- |
| `limit` | `int` | `10` | Max users per page |
| `sort` | `str` | `"-created_at"` | Sort order (prefix `-` for descending) |
| `load_sub` | `bool` | `True` | Include subscription URLs in results |
| `offset` | `int` | `0` | Pagination offset |
| `is_protocol` | `bool` | `False` | Filter by protocol type |
| `search` | `str` | — | Username substring filter |

```python
users = pg.get_users(limit=10, sort="-created_at", load_sub=True, offset=0, is_protocol=False)
```

---

### `get_user(name_pattern: str) -> User | None`

Queries `GET /api/users` with `limit=1` and `search=<pattern>`.

Returns the first matching user, or `None` when nothing is found. The pattern
is a substring match against usernames (the same search the web panel uses).

```python
user = pg.get_user("alice")
if user is None:
    print("not found")
```

---

### `add_user(new_user: NewUser) -> User`

Posts `POST /api/user`.

Creates a new user from a `NewUser` model and returns the created `User`.

- **Raises:** `UserAlreadyExistsError` when the username is taken
  (HTTP 409).

```python
user = pg.add_user(
    NewUser(
        username="alice",
        status=Status.ACTIVE,
        group_ids=[groups.groups[0].id], # create in first group from groups
    )
)
```

---

### `modify_user(user: User) -> User`

Sends `PUT /api/user/by-id/{user.id}`.

Updates an existing user. The whole `User` object is sent; the recommended
pattern is to fetch the user with `get_user()`, mutate the fields, and send
it back:

```python
user = pg.get_user("alice")
user.status = Status.DISABLED
user.expire += timedelta(weeks=2)
user = pg.modify_user(user)
```

Returns the updated `User` model.

---

### `from_template(username: str, template_id: int) -> User | None`

Posts `POST /api/user/from_template`.

Creates a user from a pre-defined template:

```python
user = pg.from_template("alice-tpl", 3) # 3 - template number
```

- **Raises:** `UserAlreadyExistsError` when the username is taken (HTTP 409).

---

## Common behavior

### Automatic token renewal

Every public method (except `auth()`) goes through `_make_api_request_reauth`:

1. If no token is stored, authenticate first.
2. Send the request with `Authorization: Bearer <token>`.
3. If the response is `401` (expired/invalid token), authenticate again and
   retry the request **once**.

This means tokens are transparently renewed; you don't need to watch
expiration dates or re-auth manually.

### Response validation

Successful responses (HTTP `200`/`201`) are parsed and validated with Pydantic
before being returned. A validation failure means the panel returned data the
models don't describe (usually a panel version mismatch) and raises
`pydantic.ValidationError`.

### HTTP error handling

Any status code other than `200`/`201` raises `APIResponseError`
(except `409`, which is mapped to `UserAlreadyExistsError` in
`add_user` / `from_template`, and the auth endpoint, which maps failures to
`AuthorizationError`).

### Networking

- Each request opens a fresh `httpx.Client` / `AsyncClient` (context-managed,
  always closed).
- A new session per request means no connection pooling; fine for low-volume
  scripts, but if you make high-frequency calls, consider batching work per
  process or contributing pooling support.
- All httpx transport errors (`httpx.ConnectError`, `TimeoutException`, etc.)
  propagate as-is.
