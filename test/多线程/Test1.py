import time, threading

# threading 库可以在单独的线程中执行任何的在 Python 中可以调用的对象。
# 你可以创建一个 Thread 对象并将你要执行的对象以 target 参数的形式提供给该对象。 下面是一个简单的例子：
# 新线程执行的代码:

def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')  # 将函数调用线程
t.start()   # 启动线程


print('thread %s ended.' % threading.current_thread().name)

# Python中的线程会在一个单独的系统级线程中执行（比如说一个 POSIX 线程或者一个 Windows 线程），这些线程将由操作系统来全权管理。线程一旦启动，
# 将独立执行直到目标函数返回。你可以查询一个线程对象的状态，
# 看它是否还在执行：is_alive()
if t.is_alive():
    print('Still running')
else:
    print('Completed')

t.join()  # 将一个线程加入到当前线程，并等待它终止

# 多线程和多进程最大的不同在于，多进程中，
# 同一个变量，各自有一份拷贝存在于每个进程中，互不影响
# ，而多线程中，所有变量都由所有线程共享，所
# 以，任何一个变量都可以被任何一个线程修改，
# 因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了。

balance = 0

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n
"""
def run_thread(n):
    for i in range(100000):
        change_it(n)

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
"""
# 加锁保护
balance = 0
lock = threading.Lock()

def run_thread(n):
    for i in range(100000):
        # 先要获取锁:
        lock.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()

print(balance)

import  multiprocessing
def loop():
    x = 0
    while True:
        x = x ^ 1

for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target=loop)
    t.start()

