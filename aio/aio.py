import asyncio
import time


async def f():
    await asyncio.sleep(1)


async def f1():
    task = [f() for _ in range(3)]
    await asyncio.gather(*task)


async def f2():
    for _ in range(3):
        await f()


async def f3():
    await asyncio.wait([f() for _ in range(3)])


if __name__ == '__main__':
    start = time.time()
    asyncio.run(f3())
    print(time.time() - start)
