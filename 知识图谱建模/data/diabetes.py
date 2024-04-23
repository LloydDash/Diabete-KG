# 抽取所有糖尿病
# 统一格式、去重
# 入院诊断 数值 为固定格式的单个实体，无需字符串匹配
import os
cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])
# print(cur_dir)
data_path = os.path.join(cur_dir,'patient.json')
# print(data_path)
f = open(data_path,encoding='utf-8')

import json
for d in f:
    data= json.loads(d)

diabetes = []
# 去除数据中干扰字符，如‘糖尿病酮症,’,‘2型糖尿病？’, ‘2型糖尿病。’,‘2型糖尿病\xa0\xa0神经炎(股外侧)’
whitespace = [' ',',','？','。','\xa0']
for i in range(len(data)):

    data_json = data[i]
    diabete = data_json['入院诊断 数值 ']

    # 可能存在入院诊断 数值 为空的情况，如1516
    # 添加糖尿病实体
    if str(diabete)!='nan':
        # diabetes.append(diabete)
        clean_diabete = "".join([c for c in diabete if c not in whitespace])
        # 统一数字表示
        clean_diabete = clean_diabete.replace('I','1')
        # 更正错别字
        clean_diabete = clean_diabete.replace('形','型')

        diabetes.append(clean_diabete)
diabetes = set(diabetes)
print(diabetes,len(diabetes))

f_diabetes = open( os.path.join(cur_dir,'diabetes.txt'), 'w', encoding = 'utf-8')

f_diabetes.write('\n'.join(list(diabetes)))

f_diabetes.close()