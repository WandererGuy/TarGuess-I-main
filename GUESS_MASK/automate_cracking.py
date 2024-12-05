from format_finder import create_format_dict
import os 
import argparse
import configparser
import uuid
config = configparser.ConfigParser()
config.read(os.path.join('config', 'config.ini'))
# train_result_refined_path = config['GUESS_MASK']['train_result_refined_path']
static_folder_train = os.path.join('static','train_result')
def read_input(target_info_file):
    info_dict = {}
    with open (target_info_file, "r") as f:
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

def replace_format(select_num, info_dict, train_result_refined_path):
    name_str, birth, email, phone, account, gid = info_dict['name_str'], info_dict['birth'], info_dict['email'], info_dict['phone'], info_dict['account'], info_dict['gid']
    format_dict = create_format_dict(name_str, birth, email, phone, account, gid)
    raw_lst = []
    new_lst = []
    with open (train_result_refined_path, 'r') as file:
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

def generate_mask_file(mask_file_path, file_path):
    mask_file = open(mask_file_path, 'w')
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

def main():
    parser = argparse.ArgumentParser(description="parse input data")
    parser.add_argument('--mask_file_path', type=str)
    parser.add_argument('--target_info_file', type=str)
    parser.add_argument('--max_mask_generate', type=str)
    parser.add_argument('--train_result_refined_path', type=str)
    args = parser.parse_args()
    mask_file_path = args.mask_file_path
    target_info_file = args.target_info_file
    train_result_refined_path = args.train_result_refined_path
    max_mask_generate = int(args.max_mask_generate)
    os.makedirs(os.path.dirname(mask_file_path), exist_ok=True)
    t = os.path.join('GUESS_MASK','format_translation')
    os.makedirs(t, exist_ok=True)
    f = os.path.join(t, str(uuid.uuid4()) + '.txt')
    info_dict = read_input(target_info_file)
    with open(f, 'w') as file:
        raw_lst, new_lst = replace_format(max_mask_generate, info_dict, train_result_refined_path)
        for raw, new in zip(raw_lst, new_lst):
            file.write(f"{raw}\t{new}\n")
    # f is just intermediate file to store format translation
    generate_mask_file(mask_file_path, f)

if __name__ == '__main__':
    main()





