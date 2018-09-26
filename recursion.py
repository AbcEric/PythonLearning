#
def num(n):
    if n == 1 or n == 2:
        return 1

    if n == 3:
        return 2

    return num(n - 1) + num(n - 3)

# 数字通过加减乘除凑成24！


resultList = []
# 记录结果：避免重复
def AddResult(nList):
    for i in range(len(resultList)):
        #print("ADD:", resultList[i], nList)
        if resultList[i] == nList or resultList[i] == [nList[1], nList[0]]:
            return

    resultList.append(nList)

def Get24(nList):
    # 结束条件：2个数加减乘除为24！
    num = len(nList)
    if num == 2:
        if nList[1] != 0:
            if nList[0] + nList[1] == 24 or abs(nList[0] - nList[1]) == 24 or nList[0] * nList[1] == 24 or nList[0] / nList[1] == 24:
                #print("True:", nList)
                AddResult(nList)
                return True
        if nList[0] != 0:
            if nList[0] + nList[1] == 24 or abs(nList[0] - nList[1]) == 24 or nList[0] * nList[1] == 24 or nList[1] / nList[0] == 24:
                #print("True:", nList)
                AddResult(nList)
                return True
        return False
    else:
        # combine two number then recursion:
        for i in range(0, num-1):
            for j in range(i+1, num):
                # Add
                # x = nList[i] + nList[j]
                nextList = GetnextList(nList, i, j, "+")
                # print(i, j, nextList)
                if Get24(nextList):
                    print(nList, nextList)
                    break

                nextList = GetnextList(nList, i, j, "+")
                #print(i, j, nextList)
                if Get24(nextList):
                    print(nList, nextList)
                    break
                nextList = GetnextList(nList, i, j, ">")
                #print(i, j, nextList)
                if Get24(nextList):
                    print(nList, nextList)
                    break
                nextList = GetnextList(nList, i, j, "<")
                #print(i, j, nextList)
                if Get24(nextList):
                    print(nList, nextList)
                    break
                nextList = GetnextList(nList, i, j, "*")
                #print(i, j, nextList)
                if Get24(nextList):
                    print(nList, nextList)
                    break
                nextList = GetnextList(nList, i, j, "/")
                #print(i, j, nextList)
                if Get24(nextList):
                    print(nList, nextList)
                    break
                nextList = GetnextList(nList, i, j, "\\")
                #print(i, j, nextList)
                if Get24(nextList):
                    print(nList, nextList)
                    break
        #print(nList)

def GetnextList(nList, i, j, TYPE):
    nextList = [0]* (len(nList)-1)

    for k in range(0, len(nList)-1):
        if k < i:
            nextList[k] = nList[k]
        elif k == i:
            if TYPE == "+":
                nextList[k] = nList[i] + nList[j]
            elif TYPE == "*":
                nextList[k] = nList[i] * nList[j]
            elif TYPE == ">":
                nextList[k] = nList[i] - nList[j]
            elif TYPE == "<":
                nextList[k] = nList[j] - nList[i]
            elif TYPE == "/":
                if nList[j] == 0:
                    nextList[k] = 999999
                else:
                    nextList[k] = nList[i] / nList[j]
            elif TYPE == "\\":
                if nList[i] == 0:
                    nextList[k] = 999990
                else:
                    nextList[k] = nList[j] / nList[i]

        elif k > i and k < j:
            nextList[k] = nList[k]
        elif k >= j:
            nextList[k] = nList[k+1]

    return nextList

#print(num(10))

nl = list([2, 3, 6, 1])
nl = list([4, 2, 6, 8])
#nl = list([9, 7, 2, 1])
#nl = list([1, 2, 3, 4])
print("LIST = ", nl)

#print(GetnextList(nl, 2, 3, "/"))

print(Get24(nl))
print("Total Result: ", len(resultList))
for i in range(len(resultList)):
    print(i, " - ", resultList[i])
