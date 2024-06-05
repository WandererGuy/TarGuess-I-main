import pandas as pd




# columns   = ['id', 'username', 'password', 'email', 'firstname', 'lastname', 'birthday', 'gender', 'address', 'tel']


# df = pd.read_csv('7M.csv')
# import numpy as np
# array = np.array_split(df, 10)
# for index, item in enumerate(array):
#     df = pd.DataFrame(item , columns=columns)
#     df.to_csv(f'{index}.csv')



# df = pd.read_csv('0.csv')
# new_df = df[['username', 'password', 'email', 'firstname', 'lastname', 'birthday', 'gender', 'address', 'tel']]

# new_df['plain_password'] = ''
# new_df['fullname'] = new_df['firstname'] + ' ' + new_df['lastname']
# gender_map = {1: 'Male', 0: 'Female'}
# new_df['gender'] = new_df['gender'].map(gender_map)

# # Split the email into two parts at the '@'
# new_df[['email_prefix', 'email_domain']] = new_df['email'].str.split('@', expand=True)
# update_df = new_df[['username', 'password', 'plain_password', 'email_prefix','email_domain',  'fullname', 'birthday', 'gender', 'address', 'tel']]
# update_df.to_csv('update_0.csv', index=False)






# Example DataFrame with a column 'password'

df = pd.read_csv('update_0.csv', index_col=0)
# Path to the output text file
output_file = 'passwords_0.txt'

# Number of passwords per group
group_size = 25

pass_list = df['password'].dropna().tolist()
print (len(pass_list))
pass_list = list(set(pass_list))
print (len(pass_list))

with open(output_file, 'w') as f:
    for i in range(0, len(df), group_size):
        # Extract passwords as a list and filter out None values
        passwords = pass_list[i:i+group_size]
        # Write passwords to the file
        for item in passwords:
            f.write(item)
            f.write('\n')
        f.write('\n')

