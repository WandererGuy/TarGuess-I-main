
import os 
import pandas as pd 
import time 
class User:
    def __init__(self, password="", full_name="", birth="", email="", account_name="", id_num="", phone=""):
        # Handle missing values during initialization
        self.password = self.handle_missing(password).lower()
        self.full_name = self.handle_missing(full_name)
        self.birth = self.handle_missing(birth)
        self.email = self.handle_missing(email)
        self.account_name = self.handle_missing(account_name)
        self.id_num = self.handle_missing(id_num)
        self.phone = self.handle_missing(phone)
        self.split_name()  # Call the split_name method properly
        self.fix_birthday()

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
    def fix_birthday(self):
        # in zing csv: 1987-02-25 00:00:00.0
        # birthday: Birthday in this form (e.g., 19-1-1985 or 19-01-1985)
        if self.birth.count('-') >= 2:
            year = self.birth.split('-', 1)[0]
            month_date = self.birth.split('-', 1)[1]
            month = month_date.split('-', 1)[0]
            date = month_date.split('-', 1)[1]
            if len(date) >= 2:
                date = date[:2]
                date = date.strip()
                self.birth = date + '-' + month + '-' + year
            else:
                self.birth = ''
        else:
            self.birth = ''


    @staticmethod
    def handle_missing(value):
        """
        Handle missing values by returning an empty string if the value is None or NaN.
        """
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return ''
        return str(value)
    
# only need to change the value of this dict 
mapping_columns = {"account_name": "accountname", 
                   "password": "password", 
                   "email": "email", 
                   "full_name": "fullname",
                   "birth": "birthday",
                   "phone": "telephone"}

def main(test_file):

    # test_file = os.listdir(zing)[0]
    # test_file = os.path.join(zing, test_file)
    test_file_name = os.path.basename(test_file)
    df = pd.read_csv(test_file)
    new_df = df[[mapping_columns['account_name'], 
                 mapping_columns['password'], 
                 mapping_columns['email'], 
                 mapping_columns['full_name'], 
                 mapping_columns['birth'], 
                 mapping_columns['phone']]]

    user_data = []
    count = 0
    # Process each row and create a User object
    for _, row in new_df.iterrows():
        count += 1
        if count % 100000 == 0 :
            print (count)

        account_name = row[mapping_columns['account_name']]
        password = row[mapping_columns['password']]
        email = row[mapping_columns['email']]
        full_name = row[mapping_columns['full_name']]
        birth = row[mapping_columns['birth']]
        phone = row[mapping_columns['phone']]

        # Create a User object
        user = User(
            password=password,
            full_name=full_name,
            birth=birth,
            email=email,
            account_name=account_name,
            phone=phone, 
            id_num = count
        )

        # Add the User object to the list
        # Add the processed user data to the list
        # add to each column 1 value 
        user_data.append({
            'id': user.id_num,
            'username': user.account_name,
            'password': user.password,
            'email': user.email,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'birthday': user.birth,
            'tel': user.phone
        })

    necessary_cols = ['id', 'username', 'password', 'email', 'firstname', 'lastname', 'birthday', 'tel']

    save_folder = 'processed_csv'
    # Create a new DataFrame with the necessary columns
    processed_df = pd.DataFrame(user_data, columns=necessary_cols)
    # Save the DataFrame as a CSV file
    processed_df.to_csv(f'{save_folder}/zing_{test_file_name}', index=False)


def count_columns(csv_line):
    inside_quote = False
    columns = 0
    for char in csv_line:
        if char == '"':
            inside_quote = not inside_quote
        elif char == ',' and not inside_quote:
            columns += 1
    return columns + 1  # Add 1 for the last column




def checking_invalid_line(folder, filename_ls, num_cols):
    error_num = 0 
    for filename in filename_ls:
        
        with open (os.path.join(folder, filename), 'r', encoding='utf-8', errors='ignore') as f:
            print ('checking for error line in ', os.path.join(folder, filename))
            lines = f.readlines()
            for line in lines:
                if count_columns(csv_line = line) != num_cols:                    
                    error_num += 1
        if error_num > 0:
            print ('in file', os.path.join(folder, filename))
            print ('error num', error_num)
            print ('total line', len(lines))
            raise Exception('file invalid lines, please fix it')


def removing_invalid_line(folder, filename, num_cols):
    '''
    make sure the csv is good condition  to proceed to next step 
    '''
    valid_ls = []
    # for filename in os.listdir(folder):
    with open (os.path.join(folder, filename), 'r', encoding='utf-8', errors='ignore') as f:
        print ('checking error line in ', os.path.join(folder, filename))
        lines = f.readlines()
        for line in lines:
            if count_columns(csv_line = line) != num_cols:                    
                # raise Exception('invalid line, please fix it')
                pass
            else:
                valid_ls.append(line)
    os.rename(os.path.join(folder, filename), os.path.join(folder, filename.replace('.csv', '_old.csv')))
    with open (os.path.join(folder, filename), 'w', encoding='utf-8', errors='ignore') as f:
        for item in valid_ls:
            f.write(item)
    print ('new file replace in same path', os.path.join(folder, filename))


if __name__ == "__main__":
    '''
    this script is for processing zing csv breach dataset
    what it do:
    first check for file with error line 
    then fix that specific file by removing_invalid_line function
    '''

    fix_flag = False # set to true if you want to fix specific file (which will raise error it have line invalid (ex: 3 col instead of 4 col))
    filename_to_fix = 'xan.csv' # the specific file 


    zing = r"C:\Users\Admin\CODE\work\PASSWORD_CRACK\PASSCRACK_MATERIAL\WORDLISTS\ZING_TAILIEUVN_LEAK\28M_zing_split_cleaned"
    standard = 'accountname,accountstatus,password,gamecode,email,questionid,answer,personaltypeid,personalid,fullname,gender,birthday,telephone,address,countryid,cityid,districtid,regdate,regip'
    num_cols = count_columns(csv_line = standard)    
    print ('number of columns', num_cols)


    if fix_flag == True:
        removing_invalid_line(zing, 
                              filename_to_fix, 
                              num_cols)
    t = os.listdir(zing)
    # checking_invalid_line(zing, t, num_cols)

    for filename in os.listdir(zing):
            file_path = os.path.join(zing, filename)
            main(test_file = file_path)

