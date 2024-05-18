import numpy as np
import pandas as pd
import warnings
import re
warnings.filterwarnings("ignore")

# y_all_pred_diabetes=pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/pred_diabetes_test.xlsx',index_col=0)
# y_all_diabetes=pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/drugs_antiDiabetes_tester.xlsx',header=None)
# y_all_pred_not=pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/pred_not_diabetes_test.xlsx',index_col=0)
# y_all_not=pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/drugs_without_antiDiabetes_tester.xlsx',header=None)
#
# y_all_pred=pd.concat([y_all_pred_diabetes,y_all_pred_not],axis=1,join='inner',ignore_index=True).values
# y_all=pd.concat([y_all_diabetes,y_all_not],axis=1,join='inner',ignore_index=True).values
# print(y_all_pred.shape)
# print(y_all.shape)

y_all=pd.read_excel(r'D:\Users\李乐意\PycharmProjects\shumo\zsgc_prac\test_result.xlsx',index_col=0).values
y_all_pred=pd.read_csv(r'D:\Users\李乐意\PycharmProjects\shumo\zsgc_prac\test.csv').values
print(y_all_pred.shape)

Precision=0
Recall=0
F1=0
sum=0
list_num=[]
for i in range(790):
    diabete=y_all_pred[i][0]
    not_diabete=y_all_pred[i][1]
    if(diabete=='[]') and (not_diabete=='[]'):
        list_num.append(i)
        continue
print(list_num)
    # sum+=1
    # for k in re.split(r"[,\[\]]", diabete):
    #    if (k!=''):
    #     if (k!='nan') :
    #        Pred_size+=1
    # for k in re.split(r"[,\[\]]", not_diabete):
    #    if (k!=''):
    #     if (k!='nan'):
    #        Pred_size+=1
    # print(Pred_size)
    # # Pred_size=len(re.split(r"\s*,\s*", diabete))+len(re.split(r"\s*,\s*", not_diabete))
    # print(len(re.split(r"\s*,\s*", diabete))+len(re.split(r"\s*,\s*", not_diabete)))
    #
    # for j in y_all[i]:
    #     if (pd.notna(j)):
    #         Ref_size+=1
    #         if ((j in diabete)or(j in not_diabete)):
    #             Inter_tmp+=1
    #
    # if(Pred_size==0):
    #     Precision_tmp = 1.0
    # else:
    #     Precision_tmp = Inter_tmp / Pred_size
    # if(Ref_size==0):
    #     Recall_tmp = 1.0
    # else:
    #     Recall_tmp = Inter_tmp / Ref_size
    # if(Recall_tmp==Precision_tmp) and (Recall_tmp==0):
    #   F1_tmp= 0.0
    # else:
    #   F1_tmp=(2*Precision_tmp*Recall_tmp)/(Precision_tmp+Recall_tmp)
    # # print(Precision_tmp)
    # Precision+=Precision_tmp
    # Recall+=Recall_tmp
    # F1+=F1_tmp
#
# print("Precision:",Precision/sum)
# print("Recall:",Recall/sum)
# print("F1:",F1/sum)
# print(sum)
# Precision=0
# Recall=0
# F1=0
# for i in range(0,790):
#     Inter_tmp=0
#     Pred_size=0
#     Ref_size=0
#     for j in range(0,200):
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
#     print(Precision_tmp)
#     Precision+=Precision_tmp/790
#     Recall+=Recall_tmp/790
#     F1+=F1_tmp/790
# print("Precision:",Precision)
# print("Recall:",Recall)
# print("F1:",F1)