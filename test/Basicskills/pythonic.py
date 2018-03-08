# -*- coding: utf-8 -*-

# 交换值
a = 1
b = 2
a, b = b, a
print(a, b)

# 链式比较
print(1 <= b <= a < 10)  # True


# 真值判断
"""
简而言之，Python的写法就是对于任意对象，直接判断其真假，
无需写判断条件，这样既能保证正确性，又能减少代码量
真	               假
True	          False
任意非空字符串	      空的字符串 ''
任意非0数字	      数字0
任意非空容器	      空的容器 [] () {} set()
其他任意非False	  None
"""


"""
善用内置函数：any all reversed 

"""
# 列表反转

L =[1,2,3,4,5]
rl = reversed(L) #返回一个迭代器
print(rl)

# 列表推倒式
# 当读者能够清晰理解你这条语句是要生成一个列表，除此以外什么都没有做的时候。
old_list = [1, 2]
new_list = [v for v in old_list if v > 0]
print(new_list)


# 字符串列表的连接
strList = ["Python", "is", "good"]
res = ' '.join(strList)  # Python is good
print(res)

# 列表求和，最大值，最小值，乘积
numList = [1,2,3,4,5]
Sum = sum(numList)  #sum = 15
maxNum = max(numList) #maxNum = 5
minNum = min(numList) #minNum = 1

from operator import mul
from functools import reduce

prod = reduce(mul, numList) #prod = 120
print(prod)

# 获取字典值时
dic = {'name': 'Tim', 'age': 23}
dic['workage'] = dic.get('workage', "自定义值") + "test"
print(dic)

# for else 语句

for x in range(1, 5):
    if x == 5:
        print('find 5')
        break
else:
    print('can not find 5!')

# 使用迭代器，生成器,装饰器


class AnyIter(object):
    def __init__(self, data, safe=False):
        """ The initialization of iterators """
        self.safe = safe
        self.iter = iter(data)
    def __iter__(self):
        """ return a iterator """
        return self

    def __next__(self, count=1):
        """ Return arbitrary numbers of elements """
        retval = []
        for item in range(count):
            try:
                retval.append(self.iter.__next__())
            except StopIteration:
                if self.safe:
                    break
                else:
                    raise    # reraise the exception again
        return retval


if __name__ == '__main__':
    a = AnyIter(range(10), True)
    b = iter(a)
    for item in range(1, 5):
        print('{}:{}'.format(item, a.__next__(item)))


# 使用with
"""
关闭一个文件
释放一个锁
创建一个临时的代码补丁
在特殊环境中运行受保护的代码
"""
