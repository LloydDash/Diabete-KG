import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

y_diabetes=pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/pred_diabetes_test_decode.xlsx',header=None)
y_not_diabetes=pd.read_excel(r'D:/Users/李乐意/PycharmProjects/shumo/zsgc_prac/pred_not_diabetes_test_decode.xlsx',header=None)
print(y_diabetes.shape)
print(y_not_diabetes.shape)

y_not_diabetes.loc[len(y_not_diabetes.index)] = ['','','','']
print(y_not_diabetes.shape)
# 列拼接
df=pd.concat([y_diabetes,y_not_diabetes],axis=1,join='inner',ignore_index=True)
# df.fillna(method = 'ffill', axis = 1) # 将通过前向填充 (ffill) 方法用同一行的前一个数作为填充
print(df)

pd.DataFrame(df).to_excel('pred_result.xlsx')
