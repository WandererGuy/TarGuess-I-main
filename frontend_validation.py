from routers.model import MyHTTPException, my_exception_handler
import re
import unidecode
def empty_to_none(value):
    return None if value == '' else value

    
def is_utf8(string):
    try:
        # Try encoding and decoding the string to UTF-8
        string.encode('utf-8').decode('utf-8')
    except UnicodeDecodeError:
        raise MyHTTPException(status_code=400,
                             message = f'{string} is not a valid UTF-8 string')

def full_name_validation(full_name = ''):
    if full_name != '':
        full_name = full_name.lower()
        full_name = unidecode.unidecode(full_name)
        full_name = full_name.strip()
        my_list = full_name.split(' ')
        if len(my_list) < 3:
            message = "Full name must have 3 or more compnents"
            raise MyHTTPException(status_code=400,
                                    message = message)

def birth_validation(birth):
    if birth and not re.match(r'^\d{2}-\d{2}-\d{4}$', birth):
        raise MyHTTPException(status_code=400,
                              message = "Birth date must be in DD-MM-YYYY format")

def email_validation(email):
    if '@' not in email:
        raise MyHTTPException(status_code=400,
                              message = "Email must be a valid email address with @ in email")
    else:
        pre, post = email.split('@')
        if pre == '' or post == '':
            raise MyHTTPException(status_code=400,
                                  message = "Email must be a valid email address with prefix, @ and postfix")

def id_num_validation(id_num):
    allow = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range (len(id_num)):
        if id_num[i] not in allow:
            raise MyHTTPException(status_code=400,
                                  message = "ID number can only contain digits")
def phone_validation(phone):
    allow = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range (len(phone)):
        if phone[i] not in allow:
            raise MyHTTPException(status_code=400,
                                  message = "phone number can only contain digits")



def target_input_validation(target_info: dict):
    if not target_info['full_name'] == None:
        full_name_validation(target_info['full_name'])
    if not target_info['birth'] == None:
        birth_validation(target_info['birth'])
    if not target_info['email'] == None:
        email_validation(target_info['email'])
    if not target_info['id_num'] == None:
        id_num_validation(target_info['id_num'])
    if not target_info['phone'] == None:
        phone_validation(target_info['phone'])



digit_lst = '0123456789'
letter_lst = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def check_class(char):
    if char in digit_lst:
        return 'D'
    elif char in letter_lst:
        return 'L'
    else:
        return 'S'
def kw_ls_check(new_kw_ls):
    for kw in new_kw_ls:
        ref_class = check_class(kw[0])
        for char in kw:
            if check_class(char) != ref_class:
                return False, kw 
    return True, None   