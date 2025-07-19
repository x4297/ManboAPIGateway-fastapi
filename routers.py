from ipaddress import IPv4Address

from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import Authentication, Message, get_db_session
from message_sender import MessageSender
from settings import App1Config, CommonConfig
from models import SMSLogModel, StatusEnum
from throttle import ThrottleByMobile, ThrottleByIP


openapi_url = "/openapi.json" if CommonConfig.debug else None

# 为了在此添加中间件，改用FastAPI，而不是APIRouter
router = FastAPI(openapi_url=openapi_url)


@router.post("/app1", dependencies=[Depends(Authentication(App1Config))])
async def app1_send_message(request: Request, msg: Message = Depends(Message()), session: AsyncSession = Depends(get_db_session)):
    msg_sender = MessageSender(msg.mobile, msg.content, App1Config)

    sms_log = SMSLogModel(application=App1Config.application_name, mobile=msg.mobile, content=msg.content)

    try:
        await ThrottleByIP(config=App1Config)(IPv4Address(request.client.host), session)  # type: ignore
        await ThrottleByMobile(config=App1Config)(msg.mobile, session)

        r = await msg_sender.send_message()
        sms_log.status = StatusEnum.success  # type: ignore
    except Exception as e:
        sms_log.status = StatusEnum.failed  # type: ignore
        sms_log.comment = e.__repr__()
        r = {"code": 1, "msg": e.__repr__()}

    session.add(sms_log)
    await session.commit()

    return r


# 引入中间件，为了避免循环依赖，延迟导入
import middlewares
