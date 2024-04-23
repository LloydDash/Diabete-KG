# Diabete-KG
糖尿病知识图谱建模及用药推荐

数据源：糖尿病病人住院数据、内分泌降糖药物、其他资源（如百科或其他Web网页，医学领域词库，专业文献书籍）

知识图谱构建：知识抽取、本体建模

用药推荐：基于构建的糖尿病知识图谱，选择模型，统计模型与知识图谱结合使用，预测糖尿病病人使用的药物

一、数据文件说明：

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


二、代码功能说明：

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


三、环境配置说明：

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


整体方案：

知识图谱构建任务：

先对住院数据进行初步处理，从中提取出疾病名称、药品名称等信息。然后按糖尿病和非糖尿病、降糖药和非降糖药进行细分，并与其他信息一起用于构建知识图谱。再对文字标签进行编码，尝试知识图谱查询。最后用不同的机器学习算法进行训练，用训练得到的模型预测带药情况，并选择出最佳模型。

数据处理：

(1)对原始文本的观察：

A.糖尿病病人住院数据.xlsx：

1.“入院诊断 数值 ”列：糖尿病种类，抽取得到糖尿病实体（Diabete）
2.“出院诊断”列：糖尿病外病症（并发症），抽取得到其他疾病实体（Illness）
- 用途： 
1）加入病人信息的知识库 
2）用于给药方案的额外考虑因素（降糖药物） 
3）判断非糖尿病药物
- 观察：
1）发现各药物由逗号分隔开，格式固定，故易于直接提取命名实体
2）有糖尿病实体（Diabete）之外的糖尿病名称出现，额外抽取得到完整糖尿	病实体（Diabetes_Complete）
3.“出院带药”列：糖尿病药物及非糖尿病药物，包含降糖药（Diabete_Drug）和其他药物实体（Drug） 
- 用途： 
1）加入病人信息的知识库 
2）由并发症判断
- 观察： 
发现文本疑似为医生手写处方，多药物伴随规格、用法用量，格式自由无统一	规律可循，故未找到合适方法（如正则化）直接从中提取药物实体

B.内分泌降糖药物.xls：

“药物名称”列提取降糖药实体（Diabete_Drug）


(2)对原始数据的清洗：

A.糖尿病病人住院数据.xlsx：

“入院诊断 数值 ”列：
1）部分原始数据疑似存在错别字：第N型写成第N形
2）部分原始数据数字表示不一致：I或1
3）部分原始数据存在干扰字符：空格、逗号、问号、句号

B.内分泌降糖药物.xls：

1.每个实体后跟随括号，为药物别名；存在一个药名为另一药名的子串
2.糖尿病病人住院数据.xlsx中出院带药可能含降糖药原名或别名
3.在出院带药中进行字符串匹配 
- 方案： 
1）本名、别名分开匹配，最后异或合并 
2）重合字符串排除子串，本名、别名依次查重
- 重合字符串：
1）诺和锐，诺和锐30
		2）精蛋白生物合成人胰岛素注射液，生物合成人胰岛素，重合但不影响
4.名称含两个括号：
1）精蛋白锌重组赖脯胰岛素混合注射液（50R）（优泌乐50），
		2）精蛋白生物合成人胰岛素注射液（预混30R）（诺和灵30R），
		3）精蛋白生物合成人胰岛素注射液（预混50R）（诺和灵50R）
		前一个括号为本名一部分
编程测试名称含两个括号的实体在出院带药中的配对情况，
总结命名规则：
		1）配对无：精蛋白锌重组赖脯胰岛素混合注射液（50R）
		仅有：精蛋白锌重组赖脯胰岛素混合注射液，精蛋白锌重组赖脯胰岛素混			合注射液50(优泌乐50)，精蛋白锌重组赖脯胰岛素混合注射液(优泌乐50)，优			泌乐50(精蛋白锌重组赖脯胰岛素混合注射液)
		2）配对无：预混30R，预混50R
		仅有：诺和灵30R，诺和灵50R
		3）配对无：精蛋白生物合成人胰岛素注射液
		仅有：诺和灵30R，诺和灵50R，诺和灵N
		4）配对无：生物合成人胰岛素
		仅有：诺和灵R
5.用括号分隔降糖药本名、别名，分别用2个列表存储
6.查找重合字符串情况，对每个药物用单独列表存储其子串药物下标
7.对每一个病人分别用降糖药原名和别名匹配其出院带降糖药，并排除重合子串

C.药品字典.txt：

由于无现成的非降糖药文本作为完整数据库，故采用另一种方法抽取实体：
取一个空列表，从“出院带药”那一列的前十行中提取出所有药品名称放入这个空列表中，然后遍历这一列。调出没有输出结果的行，其中就是遗漏的药品名称。将一部分行中遗漏的药品名称提取出来后再放入该列表中，再进行遍历。循环上述过程一直到没有遗漏为止，输出这个列表就得到了药品名称的列表。实际上这个方法依然有遗漏某些药	品名称的可能性。后续在进行随机抽查的过程中也发现了遗漏的药品名称。所以还进行了人工补录。

知识图谱建模：

(1)建立6类节点：

1.糖尿病实体diabetes:读取提前提取好的入院诊断糖尿病txt文件
2.疾病实体illnesses:读取提前提取好的出院诊断疾病txt文件
3.糖尿病完整实体diabetes_complete:读取提前提取好的出院诊断糖尿病txt文件
4.非降糖药实体drugs: 读取提前提取好的出院诊断药物csv文件
5.降糖药实体diabete_drugs读入提前提取好的降糖药物xlsx文件
6.病人实体patients:
1）包含10类属性：
字符串存储：name, checkin, checkout, gender, prescription
列表存储：prediagnosis, postdiagnosis, diabete_drug, other_drug, check
2）读入病人降糖药物信息xlsx文件，读取diabete_drug属性
3）读入病人出院带药信息xlsx文件，读取prescription, other_drug属性
4）打开json文件，以字典列表读入其他属性

(2)建立节点实体关系：入院诊断-降糖药关系


用药推荐任务：

知识图谱查询：

对每一位待预测病人，首先按“入院诊断 数值 ”列对应prediagnosis属性查询知识图谱，筛查出与待预测病人同种糖尿病类型的病人实体；再从待预测病人的“出院诊断”列抽取各疾病实体，以列表形式存储，并依次与知识图谱中每位病人的postdiagnosis属性列表取交集，据此得到交集基数最大的病人，即作为与待预测病人相似度最大的病人实体列表；最后分别取该病人实体列表的降糖药diabete_drug的并集和非降糖药other_drug的并集，作为最后的给药方案集合。

测试得到最高召回率0.555，设想在后续统计模型预测时以知识图谱查询得到的给药方案为取药的集合，从而达到知识图谱与统计模型的结合运用。

机器学习算法：

整体思路是在训练集上提取病人病情信息（糖尿病相关疾病和其他疾病）和出院带药情况并采用比较好的机器学习算法（主要比较了随机森林模型、多项式贝叶斯和伯努利贝叶斯模型）用来拟合和训练，用训练好的模型在测试集上预测出院带药结果。

总体结果显示随机森林算法预测指标较好，对于降糖药物预测F1可以达到较高的0.409，但由于对于非降糖药物的预测召回率较低，这是因为非降糖药物很多（172种），而很多训练数据只含有一两种甚至不含非降糖药，十分稀疏，因而使用随机森林在测试集上预测非降糖药给出的结果必然是稀疏的，但实际测试集很多结果含有多种非降糖药，因此Recall很低。
因此总体F1在0.305左右，相比于其他机器学习算法要高出一些。伯努利贝叶斯分类器预测的结果整体与随机森林相近，而利用图谱查询得到的结果，查全率有所提升，但准确率过低，所以整体不如前面两个方法。

知识图谱查询与机器学习算法结合:

先进行“一”中知识图谱查询得到每个病人的用药预测，再将这些预测出的带药集合分别作为每个病人后续进一步细化取药的全集，用机器学习算法在每个病人各自的取药全集中预测出带药结果。这里的机器学习算法直接选用“二”中性能最好的随机森林模型。

除了准确率较单独用图谱查询有些许下降外，召回率与F1均相应提高；与单独的随机森林算法性能相比，大幅提高了召回率，超过随机森林的2倍，并且保持了不过于低的F1值，F1和准确率基本在随机森林性能的二分之一。

