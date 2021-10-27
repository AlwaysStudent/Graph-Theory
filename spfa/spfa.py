import queue
import sys

import graph


class LinkList:
    def __init__(self, vertex=-1):
        self.vertex = vertex
        self.next = [None]


class SPFA:
    def __init__(self, g: graph.Graph):
        # 存储图的信息
        self.graph = g
        # 存储前置节点信息
        self.pre_vertex = [{"ShortestPreVertex": [-1], "SecondShortestPreVertex": [-1]} for i in
                           range(g.vertex_number + 1)]
        # 存储入队次数
        self.count = [0 for i in range(g.vertex_number + 1)]
        # 存储该点是否在队列中
        self.flag = [False for i in range(g.vertex_number + 1)]
        # 存储最短路的前置节点
        self.distance = [sys.maxsize for i in range(g.vertex_number + 1)]
        # 存储单源点起点位置
        self.vertex = -1
    
    def run(self, vertex):
        # 设置单源点起点位置
        self.vertex = vertex
        # 声明队列并将起点放入队列
        op = queue.Queue()
        op.put(vertex)
        # 完成起点到起点的初始化
        self.distance[vertex] = 0
        self.flag[vertex] = True
        self.count[vertex] += 1
        # 当队列不为空时进行循环
        while not op.empty():
            # 获取当前节点
            temp = op.get()
            # 对当前节点进行松弛
            for key, value in self.graph.edge[temp].items():
                # 如果存在最短路径权重相同的情况, 则将当前路径也加入到最短路径中
                if self.distance[temp] + value == self.distance[key]:
                    # 为了避免出现重复多个节点, 因此进行去重
                    flag = False
                    for i in self.pre_vertex[key]["ShortestPreVertex"]:
                        if i == temp:
                            flag = True
                            break
                    if flag is False:
                        self.pre_vertex[key]["ShortestPreVertex"].append(temp)
                
                # 如果当前节点可以进行松弛, 就更新当前节点的最短路和次短路, 其中次短路为之前的最短路, 最短路为新更新的节点
                if self.distance[temp] + value < self.distance[key]:
                    self.distance[key] = self.distance[temp] + value
                    self.pre_vertex[key]["SecondShortestPreVertex"] = self.pre_vertex[key]["ShortestPreVertex"]
                    self.pre_vertex[key]["ShortestPreVertex"] = [temp]
                    # 如果松弛后的最短路节点不在当前队列中, 那么加入当前队列
                    if self.flag[key] is False:
                        op.put(key)
                        self.count[key] += 1
                        self.flag[key] = True
                # 如果某个节点入队的次数超过总的节点个数, 那么就证明一定存在负圈
                for i in self.count:
                    if i >= self.graph.vertex_number:
                        raise ValueError("存在负圈!")

    # 输出
    def print(self):
        for i in range(len(self.pre_vertex)):
            print(f"-------------------------")
            print(f"From [{self.vertex}] to [{i}]: ")
            
            # 构建存储最短路的字典
            sw = self.create_dict(self.pre_vertex[i]["ShortestPreVertex"], "ShortestPreVertex")
            # 构建存储次短路的字典
            ssw = self.create_dict(self.pre_vertex[i]["SecondShortestPreVertex"], "ShortestPreVertex")

            print(f"-- ShortestPreVertex: ")
            # 计算并输出最短路路径上的节点和距离
            self.format_calc_path(sw, i)
            print(f"-- SecondShortestPreVertex: ")
            # 计算并输出次短路路径上的节点和距离
            self.format_calc_path(ssw, i)
    
    # 计算并输出指定路径的节点和距离
    def format_calc_path(self, shortest_path_dict: dict, current_vertex):
        # 对于源点的处理方式
        if shortest_path_dict is None:
            return f"Just Direct to {self.vertex}"
        # 初始化存储所有格式化完成需要输出的字符串
        format_string_list = []
        # 使用递归函数打开最短路所记录的字典
        path_list_without_handle = open_dict_to_list(shortest_path_dict, current_vertex)
        # 对路径数组进行处理并返回真实路径
        temp_list = [i.split("-")[:-1] for i in path_list_without_handle]
        path_list = []
        for i in temp_list:
            path_list.append([int(j) for j in i])
        # 记录所有的路径长度的数组
        count_list = []
        # 计算路径并根据路径上的节点格式化输出字符串
        for i in path_list:
            temp_string = f""
            count = 0
            for j in range(len(i)):
                if j < len(i) - 1:
                    count += self.graph.edge[i[j]][i[j + 1]]
                temp_string += f"[{i[j]}]->"
            count_list.append(count)
            temp_string += f"[Finish]\nDistance: {count}"
            format_string_list.append(temp_string)
        # 对于一些可能存在问题的次短路进行筛选
        temp = sys.maxsize
        index_list = []
        for index in range(len(count_list)):
            if count_list[index] < temp:
                temp = count_list[index]
                index_list = [index]
            if count_list[index] == temp:
                index_list.append(index)
        # 输出筛选结果
        for i in index_list:
            print(format_string_list[i])
    
    # 使用递归的方式, 通过前置节点数组, 构成路径上的节点组成的字典
    def create_dict(self, current, key):
        if current == [-1]:
            return None
        temp = dict()
        for i in current:
            temp[i] = self.create_dict(self.pre_vertex[i][key], key)
        return temp


# 使用递归的方式, 将路径节点组成的字典拆解并构成记录路径经过节点的字符串
def open_dict_to_list(path_dict, current):
    if path_dict is None:
        return [str(current) + "-"]
    path_list = []
    for i in path_dict.keys():
        temp = open_dict_to_list(path_dict[i], i)
        path_list.extend(temp)
    path = []
    for i in path_list:
        path.append(f"{i}{current}-")
    return path
    

def main():
    # 建立图的对象
    g = graph.Graph()
    # 从文件中读出数据
    g.read_from_csv("./data/graph-generated.csv")
    # 使用图的对象建立spfa算法对象
    spfa = SPFA(g)
    # 以0为单源点求其到其他所有节点的最短路
    spfa.run(0)
    # 输出结果
    spfa.print()


if __name__ == '__main__':
    main()
