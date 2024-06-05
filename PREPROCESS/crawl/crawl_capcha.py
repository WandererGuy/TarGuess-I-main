# import os
# import time
# import logging
# import requests
# import traceback
# import multiprocessing
# from time import sleep
# from datetime import datetime, timedelta
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from tqdm import tqdm
# import cv2
# import urllib.request
# import numpy as np
# import io

# # Base URL of the server
# base_url = "http://10.0.68.103:8004"
# url = "http://10.0.68.103:8004/process-image"



# print ('STARTING PROCESS')
# response = requests.get(base_url)
# response_yolo = requests.get(base_url+'/load_model_yolo')
# response_ocr = requests.get(base_url+'/load_model_ocr')
# print (response.text)
# print (response_yolo.text)
# print (response_ocr.text)
# time.sleep(10)
# check_yolo = requests.get(base_url+'/ping_yolo')
# check_ocr = requests.get(base_url+'/ping_ocr')
# print (check_yolo.text)
# print (check_ocr.text)

# # Configure logging to write to a file
# logging.basicConfig(level=logging.DEBUG,
#                     filename='example.log',  # Name of the log file
#                     filemode='a',  # Append mode, which allows you to add to the file without overwriting it
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# service = Service(executable_path='./chromedriver.exe')
# options = webdriver.ChromeOptions()
# browser = webdriver.Chrome(service=service, options=options)

# # 2. Mở thử một trang web
# website = 'https://hashes.com/en/decrypt/hash'

# # Path to save the files
# database_path = './DATABASE'
# os.makedirs(database_path, exist_ok=True)

# # Define the cooldown function

# def upload_to_server(file_path):
#     """
#     Upload an image to the server and get the OCR result.
#     """
#     global url
#     with open(file_path, "rb") as file:
#         response = requests.post(url, files={'file': file})
#     ocr_output = response.json()['ocr_result']
#     return ocr_output

# def log_current_time():
#     """
#     Log the current time to the cooldown log file.
#     """
#     current_time = datetime.now()
#     with open('log_cooldown.txt', 'a') as file:
#         file.write(current_time.strftime('%Y-%m-%d %H:%M:%S') + '\n')

# def check_cooldown():
#     """
#     Check if the cooldown period has expired.
#     """
#     try:
#         with open('log_cooldown.txt', 'r') as file:
#             lines = file.readlines()
#             if not lines:
#                 return 0
#             last_time_str = lines[-1].strip()
#             last_time = datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
#             current_time = datetime.now()
#             cooldown_time = last_time + timedelta(seconds=10)
#             remaining_time = (cooldown_time - current_time).total_seconds()
#             if remaining_time > 0:
#                 return remaining_time
#             else:
#                 return 0
#     except FileNotFoundError:
#         return 0

# def get_next_filename(specific_folder_name):
#     """
#     Get the next filename for saving captcha images.
#     """
#     max_num = 0
#     for filename in os.listdir(specific_folder_name):
#         if filename.endswith('.jpg') and filename[:-4].isdigit():
#             num = int(filename[:-4])
#             if num > max_num:
#                 max_num = num
#     return f"{max_num + 1}.jpg"

# def create_next_folder(base_path):
#     """
#     Create the next folder for storing images.
#     """
#     index = 0
#     while True:
#         folder_name = os.path.join(base_path, str(index))
#         if not os.path.exists(folder_name):
#             os.makedirs(folder_name)
#             print(f"Created folder: {folder_name}")
#             break
#         index += 1
#     return folder_name

# def split_list(lst, n):
#     """
#     Split a list into n chunks.
#     """
#     chunk_size = len(lst) / n
#     chunks = []
#     start = 0
#     int_chunk_size = int(chunk_size)
#     for i in range(n):
#         if i == n-1:
#             chunks.append(lst[start:])
#             break
#         else:
#             end = start + int_chunk_size
#             chunks.append(lst[start:end])
#             start += int_chunk_size
#     return chunks

# def extract_last_time():
#     """
#     Extract the last time from the cooldown log.
#     """
#     with open('log_cooldown.txt', 'r') as file:
#         lines = file.readlines()
#         if not lines:
#             return 0
#         last_time_str = lines[-1].strip()
#         return last_time_str

# def fill_captcha(specific_folder_path):
#     """
#     Fill the captcha by extracting and processing the captcha image.
#     """
#     pic_path = '/html/body/div[2]/div[2]/div[2]/div[2]/form/div[2]/div[3]/img'
#     img = browser.find_element(By.XPATH, pic_path)
#     src = img.get_attribute('src')

#     req = urllib.request.urlopen(src)
#     arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
#     img = cv2.imdecode(arr, -1)

#     new_filename = get_next_filename(os.path.join(database_path, specific_folder_path))
#     new_filepath = os.path.join(database_path, specific_folder_path, new_filename)
#     cv2.imwrite(new_filepath, img)
#     sleep(1)
#     ocr_output = upload_to_server(new_filepath)

#     capcha_xpath = '/html/body/div[2]/div[2]/div[2]/div[2]/form/div[2]/div[4]/input[3]'
#     end_capcha = browser.find_element(By.XPATH, capcha_xpath)
#     end_capcha.clear()
#     end_capcha.send_keys(ocr_output)

# def task(index):
#     """
#     Task function to process each chunk of hashes.
#     """
#     f_crack = open("passwords_0_crack.txt", "a")
#     browser.get(website)
#     hash_list = chunks[index]
#     sleep(3)
#     hash_str = ''
#     count = 0
#     specific_folder_path = create_next_folder(database_path)
#     specific_folder_path = os.path.basename(specific_folder_path)
#     for item in tqdm(hash_list):
#         if count % 26 == 0 and count != 0:
#             sleep(3)
#             flag = True
#             while flag:
#                 try:
#                     fill_captcha(specific_folder_path)
#                 except Exception as e:
#                     print(f'Error: {e}')
#                     with io.StringIO() as buf:
#                         traceback.print_exc(file=buf)
#                         traceback_str = buf.getvalue()
#                     with open('error_log.txt', 'a') as f:
#                         f.write(f'Error: {e}\n')
#                         f.write(traceback_str)
#                     flag = False

#             end = browser.find_element(By.ID, "hashes")
#             end.clear()
#             end.send_keys(hash_str)
#             button_xpath = "/html/body/div[2]/div[2]/div[1]/div[2]/form/div[3]/button"
#             btn = browser.find_element(By.XPATH, button_xpath)
#             sleep(1)
#             btn.click()
#             no_valid_flag = True
#             invalid_class = '/html/body/div[2]/div[2]/div[1]'
#             while no_valid_flag:
#                 try:
#                     invalid_check = browser.find_element(By.XPATH, invalid_class)
#                     if '10' in invalid_check.text:
#                         last_time = extract_last_time()
#                         last_time = datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
#                         period = datetime.now() - last_time
#                         if period > timedelta(seconds=10):
#                             log_current_time()
#                             sleep(10)
#                     remaining_cooldown = check_cooldown()
#                     if remaining_cooldown > 0:
#                         time.sleep(remaining_cooldown)
#                     fill_captcha(specific_folder_path)
#                     btn.click()
#                 except Exception as e:
#                     print(f'Error: {e}')
#                     with io.StringIO() as buf:
#                         traceback.print_exc(file=buf)
#                         traceback_str = buf.getvalue()
#                     with open('error_log.txt', 'a') as f:
#                         f.write(f'Error: {e}\n')
#                         f.write(traceback_str)
#                     btn.click()
#                     no_valid_flag = False

#             password_crack = []
#             for index in range(1, 25):
#                 try:
#                     answer_class = f"/html/body/div[2]/div[2]/div/div[2]/pre/div[{index}]"
#                     answer = browser.find_element(By.XPATH, answer_class)
#                     password_crack.append(answer.text)
#                 except Exception as e:
#                     print(f'Error: {e}')
#                     with io.StringIO() as buf:
#                         traceback.print_exc(file=buf)
#                         traceback_str = buf.getvalue()
#                     with open('error_log.txt', 'a') as f:
#                         f.write(f'Error: {e}\n')
#                         f.write(traceback_str)
#                     break
#             button_xpath = "/html/body/div[2]/div[2]/div/a/button"
#             btn = browser.find_element(By.XPATH, button_xpath)
#             sleep(1)
#             btn.click()

#             for item in password_crack:
#                 f_crack.writelines(f'{item}\n')
#             f_crack.close()
#             f_crack = open("passwords_0_crack.txt", "a")
#             hash_str = ''
#             count = 0
#         if item == '':
#             pass
#         else:
#             hash_str += item + '\n'
#             count += 1

# if __name__ == '__main__':
#     # Configure logging
#     logging.basicConfig(level=logging.DEBUG,
#                         filename='example.log',
#                         filemode='a',
#                         format='%(asctime)s - %(levelname)s - %(message)s')

#     # Start Chrome driver
#     service = Service(executable_path='./chromedriver.exe')
#     options = webdriver.ChromeOptions()
#     browser = webdriver.Chrome(service=service, options=options)

#     # Open website
#     website = 'https://hashes.com/en/decrypt/hash'

#     # Path to save files
#     database_path = './DATABASE'
#     os.makedirs(database_path, exist_ok=True)

#     # Clear existing files
#     open('passwords_0_crack.txt', 'w').close()
#     open('error_log.txt', 'w').close()

#     # Read hashes from file and split into chunks
#     with open('REMAINING_PASS.txt', 'r') as f:
#         hashes = f.readlines()
#         chunks = split_list(hashes, 3)

#     # Log start time and start multiprocessing tasks
#     log_current_time()
#     index_ls = [0, 1, 2]
#     with multiprocessing.Pool(3) as p:
#         p.map(task, index_ls)

#     print("All workers have completed.")







from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
import logging 
# from tqdm import tqdm
from multiprocessing import Pool, Process
import os 
from time import sleep
import multiprocessing
import cv2
import urllib.request
import numpy as np
from tqdm import tqdm   
import time
import requests
import traceback
import io

base_url = "http://10.0.68.103:8004"
url = "http://10.0.68.103:8004/process-image"
def upload_to_server(file_path):
    # URL of the FastAPI server endpoint
    global url
    # Path to the image you want to upload

    # Open the image file in binary mode
    with open(file_path, "rb") as file:
        print (file)
        response = requests.post(url, files={'file': file})

    ocr_output = response.json()['ocr_result']     

    # Print the response from the server
    return ocr_output



print ('STARTING PROCESS')
response = requests.get(base_url)
response_yolo = requests.get(base_url+'/load_model_yolo')
response_ocr = requests.get(base_url+'/load_model_ocr')
print (response.text)
print (response_yolo.text)
print (response_ocr.text)
time.sleep(10)
check_yolo = requests.get(base_url+'/ping_yolo')
check_ocr = requests.get(base_url+'/ping_ocr')
print (check_yolo.text)
print (check_ocr.text)








# Configure logging to write to a file
logging.basicConfig(level=logging.DEBUG,
                    filename='example.log',  # Name of the log file
                    filemode='a',  # Append mode, which allows you to add to the file without overwriting it
                    format='%(asctime)s - %(levelname)s - %(message)s')

service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
browser = webdriver.Chrome(service=service, options=options)

# 2. Mở thử một trang web
website = 'https://hashes.com/en/decrypt/hash'

# Path to save the files
database_path = './DATABASE'
os.makedirs(database_path, exist_ok=True)

# Define the cooldown function

from datetime import datetime, timedelta



def log_current_time():
    print ('LLLLLLLOGGGGGGG')
    current_time = datetime.now()
    with open('log_cooldown.txt', 'a') as file:
        file.write(current_time.strftime('%Y-%m-%d %H:%M:%S') + '\n')


def check_cooldown():
    try:
        with open('log_cooldown.txt', 'r') as file:
            lines = file.readlines()
            if not lines:
                return 0  # File is empty, no cooldown needed
            last_time_str = lines[-1].strip()
            last_time = datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
            current_time = datetime.now()
            cooldown_time = last_time + timedelta(seconds=10)
            remaining_time = (cooldown_time - current_time).total_seconds()
            if remaining_time > 0:
                return remaining_time  # Return the remaining cooldown time
            else:
                return 0  # Cooldown period is over
    except FileNotFoundError:
        return 0  # File does not exist, no cooldown needed



def fill_captcha(specific_folder_path):
    # if 'captcha' in invalid_check.text:
        # fill_captcha(specific_folder_path)

        pic_path = '/html/body/div[2]/div[2]/div[2]/div[2]/form/div[2]/div[3]/img'
        print ('********************')
        print (os.path.join(database_path,specific_folder_path))
        img = browser.find_element(By.XPATH,pic_path)
        src = img.get_attribute('src')
        ### load capcha img 
        req = urllib.request.urlopen(src)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'

        # Generate the filename
        new_filename = get_next_filename(os.path.join(database_path,specific_folder_path))
        new_filepath = os.path.join(database_path,specific_folder_path, new_filename)
        print ('**************')
        print (new_filepath)
        print ('**************')
        cv2.imwrite(new_filepath, img)
        sleep(1)
        start = time.time()
        ocr_output = upload_to_server(new_filepath)
        print ('Process OCR takes:', time.time()-start)
        # sleep(1)
        # browser.refresh()

        capcha_xpath = '/html/body/div[2]/div[2]/div[2]/div[2]/form/div[2]/div[4]/input[3]'
        end_capcha = browser.find_element(By.XPATH,capcha_xpath)

        end_capcha.clear()
        end_capcha.send_keys(ocr_output) 



# Find the highest number used in the filenames within the folder
def get_next_filename(specific_folder_name):
    max_num = 0
    for filename in os.listdir(specific_folder_name):
        if filename.endswith('.jpg') and filename[:-4].isdigit():
            num = int(filename[:-4])
            if num > max_num:
                max_num = num
    return f"{max_num + 1}.jpg"


def create_next_folder(base_path):
    index = 0
    while True:
        folder_name = os.path.join(base_path, str(index))
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Created folder: {folder_name}")
            break
        index += 1
    return folder_name

def split_list(lst, n):
    chunk_size = len(lst) / n
    chunks = []
    start = 0
    int_chunk_size = int(chunk_size)
    for i in range (n):
        if i == n-1:
            chunks.append(lst[start:])
            break
        else:
            end = start + int_chunk_size
            chunks.append(lst[start:end])
            start = start + int_chunk_size
    return chunks

open('passwords_0_crack.txt', 'w').close()
open('error_log.txt', 'w').close()

with open('REMAINING_PASS.txt','r') as f:
    hashes = f.readlines()
    chunks = split_list(hashes, 3)

def extract_last_time():
    with open('log_cooldown.txt', 'r') as file:
        lines = file.readlines()
        if not lines:
            return 0  # File is empty, no cooldown needed
        last_time_str = lines[-1].strip()
        return last_time_str

def task (index):
        f_crack = open("passwords_0_crack.txt", "a")
        browser.get(website)
        hash_list = chunks[index]                                                                                         
        sleep(3)
        print ('*************************************************************')
        print (len(hash_list))
        print ('START ', index)
        hash_str = ''
        count = 0 
        specific_folder_path = create_next_folder(database_path)
        specific_folder_path = os.path.basename(specific_folder_path)
        for item in tqdm(hash_list):
            if count % 26 == 0 and count!= 0:
                sleep(3)
                flag = True
                while flag:
                    try:
                        fill_captcha(specific_folder_path)
                    except Exception as e:
                        # Print the error message
                        print(f'Error: {e}')
                        
                        # Capture the traceback
                        with io.StringIO() as buf:
                            traceback.print_exc(file=buf)
                            traceback_str = buf.getvalue()
                            
                        # Print the traceback to the console
                        print(traceback_str)
                        
                        # Save the error message and traceback to a file
                        with open('error_log.txt', 'a') as f:
                            f.write(f'Error: {e}\n')
                            f.write(traceback_str)
                                        
                            print ('NO CAP')
                            flag = False
                    # src = img.get_attribute('src')
                    # print ('image link : ',src)

                    # ### load capcha img 
                    # req = urllib.request.urlopen(src)
                    # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                    # img = cv2.imdecode(arr, -1) # 'Load it as it is'

                    # cv2.imshow('random_title', img)
                    # cv2.imsave("test.png", img)
                    # ### fill in capcha 

                    # capcha_xpath = '/html/body/div[2]/div[2]/div[2]/div[2]/form/div[2]/div[4]/input[3]'
                    # end_capcha = browser.find_element(By.XPATH,capcha_xpath)
                    # capcha_text = input()

                    # end_capcha.clear()
                    # end_capcha.send_keys(capcha_text)

                end = browser.find_element(By.ID,"hashes")
                end.clear()
                end.send_keys(hash_str)
                ### submit button 
                button_xpath = "/html/body/div[2]/div[2]/div[1]/div[2]/form/div[3]/button"
                btn = browser.find_element(By.XPATH,button_xpath)
                sleep(1)
                btn.click() 
                no_valid_flag = True
                # invalid_class=" my-center alert alert-dismissible alert-danger"
                invalid_class = '/html/body/div[2]/div[2]/div[1]'
                


                while no_valid_flag: # check for cooldown exist or not
                    try:
                        
                            
                        invalid_check = browser.find_element(By.XPATH,invalid_class)
                        print ('*******COOLDOWN*****')
                        print (invalid_check.text)
                        button_xpath = "/html/body/div[2]/div[2]/div[2]/div[2]/form/div[3]/button"
                        btn = browser.find_element(By.XPATH,button_xpath)
                        try : 
                                # sand clock between all process 
                                invalid_check = browser.find_element(By.XPATH,invalid_class)
                                print ('*******COOLDOWN*****')
                                print (invalid_check.text)
                                # found a string '10' see if can adđ to text file 
                                print ('******************** 111111')
                                if '10' in invalid_check.text:
                                   print (f'************ {extract_last_time()}')
                                   last_time = extract_last_time()
                                   print (f'******** {datetime.now()}') 
                                   last_time = datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')

                                   period = datetime.now() - last_time 
                                   print ('PERIODDDDDDD',period)
                                   if period > timedelta(seconds=10):
                                       log_current_time()
                                       sleep(10)
                                       print ('******************** 222222')
                                print ('******************** 3333333')

                                remaining_cooldown = check_cooldown()
                                if remaining_cooldown > 0:
                                    print(f"Cooldown period is not over. Waiting for {remaining_cooldown:.2f} seconds.")
                                    time.sleep(remaining_cooldown)
                                print ('COOLDOWN OVER')
                                print ('******************** 4444444444')
                                fill_captcha(specific_folder_path)
                                btn.click()
                        except Exception as e:
                            # Print the error message
                            print(f'Error: {e}')
                            
                            # Capture the traceback
                            with io.StringIO() as buf:
                                traceback.print_exc(file=buf)
                                traceback_str = buf.getvalue()
                                
                            # Print the traceback to the console
                            print(traceback_str)
                            
                            # Save the error message and traceback to a file
                            with open('error_log.txt', 'a') as f:
                                f.write(f'Error: {e}\n')
                                f.write(traceback_str)

                            btn.click()
                        print ('CLCIKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK')
                        # sleep(1)
                        continue
                    except Exception as e:
                        # Print the error message
                        print(f'Error: {e}')
                        
                        # Capture the traceback
                        with io.StringIO() as buf:
                            traceback.print_exc(file=buf)
                            traceback_str = buf.getvalue()
                            
                        # Print the traceback to the console
                        print(traceback_str)
                        
                        # Save the error message and traceback to a file
                        with open('error_log.txt', 'a') as f:
                            f.write(f'Error: {e}\n')
                            f.write(traceback_str)

                 

                        no_valid_flag = False
                password_crack = []

                for index in range (1,25):
                    try:
                        answer_class=f"/html/body/div[2]/div[2]/div/div[2]/pre/div[{index}]"
                        answer = browser.find_element(By.XPATH,answer_class)
                        password_crack.append(answer.text)
                    except Exception as e:
                        # Print the error message
                        print(f'Error: {e}')
                        
                        # Capture the traceback
                        with io.StringIO() as buf:
                            traceback.print_exc(file=buf)
                            traceback_str = buf.getvalue()
                            
                        # Print the traceback to the console
                        print(traceback_str)
                        
                        # Save the error message and traceback to a file
                        with open('error_log.txt', 'a') as f:
                            f.write(f'Error: {e}\n')
                            f.write(traceback_str)
                        break
                button_xpath = "/html/body/div[2]/div[2]/div/a/button"
                btn = browser.find_element(By.XPATH,button_xpath)
                sleep(1)
                btn.click() 

                for item in password_crack:
                    f_crack.writelines(f'{item}\n')
                f_crack.close()
                f_crack = open("passwords_0_crack.txt", "a")
                hash_str = ''
                count = 0 
            if item == '':
                pass
            else:
                hash_str += item + '\n'
                count += 1
        print ('Done hash list')

if __name__ == '__main__':

    print ('STARTING DIVIDE TASK')
    log_current_time()
    index_ls = [0,1,2]
    with Pool(3) as p:
        p.map(task, index_ls) # all cpu will together take care of this list 


    # Define the list of indices to be processed

    # Use a Pool to manage worker processes

    print("All workers have completed.")

            # 11 k samples 
            # return most fundemental iterable , even string can be breakdown to char
            # so best is to use pool for list that is so fundamental 
            # or a list that have index to progress into website  
                

