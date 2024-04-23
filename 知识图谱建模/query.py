import os
import json

from py2neo import Graph,Node,Relationship, NodeMatcher

neo_graph = Graph("http://localhost:7474", auth=("neo4j", "medneo"))

# 版本更新，find,find_one不可用
# find_code_1 = neo_graph.find(
#   label="Patient",
#   property_key="postdiagnosis",
#   property_value=['1型糖尿病','高血压病1极（极高危）','骨量减少','左侧肾上腺占位','糖尿病视网膜病变']
# )
# nodes.match返回值非节点
# find_code_1=neo_graph.nodes.match("Patient", "2型糖尿病").first()
# print (find_code_1['name'])

import pandas as pd 
cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1]) 
p_data = pd.read_excel(os.path.join(cur_dir,'data\\test_input.xlsx'))

prediagnosis_list = []
postdiagnosis_list = []
for i in range(len(p_data)):
    prediagnosis_list.append(p_data["入院诊断 数值 "][i])
    postdiagnosis_list.append(p_data["出院诊断（先联）"][i])

# NodeMatcher查询节点
matcher = NodeMatcher(neo_graph)

dd_list = []
od_list = []
d_list = []


for i in range(len(prediagnosis_list)):
    print(i)
    diabete = str(prediagnosis_list[i])
    # 按照值的大小筛选或者做一些字符串的模糊匹配，把条件表达式写成一个字符串，整体放在where语句中，用 _ 来代指匹配到的节点
    find_list = matcher.match('Patient').where(prediagnosis=diabete)

    similarity = []
    postdiagnosis = postdiagnosis_list[i]
    for node in find_list:
        sim = len(set(node["postdiagnosis"]).intersection(set(postdiagnosis)))
        similarity.append(sim)

    diabete_drug_list = []
    drug_list = []

    count = 0
    for node in find_list:

        if similarity[count]>=max(similarity):
            # print(node['name'],',',node['postdiagnosis'])
            diabete_drug = node['diabete_drug']
            drug = node['other_drug']
            diabete_drug_list.append(diabete_drug)
            drug_list.append(drug)

        count+=1

    diabete_drug_set = ()
    drug_set = ()

    if len(diabete_drug_list)>0:
        diabete_drug_set = set(diabete_drug_list[0])
        for i in range(1, len(diabete_drug_list)):
            diabete_drug_set = diabete_drug_set.union(set(diabete_drug_list[i]))
    if len(drug_list)>0:
        drug_set = set(drug_list[0])
        for i in range(1, len(drug_list)):
            drug_set = drug_set.union(set(drug_list[i]))

    dd_list.append(list(diabete_drug_set))
    od_list.append(list(drug_set))
    d_list.append([list(diabete_drug_set),list(drug_set)])

city = pd.DataFrame(d_list, columns=['降糖药', '非降糖药'])
city.to_csv(os.path.join(cur_dir,'data\\test.csv'),encoding='utf-8',index=False)