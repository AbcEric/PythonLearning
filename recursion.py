#
# recursion algorithms：
#

# 用于模拟static变量，记录全局变量
class GlobalPara:
    num = 0
    permList = []
    stack = []
    def add(self):
        GlobalPara.num += 1
    def addperm(self, nList):
        GlobalPara.permList.append(nList)

gp = GlobalPara()

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
        # 两两组合任意两个数后进行递归调用: 穷举（效率较低，位数多时会显现！），重复情况剔除在结束条件时考虑。
        # range()默认从0开始，步长为1，到指定数结束，但不包括指定数！
        for i in range(num-1):
            for j in range(i+1, num):
                nextList = GetnextLists(nList, i, j)
                for k in range(len(nextList)):
                    #if Get24(nextList[k]):
                        # print(nList, nextList[k])
                        # 找到一个后，应继续查找？否则可能漏掉除法，所有乘法都可转为除法，如8*3 == 8/(1/3) == 3/(1/8)
                        #break
                    Get24(nextList[k])

# 对指定位置两个数进行加减乘除后，返回可能的列表
def GetnextLists(nList, i, j):
    item = [0]*(len(nList)-1)
    nextLists = []

    # 判断输入参数的合法性
    if i >= j or i < 0 or j < 0 or i > (len(nList)-2) or j > (len(nList)-1):
        print("i and j must be:0=<i<j<len(List)!")
        return [nList]

    # 可以拼接，也可简化为：item[i] = nList[i] + nList[j], item[j] = nList的最后一个数，其余值均不变！
    # 但要剔除最后一个数已经使用的情况。
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

    item[i] = nList[i] * nList[j]
    nextLists.append(item.copy())

    return nextLists

# Get24()的第二种方法：先去重全排列，再用逆波兰式计算。缺点是重复的结果太多！
def Get24ByRPN(nList):
    ListPerm(nList, 0)

    # 逆波兰式的添加方法：如何自动化？
    if len(nList) != 4:
        print("Only 4 numbers is allowed")
        return False

    OP = "+-*/"
    for item in gp.permList:
        #print(item)

        for op1 in range(4):
            for op2 in range(4):
                for op3 in range(4):
                    str = '%d %d %s %d %s %d %s' % (item[0], item[1], OP[op1], item[2], OP[op2], item[3], OP[op3])
                    #print(str)
                    if RPN(str)[0] == 24: print(RPN(str)[1])   # AB*C*D*
                    str = '%d %d %s %d %d %s %s' % (item[0], item[1], OP[op1], item[2], item[3], OP[op2], OP[op3])
                    if RPN(str)[0] == 24: print(RPN(str)[1])   # AB*CD**
                    str = '%d %d %d %s %d %s %s' % (item[0], item[1], item[2], OP[op1], item[3], OP[op2], OP[op3])
                    if RPN(str)[0] == 24: print(RPN(str)[1])   # ABC*D**
                    str = '%d %d %d %s %s %d %s' % (item[0], item[1], item[2], OP[op1], OP[op2], item[3], OP[op3])
                    if RPN(str)[0] == 24: print(RPN(str)[1])   # ABC**D*
                    str = '%d %d %d %d %s %s %s' % (item[0], item[1], item[2], item[3], OP[op1], OP[op2], OP[op3])
                    if RPN(str)[0] == 24: print(RPN(str)[1])   # ABCD***

    return True

# 对列表数字进行去重全排列，结果记录在全局变量
def ListPerm(nList, pos):
    last = len(nList)

    if pos == last:
        #print(nList)
        gp.addperm(nList.copy())
    else:
        # 第i个数分别与它后面的数字交换就能得到新的排列:有问题！
        for i in range(pos, last):
            # 判断是否重复：
            if IsSwap(nList, pos, i):
                # 每次交换之后要恢复为原状
                nList[i], nList[pos] = nList[pos], nList[i]
                ListPerm(nList, pos+1)
                nList[i], nList[pos] = nList[pos], nList[i]

# 3.字符串的去重全排列：参考https://blog.csdn.net/lemon_tree12138/article/details/50986990，确保要交换的每一位都不同，即之前未交换过！
# 若字符串每一位都不同，则每次只需将首位与其他位交换，就可得到一个新的排列。再考虑去重，即判断相同的字符之前交换过否。
# 若采用非递归算法，关键在于找到替换点和被替点；
# 需要2个参数: pos表示当前位置，从0开始一直移动到最末一位。
# 例如：E=(a,b,c), 则perm(E) = a.perm(b,c) + b.perm(a,c) + c.perm(a,b) 先交换
# 其中，a.perm(b,c) = ab.perm(c) + ac.perm(b) = abc + acb依次递归进行
def StrPerm(pszStr, pos):
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
                StrPerm(pszStr, pos + 1)
                pszStr = strSwap(pszStr, i, pos)

# 去掉重复符号的全排列：在交换之前可以先判断两个符号是否相同，或者已经交换过,即nBegin和nEnd之间是否有和有过nEnd的值！
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
    stack = []      # 同时记录表达式[num, exp]
    for c in RPN_str.split():
        if c in '+-*/':
            i2 = stack.pop()
            i1 = stack.pop()
            try:
                stack.append([eval('%s' * 3 % (i1[0], c, i2[0])), '(%s %s %s)' % (i1[1], c, i2[1])])
            except (Exception) as e:
                #print("Error: ", RPN_str, e)
                return [0, ""]
        else:
            # 非运算符就压栈
            stack.append([c, c])

    # 去掉最外层括号
    explen = len(stack[0][1])
    if stack[0][1][0] == '(' and stack[0][1][explen-1] == ')':
        stack[0][1] = stack[0][1][1:explen-1]

    return stack[0]


#
# Main()入口：
#

#StrPerm("2232", 0)
#print(IsSwap("acca", 0, 2))

nl = [1, 2, 3, 4]
#nl = [7, 7, 7, 7]
nl = [6, 6, 6, 6]
nl = [5, 5, 5, 5]
nl = [2, 3, 6, 1]
nl = [4, 2, 6, 8]
nl = [9, 7, 2, 1]

print("LIST = ", nl)

Get24(nl)
print("Total solution: ", len(resultList))
for i in range(len(resultList)):
    print(i+1, " - ", resultList[i])

# 逆波兰表达式：
print(RPN('3 1 2 + * 4 * 3 /'))

Get24ByRPN(nl)

# [2,3,6,1]漏了3除8分之一
'''
4*6:
(2 + 3 - 1) * 6
2 * (3 - 1) * 6
(2 - (1 - 3)) * 6
6 * (3 - (1 - 2))

8*3:
(2 + 6) * 3 * 1
(2 + 6) * 3 / 1
(2 + 6 * 1) * 3
(2 + 6 / 1) * 3
(2 * 1 + 6) * 3
(2 / 1 + 6) * 3

8/0.333:
(2 + 6) / (1 / 3)

3/0.127:
3 / (1 / (6 + 2))

2*12
(3 - 1) * 6 * 2

'''