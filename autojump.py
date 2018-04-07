import os
import time
import random

from PIL import Image  # PIL(Python Imaging Library)提供基本图像操作,比如图像缩放、裁剪、旋转、颜色转换等

# 自动操作的关键在于识别图像上的物件，能识别出起跳点和落地点就能完成自动操作，
# 而识别算法是需要测试和调整的，因此将每次识别的图片保存在目录便于优化算法,识别的图片会比较多，放在代码目录不好看，所以单独放个临时目录，
# 这里的temp是我自己硬盘上建的一个临时文件目录，你应该自己建立一个目录，随便你起个目录名字，然后把目录路径放在这儿
logpath = "c:/temp/"

# 这个系数是测试出来的，你需要按照自己的手机实际情况调整，跳几次测试个正好能跳到目的地的数字即可，
# 如果跳的距离不够，调增；如果跳的距离超过目的地，调减。
MyIndex = 1.4

# 自己做个颜色比较函数，相差不大的算同一种颜色，敏感度可调整
def colorlike(c1, c2, drt=10):
    return abs(c1[0] - c2[0]) < drt and abs(c1[1] - c2[1]) < drt and abs(c1[2] - c2[2]) < drt

# 根据图片，识别目的地和起跳点，计算出距离
def distance(fn, logfn=None):
    # 首先我们加载这个图片
    img = Image.open(fn)
   
    # 获取屏幕的长宽值
    (xmax, ymax) = img.size
    # print("图片加载到内存:", img.format, img.size, img.mode)
    
    # 我们发现，屏幕上部总有大块的背景空白，从其中读取一个背景色的初始值
    背景标准色 = img.getpixel((xmax // 2, ymax // 4))
    # 小人色是用颜色拾取器从图像上直接取色的，选择小人脚部的颜色为准
    小人色 = (54, 60, 102)
    小人色命中点 = []
    顶点x = -1
    顶点y = -1

    # 对图片中部扫描识别，顶部和底部可以忽略了
    # 首先找小人
    # for y in range(ymax // 4, ymax * 3 // 4):
    #    for x in range(xmax):
    for y in range(ymax // 4, ymax * 3 // 4, 2):
        for x in range(xmax // 5, xmax * 4 // 5, 2):
            c = img.getpixel((x, y))
            if colorlike(img.getpixel((x, y)), 小人色):
                img.putpixel((x, y), (255, 0, 0))
                小人色命中点.append((x, y))

    # 找小人坐标
    temp = [xy[0] for xy in 小人色命中点]

    # 没有找到小人
    if len(temp) == 0:
        return 0

    小人x = sum(temp) // len(temp)
    temp = [xy[1] for xy in 小人色命中点]
    小人y = sum(temp) // len(temp)
    print("找到小人：", 小人x, 小人y)

    # 绘制小人位置：画十字
    for i in range(-20, 20):
        img.putpixel((小人x, 小人y + i), (255, 255, 0))
        img.putpixel((小人x + i, 小人y), (255, 255, 0))
        
    # 然后找目标点的顶点
    for y in range(ymax // 4, ymax * 3 // 4):
        发现物体 = False
        temp = []
        行内颜色统计 = {}
        for x in range(xmax):
            # 不判断小人顶部上方的位置，避免小人高于目标点时，将小人顶部当作目标顶点
            if abs(x - 小人x) < 100:
                continue

            c = img.getpixel((x, y))
            if not colorlike(c, 背景标准色):
                发现物体 = True
                temp.append(x)
                # img.putpixel((x, y), (255, 0, 0))  # 涂色调试用
            else:  # 只统计非物体部分颜色
                cstr = "{:d},{:d},{:d}".format(c[0], c[1], c[2])
                行内颜色统计[cstr] = 行内颜色统计.get(cstr, 0) + 1
                
        if 发现物体 and 顶点y == -1:
            顶点y = y
            顶点x = sum(temp) // len(temp)
            背景标准色 = [int(n) for n in max(行内颜色统计, key=行内颜色统计.get).split(',')]
        
    print("找到顶点：", 顶点x, 顶点y)

    for i in range(-20, 20):
        img.putpixel((顶点x, 顶点y + i), (0, 0, 0))
        img.putpixel((顶点x + i, 顶点y), (0, 0, 0))

    # 找着落点：顶点下方的中轴线上
    背景标准色2 = img.getpixel((顶点x - 1, 顶点y - 1))
    oldsize = 0
    着落点x = -1
    着落点y = -1
    count = 0

    # 与屏幕的分辨率有关：否则会出现“image index out of range”，是由于没有出界，还没有计算着落点的位置！
    # for tttt in range(1, 100):
    # tttt控制顶点y坐标向下的最大距离：step可以加大，以便加快运行速度！
    # for tttt in range(1, 200):
    for tttt in range(1, 200, 2):
        # testsize用于控制x坐标的左右延伸距离
        testsize = 1
        出界 = False
        while not 出界:
            if 顶点x - testsize < 0 or 顶点x + testsize >= xmax:
                出界 = True
            else:
                if colorlike(img.getpixel((顶点x - testsize, 顶点y + tttt)), 背景标准色2) or colorlike(
                        img.getpixel((顶点x + testsize, 顶点y + tttt)), 背景标准色2):
                    出界 = True
            if not 出界:
                #print("x = ", 顶点x, "y = ", 顶点y, " size = ", testsize, " tttt = ", tttt)
                
                img.putpixel((顶点x - testsize, 顶点y + tttt), (255, 255, 25))
                img.putpixel((顶点x + testsize, 顶点y + tttt), (255, 255, 25))
                # testsize += 1
                testsize += 2

                #print("testsize = ", testsize, " oldsize = ", oldsize, " count = ",count)

        if testsize <= oldsize:
            count += 1
            if count > 1:
                着落点x = 顶点x
                着落点y = 顶点y + tttt
                break
        else:
            count = 0
            oldsize = testsize

    # 绘制着落点
    for i in range(-20, 20):
        img.putpixel((着落点x, 着落点y + i), (255, 0, 0))
        img.putpixel((着落点x + i, 着落点y), (255, 0, 0))

    # 如何计算？
    距离 = ((小人x - 着落点x) ** 2 + (小人y - 着落点y) ** 2) ** 0.5

    # 保存有定位痕迹的图片，以备调试
    if logfn:
        img.save(logfn, 'png')

    # img.show()  # 在PyCharm下运行呢，这一句会直接调用Windows照片查看器来显示图片,方便调试，长时间挂机时请注释掉
    return 距离


# 主程序：

# 距离 = distance("C:\temp\故障\gamescreen1515915924.png",None)
# exit()

# 这是个测试程序，简单点就做个死循环好了，你也可以把它改写成按一下键盘走一步等等
while True:
    t = int(time.time())

    ret = os.system("adb shell screencap -p /sdcard/gamescreen.png")

    if ret:
        print("手机截屏失败！")
        exit()
    else:
        print('截屏', ret)
        print('下载', os.system("adb pull /sdcard/gamescreen.png {:s}gamescreen{:d}.png".format(logpath, t)))
    
        距离 = distance("{:s}gamescreen{:d}.png".format(logpath, t), "{:s}gamescreen{:d}ok.png".format(logpath, t))

        if 距离 == 0:
            print("没有找到小人！")
            exit()

        按压时间 = int(距离 * MyIndex)
    
        #print('按压', os.system("adb shell input swipe 10 20 15 {:d}  {:d}".format(random.randint(20, 80), int(距离 * MyIndex))))
        #print("adb shell input swipe 10 20 15 {:d}  {:d}".format(random.randint(5, 10), int(距离 * MyIndex)))

        # 模拟滑动，从（x1,y1）到（x2,y2）持续时间为duration。即：swipe <x1> <y1> <x2> <y2> [duration(ms)]
        # 此外还可模拟keyevent物理按键操作，tap点击屏幕，text输入文本等
        print('按压', os.system("adb shell input swipe 10 20 15 {:d}  {:d}".format(random.randint(20, 80), int(距离 * MyIndex))))

        # 需要改进：如何关闭cmd窗口？等待按键后再运行下一次，确保某些地方的停留。
        # 人为增加时延：避免系统认定作弊
        time.sleep(random.randint(1, 2))
    
