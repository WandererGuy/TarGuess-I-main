'''
all format extraction written in python 
'''



  # Example list of strings
def process_name(name):
    if not name:
        return None
    name_str = name.strip().split(' ')
    name_len = len(name_str)
    tmp = ["", "", "", "", ""]
    for i in range(name_len):
        tmp[0] += name_str[i][0]  # Adds the first character of each name_str element to tmp[0]
        tmp[1] += name_str[i]  # Concatenates all name_str elements to tmp[1]
        if i != 0:
            tmp[2] += name_str[i]  # Concatenates all name_str elements except the first one to tmp[2]

    tmp[3] = name_str[0]  # Assigns the first element of name_str to tmp[3]
    tmp[3] = tmp[3][0].upper() + tmp[3][1:]  # Converts the first character of tmp[3] to uppercase

    tmp[4] = tmp[0][1:]  # Removes the first character from tmp[0] and stores the rest in tmp[4]
    name_dict = {}
    name_dict['N'] = tmp[1]
    name_dict['a'] = tmp[2] + name_str[0]
    name_dict['b'] = tmp[0]
    name_dict['c'] = tmp[2]
    name_dict['d'] = name_str[0]
    name_dict['e'] = tmp[3]
    name_dict['f'] = tmp[4] + name_str[0]
    name_dict['g'] = name_str[0] + tmp[4]
    return name_dict

def process_birth(birth):
    birth_dict = {}
    if not birth or len(birth) != 8:
        return None
    # Add original birthdate with a tag
    birth_dict['B'] = birth
    # Remove month's leading zero
    if birth[4] == '0':
        birth_dict['h'] = birth[:4] + birth[5:]

    # Remove day's leading zero
    if birth[6] == '0':
        birth_dict['i'] = birth[:6] + birth[7]

    # Remove both month and day's leading zeros
    if birth[4] == '0' and birth[6] == '0':
        birth_dict['j'] = birth[:4] + birth[5] + birth[7]
    # Various substrings of the birthdate
    birth_dict['k'] = birth[:6]
    birth_dict['l'] = birth[2:8]
    birth_dict['m'] = birth[:4]
    birth_dict['n'] = birth[4:]
    birth_dict['o'] = birth[2:6]

    # Reordering and combining different parts
    birth_dict['p'] = birth[4:] + birth[:4]
    birth_dict['q'] = birth[4:6] + birth[:4]
    birth_dict['r'] = birth[4:] + birth[2:4]
    return birth_dict

def process_phone(phone):
    phone_dict = {}
    if phone == '':
        return None
    phone_dict = {'C': phone}
    return phone_dict

def process_gid(gid):
    gid_dict = {}
    if gid == '':
        return None
    gid_dict['G'] = gid
    last_gid = gid[-4:]
    gid_dict['w'] = last_gid
    return gid_dict

def process_email(email):
    email_dict  = {}
    pos = email.find('@')  # Assuming 'pos' is the position of '@'
    if pos == -1:

        return None  # Handle case where '@' is not found

    email_prefix = email[:pos]
    email_dict['E'] = email_prefix
    digit_seq = ""
    letter_seq = ""

    # Extract first sequence of digits
    for char in email_prefix:
        if '0' <= char <= '9':
            digit_seq += char
        elif digit_seq:  # Break once the first sequence of digits is interrupted
            break

    # Reset and extract first sequence of letters
    for char in email_prefix:
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            letter_seq += char
        elif letter_seq:  # Break once the first sequence of letters is interrupted
            break
    if digit_seq:
        email_dict['s'] = digit_seq
    else: 
        email_dict['s'] = ""
    if letter_seq:
        email_dict['t'] = letter_seq
    else:
        email_dict['t'] = ""

    return email_dict

def process_account(account):
    account_dict = {}
    if account == '':

        return None
    account_dict['A'] = account
    acc_d = ""  # To store digits
    acc_l = ""  # To store letters
    ad = False  # Flag to check if any digit is found
    al = False  # Flag to check if any letter is found

    # Extract the first sequence of digits from the account
    for char in account:
        if char.isdigit():
            acc_d += char
            ad = True
        elif ad:
            # Stop if we hit a non-digit after finding digits
            break

    # Extract the first sequence of letters from the account
    for char in account:
        if char.isalpha():
            acc_l += char
            al = True
        elif al:
            # Stop if we hit a non-letter after finding letters
            break

    # Simulate handling of the tags
    if ad and acc_d != account:
        account_dict['u'] = acc_d
    if al and acc_l != account:
        account_dict['v'] = acc_l
    return account_dict

# name = 'zhang san chuan'
# birth_date = '19940231'
# phone = '0383962428'
# gid = '1234567890'
# email = "user123abc@example.com"
# account = "123JohnDoe"



def input(name, birth_date, phone, gid, email, account):
    name_dict = process_name(name)
    birth_dict = process_birth(birth_date)
    phone_dict = process_phone(phone)
    gid_dict = process_gid(gid)
    email_dict = process_email(email)
    account_dict = process_account(account)
    all_dict = [name_dict , birth_dict , phone_dict , gid_dict , email_dict , account_dict]
    available_dict = []
    for item in all_dict:
        if item == None:
            continue
        else:
            available_dict.append(item)
    person_dict = {}
    for item in available_dict:
        person_dict = person_dict | item
    return person_dict


if __name__ == '__main__':
    input_file = 'result_folder/test.txt'
    with open (input_file, 'r') as f:
        data = f.readlines()
        for item in data:
                line = item.strip().strip('\n')
                if line == '':
                    break
                else:
                    print (line)
                    data = line.split('\\t')
                    print (data)
                    email, psw, name, gid, account, phone, birthdate = data
                    person_dict = input(name = name, birth_date = birthdate, phone = phone, gid = gid, email = email, account = account)
                    print(person_dict)