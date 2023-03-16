import asyncio

from sqlalchemy import (Column, DateTime, ForeignKey, func, Integer, String)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String(200))
    create_date = Column(DateTime, server_default=func.now())
    bs = relationship("B")

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)
    a_id = Column(ForeignKey("a.id"))
    data = Column(String(200))


async def async_main():
    engine = create_async_engine(
        "mysql+aiomysql://testdb:123456@localhost:3306/holmes",
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    A(bs=[B(), B()], data="a1"),
                    A(bs=[B()], data="a2"),
                    A(bs=[B(), B()], data="a3"),
                ]
            )
        stmt = select(A).options(selectinload(A.bs))

        result = await session.execute(stmt)

        print("result==========", result)
        for a1 in result.scalars():
            print(a1)
            print(f"created at: {a1.create_date}")
            for b1 in a1.bs:
                print(b1)

        result = await session.execute(select(A).order_by(A.id))

        _a1 = result.scalars()
        print("_a1________", _a1)
        a1 = _a1.first()
        print("a1=====", a1)

        a1.data = "new data"

        await session.commit()

        # access attribute subsequent to commit; this is what
        # expire_on_commit=False allows
        print(a1.data)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(async_main())
