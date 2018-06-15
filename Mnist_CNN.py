from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

# 输入参数实际为28x28=784个像素，输出为10个概率

# 初始化权重函数
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1);
    return tf.Variable(initial)

# 初始化偏置项
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# 定义卷积函数："SAME"表全0填充，步长为1
def conv2d(x, w):
    return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding='SAME')

# 定义一个2*2的最大池化层：过滤器尺寸2x2，步长为1，全0填充
def max_pool_2_2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


if __name__ == "__main__":

    # 定义输入变量: 图片大小28x28
    x = tf.placeholder("float", shape=[None, 784])
    # 定义输出变量: 10个数字
    y_ = tf.placeholder("float", shape=[None, 10])

    # 卷积和池化可看做图像特征的自动提取过程！

    # 初始化权重,第一层卷积，32的意思代表的是输出32个通道。
    # 其实，也就是设置32个卷积，每一个卷积都会对图像进行卷积操作，即每个小块提取32个特征值
    # 5x5代表过滤器尺寸，1表示当前层的深度，32代表过滤器的深度(处理后的深度)
    w_conv1 = weight_variable([5, 5, 1, 32])
    # 为何没有使用如下方法进行初始化，是通过下面sess.run(tf.initialize_all_variables())完成!!!
    # w_conv1 = tf.get_variable('weights', [5,5,1,32], initializer = tf.truncated_normal_initializer(stddev=0.1))

    # 初始化偏置项
    b_conv1 = bias_variable([32])

    # 将输入的x（黑白图片是二维神经元，RGB图片是三维神经元：均变成数据流？）转成一个4D向量，第2、3维对应图片的宽高，
    # 最后一维代表图片的颜色通道数
    # 输入的图像为灰度图，所以通道数为1，如果是RGB图，通道数为3
    # tf.reshape(x,[-1,28,28,1])的意思是将x自动转换成28*28*1的数组
    # -1的意思是代表不知道x的shape，它会按照后面的设置进行转换
    x_image = tf.reshape(x, [-1, 28, 28, 1])

    # conf2d卷积并激活：卷积层节点的输入只是上一层的部分节点（通常3x3或5x5），连接参数将比全连接方式大副减少。
    # 处理后的节点矩阵将变得更深！
    # relu为ReLU激活函数：实现去线性化
    # 输入：28x28x1   输出：28x28x32矩阵
    h_conv1 = tf.nn.relu(conv2d(x_image, w_conv1) + b_conv1)

    # 池化:缩小矩阵的大小，但不会改变三位矩阵的深度，相当于降低分辨率。
    # 目的是减少最后全连接层中的参数，在加快计算速度的同时可防止过拟合问题。
    # 采用最大池化层（max pooling），不是节点的加权和，采用更加简单的最大值。
    # 池化后的大小确定：过滤器即池化视野为2x2，strides为1（见上）步长，因此大小减半
    # 输入：28x28x32矩阵   输出：14x14x32
    h_pool1 = max_pool_2_2(h_conv1)

    # 第二层卷积：
    # 初始权重：过滤器尺寸5x5，从当前层深度32（上一层的输出）处理到64
    w_conv2 = weight_variable([5, 5, 32, 64])

    # 初始化偏置项
    b_conv2 = bias_variable([64])

    # 将第一层卷积池化后的结果作为第二层卷积的输入
    # 输入：14x14x32   输出：14x14x64
    h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)

    # 池化：14x14x64   输出：7x7x64
    h_pool2 = max_pool_2_2(h_conv2)

    # 设置全连接层的权重：1024是与下面的全连接参数对应，7x7x64是上面的输出？
    w_fc1 = weight_variable([7 * 7 * 64, 1024])

    # 设置全连接层的偏置
    b_fc1 = bias_variable([1024])

    # 将第二层卷积池化后的结果，转成一个7*7*64的数组（本身不就是吗？目的是转4维？）
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])

    # 通过全连接之后并激活
    # matmul是矩阵相乘？
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)

    # 防止过拟合: dropout在训练时随机将部分节点的输出改为0
    keep_prob = tf.placeholder("float")
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # 输出层
    w_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    # Softmax层：用于分类，得到属于不同种类的概率分布情况
    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)

    # 日志输出，每迭代100次输出一次日志
    # 定义交叉熵为损失函数
    cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))

    # 定义最小化交叉熵
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    # 定义准确率计算
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

    # 声明Saver类用于保存模型
    saver = tf.train.Saver()

    # 计算入口：
    FIRST = 0

    with tf.Session() as sess:
        # 首次运行，需要初始化参数数据
        if FIRST == 1:
            sess.run(tf.initialize_all_variables())
            # 下载minist的手写数字的数据集
        else:
            # 恢复模型
            saver.restore(sess, "model/mnist_cnn_model.ckpt")

        mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

        #    for i in range(20000):
        for i in range(1000):
            batch = mnist.train.next_batch(50)

            if i % 100 == 0:
                train_accuracy = accuracy.eval(session=sess, feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
                print("step %d,training accuracy %g" % (i, train_accuracy))

            train_step.run(session=sess, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

        # 保存模型：
        saver.save(sess, "model/mnist_cnn_model.ckpt")

        print("test accuracy %g" % accuracy.eval(session=sess, feed_dict={
            x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

        # 如何应用训练好的模型进行预测？无需卷积等过程，直接根据输入32x32x1，调用训练好的参数得出预测结果！
