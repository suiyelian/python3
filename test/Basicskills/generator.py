# encoding:utf-8

from itertools import count
from itertools import islice
import time

counter = count(start=13)
print(next(counter))


# 可迭代对象使用iter函数转换，或者定义__iter__，__next__
# 迭代器实现斐波那契数列
class Fib:
    def __init__(self):
        self.prev = 0
        self.curr = 1

    def __iter__(self):
        return self

    def __next__(self):
        value = self.curr
        self.curr += self.prev
        self.prev = value
        return value


start = time.clock()
f = Fib()
list(islice(f, 0, 100))
end = time.clock()

print(str(end - start))


# 生成器实现斐波那契数列 生成器一定是迭代器（反之不成立）
def fib():
    prev, curr = 0, 1
    while True:
        yield curr
        prev, curr = curr, curr + prev


start = time.clock()
f = fib()
list(islice(f, 0, 100))
end = time.clock()

print(str(end - start))


# 生成器运行效率高一倍左右


def g3():  ##python 版本要大于3.3

    yield 'hello'
    return 'world'


g = g3()
print(next(g))
# print(next(g))

# 生成器支持的方法

"""
odd = class generator(object)
 |  Methods defined here:
 ......
 |  close(...) 手动关闭生成器函数，后面的调用会直接返回StopIteration异常
 |      close() -> raise GeneratorExit inside generator.
 |
 |  send(...)生成器函数最大的特点是可以接受外部传入的一个变量，并根据变量内容计算结果后返回。
 |      send(arg) -> send 'arg' into generator,
 |      return next yielded value or raise StopIteration.
 |
 |  throw(...)用来向生成器函数送入一个异常，可以结束系统定义的异常，或者自定义的异常。
     throw()后直接跑出异常并结束程序，或者消耗掉一个yield，或者在没有下一个yield的时候直接进行到程序的结尾。
 |      throw(typ[,val[,tb]]) -> raise exception in generator,
 |      return next yielded value or raise StopIteration.
 """


def gen():
    value = 0
    while True:
        receive = yield value
        if receive == 'e':
            break
        value = 'got: %s' % receive


g = gen()
print(g.send(None))
print(g.send('aaa'))
print(g.send(3))


# print(g.send('e'))

def gen1():
    while True:
        try:
            yield 'normal value'
            yield 'normal value 2'
            print('here')
        except ValueError:
            print('we got ValueError here')
        except TypeError:
            break


g = gen1()
print(next(g))
print(g.throw(ValueError))
print(next(g))


# print(g.throw(TypeError))
def flatten(nested):
    try:
        # 如果是字符串，那么手动抛出TypeError。
        if isinstance(nested, str):
            print('here3')
            raise TypeError
        for sublist in nested:
            print('here1')
            # yield flatten(sublist)
            for element in flatten(sublist):
                # yield element
                print('here2')
                print('got:', element)
    except TypeError:
        print('here')
        yield nested


L = ['aaadf', [1, 2, 3], 2, 4, [5, [6, [8, [9]], 'ddf'], 7]]
for num in flatten(L):
    print(num)

