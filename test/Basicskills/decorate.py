# encoding:utf-8


def dec(func):
    print("dec")

    def in_dec(*arg):
        print("in_dec")
        if len(arg) == 0:
            return 0

        for val in arg:
            if not isinstance(val, int):
                return 0

        return func(*arg)

    return in_dec


@dec
def my_sum(*ary):
    print("my_sum")
    return sum(ary)

# my_ = dec(my_sum)
print(my_sum(1, 2, 3, 4, 5, 6))


def deco(func):
    def in_deco():
        print('in_deco')
        return func()
    print("call deco")
    return in_deco


@deco
def bar():
    print("in bar")

print(bar())

def EntryFunc(func):
    def wrapper(*args, **kw):
         print("entry function:%s" % func.__name__)
         return func(*args, **kw)
         print("Exited function:%s" % func.__name__)
    return wrapper

@EntryFunc
def test1(a, b):
    return (a + b)

@EntryFunc
def test2(a, b):
    return (a + b)

print(test1(1,2))
print(test2(1,2))
print(test1.__name__)

