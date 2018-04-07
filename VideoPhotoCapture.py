# -*- coding: utf-8 -*-
'''
import cv2
import sys
from PIL import Imag
def CatchUsbVideo(window_name, camera_idx):
    cv2.namedWindow(window_name)

    # 视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    print("starting capture....")
    cap = cv2.VideoCapture(camera_idx)

    # 告诉OpenCV使用人脸识别分类器
#    classfier = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml")
    classfier = cv2.CascadeClassifier("C:/Python36/Lib/site-packages/cv2/data/haarcascade_frontalface_alt2.xml")
    print("classifier ok....")

    # 识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)

    count = 0

    while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:
            break

            # 将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print("gray ok .....")

        # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects) > 0:  # 大于0则检测到人脸
            count = count + 1
    return count


if __name__ == '__main__':
    result = CatchUsbVideo("识别人脸区域", 'Honey.mp4')
    if result > 0:
        print('视频中有人！！')
    else:
        print('视频中无人！！')



import cv2
import numpy as np

def detect(img, cascade):
    rects = cascade.detectMultiScale(img,1.3, 6,cv2.CASCADE_SCALE_IMAGE,(20,20))
    if  len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    print(rects)
    return rects

def draw_rects(img, rects):
    r =0
    x = 0
    y = 0
    num = 0
    for x1, y1, x2, y2 in rects:
        num = num + 1
        co1 = 0
        co2 = 0
        co3 = 0
        if(num%3 == 0): co1 = 255
        if(num%3 == 1): co2 = 255
        if(num%3 == 2): co3 = 255
        x = np.int((x1 + x2) * 0.5)
        y = np.int((y1 + y2) * 0.5)
        r = np.int(( abs(x1 - x2) + abs(y1-y2) ) * 0.25)
        cv2.circle(img, (x, y), r, (co1,co2,co3), 2)
      #  cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


img = cv2.imread("PEOP.jpg")
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.imshow("frame", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.namedWindow("gray", cv2.WINDOW_NORMAL)
#cv2.imshow("gray", gray)

face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_cascade.load("C:/Python36/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")

rects = detect(gray, face_cascade)

vis = img.copy()

draw_rects(vis,rects)

cv2.namedWindow("facedetect", cv2.WINDOW_NORMAL)
cv2.imshow("facedetect", vis)
cv2.imwrite("facedetect.jpg", vis)

cv2.waitKey(0)
cv2.destroyAllWindows()



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
#from matplotlib import pyplot as plt
from pylab import *

# 添加中文字体支持
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc",size = 14)

# 载入图像
im = cv2.imread('LYX.jpg')
cv2.namedWindow("Image")

cv2.imshow("Image", im)
cv2.waitKey (0)
cv2.destroyAllWindows()


# 颜色空间转换
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# 显示原始图像
fig = plt.figure()
subplot(121)
plt.gray()
imshow(im)
title(u'彩色图', fontproperties= font)
axis('off')
# 显示灰度化图像
plt.subplot(122)
plt.gray()
imshow(gray)
title(u'灰度图', fontproperties= font)
axis('off')

show()
'''

# -*- coding: utf-8 -*-
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()