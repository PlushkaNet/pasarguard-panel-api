from httpx import AsyncClient
from .models import *

class AuthorizationError(Exception): pass

class AsyncPasarguard:
    def __init__(self, url:str, user, password):
        self._url = url.removesuffix("/")
        self._user = user
        self._password = password

        self._token = None

    
    async def _make_api_request(self, method, url_suffix, params=None, json=None):
        async with AsyncClient() as client:
            response = await client.request(
                method,
                self._url + "/api/" + url_suffix,
                params=params,
                json=json,
                headers={
                    "Authorization":f"Bearer {self._token}"
                }
            )
            return response.text, response.status_code
        
    
    async def _make_api_request_reauth(self, method, url_suffix, params=None, json=None):
        resp, status = await self._make_api_request(method, url_suffix, params, json)
        if status == 401:
            await self.Auth()
            resp, status = await self._make_api_request(method, url_suffix, params, json)
        return resp, status


    async def _make_api_post_request(self, url_suffix, params=None, json=None):
        return await self._make_api_request_reauth("post", url_suffix, params, json)
        
    
    async def _make_api_get_request(self, url_suffix, params=None):
        return await self._make_api_request_reauth("get", url_suffix, params)


    async def Auth(self):
        async with AsyncClient() as client:
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
                    f"Message: {response.text}")
    

    async def GetSystemInfo(self) -> SystemInfo:
        text, _ = await self._make_api_get_request("system")
        return SystemInfo.model_validate_json(text)
        
    
    async def GetGeneralInfo(self) -> GeneralSettings:
        text, _ = await self._make_api_get_request("settings/general")
        return GeneralSettings.model_validate_json(text)
        

    async def GetGroups(self) -> Groups:
        text, _ = await self._make_api_get_request("groups/simple", {"all":True})
        return Groups.model_validate_json(text)


    async def GetUsers(self, **kwargs) -> Users:
        """Method for requesting users list

        Supported arguments:
            `limit` (int)
            `sort` (str)
            `load_sub` (bool)
            `offset` (int)
            `is_protocol` (bool)
            `search` (str)

        Usage example:
        ```
        users = await pg.GetUsers(limit=10, sort="-created_at",
                                  load_sub=True, offset=0,
                                  is_protocol=False)
        ```

        Default (used by web panel) kwargs are:
            `limit=10`
            `sort="-created_at"`
            `load_sub=True`
            `offset=0,`
            `is_protocol=False`
            """
        text, _ = await self._make_api_get_request("users", kwargs)
        return Users.model_validate_json(text)
        

    async def GetTemplates(self):
        raise NotImplementedError("GetTemplates currently not implemented")
    

    async def AddUser(self, new_user:NewUser) -> User:
        text, _ = await self._make_api_post_request("user", json=new_user.model_dump(mode="json"))
        return User.model_validate_json(text)
    

    async def GetUser(self, name_pattern:str) -> User | None:
        text, _ = await self._make_api_get_request("users", dict(
            limit=1,
            load_sub=True,
            is_protocol=False,
            offset=0,
            search=name_pattern
        ))
        users = Users.model_validate_json(text)
        return users.users[0] if users.total > 0 else None
    

    async def ModifyUser(self, user:User) -> User | None:
        text, status = await self._make_api_request(
            "put",
            f"user/{user.username}",
            json=user.model_dump(mode="json"))
        if status != 200: return None
        return User.model_validate_json(text)