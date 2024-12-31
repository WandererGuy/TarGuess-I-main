from fastapi import FastAPI, HTTPException, Form, APIRouter
import os 
import configparser
import re
from utils.server_utils import * 
from utils.sort_complexity import * 
from pathlib import Path
import traceback
import json 
from fill_mask import main_fill_mask, create_fill_json
from routers.model import reply_bad_request, reply_server_error, reply_success, MyHTTPException
config = configparser.ConfigParser()
config.read('config/config.ini')
current_script_directory = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_script_directory)
host_ip = config['DEFAULT']['host'] 
port_num = config['DEFAULT']['port'] 
router = APIRouter()
static_folder = os.path.join(parent_dir, 'static')
train_result_folder = os.path.join(static_folder, 'train_result')
output_wordlist_folder = os.path.join(static_folder, 'generated_target_wordlist')
output_target_fill_mask_folder = os.path.join(static_folder, 'generated_target_fill_mask')
def fix_path(path):
    return path.replace('\\\\', '/').replace('\\', '/')

from keywords_handle import main as main_kw
from keywords_handle import kw_ls_check
import time 
def check_name_valid(name = ''):
    if name != '':
        name = name.lower()
        name = unidecode.unidecode(name)
        name = name.strip()
        my_list = name.split(' ')
        if len(my_list) < 3:
            message = "Full Name must have 3 or more compnents"
            raise MyHTTPException(status_code=400,
                                    message = message)

@router.post("/generate-target-wordlist/")
async def generate_target_wordlist(
    full_name: str = Form(None),
    birth: str = Form(None),
    email: str = Form(None),
    account_name: str = Form(None),
    id_num: str = Form(None),
    phone: str = Form(None),
    max_mask_generate: str = Form(...), # given personal info , get available mask valid from top to bottom of refined train result
    train_result_refined_path: str = Form(...),
    other_keywords: str = Form(None)
):
    min_pass_len = 4
    full_name = full_name or ""
    birth = birth or ""
    email = email or ""
    account_name = account_name or ""
    id_num = id_num or ""
    phone = phone or ""
    other_keywords = other_keywords or ""

    keyword_ls = other_keywords.split(',')
    new_kw_ls = []
    for kw in keyword_ls:
        new_kw_ls.append(kw.replace(' ', ''))
    res, false_kw = kw_ls_check(new_kw_ls)
    if not res:
        return reply_bad_request(f'keyword \'{false_kw}\' must be in same class: all letter, all digit or all special character')



    if not os.path.exists(train_result_refined_path):
        message = f"file_path {train_result_refined_path} does not exist"
        return reply_bad_request(message = message)



    print ('start making json fill dictionary')
    folder_parent = os.path.dirname(train_result_refined_path)
    fill_mask_path = os.path.join(train_result_folder, folder_parent, 'fill_mask.txt')
    n = str(uuid.uuid4())
    fill_mask_target_path = os.path.join(output_target_fill_mask_folder,f'{n}.txt')
    fill_mask_target_json_path = os.path.join(output_target_fill_mask_folder,f'{n}.json')
    main_kw(new_kw_ls, 
        fill_mask_path, 
        fill_mask_target_path)
    time.sleep(2)
    mask_fill_dictionary = create_fill_json(fill_mask_path, fill_mask_target_json_path)
    with open(fill_mask_target_json_path, "r") as json_file:
            mask_fill_dictionary = json.load(json_file)


    # if birth and not re.match(r'^\d{2}-\d{2}-\d{4}$', birth):
    #     raise MyHTTPException(status_code=400,
    #                           message = "Birth date must be in DD-MM-YYYY format")
    # check_name_valid(name = full_name)

    try:            
        output = run_masklist(max_mask_generate, 
                              train_result_refined_path, 
                              name = full_name, 
                              birth = birth, 
                              email = email, 
                              accountName = account_name, 
                              id = id_num , 
                              phone = phone)
            

        output = os.path.join(parent_dir, output).replace('\\', '/')
        sorted_mask_file_path = output.replace("." + output.split('.')[-1], "_sorted." +  output.split('.')[-1])
        deduplicate_file_lines(mask_file_path = output)
        sort_by_complexity(mask_file_path = output, 
                           sorted_mask_file_path = sorted_mask_file_path, 
                           min_pass_len = min_pass_len)
        print ('mask_file_path: ', output)
        print ('sorted_mask_file_path: ', sorted_mask_file_path)

        wordlist_name = str(uuid.uuid4()) + ".txt"
        target_wordlist_path  = os.path.join(output_wordlist_folder, wordlist_name)
        main_fill_mask(mask_fill_dictionary, sorted_mask_file_path, target_wordlist_path, only_wordlist = True)
        with open(target_wordlist_path, "r") as f:
            lines = f.readlines()
            print ('number of passwords in wordlist: ', len(lines))
        url = f"http://{host_ip}:{port_num}/static/generated_target_wordlist/" + wordlist_name
        return reply_success(message = "Result saved successfully", 
                             result = {"path":fix_path(target_wordlist_path), 
                                       "url":url})
    except Exception as e:
        return reply_server_error(message = str(e))
    
@router.post("/generate-target-mask-list/")
async def generate_target_mask_list(
    full_name: str = Form(None),
    birth: str = Form(None),
    email: str = Form(None),
    account_name: str = Form(None),
    id_num: str = Form(None),
    phone: str = Form(None),
    max_mask_generate: str = Form(...), # given personal info , get available mask valid from top to bottom of refined train result
                                        
    train_result_refined_path: str = Form(...)
):
    min_pass_len = 4
    full_name = full_name or ""
    birth = birth or ""
    email = email or ""
    account_name = account_name or ""
    id_num = id_num or ""
    phone = phone or ""
    

    # if birth and not re.match(r'^\d{2}-\d{2}-\d{4}$', birth):
    #     raise MyHTTPException(status_code=400, 
    #                           message="Birth date must be in DD-MM-YYYY format"
    #                           )
    # check_name_valid(name = full_name) c cc
    if not os.path.exists(train_result_refined_path):
        message = f"file_path {train_result_refined_path} does not exist"
        return reply_bad_request(message = message)

    try:
        output = run_masklist(max_mask_generate, 
                              train_result_refined_path,
                              name = full_name, 
                              birth = birth, 
                              email = email, 
                              accountName = account_name, 
                              id = id_num, 
                              phone =phone)
        output = os.path.join(parent_dir, output).replace('\\', '/')
        sorted_mask_file_path = output.replace("." + output.split('.')[-1], "_sorted." +  output.split('.')[-1])
        deduplicate_file_lines(mask_file_path = output)
        sort_by_complexity(mask_file_path = output, 
                           sorted_mask_file_path = sorted_mask_file_path,
                           min_pass_len = min_pass_len)
        print ('mask_file_path: ', output)
        print ('sorted_mask_file_path: ', sorted_mask_file_path)
        mask_file_name = os.path.basename(sorted_mask_file_path)
        url = f"http://{host_ip}:{port_num}/static/generated_target_masklist/" + mask_file_name
        return reply_success(message = "Result saved successfully", 
                             result = {
                                "path": fix_path(sorted_mask_file_path),
                                "url": url}
        )

    except Exception as e:
        return reply_server_error(message = str(e))
