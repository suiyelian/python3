import  multiprocessing
import time, threading

# Python解释器直到所有线程都终止前仍保持运行。
# 对于需要长时间运行的线程或者需要一直运行的后台任务，
# 你应当考虑使用后台线程。 daemon=True 例如：
def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)

t = threading.Thread(target=countdown, args=(10,), daemon=True)
t.start()

#后台线程无法等待，不过，这些线程会在主线程终止时自动销毁。
# 除了如上所示的两个操作，并没有太多可以对线程做的事情。你无法结束一个线程，无法给它发送信号，无法调整它的调度，也无法执行其他高级操作。如果需要这些特性，
# 你需要自己添加。比如说，如果你需要终止线程，那么这个线程必须通过编程在某个特定点轮询来退出。

class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus %s'% n,  threading.current_thread().name)
            n -= 1
            time.sleep(5)

c = CountdownTask()
t = threading.Thread(target=c.run, args=(10,))
t.start()
c.terminate() # Signal termination
t.join()      # Wait for actual termination (if needed)

#线程的一个关键特性是每个线程都是独立运行且状态不可预测。
# 如果程序中的其他线程需要通过判断某个线程的状态来确定自己下一步的操作
# 这时线程同步问题就会变得非常棘手。为了解决这些问题，
# 我们需要使用 threading 库中的 Event 对象。
# Event 对象包含一个可由线程设置的信号标志，它允许线程等待某些事件的发生。
# 在初始情况下，event 对象中的信号标志被设置为假。如果有线程等待一个 event 对象
# ，而这个 event 对象的标志为假，那么这个线程将会被一直阻塞直至该标志为真。
# 一个线程如果将一个 event 对象的信号标志设置为真，
# 它将唤醒所有等待这个 event 对象的线程。
# 如果一个线程等待一个已经被设置为真的 event 对象，
# 那么它将忽略这个事件，继续执行。 下
# 边的代码展示了如何使用 Event 来协调线程的启动：

def countdown(n, started_evt):
    print('countdown starting')
    started_evt.set()
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)

# Create the event object that will be used to signal startup
started_evt = threading.Event()

# Launch the thread and pass the startup event
print('Launching countdown')
t = threading.Thread(target=countdown, args=(10,started_evt))
t.start()

# Wait for the thread to start
started_evt.wait()
print('countdown is running')

class PeriodicTimer:
    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cv = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run)
        t.daemon = True

        t.start()

    def run(self):
        '''
        Run the timer and notify waiting threads after each interval
        '''
        while True:
            time.sleep(self._interval)
            with self._cv:
                 self._flag ^= 1
                 self._cv.notify_all()

    def wait_for_tick(self):
        '''
        Wait for the next tick of the timer
        '''
        with self._cv:
            last_flag = self._flag
            while last_flag == self._flag:
                self._cv.wait()

# Example use of the timer
ptimer = PeriodicTimer(5)
ptimer.start()

# Two threads that synchronize on the timer
def countdown1(nticks):
    while nticks > 0:
        ptimer.wait_for_tick()
        print('T-minus', nticks)
        nticks -= 1

def countup(last):
    n = 0
    while n < last:
        ptimer.wait_for_tick()
        print('Counting', n)
        n += 1

threading.Thread(target=countdown1, args=(10,)).start()
threading.Thread(target=countup, args=(5,)).start()