# coding=utf-8

import base64
from urllib import request,parse

def GetAccessToken():
    url = 'https://aip.baidubce.com/oauth/2.0/token?'
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'XzGs8khP2lCjhyyQq7Yg5aoA',
        'client_secret': 'Xf1MZzVn12gSdxnboQRInRu7cdH1WcYS'
    }
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)
    page = request.urlopen(req)

    # 将其转换为dict字典
    #token = eval(page.read().decode('utf-8'))
    token = eval(page.read())

    # 只返回access_token部分
    return token["access_token"]

'''
    1.人脸探测
'''
def FaceDetct(pic):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v1/detect"

    # 二进制方式打开图片文件
    f = open(pic, 'rb')
    img = base64.b64encode(f.read())

    params = {"face_fields": "age,beauty,expression,faceshape,gender,glasses,race,qualities", "image": img,
              "max_face_num": 5}

    # 注意：在urlencode后要加encode，否则会报"POST data should be bytes, an iterable of bytes, or a file object. It cannot be of type str."
    params = parse.urlencode(params).encode(encoding='UTF8')

    access_token = GetAccessToken()

    request_url = request_url + "?access_token=" + access_token

    # print(request_url)

    req = request.Request(url=request_url, data=params)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = request.urlopen(req).read()
    #content = response.decode('utf-8')
    content = response

    if content:
        print(content)

    return


'''
    2.人脸对比
'''

def FaceMatch(pic1, pic2):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v2/match"

    f = open(pic1, 'rb')
    # 参数images：图像base64编码
    img1 = base64.b64encode(f.read())
    # 二进制方式打开图文件

    f = open(pic2, 'rb')
    # 参数images：图像base64编码
    img2 = base64.b64encode(f.read())

    # 将byte转为string
    params = {"images": img1.decode() + ',' + img2.decode(), "image_liveness":"faceliveness,faceliveness"}
    params = parse.urlencode(params).encode(encoding='UTF8')

    access_token = GetAccessToken()
    request_url = request_url + "?access_token=" + access_token
    req = request.Request(url=request_url, data=params)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = request.urlopen(req)
    #content = response.read().decode('utf-8')
    content = response.read()

    if content:
        print(content)

    return

'''
    人脸识别（用于计算指定组内用户，与上传图像中人脸的相似度，识别前提为您已经创建了一个人脸库。）
'''

def FaceVerify():

    return


FaceDetct("LHC2.jpg")

FaceMatch("LHC1.jpg", "LYX.jpg")

exit(0)


''' 
# 调用AipFace方式

from aip import AipFace

# 定义常量: APPID AK SK
APPI_KEY = 'XzGs8khP2lCjhyyQq7Yg5aoA'
SE_ID = '10796454'
APCRET_KEY = 'Xf1MZzVn12gSdxnboQRInRu7cdH1WcYS'

# 初始化AipFace对象
aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
filePath = "QMN3.jpg"
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 定义参数变量
options = {
    'max_face_num': 1,
    'face_fields': "age,beauty,expression,faceshape,race,gender,landmark,glasses,qualities",
}
# 调用人脸属性检测接口
result = aipFace.detect(get_file_content(filePath),options)

print(result)
print(type(result))
'''

