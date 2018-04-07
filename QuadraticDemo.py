import tensorflow as tf
import numpy as np

# 构造一元二次方程的函数：测试TensorFlow
# 运行有问题

# 1. 数据生成：以[x,y]作为特征，此外还有xx, yy, xy, sin(x), sin(y)等
# 300个点，等差分布在-1和1之间，并转化为300x1的二维数组
x_data = np.linspace(-1, 1, 300)[:, np.newaxis]

# 加入噪声点，方差为0.05的正态分布
noise = np.random.normal(0, 0.05, x_data.shape)

# y = x^2 - 0.5
y_data = np.square(x_data) - 0.5 + noise

# 创建图？ 定义x和y的占位符，作为输入神经网络的变量
# placeholder临时替代任意操作的张量（即数据），在调用Session对象的run（）方法时使用填充数据作为调用的参数, [None,1]为shape，表明为“none x 1”数组？
'''
xs = tf.placeholder(tf.float32, [None,1])
ys = tf.placeholder(tf.float32, [None,1])
'''
xs = x_data
ys = y_data

# 2. 构建网络模型

# 定义隐藏层和输出层: 输入数据，输入数据的维度，输出数据的维度和激活函数，每一层经过向量化y=weights*x = biases的处理，经过激活函数的非线性化处理后，得到最终输出结果
def add_layer(inputs, in_size, out_size, activation_function = None):
    # 构建权重：隐藏层之间（或隐藏层与输出层）的连接线表示权重，连接线的粗细与深浅表示权重的绝对值大小
    weights = tf.Variable(tf.random_normal([in_size, out_size]))
    # 构建偏置：
    biases = tf.Variable(tf.zeros(1, out_size) + 0.1)
    # 矩阵相乘：matmul为矩阵操作运算
    Wx_plus_b = tf.matmul(inputs, weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs


# 构建隐藏层：隐藏层有20个神经单元
# relu为激活函数，运行时激活神经网络中某一部分神经元，将激活信息向后传入下一层神经网络，定义为f(x) = max(x,0), 加入非线性因素，弥补线性模型的表达力。
# 常见的激活函数有sigmoid, tanh, relu,softplus这4种
h1 = add_layer(xs, 1, 20, activation_function = tf.nn.relu)

# 构建输出层：输出有1个神经元
prediction = add_layer(h1, 20, 1, activation_function = None)

# 构建损失函数：对预测值和真实值差的平方求和再取平均
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices = [1]))

# 运用剃度下降法，以0.1的学习速率最小化损失
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

# 3. 训练模型

# 训练1000次， 每50次输出损失值
init = tf.global_variables_initializer()

# 创建会话
sess = tf.Session()

sess.run(init)

for i in range(1000):
    sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
    if i % 50 == 0:
        print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))
