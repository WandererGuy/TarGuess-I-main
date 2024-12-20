from fastapi import FastAPI, HTTPException, Form, APIRouter
import os 
import configparser
import re
from utils.server_utils import * 
from utils.sort_complexity import * 
from pathlib import Path
import traceback
from fill_mask import main_fill_mask
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
def fix_path(path):
    return path.replace('\\\\', '/').replace('\\', '/')


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
    max_mask_generate: str = Form(...),
    train_result_refined_path: str = Form(...)
):
    full_name = full_name or ""
    birth = birth or ""
    email = email or ""
    account_name = account_name or ""
    id_num = id_num or ""
    phone = phone or ""
    

    # if birth and not re.match(r'^\d{2}-\d{2}-\d{4}$', birth):
    #     raise MyHTTPException(status_code=400,
    #                           message = "Birth date must be in DD-MM-YYYY format")
    # check_name_valid(name = full_name)
    train_result_refined_path = os.path.join(train_result_folder, train_result_refined_path)
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
                              id = id_num , 
                              phone = phone)
        output = os.path.join(parent_dir, output).replace('\\', '/')
        sorted_mask_file_path = output.replace("." + output.split('.')[-1], "_sorted." +  output.split('.')[-1])
        deduplicate_file_lines(mask_file_path = output)
        sort_by_complexity(mask_file_path = output, sorted_mask_file_path = sorted_mask_file_path)
        print ('mask_file_path: ', output)
        print ('sorted_mask_file_path: ', sorted_mask_file_path)

        wordlist_name = str(uuid.uuid4()) + ".txt"
        target_wordlist_path  = os.path.join(output_wordlist_folder, wordlist_name)
        main_fill_mask(sorted_mask_file_path, target_wordlist_path, only_wordlist = True)
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
    max_mask_generate: str = Form(...),
    train_result_refined_path: str = Form(...)
):
    
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
    # check_name_valid(name = full_name)
    train_result_refined_path = os.path.join(train_result_folder, train_result_refined_path)
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
        sort_by_complexity(mask_file_path = output, sorted_mask_file_path = sorted_mask_file_path)
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
