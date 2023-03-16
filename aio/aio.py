import asyncio
import time


async def reade_db() -> str:
    await asyncio.sleep(1.5)
    return "db"


async def reade_cache() -> int:
    await asyncio.sleep(1)
    return 3


async def reade_es():
    await asyncio.sleep(1)
    return "es"


async def f1():
    task = [reade_db(), reade_cache(), reade_es()]
    g = await asyncio.gather(*task)
    print(g)


async def f2():
    db = await reade_db()
    cache = await reade_cache()
    es = await reade_es()
    print(db, cache, es)


async def f3():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(reade_db())
        task2 = tg.create_task(reade_cache())
        task3 = tg.create_task(reade_es())
    print(task1, task2, task3)


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(f3())
    print(time.perf_counter() - start)
