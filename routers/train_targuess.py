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
def fix_path(path):
    return path.replace('\\\\', '/').replace('\\', '/')

def load_config(config_path='config/train.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

@router.post("/preprocess-train-dataset/")
async def preprocess_train_dataset(
    dataset_path: str = Form(...),
    hash_dict_path: str = Form(None)
    ):
    for item in [dataset_path, hash_dict_path]:
        if not os.path.exists(item):
            message = f"file_path {item} does not exist"
            return reply_bad_request(message = message)

    try:
        save_name = str(uuid.uuid4()) + '.txt'
        save_train_path = os.path.join(train_dataset_folder, save_name)
        final_txt = load_config()['new_final_txt_path']
        # just remove to make sure new result do write 
        if os.path.exists(final_txt):
            os.remove(final_txt)
        # preprocess and validate dataset 
        raw_dataset_path, password_type = check_valid_and_refine(dataset_path)
        python_file = os.path.join(parent_dir, 'TRAIN', 'src', 'tailieuvn_data', 'create_train_dataset.py')
        process = subprocess.Popen(['python', 
                                    python_file, 
                                    '--raw_dataset_path', 
                                    raw_dataset_path, 
                                    '--password_type',
                                    password_type, 
                                    '--hash_dict_path',
                                    hash_dict_path, 
                                    '--save_train_path',
                                    save_train_path
                                    ], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)
        stdout, stderr = process.communicate()
        print("Output:", stdout)
        if stderr:
            print("Errors:", stderr)
        print('final out put in :', final_txt)
        print("Output:", stdout)
        url = f"http://{host_ip}:{port_num}/static/train_dataset/" + save_name

        return reply_success(message = 'dataset ready for training', 
                             result = {
                            'save_train_path': fix_path(save_train_path), 
                            'url': url})
    except Exception as e:
        return reply_server_error(e)

@router.post("/train-targuess/")
async def train_targuess(
    save_train_path: str = Form(...)
    ):
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
        shutil.copyfile(save_train_path, train_input_file)
        print ('------------------------- start training -------------------------')
        batch_file = "train_command.bat"
        result = subprocess.run([batch_file], capture_output=True, text=True)
        print("Output:", result.stdout)
        if result.stderr == None:
            print("Errors:", result.stderr)   
        print ('done running train_command.bat, result in GUESS/src/train_result/OUTPUT_TRAIN.txt')  
        print ('------------------------- refine template mask file for inference -------------------------')
        python_file = os.path.join('GUESS','src','b_create_new_rule.py')
        process = subprocess.Popen(['python', 
                                    python_file
                                    ],
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)
        stdout, stderr = process.communicate()
        print("Output:", stdout)
        if stderr:
            print("Errors:", stderr)
        print("Output:", stdout)
        path = os.path.join('GUESS', 'src', 'train_result', 'train_result_refined.txt')
        name = str(uuid.uuid4()) + '.txt'
        save_path = os.path.join(train_result_folder, name)
        shutil.copyfile(path, save_path)
        url = f"http://{host_ip}:{port_num}/static/train_result/" + name

        return reply_success(message = 'Done training and refine mask file, ready for infer (guess) password.',
                             result = {
                                "train_result_refined_path": fix_path(save_path),
                                "url": url}
                                )
    except Exception as e:
        return reply_server_error(e)
