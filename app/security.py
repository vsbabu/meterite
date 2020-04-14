from . import config

# https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN

api_key_query = APIKeyQuery(name=config.Settings().api_key_name, auto_error=False)
api_key_header = APIKeyHeader(name=config.Settings().api_key_name, auto_error=False)
api_key_cookie = APIKeyCookie(name=config.Settings().api_key_name, auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):
    api_tokens = config.Settings().api_tokens
    org = api_tokens.get(api_key_query)
    if org is not None:
        return org
    org = api_tokens.get(api_key_header)
    if org is not None:
        return org
    # since we are storing org in cookie, let us do a reverse
    # map lookup to see if there is a key for this org; only
    # for cookies
    if api_key_cookie is None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    k = list(api_tokens.keys())[list(api_tokens.values()).index(api_key_cookie)]
    if k is not None:
        return api_key_cookie
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
