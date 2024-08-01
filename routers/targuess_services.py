from fastapi import FastAPI, HTTPException, Form, APIRouter
import os 
import uvicorn
import logging
import configparser
import subprocess
import re
from fastapi.staticfiles import StaticFiles
from utils.server_utils import * 
config = configparser.ConfigParser()
config.read('config/config.ini')

host_ip = config['DEFAULT']['host'] 
port_num = config['DEFAULT']['port'] 
router = APIRouter()
@router.post("/GenerateTargetWordlist/")
async def GenerateTargetWordlist(
    full_name: str = Form(None),
    birth: str = Form(None),
    email: str = Form(None),
    account_name: str = Form(None),
    id_num: str = Form(None),
    phone: str = Form(None),
    maximum_guess_num: int = Form(...),
    minimum_prob: int = Form(...),
    password_min_len: int = Form(...),
    password_max_len: int = Form(...)
):
    try:
        full_name = full_name or ""
        birth = birth or ""
        email = email or ""
        account_name = account_name or ""
        id_num = id_num or ""
        phone = phone or ""

        if birth and not re.match(r'^\d{2}-\d{2}-\d{4}$', birth):
            raise HTTPException(status_code=400, detail='Birth date must be in DD-MM-YYYY format')
        
        updates = {
            'maximum_guess_num': maximum_guess_num,
            'minimum_prob': minimum_prob,
            'password_max_len': password_max_len,
            'password_min_len': password_min_len
        }
        # change config ini file 
        update_wordlist_config(updates)
        
        output = run_wordlist(full_name, birth, email, account_name, id_num, phone)
        file_path = os.path.basename(output)
        path = f"http://{host_ip}:{port_num}/static/generated_target_wordlist/" + file_path
        return {"message": "File saved successfully", "url":path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/GenerateTargetMaskList/")
async def GenerateTargetMaskList(
    full_name: str = Form(None),
    birth: str = Form(None),
    email: str = Form(None),
    account_name: str = Form(None),
    id_num: str = Form(None),
    phone: str = Form(None),
    max_mask_generate: int = Form(...)
):
    try:
        full_name = full_name or ""
        birth = birth or ""
        email = email or ""
        account_name = account_name or ""
        id_num = id_num or ""
        phone = phone or ""
        

        if birth and not re.match(r'^\d{2}-\d{2}-\d{4}$', birth):
            raise HTTPException(status_code=400, detail='Birth date must be in DD-MM-YYYY format')

        updates = {
            'max_mask_generate': max_mask_generate
        }
        # change config ini file 
        update_masklist_config(updates)

        output = run_masklist(full_name, birth, email, account_name, id_num, phone)
        file_path = os.path.basename(output)
        path = f"http://{host_ip}:{port_num}/static/generated_target_masklist/" + file_path
        return {"message": "File saved successfully", "url":path}    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))