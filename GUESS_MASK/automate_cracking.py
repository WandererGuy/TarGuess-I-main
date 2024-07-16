from format_finder import create_format_dict

# name_str = ['ynhi', 'nguyen', 'luu']
# birth = '20001231'
# email = 'nhi30k@gmail.com'
# phone = '0383962428'
# account = 'ynhiluu3112'
# gid = '001201000681'

import configparser
config = configparser.ConfigParser()
config.read('config.ini')
max_mask_generate = config['DEFAULT']['max_mask_generate'] 

def read_input():
    info_dict = {}
    with open ("GUESS/src/result_folder/test.txt", "r") as f:
        line = f.readline()
        line = line.strip('\n')
        email, _, fullName, gid, accountName, phone, birth = line.split('\\t')
        info_dict['email'] = email
        info_dict['name_str'] = fullName.strip().split(' ')
        info_dict['gid'] = gid
        info_dict['account'] = accountName
        info_dict['phone'] = phone
        info_dict['birth'] = birth
    return info_dict

def replace_format(select_num, info_dict):
    name_str, birth, email, phone, account, gid = info_dict['name_str'], info_dict['birth'], info_dict['email'], info_dict['phone'], info_dict['account'], info_dict['gid']
    format_dict = create_format_dict(name_str, birth, email, phone, account, gid)
    raw_lst = []
    new_lst = []
    with open ('test.txt', 'r') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            if index == select_num:
                break
            line = line.strip('\n')
            raw = line.split('\t')[0]
            new = ''
            for i in range(len(raw)):
                if raw[i] in format_dict.keys():
                    new += format_dict[raw[i]]
                else:
                    new += raw[i]
            raw_lst.append(raw)
            new_lst.append(new)
            # print (raw, '\t', new)
    return raw_lst, new_lst

def create_mask(trans_format):
    mask = trans_format.replace('D', '?d').replace('L', '?l').replace('S', '?s')
    return mask 

def generate_mask_file(file_path):
    mask_file = open('generated_target_masklist/mask.hcmask', 'w')
    with open (file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            _, trans_format = line.split('\t')
            if 'D' in trans_format or 'L' in trans_format or 'S' in trans_format:
                mask = create_mask(trans_format)
                mask_file.write(mask + '\n')
            else:
                mask_file.write(trans_format + '\n')

if __name__ == '__main__':
    f = 'format_translation.txt'
    info_dict = read_input()
    with open(f, 'w') as file:
        raw_lst, new_lst = replace_format(max_mask_generate, info_dict)
        for raw, new in zip(raw_lst, new_lst):
            file.write(f"{raw}\t{new}\n")
    generate_mask_file(f)




