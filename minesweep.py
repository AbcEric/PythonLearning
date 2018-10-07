#
# 扫雷算法：minesweep.py
#
'''
1. 需要显示提示的数字；
2. 如何自动判断？
'''
import numpy as np

# 图的遍历：递归

X = 5
Y = 7
mineList = [[0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 1]]
openFlag = np.zeros((X, Y))

def getNumber(x, y):

    return mineList[x][y]

def inArea(x, y):
    if x in range(0, X) and y in range(0, Y):
        return True
    else:
        return False

def isMine(x, y):
    return mineList[x][y]

def mineOpen(x, y):
    if not inArea(x, y):
        print("Out of index!")

    if isMine(x, y):
        print("Sorry: bad luck!")
        mineList[x][y] = 'x'
    else:
        openFlag[x][y] = 1

    #if getNumber(x, y) == 0:
        ''' 会把对角线的元素也翻开
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                #print(i, j, inArea(i, j), openFlag[i][j], isMine(i, j))
                if inArea(i, j) and openFlag[i][j] == 0 and isMine(i, j) == 0:
                    mineOpen(i, j)
        '''
        mineList[x][y] = " "
        i = x-1
        j = y
        if inArea(i, j) and openFlag[i][j] == 0 and isMine(i, j) == 0:
            mineOpen(i, j)
        i = x+1
        j = y
        if inArea(i, j) and openFlag[i][j] == 0 and isMine(i, j) == 0:
            mineOpen(i, j)
        i = x
        j = y-1
        if inArea(i, j) and openFlag[i][j] == 0 and isMine(i, j) == 0:
            mineOpen(i, j)
        i = x
        j = y+1
        if inArea(i, j) and openFlag[i][j] == 0 and isMine(i, j) == 0:
            mineOpen(i, j)

# flag == 1 显示所有实际值
# flag == 0 仅显示已翻开
def mineShow(flag):
    for i in range(X):
        for j in range(Y):
            #print(i, j)
            if openFlag[i][j] or flag == 1:
                print(mineList[i][j], end=' ')
            else:
                print("*", end=' ')
        print("")

# Main()入口
#print(mineList, openFlag)
mineShow(1)
#mineOpen(1, 2)
mineOpen(2, 2)
mineShow(0)

