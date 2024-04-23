# Diabete-KG
糖尿病知识图谱建模及用药推荐

数据文件说明：

知识图谱：
1. patient.xlsx：糖尿病病人住院原始数据
2. drug.xls：内分泌降糖药物原始数据
3. Drug.xlsx：降糖药物xlsx汇总文件
4. Medicine.xlsx：病人降糖药物信息xlsx文件
5. patient.json：病人住院信息json文件
6. Prescription.xlsx：病人出院带药信息xlsx文件
7. Drug_complete.csv：出院诊断药物csv汇总文件
8. drugs_without_antiDiabetes.xlsx：非降糖药xlsx汇总文件
9. 其他txt文件：实体抽取txt汇总文件
10. 其他json文件：neo4j知识图谱中下载的各类节点json文件
11. 其他csv文件：知识图谱建模的实体、关系csv文件

知识图谱查询：
1. test_input.xlsx：测试数据输入文件
2. test.xlsx：预测所有药物结果

随机森林算法：
1. pred_diabetes_test.xlsx：预测降糖药结果（编码形式）

2. pred_not_diabetes_test.xlsx：预测非降糖药结果（编码形式）

3. pred_diabetes_test_decode.xlsx：预测降糖药结果（解码后）

4. pred_not_diabetes_test_decode.xlsx：预测非降糖药结果（解码后）

5. pred_result.xlsx：预测所有药物结果

知识图谱查询与随机森林结合：
1.  pred_all_last.xlsx：预测所有药物结果（编码形式）

2. pred_all.xlsx：预测所有药物结果（解码后）


代码功能说明：

主要代码：
1. build_patientgraph.py：配置并启动neo4j后运行，开始自动构建neo4j知识图谱，打开网址http://localhost:7474，账户名为neo4j，密码为medneo

2. query.py：构建知识图谱后运行，读入当前目录中data文件夹下的test_input.xlsx，查询得到给药方案并在data文件夹下输出为test.csv文件

3. pred.py：使用机器学习算法(随机森林、伯努利贝叶斯)预测降糖药
4. pred_other.py：使用机器学习算法(随机森林、伯努利贝叶斯)预测非降糖药
5. result_diaberes.py：计算降糖药Precision、Recall、F1
6. result_not_diaberes.py：计算非降糖药Precision、Recall、F1
7. result.py：计算所有药物总体Precision、Recall、F1
8. merge_result.py：输出预测结果文件
9. result_new.py：计算知识图谱查询和机器学习算法合并后预测结果以及指标

辅助代码（data文件夹下）：
1. preprocessing.ipynb：进行初步的数据处理，输出降糖药物xlsx文件Drug.xlsx、病人降糖药物信息xlsx文件Medicine.xlsx

2. jsonify.ipynb：病人数据转化为JSON文件，分批次输出生成病人json文件patient_0.json - patient_9.json，后续合并成patient.json

3. diabetes.py： 从病人入院诊断信息中抽取所有糖尿病，输出入院诊断糖尿病txt文件diabetes.txt

4. illnesses.py： 从病人出院诊断信息中抽取所有疾病，并提取出其中含有的糖尿病，输出出院诊断疾病txt文件illnesses.txt，出院诊断糖尿病txt文件diabetes_complete.txt

5. drugs.py：从病人数据中抽取所有药物
6. arguments.yaml：drugs.py参数文件

7. csv1.py：生成知识图谱实体csv文件entities.csv，存储实体类别和id信息
8. csv2.py：生成知识图谱实体csv文件entities_attr.csv，存储实体属性三元组
9. csv3.py：生成知识图谱实体csv文件relationships.csv，存储实体关系三元组


环境配置说明：

知识图谱建模代码环境配置：
1.Python配置环境：
Python 3.11.4
numpy==1.25.2
pandas==2.0.3
py2neo==2021.2.4
2.安装neo4j:
在neo4j\bin文件夹下用命令行运行neo4j.bat console

机器学习算法代码环境配置：
Python配置环境：
Python 3.10
PyCharm Community Edition 2023.1.1
