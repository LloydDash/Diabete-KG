import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# 数据预处理
X = pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/diabetes_code.xlsx').values
y = pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/drug_antiDiabetes_code.xlsx').iloc[:,5:6].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=50, criterion='entropy', random_state=42)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print("预测结果：", pd.DataFrame(y_pred))

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
result = confusion_matrix(y_test, y_pred)
print("混淆矩阵：")
print(result)

result1 = classification_report(y_test, y_pred)
print("分类报告：")
print(result1)

result2 = accuracy_score(y_test, y_pred)
print("准确率：", result2)
