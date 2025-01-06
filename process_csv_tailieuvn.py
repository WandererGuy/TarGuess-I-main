
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
        # self.fix_birthday()

    def split_name(self): # Nguyen Anh Vien
        self.full_name = self.full_name.strip()
        # Ensure full_name has at least two parts to split
        if ' ' in self.full_name:
            self.firstname = self.full_name.rsplit(' ', 1)[1]
            self.lastname = self.full_name.rsplit(' ', 1)[0]
        else:
            self.firstname = self.full_name  # If no space, assume full_name is just the first name
            self.lastname = ""
            # in code, fullname = firstname + ' '  + lastname 
    # def fix_birthday(self):
    #     # in zing csv: 1987-02-25 00:00:00.0
    #     # in tailieuvn : 19-1-1985
    #     # birthday: Birthday in this form (e.g., 19-1-1985 or 19-01-1985)
    #     if self.birth.count('-') >= 2:
    #         year = self.birth.split('-', 1)[0]
    #         month_date = self.birth.split('-', 1)[1]
    #         month = month_date.split('-', 1)[0]
    #         date = month_date.split('-', 1)[1]
    #         if len(date) >= 2:
    #             date = date[:2]
    #             date = date.strip()
    #             self.birth = date + '-' + month + '-' + year
    #         else:
    #             self.birth = ''
    #     else:
    #         self.birth = ''


    @staticmethod
    def handle_missing(value):
        """
        Handle missing values by returning an empty string if the value is None or NaN.
        """
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return ''
        return str(value)
    
# only need to change the value of this dict 


mapping_columns = {"account_name": "username", 
                   "password": "password", 
                   "email": "email", 
                   "full_name": "fullname",
                   "birth": "birthday",
                   "phone": "tel"}

def main(test_file):
    # test_file = os.listdir(zing)[0]
    # test_file = os.path.join(zing, test_file)
    test_file_name = os.path.basename(test_file)
    df = pd.read_csv(test_file)

    # Create the fullname column
    df[mapping_columns['full_name']] = df['lastname'] + ' ' + df['firstname'] 

    new_df = df[[mapping_columns['account_name'], 
                 mapping_columns['password'], 
                 mapping_columns['email'], 
                 mapping_columns['full_name'], 
                 mapping_columns['birth'], 
                 mapping_columns['phone']]]

    user_data = []
    count = 0
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
    processed_df.to_csv(f'{save_folder}/{test_file_name}', index=False)


if __name__ == "__main__":
    # zing = r"C:\Users\Admin\CODE\work\PASSWORD_CRACK\PASSCRACK_MATERIAL\WORDLISTS\ZING_TAILIEUVN_LEAK\28M_zing_split_cleaned"
    tailieu = r"C:\Users\Admin\CODE\work\PASSWORD_CRACK\PASSCRACK_MATERIAL\WORDLISTS\ZING_TAILIEUVN_LEAK\7M_split_cleaned"
    # for filename in os.listdir(zing):
    #     file_path = os.path.join(zing, filename)
    #     print (file_path)

    # for filename in os.listdir(tailieu):
    #     file_path = os.path.join(tailieu, filename)
    for filename in os.listdir(tailieu):
            file_path = os.path.join(tailieu, filename)
            main(test_file = file_path)

