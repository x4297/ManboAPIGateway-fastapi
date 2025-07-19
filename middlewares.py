from ipaddress import IPv4Address

from fastapi import Request, Response

from routers import router
from models import AccessLogModel
from db import session_maker


@router.middleware("http")
async def access_log_middleware(request: Request, call_next):
    response = await call_next(request)  # type: Response

    async with session_maker() as session:
        log = AccessLogModel(
            status_code=response.status_code,
            method=request.method,
            url=request.url.__repr__(),
            source_ip=IPv4Address(request.client.host)  # type: ignore
        )

        session.add(log)
        await session.commit()

    return response
