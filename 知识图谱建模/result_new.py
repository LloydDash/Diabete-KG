import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

import os
cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])

y_all_pred_diabetes=pd.read_excel(os.path.join(cur_dir, 'train\\tupu_diabetes_code.xlsx'),header=None)
y_all_diabetes=pd.read_excel(os.path.join(cur_dir, 'train\\drugs_antiDiabetes_tester.xlsx'),header=None)
y_all_pred_not=pd.read_excel(os.path.join(cur_dir, 'train\\tupu_others_code.xlsx'),header=None)
y_all_not=pd.read_excel(os.path.join(cur_dir, 'train\\drugs_without_antiDiabetes_tester.xlsx'),header=None)

y_all_pred=pd.concat([y_all_pred_diabetes,y_all_pred_not],axis=1,join='inner',ignore_index=True).values
y_all=pd.concat([y_all_diabetes,y_all_not],axis=1,join='inner',ignore_index=True).values
print(y_all_pred.shape)
print(y_all.shape)


y_all_pred_0=pd.read_csv(os.path.join(cur_dir, 'train\\test.csv')).values
# print(y_all_pred_0.shape)
list_num=[]
for i in range(790):
    diabete=y_all_pred_0[i][0]
    not_diabete=y_all_pred_0[i][1]
    if(diabete=='[]') and (not_diabete=='[]'):
        list_num.append(i)
        continue
print(list_num)

y_all_pred_diabetes_a=pd.read_excel(os.path.join(cur_dir, 'train\\pred_diabetes_test.xlsx'),index_col=0)
y_all_pred_not_a=pd.read_excel(os.path.join(cur_dir, 'train\\pred_not_diabetes_test.xlsx'),index_col=0)
y_all_pred_a=pd.concat([y_all_pred_diabetes_a,y_all_pred_not_a],axis=1,join='inner',ignore_index=True).values
print(y_all_pred_a.shape)

Precision=0
Recall=0
F1=0
for i in range(0,790):
    Inter_tmp=0
    Pred_size=0
    Ref_size=0

    if (i in list_num):
        y_all_pred[i]=y_all_pred_a[i]
    for j in range(0,200):
      if (y_all_pred[i][j]==1):
         Pred_size+=1
         if (y_all_pred[i][j] == y_all[i][j]):
             Inter_tmp += 1
      if (y_all[i][j]==1):
         Ref_size+=1

    if (Pred_size==0):
        Precision_tmp = 1.0
    else:
        Precision_tmp = Inter_tmp / Pred_size
    if (Ref_size==0):
        Recall_tmp = 1.0
    else:
        Recall_tmp = Inter_tmp / Ref_size
    if(Recall_tmp==Precision_tmp) and (Recall_tmp==0):
      F1_tmp= 0.0
    else:
      F1_tmp=(2*Precision_tmp*Recall_tmp)/(Precision_tmp+Recall_tmp)
    print(Precision_tmp)
    Precision+=Precision_tmp
    Recall+=Recall_tmp
    F1+=F1_tmp
print("Precision:",Precision/sum)
print("Recall:",Recall/sum)
print("F1:",F1/sum)
# pd.DataFrame(y_all_pred).to_excel('pred_all_last.xlsx')