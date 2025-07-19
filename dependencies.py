from typing import Annotated, Type

from fastapi import Body, HTTPException, status, Request

from settings import BaseConfig
from db import session_maker


class Message:
    def __call__(
        self,
        mobile: Annotated[str, Body(pattern="^\\d{11}(,\\d{11})*$")],
        content: Annotated[str, Body(max_length=2048)]
    ):
        self.mobile = mobile
        self.content = content

        return self


class Authentication:
    def __init__(self, config: Type[BaseConfig]):
        self.config = config

    def __call__(
        self,
        request: Request,
        appid: Annotated[str, Body()],
        secret: Annotated[str, Body()],
    ):
        if self.config.authentication.get(appid, None) != secret:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="appid或secret错误")

        if request.client.host not in self.config.allowed_ips:  # type: ignore
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ip地址未在白名单中")


async def get_db_session():
    session = session_maker()
    try:
        yield session
    finally:
        await session.close()
