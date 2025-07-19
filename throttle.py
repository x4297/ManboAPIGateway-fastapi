from ipaddress import IPv4Address
from typing import Type
from datetime import datetime, timezone, timedelta

from sqlalchemy.sql import select, func
from sqlalchemy.ext.asyncio import  AsyncSession

from models import AccessLogModel, SMSLogModel
from settings import BaseConfig
from exceptions import ThrottleByIPException, ThrottleByMobileException


class ThrottleByIP:
    def __init__(self, config: Type[BaseConfig]):
        self.config = config

    async def __call__(self, ip: IPv4Address, session: AsyncSession):
        res = await session.execute(
            select(func.count()).select_from(AccessLogModel)
            .where(
                AccessLogModel.date_time > datetime.now(timezone.utc) - timedelta(
                    seconds=self.config.throttle_ip_duration)
            ).where(AccessLogModel.source_ip == ip)
        )

        if res.one()[0] >= self.config.throttle_ip_limit:
            raise ThrottleByIPException("此IP请求速率过快")


class ThrottleByMobile:
    def __init__(self, config: Type[BaseConfig]):
        self.config = config

    async def __call__(self, mobile: str, session: AsyncSession):
        res = await session.execute(
            select(func.count()).select_from(SMSLogModel)
            .where(
                SMSLogModel.date_time > datetime.now(timezone.utc) - timedelta(
                    seconds=self.config.throttle_mobile_duration)
            ).where(SMSLogModel.mobile == mobile).where(SMSLogModel.application == self.config.application_name)
        )

        if res.one()[0] >= self.config.throttle_mobile_limit:
            raise ThrottleByMobileException("此手机号发送频率过高")
