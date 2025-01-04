# # train_res = {
# # '1.csv': {'status_code': 200, 'message': 'dataset ready for training', 'result': {'save_train_path': 'C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/train_dataset/a7eb19a3-6b7e-4e70-ad78-32cc9b820aff.txt', 'url': 'http://192.168.1.4:4003/static/train_dataset/a7eb19a3-6b7e-4e70-ad78-32cc9b820aff.txt'}},
# # '2.csv': {'status_code': 200, 'message': 'dataset ready for training', 'result': {'save_train_path': 'C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/train_dataset/5fd8b728-ada6-42c5-9731-14963e146d6a.txt', 'url': 'http://192.168.1.4:4003/static/train_dataset/5fd8b728-ada6-42c5-9731-14963e146d6a.txt'}},
# # '3.csv': {'status_code': 200, 'message': 'dataset ready for training', 'result': {'save_train_path': 'C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/train_dataset/5ac9b351-f466-44e8-8902-c58012d34c03.txt', 'url': 'http://192.168.1.4:4003/static/train_dataset/5ac9b351-f466-44e8-8902-c58012d34c03.txt'}},
# # '4.csv': {'status_code': 200, 'message': 'dataset ready for training', 'result': {'save_train_path': 'C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/train_dataset/51a36689-476a-4a1f-9591-981edf1c01e3.txt', 'url': 'http://192.168.1.4:4003/static/train_dataset/51a36689-476a-4a1f-9591-981edf1c01e3.txt'}},
# # '5.csv': {'status_code': 200, 'message': 'dataset ready for training', 'result': {'save_train_path': 'C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/train_dataset/7b56cd99-5fb2-49f0-8d24-972c895abe0e.txt', 'url': 'http://192.168.1.4:4003/static/train_dataset/7b56cd99-5fb2-49f0-8d24-972c895abe0e.txt'}},
# # '6.csv': {'status_code': 200, 'message': 'dataset ready for training', 'result': {'save_train_path': 'C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/train_dataset/d80b8913-1fc7-4310-81c1-318cdf23b8cf.txt', 'url': 'http://192.168.1.4:4003/static/train_dataset/d80b8913-1fc7-4310-81c1-318cdf23b8cf.txt'}},
# # '7.csv': {'status_code': 200, 'message': 'dataset ready for training', 'result': {'save_train_path': 'C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/train_dataset/861fbcdd-8f47-44b5-b56b-ad17484478df.txt', 'url': 'http://192.168.1.4:4003/static/train_dataset/861fbcdd-8f47-44b5-b56b-ad17484478df.txt'}},
# # '8.csv': {'status_code': 200, 'message': 'dataset ready for training', 'result': {'save_train_path': 'C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/train_dataset/5d2a0760-d3d2-4624-8359-7db43433c95c.txt', 'url': 'http://192.168.1.4:4003/static/train_dataset/5d2a0760-d3d2-4624-8359-7db43433c95c.txt'}},
# # '9.csv': {'status_code': 200, 'message': 'dataset ready for training', 'result': {'save_train_path': 'C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/train_dataset/c531b379-c5cd-4a8b-8101-614f62acc900.txt', 'url': 'http://192.168.1.4:4003/static/train_dataset/c531b379-c5cd-4a8b-8101-614f62acc900.txt'}}
# # }

# # sum_ls = []
# # for key, value in train_res.items():
# #     item = value["result"]["save_train_path"]
# #     with open (item, 'r', encoding = 'utf-8', errors='ignore') as f:
# #         sum_ls.append(f.read())
# #         sum_ls.append('\n') 

# # with open ('all_train_zing_dataset.txt', 'w', encoding = 'utf-8', errors='ignore') as f:
# #     f.writelines(sum_ls)


# pcfg trawling 

# pcfg 
from tqdm import tqdm
import json
from fill_mask import single_mask_analysis
from itertools import product
import time 

MAX_VOCAB = 10
def create_wordlist_single_mask(single_mask, mask_fill_dictionary):
    # single_mask = '?d?dbombay?d'
    res = single_mask_analysis(single_mask, mask_fill_dictionary)
    new_res = []
    
    for item in res:
        
        if len(item) > MAX_VOCAB:
            item = item[:MAX_VOCAB]
 
        new_res.append(item)
    # Generate the Cartesian product
    combinations = list(product(*new_res))
    pcfg_ls = {}
    # Calculate and display probabilities
    for combo in combinations:
        password = ''
        prob = 1
        for component in combo:
            password += component[0]
            prob *= float(component[1])
        if password not in pcfg_ls:
            pcfg_ls[password] = prob
        pcfg_ls[password] += prob
    return pcfg_ls


def add_to_dict(key, value, all_pcfg_wordlist):
    if key in all_pcfg_wordlist:
        all_pcfg_wordlist[key] += value
    else:
        all_pcfg_wordlist[key] = value

    return all_pcfg_wordlist


'''
'''

json_file = open(r'C:\Users\Admin\CODE\work\PASSWORD_CRACK\TarGuess-I-main\static\generated_target_fill_mask\ddac6335-4872-4e3d-beb4-740bf33f082c_additional.json')
mask_fill_dictionary = json.load(json_file)


pcfg_ls = {}
target_mask_file_path = r'C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/generated_target_masklist/6828971a-036c-4841-afaf-d64986282a13_sorted.hcmask'
all_pcfg_wordlist = {}


with open(target_mask_file_path, 'r') as f:
    lines = f.readlines()
    for line in tqdm(lines, total = len(lines)):
        single_mask = line.strip('\n').strip()
        single_mask_wordlist_dict = create_wordlist_single_mask(single_mask, mask_fill_dictionary)
        for key, value in single_mask_wordlist_dict.items():
            all_pcfg_wordlist = add_to_dict(key, value, all_pcfg_wordlist)

sorted_items_desc = sorted(all_pcfg_wordlist.items(), key=lambda item: item[1], reverse=True)

with open('pcfg_wordlist.txt', 'w') as f:
    for key, value in tqdm(sorted_items_desc, total = len(sorted_items_desc)):
        f.write(f'{key} {value}\n')


# class Mask():
#     def __init__(self, mask, fill_mask_dict):
#         self.mask = mask
#         self.fill_mask_dict = fill_mask_dict

#     def create