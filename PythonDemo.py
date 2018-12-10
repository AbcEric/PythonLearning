#
# Python语句测试
#
# 1. 生成器
#

# 斐波那契数列生成器:
# 传统实现方式：当n很大时，系统开销大，执行时间长
def fac1(n):
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result

# 生成器方式：更为简洁，每次只生成1个
def fac2(n):
    a, b = 1, 1
    while a < n:
        yield a
        a, b = b, a+b

def lifang(n):
    result = []
    for i in range(n):
        result.append(i ** 3)
    return result

# for i, f in enumerate(fac1(10)):
#     print(i, f)

# 生成器取值：用next方法
f = fac2(10)
print(next(f))
print(next(f))
print(next(f))
print(next(f))

# 或for循环
f = fac2(10)
for i, v in enumerate(f):
    print(i, v)

# print(lifang(10000000))