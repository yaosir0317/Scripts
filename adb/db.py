import asyncio
import uuid
from asyncio import current_task
from _datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import (
    INTEGER,
    Column,
    DateTime,
    String,
    delete,
    Text, select, insert, update,
)
from sqlalchemy.orm import declarative_base

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_async_engine(
    f"mysql+asyncmy://root:123456@localhost:3306/yao?charset=utf8mb4",  # noqa
    echo=False,
    echo_pool=True,
    future=True,
    pool_size=50,
    max_overflow=50,
    pool_recycle=3600,
    pool_timeout=30,
)

async_session_factory = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True,
)
session = async_scoped_session(async_session_factory, scopefunc=current_task)


class TT(BaseModel):
    id: Optional[uuid.UUID] = uuid.uuid4()
    name: str


class Shop(Base):

    __tablename__ = "shop"

    id = Column(INTEGER, primary_key=True, autoincrement=True, comment="主键id")
    batch_prop = Column(String(100), doc="物流或其他属性 名称")
    shop_id = Column(INTEGER, nullable=True, comment="店铺id")
    original_vid = Column(String(100), doc="原始值 - 上货需要的")
    text = Column(String(100), doc="显示值名称")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, doc="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, doc="更新时间")


async def insert_yao(num):
    await session.execute(insert(Shop).values(batch_prop=f"yao{num}", shop_id=num, original_vid=num, text=num))
    await session.commit()


async def bulk_insert_yao(num_list: list):
    objs = [dict(batch_prop=f"yao{i}", shop_id=i, original_vid=i, text=i) for i in num_list]
    a = await session.execute(
        insert(Shop), objs
    )
    print(a.inserted_primary_key_rows)
    await session.commit()


async def select_yao():
    ret = await session.execute(select(Shop))
    for i in ret.scalars():
        print(i.__dict__)


async def delete_yao():
    ret = await session.execute(select(Shop).where(Shop.id == 17))
    # print(ret.scalar_one().__dict__)
    ret = ret.scalars().one()
    print(ret.__dict__)
    await session.delete(ret)
    await session.commit()


async def delete_mu():
    query = Shop.id.in_([23, 24, 25])
    await session.execute(
        delete(Shop).where(query)
    )
    await session.commit()


async def select_yao2():
    ret = await session.execute(
        select(Shop.id, Shop.text).where(Shop.id.in_([30, 31]))
    )
    for i in ret.mappings():
        print(i)


async def main():
    await select_yao()
    await select_yao2()


if __name__ == '__main__':
    asyncio.run(main())
