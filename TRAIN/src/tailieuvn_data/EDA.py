import pandas as pd 
from time import sleep
filepath = 'final.csv'

df = pd.read_csv(filepath)

print (df.columns)


def cal_str_value_column(lst):
    count = 0 
    for item in lst:
        if isinstance(item, str):
            count += 1 
    print (count/len(lst))


for column in df.columns:
    items = df[column]
    cal_str_value_column(items)
    print ('COLUMN NAME', column)
    print ('***********')
