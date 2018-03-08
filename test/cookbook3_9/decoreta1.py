from functools import wraps, partial
import logging
# 带参数
def logged1(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)

    return wrapper

# Example use
@logged1
def add(x, y):
    return x + y

@logged1(level=logging.CRITICAL, name='example')
def spam():
    print('Spam!')