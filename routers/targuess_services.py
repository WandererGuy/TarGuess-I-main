from fastapi import FastAPI, HTTPException, Form, APIRouter
import os 
import configparser
import re
from utils.server_utils import * 
from utils.sort_complexity import * 
from pathlib import Path
import traceback
from frontend_validation import target_input_validation, kw_ls_check, is_utf8, empty_to_none

import json 
from utils.create_pcfg_wordlist import make_pcfg_wordlist
from utils.fill_mask import main_fill_mask, create_fill_json
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

from utils.keywords_handle import main as main_kw
from utils.keywords_handle import kw_ls_check
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

port_validate_input_server = int(config['DEFAULT']['port_validate_input_server'])
TARGUESS_VALIDATE_INPUT_URL = f"http://{host_ip}:{port_validate_input_server}/validate-input-server/"
import requests
def targuess_validate_input_for_app(target_info: dict):
    if "other_keywords" not in target_info:
        target_info['other_keywords'] = ''
    print ('start validating input ...')
    if target_info['other_keywords'].strip() != '':
        keyword_ls = target_info['other_keywords'].split(',')
        new_kw_ls = []
        for kw in keyword_ls:
            new_kw_ls.append(kw.replace(' ', ''))
        res, false_kw = kw_ls_check(new_kw_ls)
        if not res:
            return reply_bad_request(f'keyword \'{false_kw}\' must be in same class: all letter, all digit or all special character')
    # standardize input 
    for key, value in target_info.items():
        target_info[key] = empty_to_none(value)
        if target_info[key] != None:
            is_utf8(target_info[key])
    target_input_validation(target_info)
'''
normal wordlist :
- sorted mask file by keyspqce (or complexity)
- fill mask dictionary into those mask (prob descend)
- keep filling for that mask until cannot fill above 100000 passwords per mask 
LIMIT_COMBINATION_NUM = 10**5 # total combination allow for each mask class  


pcfg wordlist: (testing to see if better) (actually care about prob specific number )
- any mask file is ok (here choose sorted mask file)
- fill mask dictionary into those mask (prob descend)
calculate prob of each password (p(alice123manh) = P(MASK)*p(alice)*p(123)*p(manh) 
if 'manh' is in the mask already then prob(manh)) = 1
- max vocab for each fill is 10 as set 
'''
@router.post("/generate-target-wordlist/")
async def generate_target_wordlist(
    full_name: str = Form(None),
    birth: str = Form(None),
    email: str = Form(None),
    account_name: str = Form(None),
    id_num: str = Form(None),
    phone: str = Form(None),
    max_mask_generate: str = Form(...), # given personal info , get available mask valid from top to bottom of refined train result
    train_result_refined_path: str = Form(...), # name of refined train result folder , not full path
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

    if other_keywords.strip() != '':

        keyword_ls = other_keywords.split(',')
        new_kw_ls = []
        for kw in keyword_ls:
            new_kw_ls.append(kw.replace(' ', ''))
        res, false_kw = kw_ls_check(new_kw_ls)
        if not res:
            return reply_bad_request(f'keyword \'{false_kw}\' must be in same class: all letter, all digit or all special character')

    else:
        new_kw_ls = []

    train_result_refined_path = os.path.join(train_result_folder, train_result_refined_path, 'train_result_refined.txt')
    if not os.path.exists(train_result_refined_path):
        message = f"file_path {train_result_refined_path} does not exist"
        return reply_bad_request(message = message)


    '''
    validating full scan again 
    '''
    target_info = {
        "full_name": full_name,
        "birth": birth,
        "email": email,
        "account_name": account_name,
        "id_num": id_num,
        "phone": phone,
        "other_keywords": other_keywords
    }
    targuess_validate_input_for_app(target_info)
    print ('validate input done')

    print ('start making json fill dictionary')
    folder_parent = os.path.dirname(train_result_refined_path)
    fill_mask_path = os.path.join(train_result_folder, folder_parent, 'fill_mask.txt')
    n = str(uuid.uuid4())
    fill_mask_target_path = os.path.join(output_target_fill_mask_folder,f'{n}.txt')
    fill_mask_target_json_path = os.path.join(output_target_fill_mask_folder,f'{n}.json')
    additional_json_path = os.path.join(output_target_fill_mask_folder,f'{n}_additional.json')
    main_kw(new_kw_ls, 
        fill_mask_path, 
        fill_mask_target_path)
    time.sleep(2)




    mask_fill_dictionary, additional_json_dict = create_fill_json(fill_mask_path, fill_mask_target_json_path, additional_json_path)
    
    # with open (fill_mask_target_json_path, 'w') as file:
    #     json.dump(mask_fill_dictionary, file, indent=4)
    # with open (additional_json_path, 'w') as file:
    #     json.dump(additional_json_dict, file, indent=4)

    try:            
        output, mask_prob_path = run_masklist(max_mask_generate, 
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
        pcfg_wordlist_name = wordlist_name.replace(".txt", "_pcfg.txt")
        target_wordlist_path  = os.path.join(output_wordlist_folder, wordlist_name)
        target_pcfg_wordlist_path = os.path.join(output_wordlist_folder, pcfg_wordlist_name)


        main_fill_mask(mask_fill_dictionary, sorted_mask_file_path, target_wordlist_path, only_wordlist = True)

        make_pcfg_wordlist(mask_fill_dictionary = additional_json_dict, 
                        mask_prob_path = mask_prob_path, 
                        destination_pcfg_wordlist_path = target_pcfg_wordlist_path)

        url = f"http://{host_ip}:{port_num}/static/generated_target_wordlist/" + wordlist_name
        url_pcfg = f"http://{host_ip}:{port_num}/static/generated_target_wordlist/" + pcfg_wordlist_name
        return reply_success(message = "Result saved successfully", 
                             result = {
                                        "path":fix_path(target_wordlist_path), 
                                       "pcfg_path":fix_path(target_pcfg_wordlist_path),
                                       "url":url,
                                        "url_pcfg":url_pcfg
                                        })
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
    max_mask_generate: str = Form(...),                          
    train_result_refined_path: str = Form(...) # name of refined train result folder , not full path
):
    '''
    generate mask list for a target person 
    Args:
        full_name: full name of target person
        birth: birth date of target person in form (DD-MM-YYYY)
        email: email of target person (must have @)
        account_name: account name or username of target person (on any website)
        id_num: id number of target person
        phone: phone number of target person
        max_mask_generate: maximum number of mask to generate (cannot exceed train_result_refined_path mask number) 
        (given the personal info of target person) (from high probability to low probability) ()the more info given , the more mask can be mapped from the train_result_refined_path)
        train_result_refined_path: path to refined train result output
    '''
    min_pass_len = 4

    full_name = full_name or ""
    birth = birth or ""
    email = email or ""
    account_name = account_name or ""
    id_num = id_num or ""
    phone = phone or ""

    train_result_refined_path = os.path.join(train_result_folder, train_result_refined_path, 'train_result_refined.txt')
    if not os.path.exists(train_result_refined_path):
        message = f"file_path {train_result_refined_path} does not exist"
        return reply_bad_request(message = message)
    
    target_info = {
        "full_name": full_name,
        "birth": birth,
        "email": email,
        "account_name": account_name,
        "id_num": id_num,
        "phone": phone,
    }
    targuess_validate_input_for_app(target_info)
    print ('validate input done')

    try:
        output, _ = run_masklist(max_mask_generate, 
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


    # if birth and not re.match(r'^\d{2}-\d{2}-\d{4}$', birth):
    #     raise MyHTTPException(status_code=400,
    #                           message = "Birth date must be in DD-MM-YYYY format")
    # check_name_valid(name = full_name)


