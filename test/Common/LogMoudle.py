# encoding:utf-8

import logging
import sys
import threading
import time

Lock = threading.Lock()


class LogSingleton():
    __LogInstance = None

    def __init__(self):

        pass

    def __new__(cls, *args, **kwargs):
        print(cls.__LogInstance)
        if not cls.__LogInstance:
            try:
                Lock.acquire()
                # double check
                if not cls.__LogInstance:
                    cls.__LogInstance = logging.getLogger("Log")
            finally:
                Lock.release()
        return cls.__LogInstance


def GetLog():
    # 获取logger实例，如果参数为空则返回root logger
    logger = LogSingleton()
    print(logger)

    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

    # 文件日志
    file_handler = logging.FileHandler("test.log")
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值

    # 为logger添加的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 指定日志的最低输出级别，默认为WARN级别
    logger.setLevel(logging.INFO)
    return logger

log = GetLog()


# 类装饰器
class EntryExit(object):

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        start = time.clock()
        log.info("Entering function name:%s", self.f.__name__)
        returnTmp = self.f(*args, **kwargs)
        end = time.clock()
        log.info("end function %s and cost time:%s", self.f.__name__, (end - start))
        return returnTmp


# 函数装饰器
def entryExit(func):
    def wrapper(*args, **kwargs):
        start = time.clock()
        log.info("Entering function name:%s", func.__name__)
        returnTmp = func(*args, **kwargs)
        end = time.clock()
        log.info("end function %s and cost time:%s", func.__name__, (end - start))
        return returnTmp
    return wrapper


@entryExit
def testClass(a, b):
    return(a + b)


if __name__ == "__main__":
    print(testClass(1, 2))


















