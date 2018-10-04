#
# 正态分布的模拟：normal distribution simulate
#

'''
Q:
1.直方图显示和x坐标没有对齐，有时部分位置显示为空？
2.如何模拟其动态下落过程？

'''
# 模拟的分布状态个数：实际值要加1（即5个点有6个下落位置）
DIST_NUM = 10
# 模拟的运行次数
RUN_NUM = 500

result_sum = [0] * (DIST_NUM + 1)
result_list = []
'''                  x
                   x  x
                 x  x  x
               x  x  x  x
'''
import random

# 左右的几率相等，均为0.5
def RandJump(input):
    if random.randint(0, 1) == 0:
        return input
    else:
        return input + 1

from matplotlib import pyplot as plt

# 参数依次为list,种类个数，抬头,X轴标签,Y轴标签,XY轴的范围
def draw_hist(myList, Num, Title, Xlabel, Ylabel, Xmin, Xmax, Ymin, Ymax):
    plt.hist(myList, bins = Num)
    plt.xlabel(Xlabel)
    plt.xlim(Xmin, Xmax)
    plt.ylabel(Ylabel)
    plt.ylim(Ymin, Ymax)
    plt.title(Title)
    plt.show()

def count_elements(seq) -> dict:
    """Tally elements from `seq`."""
    hist = {}
    for i in seq:
        hist[i] = hist.get(i, 0) + 1

    return hist

def ascii_histogram(seq) -> None:
    """A horizontal frequency-table/histogram plot."""
    counted = count_elements(seq)
    for k in sorted(counted):
        print('{0:5d} {1}'.format(k, '+' * counted[k]))

#
# Main:
#
for i in range(RUN_NUM):
    item = [0]
    output = 0
    for j in range(DIST_NUM):
        output = RandJump(output)
        item.append(output)

    # print(item)
    result_sum[item[-1]] += 1
    result_list.append(item[-1])

print(result_sum,result_list)

ascii_histogram(result_list)

draw_hist(result_list, DIST_NUM+1, 'Normal Distribution', 'Number', 'Total', 0, DIST_NUM+2, 0, 5*RUN_NUM/DIST_NUM)  # 直方图展示
