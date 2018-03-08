import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

s = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s)

dates = pd.date_range('20170101',periods=6)
print(dates)

# 创建一个数据表
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
print(df)
df2 = pd.DataFrame({'A': 1,
                    'B': pd.Timestamp('20130102'),
                    'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                    'D': np.array([3] * 4,dtype='int32'),
                    'E': pd.Categorical(["test", "train", "test", "train"]),
                    'F': 'foo'})
print(df2, df2.dtypes,df.describe())

# 查看数据 df2.head() df2.tail(3)  df.describe()(简要统计)
print(df2.tail(3), df2.head(), df.describe())

#　显示数据框的索引，列名和值　df2.index

print(df2.index)

# 数据转置

print(df2)

print(df2.sort_index(axis=1, ascending=False))

# 对于选择数据和设置数据来说，标准的python和numpy表达式非常直观而且对于交互式
# 工作来说很难进行的，对于应用性代码来说，我们比较推荐最优化的pandas数据获取方法，
# 例如.at, .iat, .loc, .iloc and .ix

"""
print(df2["A"], df2.A)
print(df2[0:3])

print("===")
# 用标签来截取一行数据
print(dates[0])
print(df.loc[dates[1]])
print("===")
print(pd.date_range('20130102', periods=6))

s1 = pd.Series([1,2,3,4,5,6], index=pd.date_range('20130102', periods=6))
df['F'] = s1
df.at[dates[0],'A'] = 0
df.loc[:,'D'] = np.array([5] * len(df))
"""
df.reindex(index=dates[0:4], columns=list(df.columns) + ['E'])
df.loc[dates[0]:dates[1],'E'] = 1
print(df)

print(df.dropna(how='any'))

# 填充丢失的值（NA值） 判断是否NA值（isna）

df.fillna(value=5)

s = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)
print(dates,s)

print(df)
print(df.apply(np.cumsum))
s = pd.Series(np.random.randint(0, 7, size=10))
print(s)
print(s.value_counts())
left = pd.DataFrame({'key': ['foo', 'fo'], 'lval': [1, 2]})
right = pd.DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})
print(pd.merge(left, right, on='key'))

tuples = list(zip(*[['bar', 'bar', 'baz', 'baz',
                     'foo', 'foo', 'qux', 'qux'],['one', 'two', 'one', 'two',
                     'one', 'two', 'one', 'two']]))
print(tuples)

index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])

print(index)

df = pd.DataFrame(np.random.randn(8, 2), index=index, columns=['A', 'B'])

print(df)
df2 = df[:4]
print(df2)


df = pd.DataFrame({'A' : ['one', 'one', 'two', 'three'] * 3,
'B' : ['A', 'B', 'C'] * 4,
'C' : ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'] * 2,
'D' : np.random.randn(12),
'E' : np.random.randn(12)})

print(df)
print(pd.pivot_table(df, values='D', index=['A', 'B'], columns=['C']))

rng = pd.date_range('1/1/2012', periods=100, freq='S')
print(rng)
ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)
print(ts)
print(ts.resample('5Min').sum())

prng = pd.period_range('1990Q1', '2000Q4', freq='Q-NOV')

print(prng)
ts = pd.Series(np.random.randn(len(prng)), prng)
ts.index = (prng.asfreq('M', 'e') + 1).asfreq('H', 's') + 9
print(ts)

df = pd.DataFrame({"id":[1,2,3,4,5,6], "raw_grade":['a', 'b', 'b', 'a', 'a','e']})
df["grade"] = df["raw_grade"].astype("category")
df["grade"].cat.categories = ["very good", "good", "very bad"]
print(df["grade"])


print(df.sort_values(by="grade"))

df.to_csv('foo.csv')
csvT = pd.read_csv('foo.csv')
print(csvT)
df.to_excel('foo.xlsx', sheet_name='Sheet1')
