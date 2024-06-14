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

def reorder_ls(ori_text, modified_text_ls): # my func return list but got messy order 
    correct_ls = []

def generate_possible_permu_text(elements):
    import itertools

    # Define the list


    # Generate all permutations of the same length as the original list
    all_permutations = list(itertools.permutations(elements, len(elements)))

    # Convert permutations from tuples to lists
    all_permutations_as_lists = [list(perm) for perm in all_permutations]

    # Print all permutations as lists
    for perm_list in all_permutations_as_lists:
        text = ''
        for item in perm_list:
            text += item




def break_name(text):
    clue_segment_ls = extract_meaningful_chunks_WORD_NAME_CHAR_NEW(text, word_list, name_list, english_list)
    reorder_ls(ori_text = text, clue_segment_ls)
    clue = flatten(clue_segment_ls)
    return clue 

def get_fullname(name):

    text = ''
    for i in range (len(name)):
        if name[i]in letter_list:
            text += name[i]
    print (text)

    data = text.strip().split(' ')
    full_name = []
    for item in data:
        clue = break_name(item)
        full_name.extend(clue)

    # 1 char component make no name -> delete the name , also , if not meaningful then remove
    full_name_text = ''
    for item in full_name:
        flag = check_meaningful(item)
        if len(item) == 1 or flag == False:
            full_name_text = None 
            return None

        full_name_text += item +' '
    return full_name_text.strip()


ex = 'Minhbeo@ Phamminhbeothayminhtue43'
ex = ex.lower()
full_name_text = get_fullname(ex)
print (full_name_text)


