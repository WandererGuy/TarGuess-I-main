'''example of train dataset 
,id,username,password,email,firstname,lastname,birthday,gender,address,tel                                       
0,,rinocococ,e10adc3949ba59abbe56e057f20f883e,vtailieu@gmail.com,Minh Trâm,Từ,19-1-1985,1.0,"56 vancao, phuong tan loi, tp.bmt , tinh daklak",0973276483
1,,lamfriends2000,c640856549e3cf8dfd35274ad9e62736,lamfriends2000@yahoo.com,Lam,Thai Xuan,,1.0,,
2,,hanguyen,a667f8ec02cb7d3f205a36658367169e,congha76@yahoo.com,Ha,Nguyen,,0.0,,
3,,ngocanhcdtk5,e2f5bbdb11e0089051185fe540227f85,ngocanhcdtk5@gmail.com,Anh,Nguyen Ngoc,,0.0,,
4,,manh_sanh_co_don,e2f5bbdb11e0089051185fe540227f85,ngocanha3@gmail.com,Anh,Nguyen Ngoc,,0.0,,
5,,manh_sanh_co_don_cdt,e2f5bbdb11e0089051185fe540227f85,ngocanh_hy87@yahoo.com,Anh,Nguyen Ngoc,,0.0,,
6,,nonameteam,d48b279000cc65c062cb1e1d4a979ba3,nnt@gmail.com,Noname,Team,,0.0,,
7,,myphuong,e71c617b3b17ecc166a6a5a8eccf0302,cdspthk1142@qtttc.edu.vn,Mỹ Phương,Nguyễn Thị,,0.0,,
8,,phuong_my,e71c617b3b17ecc166a6a5a8eccf0302,giotlesau_872000@yahoo.com,Mỹ Phương,Nguyễn Thị,,0.0,,
9,,dangquangtai,11c0e20f98e63cc8049a7c6168f1f483,haiauvocanh_goikevodanh2005@yahoo.com,Tai,Dang Quang,,0.0,,
10,,daiquangtang,11c0e20f98e63cc8049a7c6168f1f483,haiauvocanh_goikevodanh2005@gmail.com,Tang,Dai Quang,,0.0,,
11,,nhatchinh,de03ebd7140cd135176bbc0ddae1f30e,nhatchinhbc@hotmail.com,Chinh,Luong Nguyen Nhat,,0.0,,

Usage:
python TRAIN\src\tailieuvn_data\create_train_dataset.py


before that , 
have a raw csv file 
cd process_name 
python process_name.py -> to create a pprocess_name/output.txt
cd ..
python TRAIN\src\tailieuvn_data\create_train_dataset.py
'''

import traceback
import csv
import time 
import unidecode
import pandas as pd     
import yaml
import argparse
import shutil
import os 

hash_dict = {}
error_count = 0 

NAME_OUTPUT_FILE = None
def load_config(config_path=os.path.join('config','train.yaml')):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def create_hash_dict(hash_dict_path):
    global hash_dict
    with open (hash_dict_path, 'r', encoding='utf-8', errors='ignore') as f_dict:
        lines = f_dict.readlines()
        print ('element',len(lines))
        lines_unique = list(set(lines))
        print ('unique',len(lines_unique))
        for line in lines_unique:
            line = line.strip()
            if len(line.split(':')) == 2:
                hash_pass, plain = line.split(':')
                hash_dict[hash_pass] = plain
        print ('have hash and plain',len(hash_dict))

def remove_nan(fullname):
    if ' nan' in fullname:
        fullname = fullname.replace(' nan', '')
    return fullname


def turn_string(text):
    return str(text)
def update_raw_csv(config):
    csv_file = config['raw_csv_path']
    df = pd.read_csv(csv_file)
    df = df.astype(str)
    new_df = df[['username', 'password', 'email', 'firstname', 'lastname', 'birthday', 'gender', 'address', 'tel']]
    new_df['plain_password'] = ''
    new_df['fullname'] = new_df['firstname'] + ' ' + new_df['lastname']
    new_df['fullname'] = new_df['fullname'].apply(remove_nan)
    gender_map = {'1': 'Male', '0': 'Female'}
    new_df['gender'] = new_df['gender'].map(gender_map)

    # Split the email into two parts at the '@'
    new_df['email'] = new_df['email'].fillna('')  # Replace NaN with empty strings
    new_df = new_df[new_df['email'].str.contains('@', na=False)]  # Filter rows with valid emails
    # if line dont contain @ then first column is email , second is nan
    new_df[['email_prefix', 'email_domain']] = new_df['email'].str.split('@', expand=True, n = 1) 
    new_df['email_prefix'] = new_df['email'] # well guess still need full email
    update_df = new_df[['username', 'password', 'plain_password', 'email_prefix','email_domain',  'fullname', 'birthday', 'gender', 'address', 'tel']]
    update_df.to_csv(config['update_csv_path'], index=False)

def replace_password(hash_password):
    if hash_password in hash_dict:
        return hash_dict[hash_password]
    else:
        return None 
    
def fill_plain_pass(config, password_type):
    update_csv_file = config['update_csv_path']
    df = pd.read_csv(update_csv_file)
    df = df.map(turn_string)
    print("Length of the DataFrame ORIGINAL:", len(df))
    if password_type == 'hash':
        df['plain_password'] = df['password'].apply(replace_password)
    else:
        df['plain_password'] = df['password']
    # Remove rows where 'plain_password' is None
    df = df.dropna(subset=['plain_password'])
    print("Length of the DataFrame have plain crack:", len(df))
    return df

def fix_birthday(birthday):
    global error_count
        
    if birthday == 'nan' or birthday == '0':
        return None
    else: 
        if '-' in birthday:
            if len(birthday.split('-')) == 3:
                d, m, y = birthday.split('-')
                if len(d) < 2:
                    d = '0' + d
                if len(m) < 2:
                    m = '0' + m
            else:
                error_count += 1
                return None
            final_birthday = f'{y}{m}{d}'
            final_birthday = final_birthday.split('.')[0] # in case floating value 

            return final_birthday
        
        elif '/' in birthday:
            if len(birthday.split('/')) == 3:
                d, m, y = birthday.split('/')
                if len(d) < 2:
                    d = '0' + d
                if len(m) < 2:
                    m = '0' + m
            else:
                error_count += 1
                return None
            final_birthday = f'{y}{m}{d}'
            final_birthday = final_birthday.split('.')[0] # in case floating value 
            print (final_birthday)
            return final_birthday

def export_txt(input_filename, output_filename):
    # Reading from CSV and writing to a tab-delimited text file
    print ('------------------- export csv to txt -------------------')
    with open(input_filename, newline='', encoding='utf-8') as infile, open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, delimiter='\t')
        
        for index, row in enumerate(reader):
            if index == 0:  # Skipping the header row
                continue
            writer.writerow(row)  # Writing the row to the tab-delimited file

def decode_name(name):
    new_name = unidecode.unidecode(name)
    return new_name

def remove_question_marks(input_string):
    if input_string is None:
        return None

    else:
        return input_string.replace('?', '')

def finalize(config, df):
    '''
    'email_prefix',
    'plain_password', 
    'fullname', 
    GID
    'username', 
    'tel'
    'birthday', 

    desdired input visit doc 
    minimalist by delete unneed
    goal: train good , less fragment , more workflow , so i dont have to remember how to do many stuff 
    to create a good trainign set , i must follow process rule , so that it can learn actually
    birthday : 19940131
    email prefix
    username normal
    gid -> blank for now
    name is quite unstable , so i will make more rule for name instead of hoan vi name 
    after all this check output train to see if i need any more rule 
    '''
    new_df = df[['email_prefix', 'plain_password', 'fullname', 'username', 'tel', 'birthday']]
    new_df['GID'] = ''
    new_df['birthday'] = new_df['birthday'].apply(fix_birthday)
    new_df['fullname'] = new_df['fullname'].apply(decode_name)

    # Reorder and rename columns
    new_df = new_df[['email_prefix', 'plain_password', 'fullname', 'GID', 'username', 'tel', 'birthday']].rename(
        columns={
            'email_prefix': 'Email',
            'plain_password': 'Password',
            'fullname': 'Name',
            'GID': 'GID',
            'username': 'Account',
            'tel': 'Phone',
            'birthday': 'Birth',     
        }
    )
    new_df['Email'] = new_df['Email'].apply(remove_question_marks)
    new_df['Name'] = new_df['Name'].apply(remove_question_marks)
    new_df['Phone'] = new_df['Phone'].apply(remove_question_marks)
    new_df['Birth'] = new_df['Birth'].apply(remove_question_marks)
    new_df['Account'] = new_df['Account'].apply(remove_question_marks)
    new_df['GID'] = new_df['GID'].apply(remove_question_marks)
    new_df.to_csv(config['pre_final_csv_path'], index=False)

miss_name = []
def look_up(name, name_dict):
    global miss_name
    try:
        return name_dict[name].lower() 
    except Exception as e: # not in dict name 
        miss_name.append(e)
        return None

password_err = 0 
def lower_word(word):
    global password_err
    try:
        return word.lower()
    except:
        password_err += 1



pseudo_birthday = '19991218'
pseudo_year = '1999'
pseudo_month = '12'
pseudo_day = '18'
def handle_birth(birth): 
    birth = str(birth)
    if 'Year' in birth:
        birth = birth.replace('Year', pseudo_year)
    if 'Month' in birth:
        birth = birth.replace('Month', pseudo_month)
    if 'Day' in birth:
        birth = birth.replace('Day', pseudo_day)
    try:
        
        birth = birth.split('.', 1)[0] # sometimes it has float number 
        birth = int(birth)
    except:
        birth = int(pseudo_birthday)
    return birth

def post_process_csv(new_final_csv_path, file_path):
    '''read name txt 
    create dict for look up 
    read csv
    substitute name with fix name 
    if name == None -> delete row 
    write on new csv '''
    name_dict = {}
    with open (NAME_OUTPUT_FILE, 'r') as file :
        lines = file.readlines()
        for line in lines:
            
            line = line.strip('\n')
            if '---> ' in line:
                fix_name = line.split('---> ')[1]
                if ori_name not in name_dict:
                    name_dict[ori_name] = fix_name
                else:
                    print ('WTF it duplicate lmao')
            else:
                ori_name = line

    df = pd.read_csv(file_path)
    # df = df.dropna(subset=['Birth'])
    # Convert 'Birth' column to integer
    df['Birth'] = df['Birth'].apply(lambda x: handle_birth(x) if not pd.isna(x) else x)
    df['Birth'] = df['Birth'].fillna(pseudo_birthday).astype(int)
    df['Name'] = df['Name'].apply(lambda x: look_up(x, name_dict))
    # lower password for simpler 
    df['Password'] = df['Password'].apply(lower_word)
    # for name == None or '' -> bad for learning folr model -> remove 
    remove_row = []
    for index, item in df['Name'].items():
        if item == None or item == '' or item == 'nan' or item == 'None':
            remove_row.append(index)
    df = df.drop(remove_row)
    print ('******* done remove *******')
        # df.at[index,'PossibleNameClue'] = xoa_dau(new_item).strip() 
    df.to_csv(new_final_csv_path, index=False)


def main():
    global NAME_OUTPUT_FILE
    parser = argparse.ArgumentParser(description="parse input data")
    parser.add_argument('--raw_dataset_path', type=str)
    parser.add_argument('--password_type', type=str)
    parser.add_argument('--hash_dict_path', type=str)
    parser.add_argument('--save_train_path', type=str)
    parser.add_argument('--fix_name', type=str)
    parser.add_argument('--name_output_file', type=str)
    
    args = parser.parse_args()
    config = load_config()
    config['raw_csv_path'] =  args.raw_dataset_path
    config['hash_dict_path'] = args.hash_dict_path
    flag = args.fix_name
    
    if flag == 'False':
            print ('******* FIRST RUN create_train_dataset.py *******')
            update_raw_csv(config)  
            time.sleep(5)
            create_hash_dict(config['hash_dict_path'])
            df = fill_plain_pass(config, args.password_type)
            finalize(config, df)
    else:
            print ('******* SECOND RUN create_train_dataset.py *******')
            save_train_path = args.save_train_path
            NAME_OUTPUT_FILE = args.name_output_file
            post_process_csv(config['new_final_csv_path'], config['pre_final_csv_path'])
            print ('******* done write final csv to final.txt *******')
            export_txt(config['new_final_csv_path'], config['new_final_txt_path'])
            shutil.copyfile(config['new_final_txt_path'], save_train_path)
            before_len =  len(pd.read_csv(config['raw_csv_path']))
            after_len = len(pd.read_csv(config['new_final_csv_path']))
            error_count = before_len - after_len
            print ('invalid email, invalid name, invalid password')
            print ('TOTAL have REMOVE ROWS', error_count)
            print ('number of error password, have value is nan:',password_err)

if __name__ == "__main__":
    main()