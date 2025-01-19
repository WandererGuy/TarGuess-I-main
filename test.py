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

# import os
# path = r'C:\Users\Admin\CODE\work\PASSWORD_CRACK\TarGuess-I-main\process_name\output\zing_xac.txt'
# new_folder = os.path.join('process_name','output_new')
# os.makedirs(new_folder)
# filename = os.path.basename(path)
# new_path = os.path.join(new_folder, filename)

# ls = []
# with open(path, 'r') as f:
#     lines = f.readlines()
#     for index, line in enumerate(lines):
#         if '---->' in line:
#             if ' Nan' in line:
#                 ls.append(line.replace(' Nan', ''))
#             else: 
#                 ls.append(line)
#         else:
#             ls.append(line)
            
# with open (new_path, 'w') as f:
#     for line in ls:
#         f.write(line)

# path = r"C:\Users\Admin\CODE\work\PASSWORD_CRACK\PASSCRACK_MATERIAL\WORDLISTS\ZING_TAILIEUVN_LEAK\RAW_MATERIALS\28M\28M-Vietnam-zing.vn-Leading-News-Platform-UsersDB-csv-2015.csv"
# ls = []
# with open(path, 'r', encoding='utf-8', errors='ignore') as f:
#     lines = f.readlines()
#     for index, line in enumerate(lines):
#         if 16808989+2 >= index >= 14853650:
#             ls.append(line)
# with open('xai.csv', 'w', encoding='utf-8', errors='ignore') as f:
#     for item in ls:
#         f.write(item)  



def merge_json(json_ls, save_path):
    big_dict = {}
    import json 
    overwritten_keys = []
    for path in json_ls:
        with open (path, 'r') as f:
            t = json.load(f)
            for key, value in t.items():
                if key not in big_dict.keys():
                    big_dict[key] = value
                else: 
                    
                    overwritten_keys.append(key)
            # big_dict.update(t)
            # overwritten_keys = big_dict.keys() & t.keys()  # Find common keys
    print("Overwritten keys number:", len(overwritten_keys))  # Output: Overwritten keys: {'b'}

    with open (save_path, 'w') as f:
        json.dump(big_dict, f, indent=4)


import json 


import os 
import ast 
file_ls = []
ls = []
path = r'C:\Users\Admin\CODE\work\PASSWORD_CRACK\TarGuess-I-main\misc\process_raw_csv\auto_preprocess_API_result\replace_name\test.txt'

with open (path, 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        if line.startswith('pro'):
            file_ls.append(line)
        if line.startswith('{'):
            converted_dict = ast.literal_eval(line)
            ls.append(converted_dict['result']['save_train_path'])

res = list(zip(file_ls, ls))
for item in res:
    print (item)


save_path = os.path.join('merge_json_replace_name', 'zing.json')
t = {}
for item in res:
    t[item[0]] = item[1]

m = 0
json_ls = []
for key, value in t.items():
    if 'zing' in key:
        json_ls.append(value)
        with open (value, 'r') as f:
            k = len(json.load(f))
            print (k)
            m += k
print (m)


merge_json(json_ls = json_ls, 
            save_path = save_path)