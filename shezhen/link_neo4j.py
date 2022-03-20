from py2neo import Graph


# 连接neo4j数据库
def rel_neo4j():
    # 连接neo4j数据库，ip，用户名，密码
    graph = Graph("http://localhost:7474", auth=("neo4j", "neo4j"))
    return graph
