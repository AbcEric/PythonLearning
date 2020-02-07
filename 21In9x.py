# 21In9x.py:
#
# 在九宫格中，上下左右4个相连数字之和均为21，求出所有的可能排列办法：
#
# 采用解线性方程组 + 暴力求解，每种解法均有8种不同的表示方法（旋转和翻转）
#
# Q:
# 1.改进为递归求解？
#

import copy
import numpy as np


def showMatrix(matrix):
    # 显示为九宫格

    for i in range(len(matrix)):
        print(matrix[i])
    print()


def getSameMatrix(matrix_in):
    # 返回旋转和翻转后的各种组合，每一种假设自身有8种形式，相当于这8种都是同一种！
    # 也可只判断中间数和任意一边：8种情况（中间相同，该边在任何一边，左右互换都算）
    # 输入：matrix为列表List

    origianl = copy.deepcopy(matrix_in)
    matrix = copy.deepcopy(matrix_in)

    # 先上下翻转matrix[::-1], 再矩阵转置map(list,zip(*matrix)), 其中map将里面的元组转换为list：() -> []
    ret = []
    ret.append(origianl)

    # 向右旋转90°三次：
    for i in range(3):
        matrix[:] = map(list, zip(*matrix[::-1]))     # 将所有都转换为列表！
        # matrix[:] = list(zip(*matrix[::-1]))            # 转换为元祖列表！即列表元素是元祖
        ret.append(copy.deepcopy(matrix))

    # 上下翻转：
    matrix = origianl
    matrix = matrix[::-1]
    ret.append(copy.deepcopy(matrix))

    # 向右旋转90°三次：
    for i in range(3):
        matrix[:] = map(list, zip(*matrix[::-1]))
        ret.append(copy.deepcopy(matrix))

    # 不需要再左右翻转，左右翻转相当于上下翻转再旋转180°。也不需要左右翻转后的选择，

    return ret


def insertResult(result, item):
    # 判断解法是否重复：不重复才保留

    for i in range(len(result)):
        one = result[i]
        ones = getSameMatrix(one)
        if item in ones:
            # print(result, " already have item: ", item, )
            print("Already exist: ", item)
            # return result
            return

    result.append(item)
    return


if __name__ == '__main__':
    A = np.mat('1,1,0,1,1,0,0,0,0; 0,1,1,0,1,1,0,0,0; 0,0,0,1,1,0,1,1,0; 0,0,0,0,1,1,0,1,1; 1,1,1,1,1,1,1,1,1')    # 构造系数矩阵 A
    A0 = np.mat('0,0,0,0,0,0,0,0,0')

    B = np.mat('21,21,21,21,45').T       # 构造转置矩阵 b （这里必须为列向量）
    B0 = np.mat('0').T

    result = []

    # T = np.array([x for x in range(1,10)]).reshape((3,3)).tolist()
    # showMatrix(T)
    # rets = getSameMatrix(T)
    # for item in rets:
    #     showMatrix(item)
    # exit(0)
    # insertResult(result, [[9,2,4],[3,7,8],[6,5,1]])
    # print("res1=", result)
    # #
    # insertResult(result, [[8,1,4],[5,7,9],[6,3,2]])
    # print("res2=", result)
    # #
    # insertResult(result, [[6,5,8],[3,7,1],[2,9,4]])
    # print("res3=", result)
    # exit(0)

    # 暴力前4个数字：确保方程个数与变量数相同。
    for i in range(9):
        A0[0, 0] = 1
        A1 = np.vstack((A, A0))
        A0[0, 0] = 0

        B0[0, 0] = i+1
        B1 = np.vstack((B, B0))
        # print(A1, B1)

        for j in range(9):
            if j in [i]:
                continue
            A0[0, 1] = 1
            A2 = np.vstack((A1, A0))
            A0[0, 1] = 0

            B0[0, 0] = j + 1
            B2 = np.vstack((B1, B0))

            for m in range(9):
                if m in [i, j]:
                    continue

                A0[0, 2] = 1
                A3 = np.vstack((A2, A0))
                A0[0, 2] = 0

                B0[0, 0] = m + 1
                B3 = np.vstack((B2, B0))

                for n in range(9):
                    if n in [i, j, m]:
                        continue

                    A0[0, 3] = 1
                    A4 = np.vstack((A3, A0))
                    A0[0, 3] = 0

                    B0[0, 0] = n + 1
                    B4 = np.vstack((B3, B0))

                    try:
                        r = np.linalg.solve(A4, B4)  # 调用 solve 函数求解

                    except Exception as e:
                        print("Error: ", str(e))

                    finally:
                        ok = True

                        # 是否均为正整数：
                        for k in r:
                            if k <= 0:
                                ok = False

                        if ok:
                            kk_set = r.T.tolist()
                            # 是否有重复数字：
                            if len(set(kk_set[0])) == 9:
                                one = np.array(kk_set[0], dtype=int).reshape((3,3)).tolist()
                                # 插入到最终结果：不重复才插入
                                insertResult(result, one)

    print(result)

    print("\nTotal solutions: ", len(result))
    for one in result:
        showMatrix(one)

    # a = map(list, zip(*result[::-1]))  # 将所有都转换为列表！
    # showMatrix(list(a))
