from fastapi import FastAPI, HTTPException
import os 
import uvicorn
import logging
from pydantic import BaseModel
import configparser
import subprocess
from dateutil import parser
import os 
from pydantic import BaseModel, validator, ValidationError
import re
import unidecode

from utils.server_utils import *


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='fastapi.log', filemode='w')
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
host_ip = config['DEFAULT']['host'] 
port_num = config['DEFAULT']['port'] 


app = FastAPI()

class InputData_wordlist(BaseModel):
    full_name: str
    birth: str  # This will now be validated for the format
    email: str
    account_name: str
    id_num: str
    phone: str
    maximum_guess_num: int
    minimum_prob : int 
    password_min_len : int
    password_max_len : int

    @validator('birth')
    def check_birth_format(cls, v):
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', v):
            raise ValueError('Birth date must be in DD-MM-YYYY format')
        return v
    
class InputData_masklist(BaseModel):
    full_name: str
    birth: str  # This will now be validated for the format
    email: str
    account_name: str
    id_num: str
    phone: str
    max_mask_generate: int

    @validator('birth')
    def check_birth_format(cls, v):
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', v):
            raise ValueError('Birth date must be in DD-MM-YYYY format')
        return v
# Endpoint to receive an image and start the processing pipeline
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/GenerateTargetWordlist/")
async def GenerateTargetWordlist(data: InputData_wordlist):
    try:
        name = data.full_name
        birth = data.birth
        email = data.email
        accountName = data.account_name
        id_num = data.id_num
        phone = data.phone
        
        updates = {
            'maximum_guess_num': data.maximum_guess_num,
            'minimum_prob': data.minimum_prob,
            'password_max_len': data.password_max_len,
            'password_min_len': data.password_min_len
        }
        # change config ini file 
        update_wordlist_config(updates)

        output = run_wordlist(name, birth, email, accountName, id_num, phone)
        file_path = output
        print(file_path) 
        return {"message": "File saved successfully", "file_path": os.path.abspath(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/GenerateTargetMaskList/")
async def GenerateTargetMaskList(data: InputData_masklist):
    try:
        name = data.full_name
        birth = data.birth
        email = data.email
        accountName = data.account_name
        id_num = data.id_num
        phone = data.phone

        updates = {
            'max_mask_generate': data.max_mask_generate
        }
        # change config ini file 
        update_masklist_config(updates)

        output = run_masklist(name, birth, email, accountName, id_num, phone)
        file_path = output
        print(file_path) 
        return {"message": "File saved successfully", "file_path": os.path.abspath(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    print ('INITIALIZING FASTAPI SERVER')
    uvicorn.run("server_api:app", host=host_ip, port=int(port_num), reload=True)

if __name__ == "__main__":
    main()