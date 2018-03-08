# encoding: utf-8

# 改变对象的字符串显示 重新定义它的 __str__() 和 __repr__() 方法

class Pair:
    """
    __repr__() 方法返回一个实例的代码表示形式
    __str__() 方法将实例转换为一个字符串
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)


def test1():
    p = Pair(3, 4)
    print('p is {0!r}'.format(p))
    print('p is {0}'.format(p))


# 为了自定义字符串的格式化，我们需要在类上面定义 __format__() 方法

_formats = {
    'ymd': '{d.year}-{d.month}-{d.day}',
    'mdy': '{d.month}/{d.day}/{d.year}',
    'dmy': '{d.day}/{d.month}/{d.year}'
    }


class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)


def test2():
    d = Date(2012, 12, 21)
    format(d)
    format(d, 'mdy')
    print('The date is {:ymd}'.format(d))
    print('The date is {:mdy}'.format(d))


# 主要是用来当成简单的数据结构的类而言，
# 你可以通过给类添加 __slots__ 属性来极大的减少实例所占的内存,非必要不推荐使用

class Date1:
    __slots__ = ['year', 'month', 'day']

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


# 创建可管理的属性

class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')

        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")

def test3():
    a = Person('Guido')
    print(a.first_name)

# 为了调用父类(超类)的一个方法，可以使用 super() 函数

class A:
    def __init__(self):
        self.x = 0

class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1

# super() 的另外一个常见用法出现在覆盖Python特殊方法的代码中
# Python会在MRO列表上从左到右开始查找基类，直到找到第一个匹配这个属性的类为止。


class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # Delegate attribute lookup to internal obj
    def __getattr__(self, name):
        return getattr(self._obj, name)

    # Delegate attribute assignment
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)  # Call original __setattr__
        else:
            setattr(self._obj, name, value)


# 在子类中，你想要扩展定义在父类中的property的功能
class Person1:
    def __init__(self, name):
        self.name = name

    # Getter function
    @property
    def name(self):
        return self._name

    # Setter function
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    # Deleter function
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")


class SubPerson(Person1):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)

def test4():
    p = Person1("buyunhui")
    print(p._name + ".")
    s = SubPerson('Guido')
    print(s.name)
    s.name = 'Larry'
    print(s.name)

# 创建新的类或实例属性
"""
一个描述器就是一个实现了三个核心的属性访问操作(get, set, delete)的类，
分别为 __get__() 、__set__() 和 __delete__() 
这三个特殊的方法。 这些方法接受一个实例作为输入，之后相应的操作实例底层的字典。
"""

# Descriptor attribute for an integer type-checked attribute
class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

"""
# Descriptor for a type-checked attribute
class Typed:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected ' + str(self.expected_type))
        instance.__dict__[self.name] = value
    def __delete__(self, instance):
        del instance.__dict__[self.name]

# Class decorator that applies it to selected attributes
def typeassert(**kwargs):
    def decorate(cls):
        for name, expected_type in kwargs.items():
            # Attach a Typed descriptor to the class
            setattr(cls, name, Typed(name, expected_type))
        return cls
    return decorate

# Example use
@typeassert(name=str, shares=int, price=float)
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
"""

# 定义一个延迟属性的一种高效方法是通过使用一个描述器类

class lazyproperty():
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


# 不能更改属性值版本


def lazyproperty1(func):
    name = '_lazy_' + func.__name__
    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value
    return lazy

import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty1
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty1
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius

def test6():
    c = Circle(4.0)
    print(c.radius)
    print(c.area)

class Point:
    x = Integer('x')
    y = Integer('y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

def test5():
    p = Point(2, 3)
    print(p.x, p.y)
    p.y = 5

if __name__ == '__main__':
    test1()
    test2()

