from fastapi import FastAPI, HTTPException, Form, APIRouter
import os 
import uvicorn
import logging
import configparser
import subprocess
import re
from fastapi.staticfiles import StaticFiles
from utils.server_utils import * 
from utils.sort_complexity import * 
from utils.check_dataset import *
from pathlib import Path
from routers.model import reply_bad_request, reply_server_error, reply_success
import shutil
import yaml
import requests
import time 
from utils.common import convert_txt_to_json
from routers.process_name_server import fix_name_v2
config = configparser.ConfigParser()
config.read('config/config.ini')
current_script_directory = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_script_directory)
host_ip = config['DEFAULT']['host'] 
port_num = config['DEFAULT']['port'] 
router = APIRouter()
static_folder = os.path.join(parent_dir, 'static')
train_result_folder = os.path.join(static_folder, 'train_result')
train_dataset_folder = os.path.join(static_folder, 'train_dataset')

fix_name_url = f"http://{host_ip}:{port_num}/fix-name/"

def fix_path(path):
    return path.replace('\\\\', '/').replace('\\', '/')





def load_config(config_path='config/train.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


'''
name file path have same name as dataset file , so make sure dataset file name is unique each time , or else, it reuse old name file 
'''




''' 
this code to test if c++ code do extract as we wish 
according to our python code here 

'''
from GUESS_MASK.format_finder import create_format_dict
import json
from utils.train import deduplicate_dict, create_pattern, check_trawling_mask, collect_clue, \
find_fill, sort_dict_by_occurence
import sys
from tqdm import tqdm
import os
from utils.train_pipeline import training

    
def add_extra_mask(final_path):
        # add phone and gid 
        phone_flag = False
        gid_flag = False
        with open (final_path, 'r') as f:
            lines = f.readlines()
            if 'C\n' in lines: phone_flag = True
            if 'G\n' in lines: gid_flag = True 

        with open (final_path, 'a') as f:
            if lines[-1].strip('\n').strip() != '':
                f.write('\n')
            if phone_flag: f.write('C\n')
            if gid_flag: f.write('G')

        




@router.post("/preprocess-train-dataset/")
async def preprocess_train_dataset(
    dataset_path: str = Form(...),
    hash_dict_path: str = Form(None)
    ):
    conf = load_config()
    a = conf['update_csv_path']
    b = conf['pre_final_csv_path']
    c = conf['new_final_csv_path']
    train_input_file = conf['new_final_txt_path']
    # just remove to make sure new result do write 
    for item in [a, b, c, train_input_file]:
        if os.path.exists(item):
            os.remove(item)
            print ('delete', item)

    for item in [dataset_path, hash_dict_path]:
        if not os.path.exists(item):
            message = f"file_path {item} does not exist"
            return reply_bad_request(message = message)

    try:
        save_name = str(uuid.uuid4()) + '.txt'
        save_name_json = save_name.split('.')[0] + '.json'
        save_train_path = os.path.join(train_dataset_folder, save_name)
        save_train_json_path = os.path.join(train_dataset_folder, save_name_json)
        final_txt = load_config()['new_final_txt_path']
        # just remove to make sure new result do write 
        if os.path.exists(final_txt):
            os.remove(final_txt)
    except Exception as e:
        return reply_server_error(e)
    raw_dataset_path, password_type = check_valid_and_refine(dataset_path)
    try:
        python_file = os.path.join(parent_dir, 'TRAIN', 'src', 'tailieuvn_data', 'create_train_dataset.py')


#### create prefinal file -> use it it create process_name output -> create final file
        command = ['python', 
                python_file, 
                '--raw_dataset_path', 
                raw_dataset_path, 
                '--password_type',
                password_type, 
                '--hash_dict_path',
                hash_dict_path, 
                '--save_train_path',
                save_train_path, 
                '--fix_name',
                'False', 
                '--name_output_file',
                'random_name.txt'
                ]
        cm = ' '.join(command)
        print ('running command ')
        print (cm)
        process = subprocess.Popen(command, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True) 
        for line in process.stdout:
            print(line, end='')
        
        stdout, stderr = process.communicate()  
        if stderr:
            print("Errors:", stderr)
        time.sleep(3)


        new_name_file = os.path.basename(dataset_path).split('.')[0] + '.txt'
        name_output_file = os.path.join(parent_dir, 'process_name', 'output', new_name_file)
        print ('use pre final csv to generate name dict in ')
        print (name_output_file)
        print ('send to fix name script')
        response = fix_name_v2(fix_path(name_output_file))
        if 'success' in response.lower():
            print ('fix name success, name dictionary in ')
            print (name_output_file)
        else:
            raise MyHTTPException(status_code=500, message='process_name something error happening')


        command = ['python', 
                python_file, 
                '--raw_dataset_path', 
                raw_dataset_path, 
                '--password_type',
                password_type, 
                '--hash_dict_path',
                hash_dict_path, 
                '--save_train_path',
                save_train_path, 
                '--fix_name',
                'True', 
                '--name_output_file',
                name_output_file
                ]
        cm = ' '.join(command)
        print ('running command ', cm)
        process = subprocess.Popen(command, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True) 
        for line in process.stdout:
            print(line, end='')

        stdout, stderr = process.communicate()
        # print("Output:", stdout)
        if stderr:
            print("Errors:", stderr)
        print('final out put in :', final_txt)
        print("Output:", stdout)
         
        url = f"http://{host_ip}:{port_num}/static/train_dataset/" + save_name_json
        convert_txt_to_json(save_train_path, save_train_json_path)
        return reply_success(message = 'dataset ready for training', 
                             result = {
                            'save_train_path': fix_path(save_train_json_path), 
                            'url': url})
    except Exception as e:
        return reply_server_error(e)

@router.post("/train-targuess-cpp/")
async def train_targuess_cpp(
    save_train_path: str = Form(...)
    ):
    '''
    still have bug , not making OUTPUT_TRAIN after run exe, bug should be in cpp code 
    '''
    if not os.path.exists(save_train_path):
        message = f"file_path {save_train_path} does not exist"
        return reply_bad_request(message = message)
    if not save_train_path.endswith('.txt'):
        message = f"file_path {save_train_path} is not txt file"
        return reply_bad_request(message = message)
    try:    
        
        train_input_file = load_config()['new_final_txt_path']
        # just remove to make sure new result do write 
        if os.path.exists(train_input_file):
            os.remove(train_input_file)
        # put new train dataset into the place 
        shutil.copyfile(save_train_path, train_input_file)
        time.sleep(3)
        print ('------------------------- start training -------------------------')
        batch_file = "train_command.bat"
        result = subprocess.run([batch_file], capture_output=True, text=True)
        print("Output:", result.stdout)
        if result.stderr == None:
            print("Errors:", result.stderr)   
        print ('done running train_command.bat, result in GUESS/src/train_result/OUTPUT_TRAIN.txt')  
        print ('------------------------- refine template mask file for inference -------------------------')
        python_file = os.path.join('GUESS','src','b_create_new_rule.py')
        with subprocess.Popen(['python', 
                                    python_file
                                    ],
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True) as process:
            for line in process.stdout:
                print (line, end='')
            stdout, stderr = process.communicate()
            print("Output:", stdout)
            if stderr:
                print("Errors:", stderr)
        path = os.path.join('GUESS', 'src', 'train_result', 'train_result_refined.txt')
        name = str(uuid.uuid4()) + '.txt'
        save_path = os.path.join(train_result_folder, name)
        shutil.copyfile(path, save_path)
        time.sleep(3)
        convert_txt_to_json(save_path)
        url = f"http://{host_ip}:{port_num}/static/train_result/" + name

        return reply_success(message = 'Done training and refine mask file, ready for infer (guess) password.',
                             result = {
                                "train_result_refined_path": fix_path(save_path),
                                "url": url}
                                )
    except Exception as e:
        return reply_server_error(e)

@router.post("/train-targuess/")
async def train_targuess(
    save_train_path: str = Form(...)
    ):
    if not os.path.exists(save_train_path):
        message = f"file_path {save_train_path} does not exist"
        return reply_bad_request(message = message)
    if not save_train_path.endswith('.json'):
        message = f"file_path {save_train_path} is not json file"
        return reply_bad_request(message = message)
    train_input_path = save_train_path

    print (f'load train input file {train_input_path}...')
    if not os.path.exists(train_input_path):
        return reply_bad_request(message = f"Error: File {train_input_path} does not exist.")

    with open(train_input_path, 'r') as file:
        print ('load train input file...')
        data = json.load(file)
    try:    
        save_folder_name = str(uuid.uuid4()) 
        save_folder_path = os.path.join(train_result_folder, save_folder_name)
        os.makedirs(save_folder_path, exist_ok=True)

        target_train_output_path = os.path.join(save_folder_path, 'target_train_output.txt')     
        extra_target_train_output_path = os.path.join(save_folder_path, 'target_train_output_extra.txt') 
        # trawling_train_output_path = os.path.join(save_folder_path, 'trawling_train_output.txt')
        # extra_trawling_train_output_path = os.path.join(save_folder_path, 'trawling_train_output_extra.txt')
        final_path = os.path.join(save_folder_path,'train_result_refined.txt')

        print ('------------------------- start training -------------------------')
        print ('lets start training')
        res = training(data,
                        target_train_output_path, 
                        extra_target_train_output_path)        

        if res == "Done":
            print ('----- DONE TRAINING -----')
            print ('save train result in folder', save_folder_path)
            print ('result in ', target_train_output_path)
        print ('------------------------- refine template mask file for inference -------------------------')
        python_file = os.path.join('GUESS','src','b_create_new_rule_v2.py')
        command = ['python', 
                    python_file, 
                    '--save_folder_path',
                    save_folder_path, 
                    '--train_output_path',
                    target_train_output_path,
                    "--final_path",
                    final_path
                    ]
        cm = ' '.join(command)
        print ('running command ', cm)
        with subprocess.Popen(command,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            text=True) as process:
            for line in process.stdout:
                print (line, end='')
            stdout, stderr = process.communicate()
            print("Output:", stdout)
            if stderr:
                print("Errors:", stderr)

        url = f"http://{host_ip}:{port_num}/static/train_result/{save_folder_name}/" + 'train_result_refined.txt'
        add_extra_mask(final_path)

        return reply_success(message = 'Done training and refine mask file, ready for infer (guess) password.',
                             result = {
                                "train_result_refined_path": fix_path(final_path),
                                "url": url}
                                )
    except Exception as e:
        return reply_server_error(e)
