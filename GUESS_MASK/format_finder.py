digit_lst = '0123456789'
letter_lst = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'



def create_format_dict(name_str: list, birth: str, email:str, phone: str, account: str, gid: str):
    all_dict = {}
    ##### NAME #####
    tmp_5 = tmp_4 = tmp_2 = tmp_1 = tmp_0 = ''
    if len(name_str) == 1 and name_str[0] == '': # empty field
        all_dict['N'] = all_dict['a'] = all_dict['b'] = all_dict['c'] = all_dict['d'] = ''
        all_dict['f'] = all_dict['g'] = all_dict['V'] = all_dict['W'] = all_dict['X'] = ''
    else:
        for i in range (len(name_str)):
            if i>0:
                tmp_5 += name_str[i][0]
            tmp_0 += name_str[i][0]
            tmp_1 += name_str[i]
            if i != 0:
                tmp_2 += name_str[i]

        tmp_4 = tmp_0[1:]

        all_dict['N'] = tmp_1
        all_dict['a'] = tmp_2 + name_str[0]
        all_dict['b'] = tmp_0
        all_dict['c'] = tmp_2
        all_dict['d'] = name_str[0]
        all_dict['f'] = tmp_4 + name_str[0]
        all_dict['g'] = name_str[0] + tmp_4
        all_dict['V'] = name_str[1]
        all_dict['W'] = name_str[2]
        all_dict['X'] = tmp_5 + name_str[0][0]
                                                    ##### BIRTH #####
    if len(birth) == 0:
        all_dict['O'] = all_dict['Q'] = all_dict['R'] = all_dict['F'] = all_dict['H'] = ''
        all_dict['I'] = all_dict['J'] = all_dict['K'] = all_dict['Y'] = all_dict['Z'] = all_dict['M'] = ''
    else:
        all_dict['O'] = birth[4:6]
        all_dict['Q'] = birth[6:8]
        all_dict['R'] = birth[0:4]
        all_dict['F'] = birth [2:4]
        if birth[4] == '0' and birth[6] != '0':
            all_dict['H'] = birth [5:6] + birth[0:4]
            all_dict['I'] = birth [5:6] + birth[2:4]
            all_dict['J'] = birth [5:6] + birth[6:8]

        if birth[4] != '0' and birth[6] == '0':
            all_dict['K'] = birth [7:8] + birth[0:4]
            all_dict['Y'] = birth [7:8] + birth[2:4]
            all_dict['Z'] = birth [7:8] + birth[4:6]

        if birth[4] == '0' and birth[6] == '0':
            all_dict['M'] = birth [7:8] + birth[5:6]


    ##### PHONE #####
    all_dict['C'] = phone

    ##### EMAIL #####
    email_prefix = email.split('@')[0]
    all_dict['E'] = email_prefix
    email_letter_str = ''
    email_digit_str = ''
    for i in range (len(email_prefix)):
        if email_prefix[i] in digit_lst:
            email_digit_str += email_prefix[i]
        elif email_prefix[i] in letter_lst:
            email_letter_str += email_prefix[i]

    all_dict['s'] = email_digit_str
    all_dict['t'] = email_letter_str

    ##### ACCOUNT #####
    all_dict['A'] = account
    account_letter_str = ''
    account_digit_str = ''
    for i in range (len(account)):
        if account[i] in digit_lst:
            account_digit_str += account[i]
        elif account[i] in letter_lst:
            account_letter_str += account[i]

    all_dict['u'] = account_digit_str
    all_dict['v'] = account_letter_str

    ##### GID #####
    all_dict['G'] = gid
    all_dict['w'] = gid[-4:]

    # for key, value in all_dict.items():
    #     print (key,'\t', value)
    return all_dict