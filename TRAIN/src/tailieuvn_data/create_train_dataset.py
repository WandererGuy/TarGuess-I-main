import traceback
import csv
import time 
import unidecode

hash_dict = {}
error_count = 0 

def create_hash_dict():
    global hash_dict
    with open ('TRAIN/src/tailieuvn_data/hash_dict.txt', 'r') as f_dict:
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

def turn_string(text):
    return str(text)
import pandas as pd     
# got 1 csv from the PREPROCESS 
def update_raw_csv():
    csv_file = 'PREPROCESS/0.csv'
    df = pd.read_csv(csv_file)
    new_df = df[['username', 'password', 'email', 'firstname', 'lastname', 'birthday', 'gender', 'address', 'tel']]
    new_df['plain_password'] = ''
    new_df['fullname'] = new_df['firstname'] + ' ' + new_df['lastname']
    gender_map = {1: 'Male', 0: 'Female'}
    new_df['gender'] = new_df['gender'].map(gender_map)

    # Split the email into two parts at the '@'
    new_df[['email_prefix', 'email_domain']] = new_df['email'].str.split('@', expand=True)
    new_df['email_prefix'] = new_df['email'] # well guess still need full email
    update_df = new_df[['username', 'password', 'plain_password', 'email_prefix','email_domain',  'fullname', 'birthday', 'gender', 'address', 'tel']]
    update_df.to_csv('TRAIN/src/tailieuvn_data/update_0.csv', index=False)

def replace_password(hash_password):
    if hash_password in hash_dict:
        return hash_dict[hash_password]
    else:
        return None 
    
def fill_plain_pass():
    update_csv_file = 'TRAIN/src/tailieuvn_data/update_0.csv'
    df = pd.read_csv(update_csv_file)
    df = df.map(turn_string)
    print("Length of the DataFrame ORIGINAL:", len(df))
    df['plain_password'] = df['password'].apply(replace_password)
    # Remove rows where 'plain_password' is None
    df = df.dropna(subset=['plain_password'])
    print("Length of the DataFrame have plain crack:", len(df))
    return df

def fix_birthday(birthday):
    global error_count
    if birthday == 'nan' or birthday == '0':
        return None
    else: 
        try:
            d, m, y = birthday.split('-')
            if len(d) < 2:
                d = '0' + d
            if len(m) < 2:
                m = '0' + m
        except Exception as e:
            print ('******')
            print (birthday)
            # Print the error message
            print(f"An error occurred: {e}")
            # Print the traceback
            traceback.print_exc()
            error_count += 1
            return None
        return f'{y}{m}{d}'

def export_txt(input_filename):
    output_filename = input_filename.replace('.csv', '.txt')
    # Reading from CSV and writing to a tab-delimited text file
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

def finalize(df):
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
    new_df.to_csv('TRAIN/src/tailieuvn_data/final.csv', index=False)


if __name__ == '__main__':

        update_raw_csv()
        time.sleep(5)
        create_hash_dict()
        df = fill_plain_pass()
        finalize(df)
        export_txt('TRAIN/src/tailieuvn_data/final.csv')
        print ('number of error birthday',error_count)