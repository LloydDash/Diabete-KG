import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

import os
cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])

y_all_pred=pd.read_excel(os.path.join(cur_dir, 'train\\pred_not_diabetes_test.xlsx'),index_col=0).values
y_all=pd.read_excel(os.path.join(cur_dir, 'train\\drugs_without_antiDiabetes_tester.xlsx'),header=None).values
print(y_all_pred)

Precision=0
Recall=0
F1=0
for i in range(0,790):
    Inter_tmp=0
    Pred_size=0
    Ref_size=0
    for j in range(0,172):
      if (y_all_pred[i][j]==1):
         Pred_size+=1
         if (y_all_pred[i][j] == y_all[i][j]):
             Inter_tmp += 1
      if (y_all[i][j]==1):
         Ref_size+=1

    if(Pred_size==0):
        Precision_tmp = 1.0
    else:
        Precision_tmp = Inter_tmp / Pred_size
    if(Ref_size==0):
        Recall_tmp = 1.0
    else:
        Recall_tmp = Inter_tmp / Ref_size
    if(Recall_tmp==Precision_tmp) and (Recall_tmp==0):
      F1_tmp= 0.0
    else:
      F1_tmp=(2*Precision_tmp*Recall_tmp)/(Precision_tmp+Recall_tmp)
    print(Precision_tmp)
    Precision+=Precision_tmp/790
    Recall+=Recall_tmp/790
    F1+=F1_tmp/790
print("Precision:",Precision)
print("Recall:",Recall)
print("F1:",F1)