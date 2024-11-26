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
config = configparser.ConfigParser()
config.read('config/config.ini')
current_script_directory = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_script_directory)
host_ip = config['DEFAULT']['host'] 
port_num = config['DEFAULT']['port'] 
router = APIRouter()
@router.post("/preprocess-train-dataset/")
async def preprocess_train_dataset(
    dataset_path: str = Form(...),
    hash_dict_path: str = Form(None)
    ):
    try:
        final_txt = os.path.join('TRAIN','src','tailieuvn_data','final.txt')
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
                                    hash_dict_path
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
        return 'dataset ready for training'
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

@router.get("/train-targuess/")
async def train_targuess():
    try:    
        print ('------------------------- start training -------------------------')
        batch_file = "train_command.bat"
        result = subprocess.run([batch_file], capture_output=True, text=True)
        print("Output:", result.stdout)
        if result.stderr == None:
            print("Errors:", result.stderr)    
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
        return r'Done training and refine mask file, ready for infer (guess) password. Weight for infer in path: GUESS\src\train_result\train_result_refined.txt'
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
