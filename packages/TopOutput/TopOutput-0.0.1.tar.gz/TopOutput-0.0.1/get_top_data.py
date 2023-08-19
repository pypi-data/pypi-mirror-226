import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
def get_top_percent(path,x):
    df=pd.read_csv(path)
    column_headers = list(df.columns.values)
    df1=df.sort_values(by=column_headers[-1], ascending=False)
    a1=df1.shape[0]
    b1=round((x/100)*a1)
    df11=df1[:b1]
    s1=sum(df1.sum(axis=1))
    s11=sum(df11.sum(axis=1))
    percent_sales=(s11/s1)*100
    return round(percent_sales,2)
