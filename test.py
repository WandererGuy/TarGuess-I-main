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

import os 

class User:
    def __init__(self, password="", full_name="", birth="", email="", account_name="", id_num="", phone=""):
        self.password = password.lower()
        self.full_name = str(full_name)
        self.birth = birth
        self.email = email
        self.account_name = account_name
        self.id_num = id_num
        self.phone = phone
        self.split_name()  # Call the split_name method properly

    def split_name(self):
        self.full_name = self.full_name.strip()
        # Ensure full_name has at least two parts to split
        if ' ' in self.full_name:
            self.firstname = self.full_name.rsplit(' ', 1)[1]
            self.lastname = self.full_name.rsplit(' ', 1)[0]
        else:
            self.firstname = self.full_name  # If no space, assume full_name is just the first name
            self.lastname = ""
            # in code, fullname = firstname + ' '  + lastname 
        

zing = r"C:\Users\Admin\CODE\work\PASSWORD_CRACK\PASSCRACK_MATERIAL\WORDLISTS\ZING_TAILIEUVN_LEAK\28M_zing_split_cleaned"
tailieu = r"C:\Users\Admin\CODE\work\PASSWORD_CRACK\PASSCRACK_MATERIAL\WORDLISTS\ZING_TAILIEUVN_LEAK\7M_split_cleaned"
# for filename in os.listdir(zing):
#     file_path = os.path.join(zing, filename)
#     print (file_path)

# for filename in os.listdir(tailieu):
#     file_path = os.path.join(tailieu, filename)

# create person json for easier access, collect 
test_file = os.listdir(zing)[0]
test_file = os.path.join(zing, test_file)
import pandas as pd 
df = pd.read_csv(test_file)
new_df = df[['accountname', 'password', 'email', 'fullname', 'birthday', 'telephone']]

user_data = []
# Process each row and create a User object
for _, row in new_df.iterrows():
    account_name = row['accountname']
    password = row['password']
    email = row['email']
    full_name = row['fullname']
    birth = row['birthday']
    phone = row['telephone']

    # Create a User object
    user = User(
        password=password,
        full_name=full_name,
        birth=birth,
        email=email,
        account_name=account_name,
        phone=phone
    )

    # Add the User object to the list
    # Add the processed user data to the list
    user_data.append({
        'id': None,  # Add a placeholder or actual id if available
        'username': user.account_name,
        'password': user.password,
        'email': user.email,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'birthday': user.birth,
        'tel': user.phone
    })

necessary_cols = ['id', 'username', 'password', 'email', 'firstname', 'lastname', 'birthday', 'tel']

# Create a new DataFrame with the necessary columns
processed_df = pd.DataFrame(user_data, columns=necessary_cols)
count = 0 
for _, row in processed_df.iterrows():
    print (row)
    count += 1
    if count == 5:
        break


    


