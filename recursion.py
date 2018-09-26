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

    # 可简化为：item[i] = nList[i] + nList[j], item[j] = nList的最后一个数，其余值均不变！不需循环
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

#
# Main()入口：
#

nl = [2, 3, 6, 1]
nl = [9, 7, 2, 1]
nl = [1, 2, 3, 4]
nl = [5, 5, 5, 5]
#nl = [7, 7, 7, 7]
nl = [6, 6, 6, 6]
nl = [4, 2, 6, 8]

print("LIST = ", nl)

Get24(nl)
print("Total solution: ", len(resultList))
for i in range(len(resultList)):
    print(i+1, " - ", resultList[i])
