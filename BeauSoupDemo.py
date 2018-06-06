from bs4 import BeautifulSoup
import re

html = """
<html><head><title>The Dormouse's story</title><name>Demo</name></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# 创建BeautifulSoup对象：
soup = BeautifulSoup(html, "lxml")

# 打印Soup
print(soup.prettify())

# 1. 获取标签Tag：name和attrs两个属性
print("\nTag:\n")
print(soup.title)
print(soup.a)       # 只返回第一个符合要求的结果

print(soup.p.nme)
print(soup.p.attrs)

# 二者等效
print(soup.p['class'])
print(soup.p.get('class'))

# 2. 获取标签内部的文字NavigableString：
print(soup.p.string)

# 3. 注释对象Comment：
print(soup.a)
print(soup.a.string)        # 输出将注释符号去掉了
# if type(soup.a.string)== bs4.element.Comment:    # 先判断对象类型
print(soup.a.string)

# 遍历文档树：
# 1. tag 的.content 属性可以将tag的子节点以列表的方式输出
print("\nCONTENT:\n")
print(soup.head.contents)

# 2.遍历所有子节点
print("子节点:")
for child in soup.body.children:
    print(child)

# 3.遍历子孙节点:.contents 和 .children 属性仅包含tag的直接子节点，.descendants 属性可以对所有tag的子孙节点进行递归循环
print("子孙节点:")
for child in soup.descendants:
    print(child)

# 4.获取多个内容:
print("String:")
for string in soup.strings:
    print(repr(string))

# 遍历文档树:
# 1.find_all()方法搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件
print("Find_all:")
print(soup.find_all(["a", "b"]))
print(soup.find_all(id='link2'))
print(soup.find_all(href=re.compile("elsie")))
