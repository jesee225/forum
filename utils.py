import time


def format_time():
    fmt = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    return dt


def log(*args, **kwargs):
    # time.time() 返回 unix time
    fmt = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(format_time())
    dt = time.strftime(fmt, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)
