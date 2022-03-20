from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd
from time import time


# # 导入Excel
# def load_data():
#     # 导入Excel文件
#     path = 'shezhen.xlsx'
#     sheet = 'Sheet1'
#     data = pd.read_excel(path, sheet_name=sheet, header=0)
#     return data
#
#
# # 连接neo4j数据库
# def rel_neo4j():
#     # 连接neo4j数据库，ip，用户名，密码
#     graph = Graph("http://localhost:7474", auth=("neo4j", "neo4j"))
#     # 清除原有数据
#     graph.delete_all()
#     return graph
#
#
# # 抽取节点
# def find_nodes(data):
#     labels = list(data)  # 0. 直接使用 list 关键字，返回一个list
#     # columns_name1 = [column for column in data]  # 1.链表推倒式_获取Pandas列名的几种方法
#     # columns_name2 = data.columns.values  # 2.通过columns字段获取，返回一个numpy型的array
#     # columns_name3 = data.columns.tolist()  # 4.df.columns 返回Index，可以通过 tolist(), 或者 list（array） 转换为list
#     # 7类节点
#     diseases = []  # 病理
#     tongue_colors = []  # 舌质颜色
#     tongue_actives = []  # 舌质老嫩
#     tongue_sizes = []  # 舌质胖瘦
#     coating_colors = []  # 舌苔颜色
#     coating_sizes = []  # 舌苔薄厚
#     fluids = []  # 津液
#     nodes = [diseases, tongue_colors, tongue_actives, tongue_sizes, coating_colors, coating_sizes, fluids]
#     # 去重提取各类节点
#     for i in range(len(nodes)):
#         for j in range(0, len(data)):
#             nodes[i].append(data[labels[i]][j])
#         nodes[i] = list(set(nodes[i]))  # 去重
#     return labels, nodes
#
#
# # 抽取关系
# def find_relation(data, labels):
#     # 6种关系
#     relations = ['disease_tongue_colors', 'disease_tongue_actives', 'disease_tongue_sizes', 'disease_coating_colors',
#                  'disease_coating_sizes', 'disease_fluids']
#     # 抽取整个表格数据
#     disease = data[labels[0]]  # 病理列
#     tongue_color = data[labels[1]]  # 舌质颜色列
#     tongue_active = data[labels[2]]  # 舌质老嫩列
#     tongue_size = data[labels[3]]  # 舌质胖瘦列
#     coating_color = data[labels[4]]  # 舌苔颜色列
#     coating_size = data[labels[5]]  # 舌苔薄厚列
#     fluid = data[labels[6]]  # 津液列
#     symptoms = [tongue_color, tongue_active, tongue_size, coating_color, coating_size, fluid]
#     # 组合关系【disease，relations，symptoms】,用元组还可以排序
#     combinations = []
#     for i in range(len(relations)):
#         for j in range(len(data)):
#             combinations.append((disease[j], relations[i], symptoms[i][j]))
#     return combinations, relations
#
#
# # 导入节点
# def creat_nodes(labels, nodes, graph):
#     # 创建新节点
#     for i in range(len(nodes)):
#         for name in nodes[i]:
#             node = Node(labels[i], name=name)  # 节点标签，名字
#             graph.create(node)
#             print(i)
#
#
# # 导入关系
# def creat_relation(data, combinations, labels, graph, relations):
#     matcher = NodeMatcher(graph)
#     for j in range(1, len(labels)):
#         for i in range(len(data[labels[0]])):
#             relation = Relationship(matcher.match(labels[0], name=data[labels[0]][i]).first(),
#                                     relations[j - 1],
#                                     matcher.match(labels[j], name=data[labels[j]][i]).first()
#                                     )
#             graph.create(relation)
#             print(i)


if __name__ == '__main__':
    print('0')
    # data = load_data()
    # print('1')
    # graph = rel_neo4j()
    # print('2')
    # (labels, nodes) = find_nodes(data)
    # print('3')
    # (combinations, relations) = find_relation(data, labels)
    # print('4')
    # creat_nodes(labels, nodes, graph)
    # print('5')
    # creat_relation(data, combinations, labels, graph, relations)
    # print('success')
