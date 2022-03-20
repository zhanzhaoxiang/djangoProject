from functools import reduce
from py2neo import Graph


# 连接neo4j数据库
def rel_neo4j():
    # 连接neo4j数据库，ip，用户名，密码
    graph = Graph("http://localhost:7474", auth=("neo4j", "neo4j"))
    return graph


# # 查询
# def search_rel(graph):
#     # 输入症状，特征查询
#     # while True:
#     # 对有这类症状的疾病查询
#     labels = ['舌质颜色', '舌质老嫩', '舌质胖瘦', '舌苔颜色', '舌苔厚薄', '津液']
#     des = ['舌质颜色(淡白，淡红，红绛，青紫)', '舌质老嫩(嫩，老，适中)', '舌质胖瘦(胖，瘦，适中)', '舌苔颜色(白苔，黄苔，灰黑苔)', '舌苔厚薄(光剥无苔，少苔，薄苔，厚苔)',
#            '津液(润苔，湿滑苔，干燥，燥糙苔，垢腻苔)']
#     relations = ['disease_tongue_colors', 'disease_tongue_actives', 'disease_tongue_sizes',
#                  'disease_coating_colors',
#                  'disease_coating_sizes', 'disease_fluids']
#     # symptom= [input('请输入{}：'.format(i)) for i in des]
#
#     symptom = user.submit()
#     print(symptom)
#     answer = []
#     answers = []  # 每个条件的结果
#     # sql查询
#     for i in range(len(symptom)):
#         answers.append(graph.run(
#             "MATCH (m:{0})-[r:{1}]-(n:临床意义) where m.name='{2}' return n.name".format(labels[i], relations[i],
#                                                                                      symptom[i])).data()
#                        )
#     for i in range(len(answers)):
#         answer.append({str(i['n.name']) for i in answers[i]})
#     # print(answer)
#     final_answer = reduce(lambda x, y: x & y, answer)  # 对查询结果取交集
#     # print(final_answer)
#     if final_answer == set():  # 若结果为空，则提示询问医生
#         final_answer = {'无结果，请询问医生'}
#     final_answer = '症状：{0}，可能染上的疾病有：{1}'.format('，'.join(symptom), '；'.join(list(final_answer)))
#     print(final_answer)
#     return list(final_answer)


# graphs = rel_neo4j()
# final_answers = search_rel(graphs)
