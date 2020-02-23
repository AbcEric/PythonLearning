#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MCTS模拟程序：每次从AVAILABLE_CHOICES中选择一个数字，经过MAX_ROUND_NUMBER轮后，综合为或接近TARGET。
#
# 原来的程序有BUG：会重复选取子节点，已修复。
#

import sys
import math
import random
import numpy as np

# AVAILABLE_CHOICES = [1, -1, 2, -2]
AVAILABLE_CHOICES = [1, -1, 2, -2, 5, 7, 13, 15, 16, 20, 25, 3, 8, 30, 50, 9, 11, 10, -3]
AVAILABLE_CHOICE_NUMBER = len(AVAILABLE_CHOICES)
MAX_ROUND_NUMBER = 25         # 轮数
BUDGET = 50                   # 每轮模拟的最大次数
TARGET = 100                  # 最终要达到的目标

class State(object):
    """
    蒙特卡罗树搜索的游戏状态，记录在某一个Node节点下的状态数据，包含当前的游戏得分、当前的游戏round数、从开始到当前的执行记录。
    需要实现判断当前状态是否达到游戏结束状态，支持从Action集合中随机取出操作。
    """

    def __init__(self):
        self.current_value = 0.0
        # For the first root node, the index is 0 and the game should start from 1
        self.current_round_index = 0
        self.cumulative_choices = []

    # 模拟选取的数字值：
    def get_current_value(self):
        return self.current_value

    def set_current_value(self, value):
        self.current_value = value

    def get_current_round_index(self):
        return self.current_round_index

    def set_current_round_index(self, turn):
        self.current_round_index = turn

    def get_cumulative_choices(self):
        return self.cumulative_choices

    def set_cumulative_choices(self, choices):
        self.cumulative_choices = choices

    # 到指定轮数就结束：
    def is_terminal(self):
        # The round index starts from 1 to max round number
        return self.current_round_index == MAX_ROUND_NUMBER

    # 与TARGET目标越接近，reward越高（0）
    def compute_reward(self):
        return -abs(TARGET - self.current_value)

    # 每次随机选择下一个节点：
    def get_next_state_with_random_choice(self):
        random_choice = random.choice([choice for choice in AVAILABLE_CHOICES])
        # print("state (%d): random_choice = %d" % (hash(self), random_choice))

        next_state = State()
        next_state.set_current_value(self.current_value + random_choice)
        next_state.set_current_round_index(self.current_round_index + 1)
        next_state.set_cumulative_choices(self.cumulative_choices +
                                          [random_choice])

        return next_state

    def __repr__(self):
        return "State: {}, value: {}, round: {}, choices: {}".format(
            hash(self), self.current_value, self.current_round_index,
            self.cumulative_choices)


class Node(object):
    """
    蒙特卡罗树搜索的树结构的Node，包含了父节点和子节点等信息，还有用于计算UCB的遍历次数和quality值，还有游戏选择这个Node的State。
    """

    def __init__(self):
        self.parent = None
        self.children = []

        self.visit_times = 0
        self.quality_value = 0.0

        self.state = None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def get_visit_times(self):
        return self.visit_times

    def set_visit_times(self, times):
        self.visit_times = times

    def visit_times_add_one(self):
        self.visit_times += 1

    def get_quality_value(self):
        return self.quality_value

    def set_quality_value(self, value):
        self.quality_value = value

    def quality_value_add_n(self, n):
        self.quality_value += n

    # 是否所有的子节点都选择过：
    def is_all_expand(self):
        return len(self.children) == AVAILABLE_CHOICE_NUMBER

    def add_child(self, sub_node):
        sub_node.set_parent(self)
        self.children.append(sub_node)

    def __repr__(self):
        return "Node: {}, Q/N: {}/{}, state: {}".format(
            hash(self), self.quality_value, self.visit_times, self.state)


def tree_policy(node):
    """
    蒙特卡罗树搜索的Selection和Expansion阶段，传入当前需要开始搜索的节点（例如根节点），根据exploration/exploitation算法返回最好的需要expend的节点，
    注意：如果节点是叶子结点直接返回。
    基本策略：是先找当前未选择过的子节点，如果有多个则随机选。如果都选择过就找权衡过exploration/exploitation的UCB值最大的，如果UCB值相等则随机选。
    """

    # Check if the current node is the leaf node
    while not node.get_state().is_terminal():

        if node.is_all_expand():
            # 当当前子节点全部访问过后，找到最佳的子节点，再继续往下访问：
            node = best_child(node, True)
        else:
            # Return the new sub node
            sub_node = expand(node)
            return sub_node

    # Return the leaf node
    return node


def default_policy(node):
    """
    蒙特卡罗树搜索的Simulation阶段，输入一个需要expand的节点，随机操作后创建新的节点，返回新增节点的reward。
    注意：输入的节点应该不是子节点，而且是有未执行的Action可以expend的。
    基本策略：是随机选择Action。
    """

    # Get the state of the game
    current_state = node.get_state()

    # Run until the game over
    while not current_state.is_terminal():
        # Pick one random action to play and get next state
        current_state = current_state.get_next_state_with_random_choice()

    # 计算模拟到终局的结果：
    final_state_reward = current_state.compute_reward()
    # print("final_reward=", final_state_reward, current_state.current_value)
    return final_state_reward


def expand(node):
    """
    输入一个节点，在该节点上拓展一个新的节点，使用random方法执行Action，返回新增的节点。
    注意：需要保证新增的节点与其他节点Action不同。
    """

    # tried_sub_node_states = [
    #     sub_node.get_state() for sub_node in node.get_children()
    # ]
    # print(" --- tried_states=", tried_sub_node_states)
    # new_state = node.get_state().get_next_state_with_random_choice()

    # Check until get the new state which has the different action from others:
    # 有问题！相同的Action由于Node ID不同，也会被视作不同的选择，也就是说永远不等都成立！
    # while new_state in tried_sub_node_states:
    #     new_state = node.get_state().get_next_state_with_random_choice()
    # print(" --- new_states=", new_state)

    tried_sub_node_states_value = [
        sub_node.get_state().get_current_value() for sub_node in node.get_children()
    ]
    # print(" --- tried_states=", tried_sub_node_states_value)
    new_state = node.get_state().get_next_state_with_random_choice()

    # 修改为根据current_value来判断是否选择过：
    while new_state.get_current_value() in tried_sub_node_states_value:
        new_state = node.get_state().get_next_state_with_random_choice()

    sub_node = Node()
    sub_node.set_state(new_state)
    node.add_child(sub_node)

    return sub_node


def best_child(node, is_exploration):
    """
    使用UCB算法，权衡exploration和exploitation后选择得分最高的子节点，
    注意: 如果是预测阶段直接选择当前Q值得分最高的, 此时is_exploration为0！
    """

    # TODO: Use the min float value
    best_score = -sys.maxsize
    best_sub_node = None

    # Travel all sub nodes to find the best one
    for sub_node in node.get_children():

        # Ignore exploration for inference
        if is_exploration:
            C = 1 / math.sqrt(2.0)
        else:
            C = 0.0

        # UCB = quality / times + C * sqrt(2 * ln(total_times) / times)
        left = sub_node.get_quality_value() / sub_node.get_visit_times()
        right = 2.0 * math.log(node.get_visit_times()) / sub_node.get_visit_times()
        score = left + C * math.sqrt(right)

        if score > best_score:
            best_sub_node = sub_node
            best_score = score

    return best_sub_node


def backup(node, reward):
    """
    蒙特卡洛树搜索的Backpropagation阶段，输入前面获取需要expend的节点和新执行Action的reward，反馈给expend节点和上游所有节点并更新对应数据。
    """

    # Update util the root node
    while node != None:
        # Update the visit times
        node.visit_times_add_one()

        # Update the quality value
        node.quality_value_add_n(reward)

        # Change the node to the parent node
        node = node.parent


def MCTS(node):
    """
    蒙特卡洛树搜索算法:
    传入一个根节点，在有限的时间内根据之前已经探索过的树结构expand新节点和更新数据，返回只要exploitation最高的子节点。
    蒙特卡洛树搜索包含四个步骤，Selection、Expansion、Simulation、Backpropagation。
    前两步使用tree policy找到值得探索的节点。
    第三步使用default policy也就是在选中的节点上随机算法选一个子节点并计算reward。
    最后一步使用backup也就是把reward更新到所有经过的选中节点的节点上。
    进行预测时：只需要根据Q值选择exploitation最大的节点即可，找到下一个最优的节点。
    """

    computation_budget = BUDGET

    # Run as much as possible under the computation budget
    for i in range(computation_budget):
        # 1. Find the best node to expand
        expand_node = tree_policy(node)
        # print(">>> expand_node=", format(expand_node))

        # 2. Random run to add node and get reward
        reward = default_policy(expand_node)

        # 3. Update all passing nodes with reward
        backup(expand_node, reward)

    # N. Get the best next node
    best_next_node = best_child(node, False)

    return best_next_node


def main():
    # Create the initialized state and initialized node
    init_state = State()
    init_node = Node()
    init_node.set_state(init_state)
    current_node = init_node

    # Set the rounds to play
    for i in range(MAX_ROUND_NUMBER):
        print("Play round: %d" % (i + 1))
        current_node = MCTS(current_node)
        print("Choose node: {}".format(current_node))


# 实现：选择数字保证累加和为1的游戏模拟?
if __name__ == "__main__":
    main()
