from fastapi import FastAPI, HTTPException, Form, APIRouter
import os 
import subprocess
from pathlib import Path
from routers.model import reply_bad_request, reply_server_error, reply_success
import shutil
import time 
import configparser


import os 

router = APIRouter()

current_script_directory = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_script_directory)
config = configparser.ConfigParser()
config.read('config/config.ini')
use_existing_processed_name = config['DEFAULT']['use_existing_processed_name'] 

'''
Describe:
most people put their name like [name][rest] in correct order .
however, entangle word, invalid english name , gibberish name 
can happen, some mistake name with family name famous case like
'nguyen'.'pham'. this script fix all these


1. **remove symbol or digit**
2. **de-entangle & check meaningful name**
    - for word more than 6 char which not in vn dict or eng dict as a whole word
    - de-component into meaningful (based on dict) (prioritize highest part collect then keep decompose)
        
        (DECOMPOSE MUST CONSIDER continue decompoose or stop , stop when component is meangful already)
        
    - > if last part not in dict → remove , if only 1 char left → remove
        
        (less trash format and less trash self pcfg)
        
3. remove duplicate component in same name
4. capitalize first letter
5. rule-based fix name
    1. if famous like ‘Nguyen’ in first → put last word forward to first place
6. see if need more adapt to rule book
    
    know that second idenitfier removes burden for more complex rule
    
    so the only important is to find main name , the rest is whatever

'''



import os 
import pandas as pd
from process_name.process_name_utils import *

letter_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
digit_list = '0123456789'
symbol_list = '!@#$%^&*()-_=+[]{};’:”,./<>?'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)


from multiprocessing import Pool
from tqdm import tqdm

NAME_OUTPUT_NAME = os.path.join(parent_dir, 'process_name','output.txt')
NAME_ERROR_NAME = os.path.join(parent_dir, 'process_name','error.txt')




def extract_name(file_path):
    # Replace 'yourfile.csv' with the path to your raw CSV file
    df = pd.read_csv(file_path)
    # Print the column names
    print(df.columns.tolist())
    name_list = df['Name'].astype(str).tolist()
    
    name_list = sorted(list(set(name_list)), key=lambda x: x[0])

    return name_list 
    # Write the list to a text file
    # with open('train_names.txt', 'w') as file:
    #     for name in name_list:
    #         file.write(f"{name}\n")

import time 

def reorder_ls(ori_text, modified_text_ls): 
    # my func return list but got messy order 
    # so now reorder by loop through the list 
    # subtract the longest string left to right   
    # Sort the list by length in decreasing order
    flat_ls = flatten(modified_text_ls)
    correct_ls = []
    sorted_list = sorted(flat_ls, key=len, reverse=True)
    remaining_text = ori_text.replace(' ', '')
    flag_pos = 0 
    # time_limit = 0.01
    # start_time = time.time()

    # check if enough char from list sum up to create ori text
    # len_check = 0
    # for item in sorted_list:
    #     len_check += len(item)
    # if len_check != len(remaining_text):
    #     return None 
    iteration = 0 
    while remaining_text != '' and iteration <= len(sorted_list): # each iter cost up 1 item in list for sure and create new remaining  
        iteration += 1 
        # elapsed_time = time.time() - start_time
        # if elapsed_time > time_limit:
        #     error_file = open('error.txt', 'a')
        #     error_file.write('**************************************************\n')
        #     print(f"Loop exceeded time limit of {time_limit} seconds, escaping loop.")
        #     error_file.write(f"Loop exceeded time limit of {time_limit} seconds at iteration for chunk {ori_text}.\n")
        #     error_file.close()

        #     return None

        for item in sorted_list:
            start_pos = remaining_text.find(item)
            if start_pos == flag_pos :
                end_pos = start_pos + len(item) - 1 
                remaining_text = remaining_text[end_pos+1:]
                correct_ls.append(item)
        # if no found 
    return correct_ls 
    
def break_name(text):
    if len(text) == 1:
        return [text]
    clue_segment_ls = extract_meaningful_chunks_WORD_NAME_CHAR_NEW(text, word_list, name_list, english_list)
    correct_ls = reorder_ls(text, clue_segment_ls)
    if correct_ls == None:
        return None 
    clue = flatten(correct_ls)
    return clue 

def get_fullname(name):

    name = name.lower()

    # remove digit and symbols 
    text = ''
    for i in range (len(name)):
        if name[i]in letter_list:
            text += name[i]
    # break down name component to meaningful chunks and rest chunks (even 1 char)
    data = text.strip().split(' ')
    full_name = []
    for item in data:
        clue = break_name(item)
        if clue == None:
            return None
        else:

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

def remove_duplicate(ls):
    store_ls = []
    for item in ls:
        if item not in store_ls:
            store_ls.append(item)
    return store_ls 

def cap_first_letter(item):
    return item[0].upper() + item [1:]

def post_process(full_name_text):
    # thit 
    # ngot 
    data = full_name_text.split(' ')
    for index, item in enumerate(data):
        if item in ['thit', 'ngot', 'vot']:
            data[index+1] = 't' + data[index+1]
            data[index] = data[index][:-1]
    fullname = ''
    data = remove_duplicate(data)

    # nguyen in first -> last comes first 
    # Check if the first element is 'nguyen'
    if data[0] in ['nguyen', 'pham', 'tran']:
        # Remove the last element and insert it at the first position
        last_element = data.pop()  # Remove and get the last element
        data.insert(0, last_element)  # Insert it at the first position
        # case : dot hi -> do thi 
    for index, item in enumerate(data):
        if item == 'hi' and data[index-1][-1] == 't':
            data[index] = 'thi'
            data[index-1] = data[index-1][:-1]
    for item in data:
        item = cap_first_letter(item)
        fullname += item + ' '
    return fullname.strip()


def fix_name(name):
    full_name_text = get_fullname(name)
    if full_name_text != None:
        full_name = post_process(full_name_text)
    else: 
        full_name = None
    return full_name

# print (fix_name('781 Nhancaoquang'))



# Open the output file in write mode
# Loop through the names
def split_list(lst):
    # Calculate the size of each part
    n = len(lst)
    part_size = n // 3

    # Calculate the start and end indices for each part
    part1 = lst[:part_size]
    part2 = lst[part_size:2 * part_size]
    part3 = lst[2 * part_size:]

    return [part1, part2, part3]
def process_all_name(name_ls):
    print ('chunk len :',len(name_ls))
    tmp_ls = []
    error_tmp_ls = []
    with open(NAME_ERROR_NAME, 'a', encoding = 'utf-8', errors = 'ignore') as error_file:
        with open(NAME_OUTPUT_NAME, 'a', encoding = 'utf-8', errors = 'ignore') as file:
            for i in tqdm(range(len(name_ls)), total = len(name_ls)):
                name = name_ls[i]
                try:
                    new_name = fix_name(name)
                    tmp_ls.append(f"{name}\n ----> {new_name}\n")
                except Exception as e:
                    error_tmp_ls.append('**************************************************\n')
                    error_tmp_ls.append(f"{name} \n {e}\n")
                if i+1 % 10000 == 0 :
                    file.writelines(tmp_ls)
                    error_file.writelines(error_tmp_ls)
                    tmp_ls = []
                    error_tmp_ls = []
            file.writelines(tmp_ls)
            error_file.writelines(error_tmp_ls)


def chunk_list(lst, n):
    """
    Splits the list `lst` into `n` chunks.
    The first few chunks will have one more element if `lst` isn't divisible by `n`.
    """
    if n <= 0:
        raise ValueError("Number of chunks 'n' must be a positive integer.")
    length = len(lst)
    chunk_size = length // n
    excess = length % n
    chunks = []
    start = 0
    for i in range(n):
        # If there are excess elements, distribute one to this chunk
        end = start + chunk_size + (1 if i < excess else 0)
        chunks.append(lst[start:end])
        start = end
    return chunks


    # Extract names
    # file_path = r'C:\Users\Admin\CODE\work\PASSWORD_CRACK\TarGuess-I-main\PREPROCESS\4.csv'
def main():
    file_path = os.path.join(parent_dir,'TRAIN','src','tailieuvn_data','pre_final.csv')

    name_ls = extract_name(file_path)

    # Open the error file in append mode for logging errors
    error_file = open(NAME_ERROR_NAME, 'w')
    error_file.close()
    file = open(NAME_OUTPUT_NAME, 'w')
    file.close()
    print (len(name_ls))
    import multiprocessing
    cpu_count = multiprocessing.cpu_count()
    cpu_count = cpu_count - 1
    chunks = chunk_list(name_ls, cpu_count)
    with Pool(cpu_count) as p:
        p.map(process_all_name, chunks) # all cpu will together take care of this list 


def check_empty_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        if data.strip() == '':
            return True
        else:
            return False

def fix_name_v2(
    name_output_file
):
        print ('making process name in', name_output_file)
        new_name_file = os.path.basename(name_output_file)
        name_folder = os.path.join('process_name', 'output')

        empty_process_name_file = False
        if os.path.exists(name_output_file):
                empty_process_name_file = check_empty_file(name_output_file)
                if empty_process_name_file:
                    os.remove(name_output_file)

        if not os.path.exists(name_output_file) or empty_process_name_file or use_existing_processed_name.lower() == 'false':
            print ('PROCESSING NAME from scratch')
            main()
            time.sleep(3)
            shutil.copy(os.path.join('process_name', 'output.txt'), 
                        name_folder)
            os.rename(os.path.join(name_folder, 'output.txt'), 
                      os.path.join(name_folder, new_name_file))
            
            return ('Success.')
        else:
            print ('ALREADY HAVE NAME OUTPUT FILE GENERATED')
            return 'Success. ALREADY HAVE NAME OUTPUT FILE GENERATED'
