 特殊方法

class ObjectDict(dict):
    def __init__(self, *args, **kwargs):
        super(ObjectDict, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        value = self[name]
        if isinstance(value, dict):
            value = ObjectDict(value)
        return value

class WidgetShowLazyLoad(object):
    def fetch_complex_attr(self, attrname):
        '''可能是比较耗时的操作， 比如从文件读取'''
        return attrname

    def __getattr__(self, name):
        if name not in self.__dict__:
             self.__dict__[name] = self.fetch_complex_attr(name)
        return self.__dict__[name]


class adaptee(object):
    def foo(self):
        print('foo in adaptee')

    def bar(self):
        print('bar in adaptee')


class adapter(object):
    def __init__(self):
        self.adaptee = adaptee()

    def foo(self):
        print('foo in adapter')
        self.adaptee.foo()

    def __getattr__(self, name):
        return getattr(self.adaptee, name)



# __getattribute
"""
可以看出，每次通过实例访问属性，都会经过__getattribute__函数。
而当属性不存在时，仍然需要访问__getattribute__，不过接着要访问__getattr__。
  b  这就好像是一个异常处理函数。 
每次访问descriptor（即实现了__get__的类），都会先经过__get__函数。 
"""
class C(object):
    a = 'abc'

    def __getattribute__(self, *args, **kwargs):
        print("__getattribute__() is called")
        return object.__getattribute__(self, *args, **kwargs)

    #        return "haha"
    def __getattr__(self, name):
        print("__getattr__() is called ")
        return name + " from getattr"

    def __get__(self, instance, owner):
        print("__get__() is called", instance, owner)
        return self

    def foo(self, x):
        print(x)


class C2(object):
    d = C()




# 元类 创建类的类
#type(object):返回一个对象的类型，与object.__class__的值相同，
# type(name,bases,dict):创建一个新的type类型，name就是新class的name，
# 值存到__name__属性中，bases是tuple类型，值会存到__bases__中，dict的值存到__dict__中　

#　__prepare__
class OrderedClass(type):

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    # namespace就是class的__dict__,这个dict类型的对象已经被填充了相应的值
    def __new__(cls, name, bases, namespace, **kwds):
        print(name, bases)
        result = type.__new__(cls, name, bases, dict(namespace))
        print(dict(namespace))
        result.members = tuple(namespace)
        return result


class A(metaclass=OrderedClass):
    def one(self):
        pass

    def two(self):
        pass

    def three(self):
        pass

    def four(self):
        pass


# 创建一个类 函数type实际上是一个元类
MyShinyClass = type('MyShinyClass', (), {})


# 元类会自动将你通常传给‘type’的参数作为自己的参数传入
class UpperAttrMetaclass(type):
    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)

        # 复用type.__new__方法
        # 这就是基本的OOP编程，没什么魔法
        return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, uppercase_attr)



class UpperAttrMetaclass1(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)

# 元类会自动将你通常传给‘type’的参数作为自己的参数传入
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    '''返回一个类对象，将属性都转为大写形式'''
    #选择所有不以'__'开头的属性
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
    # 将它们转为大写形式
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
    #通过'type'来做类对象的创建
    return type(future_class_name, future_class_parents, uppercase_attr)#返回一个类

class Foo(object):
    __metaclass__ = upper_attr
    bar = 'bip'

def test():
    """

    :return:
    """
    print(hasattr(Foo, 'bar'))
    # 输出: False
    print(hasattr(Foo, 'BAR'))

def add(x:int, y:int) -> int:
    """

    :param x:
    :param y:
    :return:
    """
    print(test)
    return x + y

if __name__ == '__main__':
    print(help(add))
