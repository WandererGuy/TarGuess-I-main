import pandas as pd
from process_name_utils import *

def extract_name():
    # Replace 'yourfile.csv' with the path to your CSV file
    file_path = 'TRAIN/src/tailieuvn_data/final.csv'
    df = pd.read_csv(file_path)

    # Print the column names
    print(df.columns.tolist())

    name_list = df['Name'].tolist()
    name_list = list(set(name_list))

    return name_list 
    # # Write the list to a text file
    # with open('train_names.txt', 'w') as file:
    #     for name in name_list:
    #         file.write(f"{name}\n")

letter_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
digit_list = '0123456789'
symbol_list = '!@#$%^&*()-_=+[]{};’:”,./<>?'


def break_name(text):
    clue_segment_ls = extract_meaningful_chunks_WORD_NAME_CHAR_NEW(text, word_list, name_list, english_list)
    clue = flatten(clue_segment_ls)
    return clue 

def get_fullname(name):

    text = ''
    for i in range (len(ex)):
        if ex[i]in letter_list:
            text += ex[i]
    print (text)

    data = text.strip().split(' ')
    full_name = []
    for item in data:
        clue = break_name(item)
        full_name.extend(clue)

    # 1 char component make no sense -> delete the name 
    full_name_text = ''
    for item in full_name:
        if len(item) == 1:
            full_name = None 
            break
        full_name_text += item +' '
    return full_name_text.strip()


ex = 'Minhbeo@ Phamminhbeo43'
ex = ex.lower()
full_name_text = get_fullname(ex)
print (full_name_text)


