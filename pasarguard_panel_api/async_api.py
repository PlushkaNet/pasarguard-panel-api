""" File with code for asynchronous version of SDK """
from typing import Optional, Any
from httpx import AsyncClient
from .models import SystemInfo, User, Users, NewUser, GeneralSettings, Groups
from .exceptions import AuthorizationError

class AsyncPasarguard:
    """ Async class for interacting with Pasarguard panel API """

    def __init__(self, url: str, user: str, password: str):
        self._url = url.removesuffix("/")
        self._user = user
        self._password = password

        self._token = None


    async def _auth(self, client: AsyncClient, /):
        response = await client.post(
            self._url + "/api/admin/token",
            data={
                "grant_type":"password",
                "username":self._user,
                "password":self._password
            }
        )
        if response.status_code == 200:
            self._token = response.json()["access_token"]
        else:
            raise AuthorizationError(
                f"Authorization failed.\n" \
                f"Status code: {response.status_code}\n" \
                f"Message: {response.text!r}"
            )


    async def _make_api_request(self, client: AsyncClient, method: str, url_suffix: str, params=None, json=None):
        """ Will perform auto auth if `_token` is None """
        if self._token is None:
            await self._auth(client)

        response = await client.request(
            method,
            self._url + "/api/" + url_suffix,
            params=params,
            json=json,
            headers={
                "Authorization": "Bearer " + self._token
            }
        )
        return response.text, response.status_code


    async def _make_api_request_reauth(self, method: str, url_suffix: str, /, params: dict[str, Any] = None, json=None):
        async with AsyncClient() as client:
            resp, status = await self._make_api_request(client, method, url_suffix, params, json)
            if status == 401:
                await self._auth(client)
                resp, status = await self._make_api_request(client, method, url_suffix, params, json)
            return resp, status


    async def _make_api_post_request(self, url_suffix: str, /, params: dict[str, Any] = None, json=None):
        return await self._make_api_request_reauth("post", url_suffix, params=params, json=json)


    async def _make_api_get_request(self, url_suffix: str, params: dict[str, Any] = None, /):
        return await self._make_api_request_reauth("get", url_suffix, params=params)


    async def auth(self):
        """
        Authentificates into Pasarguard panel by requesting a token
        Can raise `AuthorizationError`, httpx exceptions and pydantic validation exceptions
        """
        async with AsyncClient() as client:
            await self._auth(client)


    async def get_system_info(self) -> SystemInfo:
        """
        Get system info, such as version, memory usage and etc.
        Can raise `AuthorizationError`, httpx exceptions and pydantic validation exceptions
        """
        text, _ = await self._make_api_get_request("system")
        return SystemInfo.model_validate_json(text)


    async def get_general_info(self) -> GeneralSettings:
        """
        Get general info from panel, such as default proxy settings method
        Can raise `AuthorizationError`, httpx exceptions and pydantic validation exceptions
        """
        text, _ = await self._make_api_get_request("settings/general")
        return GeneralSettings.model_validate_json(text)


    async def get_froups(self) -> Groups:
        """
        Get list of groups of users
        Can raise `AuthorizationError`, httpx exceptions and pydantic validation exceptions
        """
        text, _ = await self._make_api_get_request("groups/simple", {"all": True})
        return Groups.model_validate_json(text)


    async def get_users(self, **kwargs) -> Users:
        """
        Get list of users
        `kwargs` are search filters that supported by panel

        Supported arguments:
        - limit (int)
        - sort (str)
        - load_sub (bool)
        - offset (int)
        - is_protocol (bool)
        - search (str)

        Usage example:
        ```
        users = await pg.GetUsers(
            limit=10,
            sort="-created_at",
            load_sub=True,
            offset=0,
            is_protocol=False
        )
        ```

        Default (used by web panel) kwargs are:
        - limit=10
        - sort="-created_at"
        - load_sub=True
        - offset=0
        - is_protocol=False
        Can raise `AuthorizationError`, httpx exceptions and pydantic validation exceptions
        """
        text, _ = await self._make_api_get_request("users", kwargs)
        return Users.model_validate_json(text)


    async def add_user(self, new_user: NewUser, /) -> User:
        """
        Create new user
        Returns `User` model from panel on success
        Can raise `AuthorizationError`, httpx exceptions and pydantic validation exceptions
        """
        text, _ = await self._make_api_post_request("user", json=new_user.model_dump(mode="json"))
        return User.model_validate_json(text)


    async def get_user(self, name_pattern: str, /) -> Optional[User]:
        """
        Get user from search
        Can raise `AuthorizationError`, httpx exceptions and pydantic validation exceptions
        """
        text, _ = await self._make_api_get_request(
            "users",
            dict(
                limit=1,
                load_sub=True,
                is_protocol=False,
                offset=0,
                search=name_pattern
            )
        )
        users = Users.model_validate_json(text)
        return users.users[0] if users.total > 0 else None


    async def modify_user(self, user: User, /) -> Optional[User]:
        """
        Modify existing user
        Returns `User` model from panel on success
        Returns None on non 200 status code
        Can raise `AuthorizationError`, httpx exceptions and pydantic validation exceptions
        """
        text, status = await self._make_api_request_reauth(
            "put",
            "user/" + user.username,
            json=user.model_dump(mode="json"))
        if status != 200:
            return None
        return User.model_validate_json(text)


    async def from_template(self, username: str, template_id: int, /) -> Optional[User]:
        """
        Creates user from template
        Returns `User` model from panel on success
        Returns None on non 200 status code
        Can raise `AuthorizationError`, httpx exceptions and pydantic validation exceptions
        """
        text, status = await self._make_api_post_request(
            "user/from_template",
            json={
                "user_template_id": template_id,
                "username": username
            }
        )
        if status not in (200, 201):
            return None
        return User.model_validate_json(text)
