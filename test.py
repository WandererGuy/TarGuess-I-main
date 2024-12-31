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

# from utils.common import convert, chunk_list, convert_txt_to_json
# convert_txt_to_json('train_all_train_zing_dataset_preprocessed.txt')
train_input_path = r'C:\Users\Admin\CODE\work\PASSWORD_CRACK\TarGuess-I-main\static\train_dataset\train_all_train_zing_dataset_preprocessed.json'
import json
with open(train_input_path, 'r') as file:
    data = json.load(file)
print 