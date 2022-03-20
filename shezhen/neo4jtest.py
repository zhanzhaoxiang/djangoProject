import time
from functools import reduce
from py2neo import Graph

# neo4j图数据库连接
start1 = time.time()
test_graph = Graph(
    "http://localhost:7474", auth=("neo4j", "neo4j")
)
end1 = time.time()
print('连接时间：', end1 - start1)

# 输入症状，特征查询
while True:

    # 对有这类症状的疾病查询
    symptom = input('请输入症状，特征：').split('，')
    # print(symptom)
    data4 = []  # 查询原结果组
    desc1 = []  # 查询得疾病结果
    # subject = []
    # sql查询
    for i in symptom:
        data4.append(test_graph.run(
            "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(
                i)).data())
    # print(data4)
    for i in range(len(data4)):
        desc1.append({i['m.name'] for i in data4[i]})
    # print(len(desc1))
    desc = reduce(lambda x, y: x & y, desc1)  # 对查询结果取交集
    if desc == set():  # 若结果为空，则提示询问医生
        desc = {'无结果，请询问医生'}
    # print(desc)
    # for i in data4:
    #     # print(i)
    #     subject.append(i[0]['n.name'])
    # print(subject)
    # 输出查询结果
    final_answer = '症状：{0}，可能染上的疾病有：{1}'.format('，'.join(symptom), '；'.join(list(desc)[:20]))
    print(final_answer)

    # 根据疾病结果进一步查询
    disease = input('请输入要查询的疾病：')
    start2 = time.time()
    # sql查询节点属性
    data1 = test_graph.run("MATCH (m:Disease) where m.name = '{}' return m.name,m.cause,m.prevent,"
                           "m.cure_way".format(disease)).data()
    data2 = test_graph.run(
        "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(
            disease)).data()
    data3 = test_graph.run(
        "MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(
            disease)).data()
    end2 = time.time()
    print('查询时间：', end2 - start2)

    # 对节点属性输出
    desc = [i['m.cause'] for i in data1]
    subject = data1[0]['m.name']
    final_answer = ('{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:20])))
    print(final_answer)
    desc = [i['m.prevent'] for i in data1]
    subject = data1[0]['m.name']
    final_answer = ('{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:20])))
    print(final_answer)
    desc = [';'.join(i['m.cure_way']) for i in data1]
    subject = data1[0]['m.name']
    final_answer = ('{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:20])))
    print(final_answer)

    # 查询节点的症状关系输出
    desc = [i['n.name'] for i in data2]
    subject = data2[0]['m.name']
    final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:20]))
    print(final_answer)

    # 查询节点常用药物关系输出
    desc = [i['n.name'] for i in data3]
    subject = data3[0]['m.name']
    final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:20]))
    print(final_answer)