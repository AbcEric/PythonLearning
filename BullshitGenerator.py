# -*- coding: UTF-8 -*-
#
# 狗屁不通文章生成器: 生成器的使用（优点是不会重复，每次返回一个），通过json定义简单的模型语料库。
#

import random
import json


def readJSON(fileName=""):
    if fileName != '':
        strList = fileName.split(".")
        if strList[len(strList)-1].lower() == "json":
            with open(fileName, mode='r', encoding="utf-8") as file:
                data = json.loads(file.read())
                logion = data["famous"]                 # a 代表前面垫话，b代表后面垫话
                logionbefore = data["before"]           # 在名人名言前面弄点废话
                logionafter = data['after']             # 在名人名言后面弄点废话
                bullshit = data['bosh']                 # 代表文章主要废话来源

                # return json.loads(file.read())
                return logion, logionbefore, logionafter, bullshit


# 列表遍历：生成器（与return相比，可避免数据的重复选择），epochs为重复度
def listTraversing(inputlist, epochs=1):
    pool = list(inputlist) * epochs
    while True:
        random.shuffle(pool)
        for element in pool:
            yield element


# 来点名人名言：
def getLogions(logionGenerator, logionbefore, logionafter):
    xx = next(logionGenerator)
    # 修改名人名言的前后废话，避免每次一样：
    xx = xx.replace("a", random.choice(logionbefore))
    xx = xx.replace("b", random.choice(logionafter))
    return xx


# 另起一段：
def otherParagraph():
    xx = ". "
    xx += "\r\n"
    xx += "    "
    return xx


if __name__ == "__main__":
    xx = input("请输入文章主题: ")

    # data = readJSON("data.json")
    logion, logionbefore, logionafter, bullshit = readJSON("data.json")

    # logion = data["famous"]                 # a 代表前面垫话，b代表后面垫话
    # logionbefore = data["before"]           # 在名人名言前面弄点废话
    # logionafter = data['after']             # 在名人名言后面弄点废话
    # bullshit = data['bosh']                 # 代表文章主要废话来源

    # 由名人名言+废话组成：在语料库中，主题用x代表，最后进行替换
    bullshitGenerator = listTraversing(bullshit)
    logionGenerator = listTraversing(logion)

    for x in xx:
        tmp = str()
        while len(tmp) < 2000:
            way = random.randint(0, 100)
            if way < 5:
                tmp += otherParagraph()
            elif way < 20:
                tmp += getLogions(logionGenerator, logionbefore, logionafter)
            else:
                tmp += next(bullshitGenerator)       # 绝大多数情况下，都取一句废话

        tmp = tmp.replace("x", xx)
        print(len(tmp), tmp)
