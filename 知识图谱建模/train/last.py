import numpy as np
import pandas as pd
import warnings
import re
warnings.filterwarnings("ignore")


df_y_all=pd.read_excel(r'D:\Users\李乐意\PycharmProjects\shumo\zsgc_prac\test_result.xlsx',index_col=0)
df_y_all_pred=pd.read_csv(r'D:\Users\李乐意\PycharmProjects\shumo\zsgc_prac\test.csv')
print(df_y_all_pred.iloc[:,0])
df_y_pred_diabetes=df_y_all_pred['降糖药'].str.split(',', expand=True)
df_y_pred_not_diabetes=df_y_all_pred['非降糖药'].str.split(',', expand=True)
print(df_y_pred_diabetes)
print(df_y_pred_not_diabetes)
