# 抽取所有诊断疾病
# 出院诊断（先联）为较为固定格式分隔的实体，无需字符串匹配
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
illnesses = []
# 去除数据中干扰字符，如‘性腺功能减退；’，‘胃底体交界间质瘤？’, ‘.右肺结节’,‘\xa0维生素D缺乏’
whitespace = [' ','；','？','.','\xa0']
for i in range(len(data)):

    data_json = data[i]
    # 抽取每个病人的所有诊断疾病
    # 抽取用','分隔的实体
    illness = data_json['出院诊断（先联）'].split(',')
    
    # 添加疾病实体
    for ill in illness:
        # 抽取用'、'分隔的实体
        if '、' in ill:
            ill2 = ill.split('、')
            for ill3 in ill2:    
                ill3 = "".join([c for c in ill3 if c not in whitespace])
                if len(ill3)>0:
                    illnesses.append(ill3)
                    if ill3.find('糖尿病')>=0:
                        diabetes.append(ill3)
        else:
            ill = "".join([c for c in ill if c not in whitespace])        
            if len(ill)>0:
                illnesses.append(ill)

                if ill.find('糖尿病')>=0:
                    diabetes.append(ill)
illnesses = set(illnesses)
print(illnesses,len(illnesses))

diabetes=set(diabetes)
print(diabetes,len(diabetes))

f_diabetes = open( os.path.join(cur_dir,'diabetes_complete.txt'), 'w+', encoding = 'utf-8')

f_diabetes.write('\n'.join(list(diabetes)))

f_diabetes.close()

f_illnesses = open( os.path.join(cur_dir,'illnesses.txt'), 'w+', encoding = 'utf-8')

f_illnesses.write('\n'.join(list(illnesses)))

f_illnesses.close()