#
# recursion algorithms：
#

# 1.猴子爬山问题：
def num(n):
    if n == 1 or n == 2:
        return 1

    if n == 3:
        return 2

    return num(n - 1) + num(n - 3)

# 2.数字通过加减乘除凑成24！
'''
1).如何记录递归过程? 显示具体的方法，含括号等（采用堆栈？）
2).采用了resultList外部变量，且只记录了最末两个数！得到最终2个数的情况还有多种方法！同时需去掉重复的方法，如[6,6,6,6],先加还是后加；
可对比 http://www.zhongguosou.com/game_lookup_tools/game_24_point.html
3).Get24()外部调用后无返回值，Get()内部递归调用又有返回值？ 本身可能未返回，若增加返回，会出现结果不完整。
4).逆波兰算术用运行符位置来代替括号的组合方式，用枚举法，一共5种?
'''

resultList = []
# 记录结果：避免重复
def AddResult(nList):
    for i in range(len(resultList)):
        if resultList[i] == nList or resultList[i] == [nList[1], nList[0]]:
            return False
    resultList.append(nList)
    return True

# 凑24
def Get24(nList):
    num = len(nList)

    # 结束条件：2个数加减乘除为24！
    if num == 2:
        if nList[1] != 0:
            if nList[0] + nList[1] == 24 or abs(nList[0] - nList[1]) == 24 or nList[0] * nList[1] == 24 or nList[0] / nList[1] == 24:
                # 以最终两个数来判断，会出现部分方法的遗漏，会有多种办法得到这两个数！
                AddResult(nList)
                return True
        if nList[0] != 0:
            if nList[0] + nList[1] == 24 or abs(nList[0] - nList[1]) == 24 or nList[0] * nList[1] == 24 or nList[1] / nList[0] == 24:
                AddResult(nList)
                return True
        return False
    else:
        # 两两组合任意两个数后递归调用: range()默认从0开始，步长为1，到指定数结束，但不包括指定数！
        for i in range(num-1):
            for j in range(i+1, num):
                nextList = GetnextLists(nList, i, j)
                for k in range(len(nextList)):
                    if Get24(nextList[k]):
                        #print(nList, nextList[k])
                        #找到一个后，继续查找？
                        break

# 对指定位置两个数进行加减乘除后，返回可能的列表
def GetnextLists(nList, i, j):
    item = [0]*(len(nList)-1)
    nextLists = []

    # 可简化为：item[i] = nList[i] + nList[j], item[j] = nList的最后一个数，其余值均不变！不需循环(要剔除最后一个数已经使用的情况？)
    for k in range(0, len(nList)-1):
        if k < i:
            item[k] = nList[k]
        elif k == i:
            item[k] = nList[i] + nList[j]
        elif k > i and k < j:
            item[k] = nList[k]
        elif k >= j:
            item[k] = nList[k+1]

    #采用深拷贝，避免为引用，item值改变后会全部改变，不能记录历史情况：
    nextLists.append(item.copy())

    item[i] = nList[i] * nList[j]
    nextLists.append(item.copy())
    item[i] = nList[i] - nList[j]
    nextLists.append(item.copy())
    item[i] = nList[j] - nList[i]
    nextLists.append(item.copy())

    if nList[j] != 0:
        item[i] = nList[i] / nList[j]
        nextLists.append(item.copy())
    if nList[i] != 0:
        item[i] = nList[j] / nList[i]
        nextLists.append(item.copy())

    return nextLists

# Get24()的第二种方法：简单些，计算不完整，没有全排列，只考虑了第一个数和后面每个的加减乘除的情况！
number = []
def PointsGame(n):
    if n == 1:
        if number[0] == 24:
            print("OK:", number)
            return True
        else:
            #print("NO:", number[0])
            return False

    for i in range(n):
        for j in range(i+1, n):
                a = number[i]
                b = number[j]
                number[j] = number[n-1]     # 把最后一个数填到被处理的第二个数j处
                print(n, number, a, b)
                number[i] = a + b
                if PointsGame(n - 1):
                    break
                    #return True
                number[i] = a - b
                if PointsGame(n - 1):
                    break
                    return True
                number[i] = b - a
                if PointsGame(n - 1):
                    break
                    return True
                number[i] = a * b
                if PointsGame(n - 1):
                    break
                    return True
                #if b != 0 and a%b == 0:
                if b != 0:
                    number[i] = a / b
                    if PointsGame(n - 1):
                        break
                        return True

                #if a != 0 and b%a == 0:
                if a != 0:
                    number[i] = b / a
                    if PointsGame(n - 1):
                        break
                        return True

                #回朔
                number[i] = a
                number[j] = b

        return False


# 3.字符串的去重全排列：参考https://blog.csdn.net/lemon_tree12138/article/details/50986990
# 若采用非递归算法，关键在于找到替换点和被替点；
# 用于模拟static变量，记录全局变量
class GlobalPara:
    num = 0
    def add(self):
        GlobalPara.num += 1

# 需要2个参数: pos表示当前位置，从0开始一直移动到最末一位。
# 例如：E=(a,b,c), 则perm(E) = a.perm(b,c) + b.perm(a,c) + c.perm(a,b) 先交换
# 其中，a.perm(b,c) = ab.perm(c) + ac.perm(b) = abc + acb依次递归进行
gp = GlobalPara()
def Perm(pszStr, pos):
    # 字符串长度，即末尾位置
    last = len(pszStr)
    if pos == last:
        gp.add()
        print("第", gp.num, "个排列:", pszStr)
    else:
        # 第i个数分别与它后面的数字交换就能得到新的排列:有问题！
        for i in range(pos, last):
            # 判断是否重复：
            if IsSwap(pszStr, pos, i):
                # 每次交换之后要恢复为原状
                pszStr = strSwap(pszStr, i, pos)
                Perm(pszStr, pos + 1)
                pszStr = strSwap(pszStr, i, pos)

# 去掉重复符号的全排列：在交换之前可以先判断两个符号是否相同，或者已经交换过
def IsSwap(pszStr, nBegin, nEnd):
    for i in range(nBegin, nEnd):
        #print(i,pszStr[i],pszStr[nEnd])
        # 要和nEnd的值不同才交换nBegin和nEnd值，只要二者间已有过nEnd的值，说明之前已经交换过，也不用再交换
        if pszStr[i] == pszStr[nEnd]:
            return False
    return True

# 字符串指定位置交换：string不能直接修改值！需要转换为List再拼接。
# 在python中，传递的都是对象的引用，即传址
# 对于不可变对象（list、dict等）作为函数参数，相当于C系语言的值传递；
# 对于可变对象（string、tuple和number）作为函数参数，相当于C系语言的引用传递。
# 如果要想修改新赋值后原对象不变，则需要用到python的copy模块，即对象拷贝，对象拷贝又包含浅拷贝和深拷贝。
def strSwap(str, i, j):
    if i not in range(len(str)) or j not in range(len(str)):
        return str

    strlist = list(str)
    strlist[i], strlist[j] = strlist[j], strlist[i]

    return "".join(strlist)


# 4.采用堆栈计算逆波兰表示法（Reverse Polish notation，RPN）:如何用递归实现？
# 由波兰数学家扬·武卡谢维奇1920年引入的数学表达式方式，在逆波兰记法中，所有操作符置于操作数的后面，因此也被称为后缀表示法。
# 波兰表示法的运算符在前面，逆波兰记法不需要括号来标识操作符的优先级。
# 对于4个数字而言，共有以下5中加括号的方式：ABCD***,ABC*D**,AB*CD**,ABC**D*,AB*C*D*
# (A(B(CD)))，(A((BC)D))，((AB)(CD))，((A(BC))D)，(((AB)C)D)。
def RPN(RPN_str):
    stack = []
    for c in RPN_str.split():
        if c in '+-*':
            i2 = stack.pop()
            i1 = stack.pop()
            # print(i1,c,i2)
            # print(eval('%s'*3 % (i1,c,i2)))
            stack.append(eval('%s' * 3 % (i1, c, i2)))
        else:
            # 非运算符就压栈
            stack.append(c)
    #print(stack[0])
    return stack[0]

#
# Main()入口：
#

Perm("2464", 0)
#print(IsSwap("acca", 0, 2))

nl = [2, 3, 6, 1]
nl = [9, 7, 2, 1]
nl = [1, 2, 3, 4]
#nl = [7, 7, 7, 7]
nl = [6, 6, 6, 6]
nl = [4, 2, 6, 8]
nl = [25, 5, 5]

print("LIST = ", nl)

number = nl
#if PointsGame(3):
#    print("TRUE:", number)

Get24(nl)
print("Total solution: ", len(resultList))
for i in range(len(resultList)):
    print(i+1, " - ", resultList[i])

# 逆波兰表达式：
print(RPN('3 1 2 + * 3 * 3 +'))