#
# InceptionV3.py
#
# 调研Google训练好的Inception V3模型对图片进行分类:
#
# 两种方式：
# 1.使用Tensorflow1.x调研pb模型: 可以知道更多细节;
# 2.采用Keras调用h5模型：非常简洁；
#

import tensorflow.compat.v1 as tf
import os
import tarfile
import requests
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import cv2
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from keras.applications.inception_v3 import decode_predictions
from keras.preprocessing import image


def getInceptionModel(inception_pretrain_model_dir="../DATA/InceptionV3/inception_model"):
    # inception_v3模型下载
    inception_pretrain_model_url = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'

    # 模型存放地址

    if not os.path.exists(inception_pretrain_model_dir):
        os.makedirs(inception_pretrain_model_dir)

    # 获取文件名，以及文件路径
    filename = inception_pretrain_model_url.split('/')[-1]
    filepath = os.path.join(inception_pretrain_model_dir, filename)

    # 下载模型
    if not os.path.exists(filepath):
        print('download: ', filename)
        r = requests.get(inception_pretrain_model_url, stream=True)
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    print("finished: ", filename)

    # 解压文件
    tarfile.open(filepath, 'r:gz').extractall(inception_pretrain_model_dir)

    # 模型结构存放文件
    log_dir = 'inception_log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # classify_image_graph_def.pb为google训练好的模型
    inception_graph_def_file = os.path.join(inception_pretrain_model_dir, 'classify_image_graph_def.pb')

    return

'''
with tf.Session() as sess:
    # 创建一个图来存放google训练好的模型，load graph 具体实现方法看下面的链接
    with tf.gfile.FastGFile(inception_graph_def_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    # 保存图的结构
    writer = tf.summary.FileWriter(log_dir, sess.graph)
    writer.close()
'''

class NodeLookup(object):
    def __init__(self,
                 label_lookup_path='../DATA/InceptionV3/inception_model/imagenet_2012_challenge_label_map_proto.pbtxt',
                 uid_lookup_path='../DATA/InceptionV3/inception_model/imagenet_synset_to_human_label_map.txt'):
        self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

    def load(self, label_lookup_path, uid_lookup_path):
        # 加载分类字符串n ------ 对应分类名称的文件
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        uid_to_human = {}

        # 一行一行读取数据
        for line in proto_as_ascii_lines:
            # 去掉换行符
            line = line.strip('\n')
            # 按照‘\t’分割
            parsed_items = line.split('\t')
            # 获取分类编号和分类名称
            uid = parsed_items[0]
            human_string = parsed_items[1]
            # 保存编号字符串-----与分类名称映射关系
            uid_to_human[uid] = human_string

        # 加载分类字符串n ----- 对应分类编号1-1000的文件
        proto_as_ascii_lines = tf.gfile.GFile(label_lookup_path).readlines()
        node_id_to_uid = {}

        for line in proto_as_ascii_lines:
            if line.startswith('  target_class:'):
                # 获取分类编号1-1000
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                # 获取编号字符串n****
                target_class_string = line.split(': ')[1]
                # 保存分类编号1-1000与编号字符串n****的映射关系
                node_id_to_uid[target_class] = target_class_string[1:-2]

        # 建立分类编号1-1000对应分类名称的映射关系
        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            # 获取分类名称
            name = uid_to_human[val]
            # 建立分类编号1-1000到分类名称的映射关系
            node_id_to_name[key] = name

        return node_id_to_name

    # 传入分类编号1-1000返回分类名称
    def id_to_string(self, node_id):
        if node_id not in self.node_lookup:
            return ''
        return self.node_lookup[node_id]


def tf_main(model_path):
    # 创建一个图来存放google训练好的模型  #2 load graph
    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')

        imgpath = "../DATA/InceptionV3/images"
        print("Now predict image in ", imgpath)
        # 遍历目录
        for root, dirs, files in os.walk(imgpath):
            for file in files:
                # 载入图片
                image_data = tf.gfile.FastGFile(os.path.join(root, file), 'rb').read()
                predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})  # 图片格式是jpg格式
                predictions = np.squeeze(predictions)  # 把结果转为1维

                # 打印图片路径及名称
                image_path = os.path.join(root, file)
                print(image_path)
                # 显示图片
                img = Image.open(image_path)
                plt.imshow(img)
                plt.axis('off')
                plt.show()

                # 排序
                print(predictions)
                top_k = predictions.argsort()[-5:][::-1]
                node_lookup = NodeLookup()
                for node_id in top_k:
                    # 获取分类名称
                    human_string = node_lookup.id_to_string(node_id)
                    # 获取该分类的置信度
                    score = predictions[node_id]
                    print('%s (score = %.5f)' % (human_string, score))

                print()


def keras_main():
    # inception_v3_weights_tf_dim_ordering_tf_kernels.h5: 保存在C:\Users\Eric\.keras\models目录下。
    model = InceptionV3()
    # model.summary()

    # 按照 InceptionV3 模型的默认输入尺寸
    # img = image.load_img('../DATA/InceptionV3/images/cat.jpg', target_size=(299, 299))
    #
    # # 提取特征
    # x = image.img_to_array(img)
    # x = np.expand_dims(x, axis=0)
    # x = preprocess_input(x)
    #
    # preds = model.predict(x)
    #
    # print('Predicted:', decode_predictions(preds, top=3)[0])

    imgpath = "../DATA/InceptionV3/images"
    print("Now predict image in ", imgpath)
    # 遍历目录
    for root, dirs, files in os.walk(imgpath):
        for file in files:
            img = image.load_img(os.path.join(imgpath, file), target_size=(299, 299))

            cv2.imshow("DEMO", cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
            cv2.waitKey(2000)
            # 提取特征
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            print(type(x), x.shape)
            cv2.imshow("DEMO2", x[0])
            cv2.waitKey(2000)

            preds = model.predict(x)

            print('Predicted:', decode_predictions(preds, top=3)[0])


if __name__ == '__main__':
    model = '../DATA/InceptionV3/inception_model/classify_image_graph_def.pb'

    # tf_main(model)
    keras_main()
