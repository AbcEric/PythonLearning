#
# Python语句测试：采用class方式
#


# 1.生成器
class GeneratorDemo():
    # 斐波那契数列生成器:
    # 传统实现方式：当n很大时，系统开销大，执行时间长
    def fac1(self, n):
        result = []
        a, b = 0, 1
        while b < n:
            result.append(b)
            a, b = b, a+b
        return result

    # 生成器方式：更为简洁，每次只生成1个
    def fac2(self, n):
        a, b = 1, 1
        while a < n:
            yield a
            a, b = b, a+b

    def lifang(self, n):
        result = []
        for i in range(n):
            result.append(i ** 3)
        return result

    # for i, f in enumerate(fac1(10)):
    #     print(i, f)

    # 生成器取值：用next方法
    def GetByNext(self, num):
        f = self.fac2(num)
        print(next(f))
        print(next(f))
        print(next(f))
        print(next(f))

    # 或for循环
    def GetByFor(self, num):
        f = self.fac2(num)
        for i, v in enumerate(f):
            print(i, v)
# print(lifang(10000000))


# 2.字典：与顺序无关，不排序
# 根据键取值或反之，编码用数字表示，用"CH-CODE"方式好些!
class DictDemo(object):
    def __init__(self, dic={}, msg="", num=0):
        self.msg = msg
        self.dic = dic
        self.num = num      # 当前字典元素的总数

    # 字母统计计数：
    def get_charactor_count(self):
        count = {}
        for ch in self.msg:
            count.setdefault(ch, 0)         # 若字典中没有，就将值设为0
            count[ch] += 1
        return count

    # 根据key找对应的value：也可判断该key是否存在！
    def get_value(self, key):
        return self.dic.get(key)

    # 根据value找到对应的key：
    def get_key(self, value):
        for item in self.dic.items():
            if item[1] == value:
                return item[0]

    def add_key(self, key):
        if self.get_value(key) is None:         # 没有该key对应的value，即key不存在！
            # print("key is none", key)
            self.num += 1
            self.dic[key] = self.num

    def save_dict(self, filename="char_dict.txt"):
        pass

    def restore_dict(self, filename="char_dict.txt"):
        # 注意：要恢复num
        pass
    # keys(), values(), items()方法


# gen = GeneratorDemo()
# gen.GetByFor(10)



def DictTest():
    dic = DictDemo(dic={"name": "Eric", "height": 170, "gender": "male"},
               msg="Last Christmas, I give you my heart. But I never know ....")
    # dic = DictDemo()
    print(dic.get_charactor_count())
    print(dic.get_value("height"))
    print(dic.get_key(170))
    print(dic.get_value("A"))
    dic.add_key("A")
    dic.add_key("B")
    print(dic.get_value("B"))

    for ch in dic.msg:
        dic.add_key(ch)
        print(dic.get_value(ch), end=" ")
    print()
    print(dic.dic)

import numpy

x1, k1, x2, k2 = map(int, input().split())
v1, v2 = int(str(x1) * k1), int(str(x2) * k2)
print(v1, v2)
if v1 == v2:
    print("Equal")
elif v1 > v2:
    print("Greater")
else:
    print("Less")



def repeat(x, k):
    return x ** k

str = input("Please input 4 numbers, seperated by blank:")
num = str.split(" ")

if int(num[0])<1 or int(num[2])<1 or int(num[0])>10^9 or int(num[2])>10^9:
    exit(0)
if int(num[1])<1 or int(num[3])<1 or int(num[1])>50 or int(num[3])>50:
    exit(0)

n1 = repeat(int(num[0]), int(num[1]))
n2 = repeat(int(num[2]), int(num[3]))

if n1 == n2:
    print("Equal")
elif n1 > n2:
    print("Greater")
else:
    print("Less")