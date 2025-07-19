from datetime import datetime, timezone
from ipaddress import IPv4Address, IPv6Address
import enum

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.types import BigInteger, SmallInteger, VARCHAR, CHAR, Enum
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import INET, TIMESTAMP


class StatusEnum(enum.Enum):
    success = "success"
    failed = "failed"


class Base(AsyncAttrs, DeclarativeBase):
    pass


class AccessLogModel(Base):
    __tablename__ = "log_access"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    status_code: Mapped[int] = mapped_column(SmallInteger)  # response status code
    method: Mapped[str] = mapped_column(CHAR(16))
    url: Mapped[str] = mapped_column(VARCHAR(2048))
    date_time: Mapped[datetime] = mapped_column(TIMESTAMP(True), default=lambda: datetime.now(timezone.utc))
    source_ip: Mapped[IPv4Address | IPv6Address] = mapped_column(INET)
    family: Mapped[str] = mapped_column(CHAR(5), default="inet4")


class SMSLogModel(Base):
    __tablename__ = "log_sms"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    application: Mapped[str] = mapped_column(CHAR(64), index=True)
    mobile: Mapped[str] = mapped_column(CHAR(16), index=True)
    content: Mapped[str] = mapped_column(VARCHAR(2048))
    status: Mapped[str] = mapped_column(Enum(StatusEnum))  # sucess or failed
    comment: Mapped[str | None] = mapped_column(VARCHAR(2048), nullable=True, default=None)  # error message
    date_time: Mapped[datetime] = mapped_column(TIMESTAMP(True), default=lambda: datetime.now(timezone.utc))
