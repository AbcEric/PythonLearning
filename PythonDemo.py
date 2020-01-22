#
# Python语句测试：采用class方式
#
# 1. pysnooper：snoop()装饰器代替print进行调试, 记录程序运行时变量的变化情况。（https://github.com/cool-RR/PySnooper）
#

import copy
import numpy
import pysnooper

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


# 输入四个数：n1 n2 n3 n4
# 将n1重复n2次，n3重复n4次后比较大小
def CompareMultiNum():
    print("Please input 4 numbers, seperated by blank:")
    x1, k1, x2, k2 = map(int, input().split())
    v1, v2 = int(str(x1) * k1), int(str(x2) * k2)
    print(v1, v2)
    if v1 == v2:
        print("Equal")
    elif v1 > v2:
        print("Greater")
    else:
        print("Less")

    return


#
# *潜在风险客户识别：转账形成闭环的客户，以及转入该闭环的客户
# （数据结构是关键！）
# 输入：
# 5 5 （5个客户，5条转账）
# 1,2 （代表客户1转账给客户2）
# 2,3
# 3,1
# 2,4
# 5,3
# 输出：
# 4 （只有客户4为安全客户）
def FindRisk():
    print("Please input customer total number and transaction number: ")
    nm = input().split()
    n, m = int(nm[0]), int(nm[1])
    trans = {}      # 字典dict
    safe = list(range(1, n + 1))
    print(safe)

    for _ in range(m):
        temp = list(map(int, input().split(",")))
        print(temp)
        try:
            safe.remove(temp[0])            # 作用：没有交易记录的客户编号肯定是安全的,safe为无转出交易的客户名单！
        except ValueError:
            pass

        if temp[0] not in trans.keys():
            trans[temp[0]] = [temp[1]]
        else:
            trans[temp[0]].append(temp[1])      # 添加所有的转出对象
        print("trans=", trans, "safe=", safe)

    # 对形如trans={1: [2], 2: [3], 3: [1, 4], 7: [3], 4: [5], 5: [6], 6: [4]}进行闭环判断！
    # 利用trans数据结构进行逐级判断：若A指向的对象全是安全的，说明A也是安全的，不断反向循环（即A->B->C->D,若D安全，则A,B,C都安全）
    # 或者判断是否形成闭环！（若同一个对象形成多个闭环，要确保全部找到，效率低）
    while True:
        count = 0
        temp_del = []
        print("KEY:", trans.keys())
        for i in trans.keys():
            print(i, trans[i], safe, temp_del)
            # 找到转出的对象中，有哪些不在safe安全名单中：set
            trans[i] = list(set(trans[i]).difference(set(safe)))
            print(trans[i], "trans=", trans)

            # trans[i]为[]，说明第i个对象指向的均为安全对象，将该对象添加到safe中去。
            if not trans[i]:
                safe.append(i)
                temp_del.append(i)
            else:
                count += 1
        if count == len(trans):
            break
        else:
            print("count=", count, "temp_del=", temp_del, "safe=", safe)
            # 将trans中指向[]的对象删除！即若指向的都是安全对象，则自身也是安全的
            for j in temp_del:
                del trans[j]
                print("trans=", trans)
    if safe:
        print(" ".join(list(map(str, sorted(safe)))))
    else:
        print("None")


# 方案2：
def FindRisk2():
    class GraphNode:
        def __init__(self, label):
            self.label = label
            self.children = []

    n, m = list(map(int, input().split()))
    clients = {}
    for _ in range(m):
        client1, client2 = list(map(int, input().split(',')))
        if client1 not in clients:
            clients[client1] = GraphNode(client1)
        if client2 not in clients:
            clients[client2] = GraphNode(client2)
        clients[client1].children.append(clients[client2])

    print("clients=", clients)

    def dfs(node, risk, visited):
        print(node.label, risk, visited)
        # 在visited中说明形成闭环，在risk说明转入到风险对象！
        if node.label in risk or node.label in visited:
            for client in visited:
                risk.add(client)
                print("risk=", risk)
            return

        # 遍历所有子节点：
        for adj in node.children:
            # 递归调用：
            dfs(adj, risk, visited | set([node.label]))

    risk = set()
    for client in clients:
        if client in risk:
            continue
        dfs(clients[client], risk, set())

    ans = []
    for i in range(1, n + 1):
        if i not in risk:
            ans.append(str(i))

    print('None' if not ans else ' '.join(ans))

#FindRisk2()


# 现在信用卡开展营销活动，持有我行信用卡客户推荐新户办卡，开卡成功后可获得积分奖励。
# 规定每个客户最多可推荐两个新户且一个新户只能被推荐一次。但允许链接效应，即若客户A推荐了新户B，新户B推荐新户C，
# 则客户C同时属于A和B的推荐列表。简单起见，只考虑以一个老客户A作起点推荐的情况。编程计算推荐新户数不小于n的客户列表。

# 一个dfs的问题，也就是说，分以下两步来解决：
# 1.开始时没有问题吧，m个人，每个人可以推荐n个，先把这个关系给对应上了
# 2.现在要进行dfs，从A开始，我们找当前节点与末尾形成的链子的长度，如果这个长度>+n的，即为符合条件的点
# 3.注意题目中说到的，只考虑从A出发的情况，否则我们需要多一步，在m个人中进行遍历
def GetRecomand():
    m, n = map(int, input().split(" "))
    mem = {"*": None}
    degree = set()

    class ListNode:
        def __init__(self, x):
            self.val = x
            self.left = None
            self.right = None

    for _ in range(m):
        root, left, right = input().split()

        if root not in mem:
            mem[root] = ListNode(root)
        if left not in mem:
            mem[left] = ListNode(left)
        if right not in mem:
            mem[right] = ListNode(right)

        # 建图，这种用dict复制图的方法的常见方法
        degree.add(left)
        degree.add(right)

        _root, _left, _right = mem[root], mem[left], mem[right]
        _root.left = _left
        _root.right = _right

        # print(degree, mem)

    # root 节点是入度为0的节点
    root = (set(mem) - degree).pop()

    global ans
    ans = []

    # DFS，常规操作
    def dfs(root):
        global ans
        if root:
            left = dfs(root.left)
            right = dfs(root.right)
            this = left + right + 1
            if this >= n + 1:
                ans.append(root.val)
            return this
        return 0

    dfs(mem[root])
    if ans:
        print(" ".join(ans))
    else:
        # None也要print出来，不然会少一个回车符
        print(None)

# GetRecomand()

# 判断列表中的数据能否组成指定值：
def GetSumElement(list, target):
    # 递归结束条件：当两个数相加等于指定目标，或二者之一为指定目标。(相减后递归不改变元素的本来信息)
    # print(target, list)
    if (sum(list) < target):
        return False

    if len(list) == 2:
        if list[0]+list[1] == target:
            print(list[0], list[1])
            return True
        if list[0] == target:
            print(list[0])
            return True
        if list[1] == target:
            print(list[1])
            return True
        else:
            return False
    else:
        # 降维：将指定目标分别减去列表各元素，循环进行递归。例如：[1,2,4]-目标5，变成[2,4]-目标4,[1,4]-目标3
        for i in range(len(list)):
            # listnew = copy.deepcopy(list)       # 深拷贝，避免list改变，这种方式运行效率有点低！
            # item = listnew.pop(i)               # 弹出指定位置元素，同时listnew去掉该元素
            targetnew = target - list[i]
            #targetnew = target - item

            # 元素等于新的目标，直接输出：
            if targetnew == 0:
                print(list[i])
                # print(item)
                return True
            # 由于为相加运算，不可能存在新目标为负的情况
            if targetnew > 0:
                # 去掉被减元素的其他元素组成新列表：
                if i == 0:
                    listnew = list[1:]          # 新定义的list
                else:
                    listnew = list[0:i] + list[i+1:]

                # 当后续递归返回True时，说明当前被减元素是正确的：
                if GetSumElement(listnew, targetnew):
                    print(list[i])
                    # print(item)
                    return True
        return False

# GetSumElement([1,4,9,25,40,80,50,200,121,133,179,333,246,500,900,211,999],2478)


# str是个不可变对象，每次迭代，都会生成新的str对象来存储新的字符串，num越大，创建的str对象越多，内存消耗越大。
# list是可变对象，不会重新分配空间，只是引用，速度快！
# 用pysnooper跟踪程序运行！

# 也可只跟踪部分语句，在语句前加入：with pysnooper.snoop():
@pysnooper.snoop()
# @pysnooper.snoop("file.log")
def str_list_test(num):
    str = "STR_TEST_"
    print("1:")
    str1 = str + "X" * num              # 速度快！
    print(len(str1))
    print(str1[:100])
    print("2:")
    for i in range(num):
        str += "X"                      # 当num变大时，速度很慢！
    print(len(str))
    print(str[:100])

    print("3:")
    list = ["LIST"]
    for i in range(num):
        tmplist = list.append("X")                # 速度并不慢！
    print(len(list))
    print(list[:10])
    return

# str_list_test(10000000)
str_list_test(2)

# 函数的参数传递：传引用？
#
# a = 1
# def fun_mutable(a):
#     a = 2
#
# fun_mutable(a)
# print(a)        # 输出：1
#
# a = []
# def fun_imutable(a):
#     a.append("Hi")
#     #a = ["Hi"]     # 重新定义，与原没有关系了
#
# fun_imutable(a)
# print(a)        # 输出：["Hi"]


# w.ActiveDocument.SaveAs(FileName = "test.wps")



