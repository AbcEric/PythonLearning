from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np


# 四个数通过加减乘除得到24点：如何判读是否能做到？如何最快找到，以及找到最多的方法

# double a[5]

# define EPS 1e-6
# 判断浮点数是否为0
# def isZero(x):
#    return fabs(x) <= EPS

# 数组a中n个数能否算出24
def count24(a, n):
    # 数组中仅有一个元素
    if n == 1:
        if a[0] == 24:
            return True
        else:
            return False

    # double b[5];
    b = [0]*5

    # 枚举两个数的组合
    for i in range(0,n-1):
        for j in range(i+1,n):
            m=0
            # 将剩下的n-2个数存放到数组b中
            for k in range(0,n):
                if k!=i and k!=j:
                    m = m+1
                    b[m]=a[k]

            # 元素b[m]是a[i]和a[j]相加
            b[m]=a[i]+a[j]
            if count24(b,m+1):
                print("+:", b)
                return True

            # 相减
            b[m]=a[i]-a[j]
            if count24(b,m+1):
                print("-:",b)
                return True
            b[m]=a[j]-a[i]
            if count24(b,m+1):
                print("-:",b)
                return True

            # 相乘:
            b[m]=a[i]*a[j]
            if count24(b,m+1):
                print("*:",b)
                return True

            # 相除:
            if a[j] !=0:
                b[m]=a[i]/a[j]
                if count24(b,m+1):
                    print("/:", b)
                    return True

            if a[i] !=0:
                b[m]=a[j]/a[i]
                if count24(b,m+1):
                    print("/:", b)
                    return True

    return False


# 判读是否为丑数：只能是2,3,5的倍数
def IsUgly(i):
    if i < 0:
        return False

    while i % 2 == 0:
        i = i/2
    while i % 3 == 0:
        i = i/3
    while i % 5 == 0:
        i = i/5

    if i == 1:
        return True
    else:
        return False

# 猴子上山：递归求解
def NumberCount(i):
    if i == 1 or i == 2:
        return 1
    elif i == 3:
        return 2
    elif i <= 0:
        return 0

    return NumberCount(i-1) + NumberCount(i-3)

#print(NumberCount(30))
#print(IsUgly(14))

a = [4,3,1,7]
print(a)
print(count24(a, 4))

exit(0)


iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75

#df['species'] = pd.Factor(iris.target, iris.target_names)
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
df.head()

train, test = df[df['is_train']==True], df[df['is_train']==False]

features = df.columns[:4]
clf = RandomForestClassifier(n_jobs=2)
y, _ = pd.factorize(train['species'])
clf.fit(train[features], y)

preds = iris.target_names[clf.predict(test[features])]

print("Print Result:")
print(pd.crosstab(test['species'], preds, rownames=['actual'], colnames=['preds']))
print("...")

from pandas import Series,DataFrame
df = DataFrame({'类别':['水果','水果','水果','蔬菜','蔬菜','肉类','肉类'],
                '产地':['美国','中国','中国','中国','新西兰','新西兰','美国'],
                '水果':['苹果','梨','草莓','番茄','黄瓜','羊肉','牛肉'],
               '数量':[5,5,9,3,2,10,8],
               '价格':[5,5,10,3,3,13,20]})
print(df)

print(pd.crosstab(df['类别'],df['产地'],margins=True))