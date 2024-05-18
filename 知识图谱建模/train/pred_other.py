import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# 数据预处理
df_y=pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/drug_without_antiDiabetes_code.xlsx',header=None)
print(df_y.shape)
X = pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/disease_withoutDiabetes_code1.xlsx',header=None).values
y_all=df_y.values

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

classifier = BernoulliNB()
# classifier = RandomForestClassifier(n_estimators=50, criterion='entropy', random_state=42)
y_all_pred=np.zeros((790,172),dtype=int)
X_pred = pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/disease_withoutDiabetes_code.xlsx',header=None).values

for i in range(0,172):
    y= df_y.iloc[:,i:i+1].values
    classifier.fit(X, y)
    y_pred = classifier.predict(X_pred)
    y_all_pred[:,i]=y_pred
print(y_all_pred)
pd.DataFrame(y_all_pred).to_excel('pred_not_diabetes_test_Ber.xlsx')

# Precision=0
# Recall=0
# F1=0
# for i in range(0,3604):
#     Inter_tmp=0
#     Pred_size=0
#     Ref_size=0
#     for j in range(0,172):
#       if (y_all_pred[i][j]==1):
#          Pred_size+=1
#          if (y_all_pred[i][j] == y_all[i][j]):
#              Inter_tmp += 1
#       if (y_all[i][j]==1):
#          Ref_size+=1
#
#     if(Pred_size==0):
#         Precision_tmp = 1.0
#     else:
#         Precision_tmp = Inter_tmp / Pred_size
#     if(Ref_size==0):
#         Recall_tmp = 1.0
#     else:
#         Recall_tmp = Inter_tmp / Ref_size
#     if(Recall_tmp==Precision_tmp) and (Recall_tmp==0):
#       F1_tmp= 0.0
#     else:
#       F1_tmp=(2*Precision_tmp*Recall_tmp)/(Precision_tmp+Recall_tmp)
#     print(F1_tmp)
#     Precision+=Precision_tmp/3604
#     Recall+=Recall_tmp/3604
#     F1+=F1_tmp/3604
# print(Precision)
# print(Recall)
# print(F1)

