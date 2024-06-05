from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
import logging 
from tqdm import tqdm
from multiprocessing import Pool, Process
import os 

# Configure logging to write to a file
logging.basicConfig(level=logging.DEBUG,
                    filename='example.log',  # Name of the log file
                    filemode='a',  # Append mode, which allows you to add to the file without overwriting it
                    format='%(asctime)s - %(levelname)s - %(message)s')

service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
browser = webdriver.Chrome(service=service, options=options)

# 2. Mở thử một trang web
website = 'https://www.thantai1.net/so-ket-qua'
from datetime import datetime, timedelta
current_date = datetime (2024,4,26)
present_date = current_date
data=[]
# reset utl 
ind = 0 
# from today -> press 300 days -> extract all giaiDacBiet 
# -> (after 300 result da
# -> change date (-300) -> press 300 results again -> ...
simple_dict = {}

# /html/body/div[3]/main/div/div/div[2]/div[1]/table/tbody/tr[1]/td[2]/div/div
# /html/body/div[3]/main/div/div/div[4]/div[1]/table/tbody/tr[1]/td[2]/div/div
date_class = "d-inline-block"
# GiaiDacBiet = "font-weight-bold text-danger col-12 d-block p-1 m-0"
GiaiDacBiet = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[1]/td[2]/div/div'
# G1 = "font-weight-bold col-12 d-block p-1 m-0"
G1 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[2]/td[2]/div/div'
# G2_1
G2_1 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[3]/td[2]/div/div[1]'
# G2_2 = "font-weight-bold col-6 d-block p-1 m-0 border-left"
G2_2 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[3]/td[2]/div/div[2]'
# G3_1 = "font-weight-bold col-4 d-block p-1 m-0 border-bottom"
G3_1 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/div[1]'
# G3_2 = "font-weight-bold col-4 d-block p-1 m-0 border-left border-bottom"
G3_2 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/div[2]'
# G3_3 = "font-weight-bold col-4 d-block p-1 m-0 border-left border-bottom"
G3_3 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/div[3]'
# G3_4 = "font-weight-bold col-4 d-block p-1 m-0"
G3_4 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/div[4]'
# G3_5 = "font-weight-bold col-4 d-block p-1 m-0 border-left"
G3_5 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/div[5]'
# G3_6 = "font-weight-bold col-4 d-block p-1 m-0 border-left"
G3_6 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/div[6]'
# G4_1 = "font-weight-bold col-3 d-block p-1 m-0"
G4_1 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[5]/td[2]/div/div[1]'
# G4_2 = "font-weight-bold col-3 d-block p-1 m-0 border-left"
G4_2 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[5]/td[2]/div/div[2]'
# G4_3 = "font-weight-bold col-3 d-block p-1 m-0 border-left"
G4_3 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[5]/td[2]/div/div[3]'
# G4_4 = "font-weight-bold col-3 d-block p-1 m-0 border-left"
G4_4 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[5]/td[2]/div/div[4]'
# G5_1 = "font-weight-bold col-4 d-block p-1 m-0 border-bottom"
G5_1 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[6]/td[2]/div/div[1]'
# G5_2 = "font-weight-bold col-4 d-block p-1 m-0 border-left border-bottom"
G5_2 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[6]/td[2]/div/div[2]'
# G5_3 = "font-weight-bold col-4 d-block p-1 m-0 border-left border-bottom"
G5_3 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[6]/td[2]/div/div[3]'
# G5_4 = "font-weight-bold col-4 d-block p-1 m-0"
G5_4 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[6]/td[2]/div/div[4]'
# G5_5 = "font-weight-bold col-4 d-block p-1 m-0 border-left"
G5_5 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[6]/td[2]/div/div[5]'
# G5_6 = "font-weight-bold col-4 d-block p-1 m-0 border-left"
G5_6 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[6]/td[2]/div/div[6]'
# G6_1 = "font-weight-bold col-4 d-block p-1 m-0"
G6_1 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[7]/td[2]/div/div[1]'
# G6_2 = "font-weight-bold col-4 d-block p-1 m-0 border-left"
G6_2 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[7]/td[2]/div/div[2]'
# G6_3 = "font-weight-bold col-4 d-block p-1 m-0 border-left"
G6_3 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[7]/td[2]/div/div[3]'
G7_1 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[8]/td[2]/div/div[1]'
G7_2 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[8]/td[2]/div/div[2]'
G7_3 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[8]/td[2]/div/div[3]'
G7_4 = '/html/body/div[3]/main/div/div/div[1]/div[1]/table/tbody/tr[8]/td[2]/div/div[4]'


number_of_years = 1

variable_names = [GiaiDacBiet, G1, G2_1, G2_2, G3_1, G3_2, G3_3, G3_4, G3_5, G3_6, G4_1, G4_2, G4_3, G4_4, G5_1, G5_2, G5_3, G5_4, G5_5, G5_6, G6_1, G6_2, G6_3, G7_1, G7_2, G7_3, G7_4]
variable_names_string = ["GiaiDacBiet", "G1", "G2_1", "G2_2", "G3_1", "G3_2", "G3_3", "G3_4", "G3_5", "G3_6", "G4_1", "G4_2", "G4_3", "G4_4", "G5_1", "G5_2", "G5_3", "G5_4", "G5_5", "G5_6", "G6_1", "G6_2", "G6_3", "G7_1", "G7_2", "G7_3", "G7_4"]
mapping_dict = {}
for index, item in enumerate(variable_names_string):
    mapping_dict[str(index)] = item
new_variable_ls = []
for name in variable_names:
    new_variable_ls.append(name.replace(" ", "."))

for index, item_xpath in enumerate(new_variable_ls):
    simple_dict[str(index)] = []
simple_dict['date'] = []
flag = True 


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def check_inventory(items, required=300):
    global flag
    if items < required:
        # Log the message that there are not enough items
        logging.info(f'Not enough items: lost {required - items} items')
        print (f'Not enough items: lost {required - items} items')
        flag = False
    else: 
        print ('FULL 300 items')


def task (index, item_xpath, current_date):
        # File path
        file_path = 'my_dict.txt'



        # Reading the dictionary from the file and assigning it to a variable

data:image/jpeg;base64,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
        browser.get(website)

        # set date 
        end = browser.find_element(By.ID,"end")
        end.clear()
        end.send_keys("{}-{}-{}".format(current_date.day,current_date.month,current_date.year))

        # Xpath of button 300 days : 
        button_xpath = "/html/body/div[3]/main/div/form/div[2]/div/button[9]"
        btn = browser.find_element(By.XPATH,button_xpath)
        btn.click() # have a page of 300 elements

        item_text = []
        global mapping_dict
        
        for i in tqdm(range(1,361,1)):
            
            new_item_xpath = item_xpath.replace('/html/body/div[3]/main/div/div/div[1]', f'/html/body/div[3]/main/div/div/div[{i}]')

            item = browser.find_elements(By.XPATH,new_item_xpath)
            if (i-2)%6 != 0:
                try:
                    item_text.append(item[0].text) # get a cell value in a class , until get 300 then move on to next class 
                except:
                    item_text.append(['None'])
                    print (':<')
                    continue
        print ('******')
        print (f'done take {len(item_text)} items of {mapping_dict[str(index)]}')

        date_ls = browser.find_elements(By.CLASS_NAME,date_class)
        date_ls = [item.text for item in date_ls]
        check_inventory(len(item_text))

        with open(file_path, 'r') as file:
            simple_dict = json.load(file)  # Load JSON data from the file, not the file path

        simple_dict[str(index)].append(item_text)
        simple_dict['date'].append(date_ls)
        # Writing the dictionary to a 
        with open(file_path, 'w') as file:
            json.dump(simple_dict, file)  # Use json.dump to write JSON directly into a file



def split_task(original_list, number_split):

# Splitting the list into lists of four items each
    all_tasks = [original_list[i:i+number_split] for i in range(0, len(original_list), number_split)]

# Printing the result
    return all_tasks

import json

if __name__ == '__main__':
    print (simple_dict)
    # File path
    file_path = 'my_dict.txt'
    # with open(file_path, 'w') as file:
    #     file.write(json.dumps(simple_dict)) # use `json.loads` to do the reverse

    # js = json.loads(file_path) 

    # for line in js:
    #     key, value = line.strip().split(': ')
    #     simple_dict[key] = value
    #     print ((value))
    #     input("Press Enter to continue...")

    # Write the dictionary to a file as JSON
    with open(file_path, 'w') as file:
        json.dump(simple_dict, file)  # Use json.dump to write JSON directly into a file

    while True:
        print ("process 300 days from {}-{}-{}".format(current_date.day,current_date.month,current_date.year))
        # browser.get(website)

        # # set date 
        # end = browser.find_element(By.ID,"end")
        # end.clear()
        # end.send_keys("{}-{}-{}".format(current_date.day,current_date.month,current_date.year))

        # # Xpath of button 300 days : 
        # button_xpath = "/html/body/div[3]/main/div/form/div[2]/div/button[9]"
        # btn = browser.find_element(By.XPATH,button_xpath)
        # btn.click() # have a page of 300 elements
        
        index_ls = [i for i in range (len(new_variable_ls))]
        item_path_ls = new_variable_ls
        all_task = []
        for i in range (len(new_variable_ls)):
            element = (index_ls[i], item_path_ls[i], current_date)
            all_task.append(element)    
        with Pool(4) as p:
            print ('$$$$$$$$$$$$$$$$$$$$$$$$')
            print (all_task)
            p.starmap(task, all_task) 
        current_date -= timedelta(days = 300)


        if (present_date-current_date).days > number_of_years*365:
            break
        # browser.close()
    df = pd.DataFrame(simple_dict)

    # for key in simple_dict:
    #     print ('*********')
    #     print (len(simple_dict[key])) 
    # for key in mapping_dict:
    #     column_data = simple_dict[key]
    #     column_name = mapping_dict[key]
    df.to_csv("XSMB.csv", index=True )
    # browser.close()




# from selenium import webdriver
# from time import sleep
# from selenium.webdriver.common.keys import Keys

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service

# service = Service(executable_path='./chromedriver.exe')
# options = webdriver.ChromeOptions()
# browser = webdriver.Chrome(service=service, options=options)

# # 2. Mở thử một trang web
# browser.get("https://www.thantai1.net/so-ket-qua")

# end = browser.find_element("id", "end")
# end.clear()
# end.send_keys("26-04-2024")
# sleep(1000)



# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# import pandas as pd 
# from time import sleep
# from datetime import datetime, timedelta
# from selenium.webdriver.common.by import By


# service = Service(executable_path='./chromedriver.exe')
# options = webdriver.ChromeOptions()
# browser = webdriver.Chrome(service=service, options=options)

# # 2. Mở thử một trang web
# website = 'https://www.thantai1.net/so-ket-qua'
# from datetime import datetime, timedelta
# current_date = datetime (2021,5,4)
# data=[]
# # reset utl 
# ind = 0 
# # from today -> press 300 days -> extract all giaiDacBiet 
# # -> (after 300 result days) 
# # -> change date (-300) -> press 300 results again -> ...
# while True:
#     print ("process 300 days from {}-{}-{}".format(current_date.day,current_date.month,current_date.year))
#     browser.get(website)

#     # set date 
#     end = browser.find_element(By.ID,"end")
#     end.clear()
#     end.send_keys("{}-{}-{}".format(current_date.day,current_date.month,current_date.year))

#     # Xpath of button 300 days : 
#     button_xpath = "/html/body/div[3]/main/div/form/div[2]/div/button[9]"
#     btn = browser.find_element(By.XPATH,button_xpath)
#     btn.click()
#     # giai dac biet inspect , ' ' -> '.'
#     giaiDacBietPath = 'font-weight-bold text-danger col-12 d-block p-1 m-0'
#     giaiDacBietPath = giaiDacBietPath.replace(' ','.')
#     giaiDacBiet = browser.find_elements(By.CLASS_NAME,giaiDacBietPath)
#     for row in giaiDacBiet:
#         print (row.text)
#         ind +=1 
#         data.append(row.text)

#     current_date -= timedelta(days = 300)
#     if ind > 20*365:
#         break

# df = pd.DataFrame(data, columns=['KQ'])
# df.to_csv("XSMB.csv", index=True )
# browser.close()
