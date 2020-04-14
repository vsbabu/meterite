from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi

from starlette.responses import RedirectResponse, JSONResponse
from ..security import get_api_key
from .. import config

from ..main import app

# reference - https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680

router = APIRouter()

@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(config.Settings().api_key_name, domain=config.Settings().cookie_domain)
    return response


@router.get("/docs", summary="Swagger documentation")
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="API:" + app.title)
    response.set_cookie(
        config.Settings().api_key_name,
        value=api_key,
        domain=config.Settings().cookie_domain,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response


@router.get("/redocs", summary="Redocs documentation")
async def get_redocumentation(api_key: APIKey = Depends(get_api_key)):
    response = get_redoc_html(openapi_url="/openapi.json", title="API:" + app.title)
    response.set_cookie(
        config.Settings().api_key_name,
        value=api_key,
        domain=config.Settings().cookie_domain,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

@router.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(
        get_openapi(
            title=app.title, version=app.version, routes=app.routes, description=app.description
        )
    )
    return response


@router.get("/", include_in_schema=False)
async def homepage():
    return "Yeah, server is up, but if you need to use, go to /docs?x-auth-token=...."
