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

output_file_mask = 'generated_target_masklist/mask.hcmask'  # Replace with your desired output file path

def download_file_masklist(output_file_mask):
    # Provide the path to your file
    file_path = output_file_mask
    # print ('**********', input_file)
    print ('**********', output_file_mask)
    # format_text_file(input_file, output_file_mask)

    
    # Make sure the file exists to avoid errors
    if os.path.exists(file_path):
        return file_path
    else:
        return 'Fail generate'

def process_birthday(birthday):
    try:
        # Attempt to parse the birthday in various formats
        parsed_date = parser.parse(birthday)
        # Convert to a standard format e.g., YYYY-MM-DD
        formatted_date = parsed_date.strftime("%Y%m%d")
        return formatted_date
    except ValueError:
        return "Invalid date. Please enter a valid date (e.g., DD-MM-YYYY)."

def run_masklist(name='', birth='', email='', accountName='', id='', phone=''):
    # Initializes an empty string for the full name
    print ('Receiving inputs')

    fullName = ''
    password = ''
    # Splits the name into a list and rearranges to last name first
    if name != '':
        name = name.lower()
        name = unidecode.unidecode(name)

        my_list = name.split(' ')
        my_list = [my_list[-1]] + my_list[:-1]
        # Joins elements with '|' and avoids extra '|' at the end
        for index, item in enumerate(my_list):
            if index == len(my_list) - 1:
                fullName += item
                break
            fullName += item
            fullName += ' '
    print (birth)
    print (fullName)
    birth = process_birthday(birth)
    if birth == "Invalid date. Please enter a valid date (e.g., DD-MM-YYYY).":
        return birth
    print ('write input to files')
    with open ("GUESS/src/result_folder/test.txt", "w") as f:
        f.write(email + '\\t' + password + '\\t' + fullName + '\\t' + id + '\\t' + accountName + '\\t' + phone + '\\t' + birth)
    
    current_directory = os.getcwd()
# Print the current working directory
    print("Current Working Directory:", current_directory)

    python_file = "GUESS_MASK/automate_cracking.py"
# eragonkisyrong96@gmail.com	buiduymanh1996	manh		wantedbyzeus	01647732700	14-3-1995

    # Run the batch file
    print ('running batch file to generate guesses')
    result = subprocess.run(['python', python_file], capture_output=True, text=True)
    print("Output:", result.stdout)
    if result.stderr == None:
        print("Errors:", result.stderr)   
    output = download_file_masklist(output_file_mask)
    return output 



# Function to handle the file download
input_file_wordlist = 'GUESS/src/result_folder/output.txt'  # Replace with your actual input file path
output_file_wordlist = 'generated_target_wordlist/output.txt'  # Replace with your desired output file path

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


def download_file_wordlist(input_file_wordlist, output_file_wordlist):
    # Provide the path to your file
    file_path = output_file_wordlist
    print ('**********', input_file_wordlist)
    print ('**********', output_file_wordlist)
    format_text_file(input_file_wordlist, output_file_wordlist)

    
    # Make sure the file exists to avoid errors
    if os.path.exists(file_path):
        return file_path
    else:
        return 'Fail generate'




def run_wordlist(name='', birth='', email='', accountName='', id='', phone=''):
    # Initializes an empty string for the full name
    print ('Receiving inputs')

    fullName = ''
    password = ''
    # Splits the name into a list and rearranges to last name first
    if name != '':
        name = name.lower()
        name = unidecode.unidecode(name)

        my_list = name.split(' ')
        my_list = [my_list[-1]] + my_list[:-1]
        # Joins elements with '|' and avoids extra '|' at the end
        for index, item in enumerate(my_list):
            if index == len(my_list) - 1:
                fullName += item
                break
            fullName += item
            fullName += ' '
    print (birth)
    print (fullName)
    birth = process_birthday(birth)
    if birth == "Invalid date. Please enter a valid date (e.g., DD-MM-YYYY).":
        return birth
    print ('write input to files')
    with open ("GUESS/src/result_folder/test.txt", "w") as f:
        f.write(email + '\\t' + password + '\\t' + fullName + '\\t' + id + '\\t' + accountName + '\\t' + phone + '\\t' + birth)
    batch_file = "GUESS\src\command.bat"
# eragonkisyrong96@gmail.com	buiduymanh1996	manh		wantedbyzeus	01647732700	14-3-1995

    # Run the batch file
    print ('running batch file to generate guesses')
    result = subprocess.run([batch_file], capture_output=True, text=True)
    print("Output:", result.stdout)
    if result.stderr == None:
        print("Errors:", result.stderr)   
    # with open ("GUESS/src/result_folder/output.txt", "r") as f_output:
    # output = f_output.read()
    # print (output)
    output = download_file_wordlist(input_file_wordlist, output_file_wordlist)
    return output 


def update_wordlist_config(updates):
    file_path = 'GUESS\src\config.ini'
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
    file_path = 'GUESS_MASK\config.ini'
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            key = line.split('=')[0]
            if key in updates:
                file.write(f"{key}={updates[key]}\n")
            else:
                file.write(line)

