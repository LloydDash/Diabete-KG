import os
import json
from py2neo import Graph,Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])
        self.data_path = os.path.join(cur_dir, 'data\\patient.json')
        self.g = Graph("http://localhost:7474", auth=("neo4j", "medneo"))

    '''读取文件'''
    def read_nodes(self):
        # 共6类节点
        patients = [] # 病人

        diabetes = [] # 入院诊断糖尿病
        
        illnesses = [] # 疾病

        diabetes_complete = [] # 出院诊断糖尿病

        diabete_drugs = [] # 降糖药

        drugs = [] # 药物

        patient_infos = [] # 病人信息

        cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])
        # 读取提前提取好的入院诊断糖尿病txt文件
        f = open(os.path.join(cur_dir,'data\\diabetes.txt'),encoding='utf-8')
        diabetes = f.read().split('\n')

        # 读取提前提取好的出院诊断疾病txt文件
        f = open(os.path.join(cur_dir,'data\\illnesses.txt'),encoding='utf-8')
        illnesses = f.read().split('\n')

        # 读取提前提取好的出院诊断糖尿病txt文件
        f = open(os.path.join(cur_dir,'data\\diabetes_complete.txt'),encoding='utf-8')
        diabetes_complete = f.read().split('\n')

        # 读取提前提取好的出院诊断药物csv文件
        import pandas as pd
        df = pd.read_csv(os.path.join(cur_dir,"data\\Drug_complete.csv"),encoding="utf-8")
        for d in df['药品名称']:
            drugs.append(d)


        # 构建节点实体关系
        rels_diabetes = [] # 入院诊断 - 降糖药关系
        rels_prescription = [] #　出院诊断－带药关系

        import pandas as pd
        import numpy as np  
        import openpyxl

        # 读入提前提取好的降糖药物xlsx文件
        cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])

        drug_data = pd.read_excel(os.path.join(cur_dir,"data\\Drug.xlsx"))
        d_name = drug_data['药名']
        d_code = drug_data['别名']
        drug_name = []
        drug_code = []
        
        for n in d_name:
            drug_name.append(n)
            # 添加降糖药实体
            diabete_drugs.append(n)
        for c in d_code:
            drug_code.append(c)
    
        # 读入病人降糖药物信息xlsx文件
        med_data = pd.read_excel(os.path.join(cur_dir,'data\\Medicine.xlsx'))
        
        med = []
        for i in range(len(med_data)):
            med.append([])
            med[i].append(med_data['Med0'][i])
            med[i].append(med_data['Med1'][i])
            med[i].append(med_data['Med2'][i])
            med[i].append(med_data['Med3'][i])
            med[i].append(med_data['Med4'][i])
            med[i].append(med_data['Med5'][i])
            med[i].append(med_data['Med6'][i])
            med[i].append(med_data['Med7'][i])
            med[i].append(med_data['Med8'][i])
            med[i].append(med_data['Med9'][i])
            med[i].append(med_data['Med10'][i])
            med[i].append(med_data['Med11'][i])
            med[i].append(med_data['Med12'][i])
            med[i].append(med_data['Med13'][i])
            med[i].append(med_data['Med14'][i])
            med[i].append(med_data['Med15'][i])        
            med[i].append(med_data['Med16'][i])
            med[i].append(med_data['Med17'][i])
            med[i].append(med_data['Med18'][i])
            med[i].append(med_data['Med19'][i])
            med[i].append(med_data['Med20'][i])
            med[i].append(med_data['Med21'][i])
            med[i].append(med_data['Med22'][i])
            med[i].append(med_data['Med23'][i])       
            med[i].append(med_data['Med24'][i])
            med[i].append(med_data['Med25'][i])
            med[i].append(med_data['Med26'][i])
            med[i].append(med_data['Med27'][i])

        # 读入病人出院带药信息xlsx文件
        pres_data = pd.read_excel(os.path.join(cur_dir,'data\\Prescription.xlsx'))
        pres_data = pres_data['带药列表']
        pres = []
        for i in range(len(pres_data)):
            pres.append([])
            pres_list = str(pres_data[i]).split(',')
            for j in pres_list:
                if not j in drug_name:
                    if not j in drug_code:
                        pres[i].append(j)

        count = 0

        # 打开json文件，以字典列表读入
        for d in open(self.data_path,encoding='utf-8'):
            data=json.loads(d)

        for i in range(len(data)):
            patient_dict = {}
            count += 1
            print(count)
            data_json = data[i]
            print(data_json)
            
            patient = data_json['id']
            patient_dict['id'] = patient
            patients.append(patient)

            patient_dict['入院时间'] = data_json['入院时间']
            patient_dict['出院时间'] = data_json['出院时间']
            patient_dict['性别'] = '男' if data_json['性别（男1女2） ']==1 else '女'
            

            # 可能存在出院带药为空的情况，如1516
            if str(data_json['出院带药'])!='nan':
                patient_dict['出院带药'] = data_json['出院带药']
                # 可能出现非降糖药匹配为空的情况，需手动将空值加入列表
                if len(pres[i])>0:
                    patient_dict['非降糖药'] = pres[i]
                else:
                    patient_dict['非降糖药'] = ['无']
            else:
                # 缺失出院带药数据，手动设定空值
                patient_dict['出院带药'] = '缺失'
                patient_dict['非降糖药'] = ['缺失']

            diabete_drug = []
            for j in range(len(med[i])):
                if med[i][j]==1:
                    diabete_drug.append(drug_name[j])
            patient_dict['降糖药'] = diabete_drug

            diabete = data_json['入院诊断 数值 ']
            # 统一糖尿病格式、去重
            whitespace = [' ',',','？','。','\xa0']

            # 可能存在入院诊断 数值 为空的情况，如1516
            if str(diabete)!='nan':

                clean_diabete = "".join([c for c in diabete if c not in whitespace])
                # 统一数字表示
                clean_diabete = clean_diabete.replace('I','1')
                # 更正错别字
                clean_diabete = clean_diabete.replace('形','型')

                diabete = clean_diabete

            # 添加糖尿病诊断 - 降糖药关系
            # 可能存在入院诊断 数值 为空的情况，如1516
            if str(diabete)!='nan':
                for d in diabete_drug:
                    rels_diabetes.append([diabete,d])

            # 添加糖尿病实体
            if str(diabete)!='nan':
                patient_dict['入院诊断'] = diabete
            else:
                patient_dict['入院诊断'] = '缺失'


            # 抽取每个病人的所有诊断疾病
            # 抽取用','分隔的实体
            illness = data_json['出院诊断（先联）'].split(',')
            # 统一出院诊断病格式、化字符串为列表
            whitespace = [' ','；','？','.','\xa0']
            
            ill_list = []
            # 添加疾病实体
            for ill in illness:
                # 抽取用'、'分隔的实体
                if '、' in ill:
                    ill2 = ill.split('、')
                    for ill3 in ill2:    
                        ill3 = "".join([c for c in ill3 if c not in whitespace])
                        if len(ill3)>0:
                            ill_list.append(ill3)
                else:
                    ill = "".join([c for c in ill if c not in whitespace])        
                    if len(ill)>0:
                        ill_list.append(ill)
            # 可能出现出院诊断匹配为空的情况，需手动将空值加入列表
            if len(ill_list)==0:
                ill_list.append('None')
            patient_dict['出院诊断'] = ill_list
            # patient_dict['出院诊断'] =  data_json['出院诊断（先联）']

        #    # 添加检查属性数值
        #     patient_dict['检查'] =[]
        #     num=0
        #     for c in data[i]:
        #         if num>=7:
        #             patient_dict['检查'].append(str(c)+': '+str(data[i][c]))
        #         num+=1 

            # 分别添加每个检查属性数值
            attributes=['入院体重指数 数值 ','入院收缩压','院舒张压','入院腰围 数值 ','导出年龄','发病年龄','胰岛素-空腹 数值','胰岛素-餐后30 数值','胰岛素-餐后60 数值','胰岛素-餐后120 数值',
    'C-肽-空腹 数值','C-肽-餐后30 数值','C-肽-餐后60 数值','C-肽-餐后120 数值','糖化血红蛋白 数值','谷丙转氨酶 数值','谷草转氨酶 数值','碱性磷酸酶 数值','谷酰转肽酶 数值','总胆红素 数值',
    '直接胆红素 数值','总胆汁酸 数值','尿素氮 数值','肌酐 数值','尿酸 数值','甘油三酯 数值','胆固醇 数值','H-胆固醇 数值','L-胆固醇 数值','载脂蛋白AⅠ 数值','脂蛋白(a) 数值',
    '载脂蛋白B 数值','尿微量白蛋白 数值','促甲状腺激素 数值','游离三碘甲状腺原氨酸 数值','游离甲状腺素 数值','甲状腺球蛋白抗体 数值','抗甲状腺过氧化酶抗体 数值','促甲状腺素受体抗体 数值',
    '孕酮 数值','雌二醇 数值','泌乳素 数值','总睾酮 数值','硫酸去氢表雄酮 数值','性激素结合蛋白 数值','血清骨钙素测定 数值','血清I型胶原羟末端肽β特殊序列测定 数值','血清总I型胶原氨基末端肽测定 数值',
    '25-羟基维生素D 数值','葡萄糖 数值','葡萄糖(餐后0.5h) 数值','葡萄糖(餐后1h) 数值','葡萄糖(餐后2h) 数值','尿微量白蛋白/肌酐 数值','eGFR(MDRD) 数值','甲胎蛋白 数值','癌胚抗原 数值',
    '糖类抗原125 数值','糖类抗原15-3 数值','糖类抗原19-9 数值','糖类抗原72-4 数值','糖类抗原242 数值','非小细胞肺癌相关抗原21-1 数值','神经元特异性烯醇化酶 数值','游离前列腺特异性抗原 数值',
    '总前列腺特异性抗原 数值','铁蛋白 数值','抗谷氨酸脱羧酶抗体(GAD-Ab) 数值','胰岛细胞抗体 数值','抗胰岛素抗体(IAA) 数值','出院带药缺失','妊娠','癌症','感染','糖尿病酮症','糖尿病视网膜病变',
    '糖尿病肾病','糖尿病周围神经病变','下肢动脉病变','颈动脉病变','脑血管病','冠心病','高血压病']
            attr_list = []
            for s in attributes:
                if str(data_json[s]) != 'nan':
                    # 数值强制转化为str，以统一neo4j查询格式
                    attr_list.append(str(data_json[s]))
                else:
                    attr_list.append('缺失')

            patient_dict['检查'] = attr_list

            patient_infos.append(patient_dict)
        return set(patients), set(diabetes), set(illnesses),set(diabetes_complete), set(diabete_drugs), set(drugs), rels_diabetes, patient_infos

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点'''
    def create_patients_nodes(self, patient_infos):
        count = 0
        for patient_dict in patient_infos:
            node = Node("Patient", name=patient_dict['id'], 
                        checkin=patient_dict['入院时间'],
                        checkout=patient_dict['出院时间'],
                        gender=patient_dict['性别'],
                        prediagnosis=patient_dict['入院诊断'],
                        postdiagnosis=patient_dict['出院诊断'],
                        prescription=patient_dict['出院带药'],
                        diabete_drug=patient_dict['降糖药'],
                        other_drug=patient_dict['非降糖药'],
                        check=patient_dict['检查'])
            
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        Patients, Diabetes, Illnesses, Diabetes_complete, Diabete_drugs, Drugs, rels_diabetes, patient_infos = self.read_nodes()
        self.create_node('Drug', Drugs)
        print(len(Drugs))
        self.create_node('Diabete_Drug', Diabete_drugs)
        print(len(Diabete_drugs))

        self.create_node('Illness', Illnesses)
        print(len(Illnesses))
        self.create_node('Diabete', Diabetes)
        print(len(Diabetes))
        self.create_node('Diabetes_Complete', Diabetes_complete)
        print(len(Diabetes_complete))

        self.create_patients_nodes(patient_infos)

        return

        '''创建实体关系边'''
    def create_graphrels(self):
        Patients, Diabetes, Illnesses, Diabetes_complete, Diabete_drugs, Drugs, rels_diabetes, patient_infos = self.read_nodes()        
        self.create_relationship('Diabete', 'Diabete_Drug', rels_diabetes, 'recommand_take', '出院带降糖药')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        print(edges)
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

if __name__ == '__main__':
    handler = MedicalGraph()
    print("step1:导入图谱节点中")
    handler.create_graphnodes()
    print("step2:导入图谱边中")      
    handler.create_graphrels()
    