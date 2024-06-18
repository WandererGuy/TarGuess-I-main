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


'''
(d:\_work_\2024\MANH\current-project\PASS-GUESS-project\targuess\TarGuess-I-main\targuess_env) D:\_work_\2024\MANH\current-project\PASS-GUESS-project\targuess\TarGuess-I-main\TRAIN\src\tailieuvn_data>python EDA.py
Index(['Email', 'Password', 'Name', 'GID', 'Account', 'Phone', 'Birth'], dtype='object')
1.0
COLUMN NAME Email
***********
1.0
COLUMN NAME Password
***********
0.9987989409640033
COLUMN NAME Name
***********
0.0
COLUMN NAME GID
***********
1.0
COLUMN NAME Account
***********
0.21908368839093156
COLUMN NAME Phone
***********
0.30215839952308315
COLUMN NAME Birth
***********

'''