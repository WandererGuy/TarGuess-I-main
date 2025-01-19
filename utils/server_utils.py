from fastapi import FastAPI, HTTPException
import os 
import uvicorn
import logging
from pydantic import BaseModel
import configparser
import subprocess
from dateutil import parser
import os 
import re
import unidecode
import uuid
import logging 
from routers.model import MyHTTPException

def generate_unique_filename(UPLOAD_FOLDER, extension="txt"):
    if extension != None:
        filename = f"{uuid.uuid4()}.{extension}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return filename
    else:
        filename = f"{uuid.uuid4()}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return filename 
        
def process_birthday(birthday):
    try:
        # Attempt to parse the birthday in various formats
        parsed_date = parser.parse(birthday)
        # Convert to a standard format e.g., YYYY-MM-DD
        formatted_date = parsed_date.strftime("%Y%m%d")
        return formatted_date
    except ValueError:
        raise HTTPException(status_code=400, detail= "Invalid date. Please enter a valid date (e.g., DD-MM-YYYY).")

def run_masklist(max_mask_generate: str, 
                 train_result_refined_path: str, 
                 name: str, 
                 birth:str, 
                 email:str, 
                 accountName:str, 
                 id:str, 
                 phone:str
                 ) -> tuple[str, str] :
    '''
    generate mask list for a target person
    also, that mask list with probability for later pcfg wordlist creation
    '''
    fullName = ''
    password = ''
    # Splits the name into a list and rearranges to last name first
    if name != '':
        name = name.strip().lower()
        name = unidecode.unidecode(name)
        my_list = name.split(' ')
        my_list = [my_list[-1]] + my_list[:-1]
        for index, item in enumerate(my_list):
            if index == len(my_list) - 1:
                fullName += item
                break
            fullName += item
            fullName += ' '
    if birth != '':
        birth = process_birthday(birth)
    
    p = os.path.join('GUESS','src', 'result_folder', str(uuid.uuid4()) +'.txt')
    print (f'write target info to {p} for later command')
    print ('write order: email + password + fullName + id + accountName + phone + birth')

    with open (p, "w") as f:
        f.write(email + '\\t' + password + '\\t' + fullName + '\\t' + id + '\\t' + accountName + '\\t' + phone + '\\t' + birth)

    file_mask = generate_unique_filename(os.path.join('static','generated_target_masklist'), extension='hcmask')
    file_mask_path = os.path.join('static','generated_target_masklist', file_mask)
    mask_prob_path = os.path.join('static','generated_target_masklist', file_mask.replace('.hcmask', '_prob.json'))

    python_file = os.path.join('GUESS_MASK','automate_cracking.py') 
    cmd = ['python', 
            python_file, 
            '--mask_file_path', 
            file_mask_path, 
            '--target_info_file',
            p,
            '--max_mask_generate',
            max_mask_generate, 
            '--train_result_refined_path',
            train_result_refined_path, 
            '--mask_prob_path',
            mask_prob_path
            ]
    print ('command running python file to generate guesses')
    cm = ' '.join(cmd)
    print (cm)
    print ('creating mask list using: ')
    print ('Input: train_result_refined_path :')
    print(train_result_refined_path)
    print ('Output:')
    print(file_mask_path)

    process = subprocess.Popen(cmd, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    print("Output:", stdout)
    if stderr != '' and stderr != None:
        print("Errors:", stderr)
    
    return file_mask_path, mask_prob_path

# Function to handle the file download
input_file_wordlist = os.path.join('GUESS','src','result_folder','output.txt')  # Replace with your actual input file path
output_file_wordlist_folder = os.path.join('static','generated_target_wordlist')  # Replace with your desired output file path

def format_text_file(input_file_wordlistpath, output_file_wordlistpath):
    # Read lines from the input file
    with open(input_file_wordlistpath, 'r') as file:
        lines = file.readlines()

    # Determine the maximum length of the password for formatting
    max_length = max(len(line.split('\t')[0]) for line in lines if line.strip())

    # Prepare to write formatted text to the output file
    with open(output_file_wordlistpath, 'w') as file:
        # Writing header and separator
        file.write(f"{'Password':<{max_length}} Probability\n")
        file.write('-' * (max_length + 12) + '\n')
        
        # Formatting each line and writing to the file
        for line in lines:
            if line.strip():
                password, probability = line.split('\t')
                file.write(f"{password:<{max_length}} {probability}\n")



def update_wordlist_config(updates):
    file_path = os.path.join('GUESS', 'src', 'config.ini')
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            key = line.split('=')[0]
            if key in updates:
                file.write(f"{key}={updates[key]}\n")
            else:
                file.write(line)


def update_masklist_config(updates):
    file_path = os.path.join('GUESS_MASK','config.ini')
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            key = line.split('=')[0].strip()
            if key in updates.keys():
                file.write(f"{key} = {updates[key]}\n")
            else:
                file.write(line)

