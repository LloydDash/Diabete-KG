import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import sklearn.tree as tree

import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

if __name__ == '__main__':
    df=pd.read_csv('D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/diabetes.csv')
    ill=df.values
    # print(ill)
    df1=pd.read_csv('D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/entities_attr.csv')
    patients=df1.loc[df1.实体属性=='postdiagnosis',:].loc[:,['实体属性值']].values
    X=[]
    for line in patients:
        X_line=[]
        for i in ill:
          if i[0] in line[0]:
              X_line.append(1)
          else:
              X_line.append(0)
        X.append(X_line)
    # print(X)

    df2=pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/Medicine (1).xlsx')
    # print(df2)
    medicine=df2.iloc[:,1:-1]
    y=medicine.iloc[:,1:2].values
    # y= list(np.array(y).flatten())
    print(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.4, random_state=42)

    # 将数据集划分为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 创建随机森林模型
    rf = RandomForestClassifier(n_estimators=50, criterion='entropy', random_state=42)

    # 训练模型
    rf.fit(X_train, y_train)

    # 预测测试集
    y_pred = rf.predict(X_test)
    print(pd.DataFrame(y_pred))

    # 计算准确率
    accuracy = rf.score(X_test, y_test)
    print("Accuracy:", accuracy)

