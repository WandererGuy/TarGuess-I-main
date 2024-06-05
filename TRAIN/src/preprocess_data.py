import pandas as pd
from utils import *
import re

def string_process(input_string): #for string look like list 
    items = re.findall(r'\'(.*?)\'', input_string)
    result_string = ' '.join(items)
    return result_string

file_path = 'updated_2.csv'
df = pd.read_csv(file_path)

# find top password and top password format 
for index, item in df['PossibleNameClue'].items():
    new_item = string_process(item).strip()
    df.at[index,'PossibleNameClue'] = xoa_dau(new_item).strip() 
df = df.drop_duplicates(keep = 'first')
df = df.reset_index(drop=True)
df['GID'] = ''
new_df = df[['Email_prefix', 'PasswordPlain','PossibleNameClue','GID','NickName','Phone','BDay']]

# Assuming you want to rename all the columns to new names
### name dont matter 
new_df = new_df.rename(columns={
    'Email_prefix': 'Email',
    'PasswordPlain': 'Password',
    'PossibleNameClue': 'Name',
    'GID' : 'GID',
    'NickName': 'Account',
    'Phone': 'Phone',
    'BDay' : 'Birth'
})

new_df.to_csv('targuess_data.csv', index=False)
# # // After reading the data, store it in the inf array
# # pp.email = inf[0];
# # pp.psw = inf[1];
# # pp.name = inf[2];
# # pp.gid = inf[3];
# # pp.account = inf[4];
# # pp.phone = inf[5];
# # pp.birth = inf[6];




import csv

input_filename = 'targuess_data.csv'
output_filename = 'targuess_data.txt'

# Reading from CSV and writing to a tab-delimited text file
with open(input_filename, newline='', encoding='utf-8') as infile, open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile, delimiter='\t')
    
    for index, row in enumerate(reader):
        if index == 0:  # Skipping the header row
            continue
        writer.writerow(row)  # Writing the row to the tab-delimited file

