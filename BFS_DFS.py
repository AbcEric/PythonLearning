# -*- coding:UTF-8 -*-

# def dfs(graph, start):
#     visited, stack = set(), [start]
#     while stack:
#         vertex = stack.pop()
#         if vertex not in visited:
#             visited.add(vertex)
#             stack.extend(graph[vertex] - visited)
#     return visited

# DFS: 因要递归查找，时间长，效率低（BFS：占用空间大！递归的空间也大啊？）
def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path

    # if not graph.has_key(start):
    # Python3取消了has_key
    if start not in graph:
        return None

    for node in graph[start]:
        if node not in path:    # 只能走一次！
            # 递归方式查找下一个：
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath

    return None


def find_all_paths(graph, start, end, path=[]):
    print(start, end, path)
    path = path + [start]
    if start == end:
        return [path]

    # if not graph.has_key(start):
    if start not in graph:
        return []
    paths = []

    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            print(node, "-", end, ":", newpaths)
            for newpath in newpaths:
                paths.append(newpath)

    return paths


def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    # if not graph.has_key(start):
    if start not in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

# BFS
def find_all_paths_bfs(graph, start, end):
    todo = [[start, [start]]]
    while 0 < len(todo):
        (node, path) = todo.pop(0)
        for next_node in graph[node]:
            if next_node in path:
                continue
            elif next_node == end:
                yield path + [next_node]
            else:
                todo.append([next_node, path + [next_node]])


# def recursive_dfs(graph, start, path=[]):
#     '''recursive depth first search from start'''
#     path = path + [start]
#     for node in graph[start]:
#         if not node in path:
#             path = recursive_dfs(graph, node, path)
#     return path


# def iterative_dfs(graph, start, path=[]):
#     '''iterative depth first search from start'''
#     q = [start]
#     while q:
#         v = q.pop(0)
#         if v not in path:
#             path = path + [v]
#             q = graph[v] + q
#     return path


def iterative_bfs(graph, start, path=[]):
    '''iterative breadth first search from start'''
    q = [start]
    while q:
        v = q.pop(0)
        if not v in path:
            path = path + [v]
            q = q + graph[v]
    return path

if __name__ == '__main__':
    # 采用Dict存储：相当于树Tree
    graph = {'A': ['B', 'C', 'F'],
             'B': ['C', 'D'],
             'C': ['D', 'F'],
             'D': ['C', 'E'],
             'F': ['E'],
             'E': []
             }

    print("Path:", find_path(graph, 'A', 'E'))
    print("All Path:", find_all_paths(graph, 'A', 'D'))
    print("Shortest Path:", find_shortest_path(graph, 'A', 'E'))

    print("##" * 20)

    for path in find_all_paths_bfs(graph, 'A', 'D'):
        print("All Path BFS:", path)

    print("##" * 20)

    '''
       +---- A
       |   /   \
       |  B--D--C
       |   \ | /
       +---- E
    '''
    graph = {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['D', 'E'], 'D': ['E'], 'E': ['A']}
    # print('Recursive dfs: ', recursive_dfs(graph, 'A'))
    # print('Iterative dfs: ', iterative_dfs(graph, 'A'))
    print('Iterative bfs: ', iterative_bfs(graph, 'A'))

    print("##" * 20)
