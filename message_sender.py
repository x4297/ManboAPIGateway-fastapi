from typing import Type

import httpx

from exceptions import SendMessageException
from settings import CommonConfig, BaseConfig


class MessageSender:
    # TODO: modify code according to the actual situation
    def __init__(self, mobile, content, config: Type[BaseConfig]):
        self.mobile = mobile
        self.content = content
        self.Config = config

    async def send_message(self):
        headers = {
            "appid": CommonConfig.appid,
            "secret": CommonConfig.secret,
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
        }

        data = {
            "mobile": self.mobile,
            "content": self.content,
        }

        async with httpx.AsyncClient() as client:
            r = await client.post(url=CommonConfig.url_send_message, headers=headers, data=data)

        try:
            r.raise_for_status()
        except Exception as e:
            raise SendMessageException(e)

        r = r.json()

        if r["success"] != True:
            raise SendMessageException(r["msg"])

        return r
