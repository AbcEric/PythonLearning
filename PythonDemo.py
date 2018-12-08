#
# Python语句测试
#
# 1. 生成器
#

# 斐波那契数列生成器:
# 传统实现方式：
def fac1(n):
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result

# 生成器方式：更为简洁
def fac2(n):
    a, b = 1, 1
    while a < n:
        yield a
        a, b = b, a+b

# for i, f in enumerate(fac1(10)):
#     print(i, f)

for i, f in enumerate(fac2(2)):
    print(i, f)

print(fac1(10))
print(fac2(10))