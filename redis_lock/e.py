import time
from contextlib import contextmanager
from threading import Thread

from redis import Redis


r = Redis()
key = "yaooo"
lock_command = """
    if redis.call('hexists', KEYS[1], ARGV[1]) == 1 then
        redis.call('hincrby', KEYS[1], ARGV[1], 1)
        return 1
    end
    if redis.call('exists', KEYS[1]) == 1 then
        return 0
    else
        redis.call('hset', KEYS[1], ARGV[1], 1)
        redis.call('expire', KEYS[1], ARGV[2])
    end
    return 1
    """
unlock_command = """
    if redis.call('hexists', KEYS[1], ARGV[1]) == 0 then
        return nil
    end
    local count = redis.call('hincrby', KEYS[1], ARGV[1], -1)
    if (count > 0) then
        return 0
    else
        redis.call('del', KEYS[1])
        return 1
    end
    """


def add_lock(key, value, expire):
    locked = r.register_script(lock_command)
    print(locked(keys=[key], args=[value, expire]))
    print(r.hgetall(key))


def release_lock(key, value):
    unlock = r.register_script(unlock_command)
    print(unlock(keys=[key], args=[value]))
    print(r.hgetall(key))


@contextmanager
def redis_dist_lock(key, value=1, timeout=60, cli=Redis()):
    """
    redis分布式锁
    @param key:键
    @param value:值
    @param nx:键不存在才设置
    @param timeout:过期时间
    @param cli: redis client
    @return:
    """
    unlock_script = """
    if redis.call("get",KEYS[1]) == ARGV[1] then
        return redis.call("del",KEYS[1])
    else
        return 0
    end
    """
    lock = cli.set(key, value, nx=True, ex=timeout)
    try:
        yield lock
    finally:
        print("pre release", lock, r.get(key))
        if lock:
            unlock = cli.register_script(unlock_script)
            unlock(keys=[key], args=[value])
            print("after release", lock, r.get(key))


def l1():
    with redis_dist_lock(key=key, timeout=1) as lock:
        print("l1 get lock success")
        time.sleep(1.5)
        print("l1 lock blocked", lock, r.get(key))
        time.sleep(2)
        print("l1 lock blocked finish", lock, r.get(key))
    print("l1 finish")


def l2():
    time.sleep(1)
    with redis_dist_lock(key=key, timeout=100) as lock1:
        if not lock1:
            print("l2 get lock failed")
            time.sleep(0.5)
            return l2()
        else:
            print("l2 get lock success")
            for i in range(10):
                print("l2 lock", lock1, r.get(key))
                time.sleep(0.5)
    print("l2 finish", r.get(key))


if __name__ == '__main__':
    # t1 = Thread(target=l1)
    # t2 = Thread(target=l2)
    # t1.start()
    # t2.start()

    # add_lock("lock", "unique", 60)
    release_lock("lock", "unique")
