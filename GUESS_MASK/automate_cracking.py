from format_finder import create_format_dict
import os 
import argparse
import configparser
import uuid
from tqdm import tqdm
import json
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


def replace_format(max_mask_generate, info_dict, train_result_refined_path):
    name_str, birth, email, phone, account, gid = info_dict['name_str'], info_dict['birth'], info_dict['email'], info_dict['phone'], info_dict['account'], info_dict['gid']
    format_dict = create_format_dict(name_str, birth, email, phone, account, gid)
    raw_lst = []
    new_lst = []
    count = 0 
    for key, value in format_dict.items():
        print (key, '\t', value)
    with open (train_result_refined_path, 'r') as file:
        lines = file.readlines()
        for line in tqdm(lines, total = len(lines)):
            if count == max_mask_generate:
                break
            invalid_mask = False
            line = line.strip('\n')
            raw = line.split('\t')[0]
            new = ''
            for i in range(len(raw)):
                if raw[i] in format_dict.keys():
                    if format_dict[raw[i]] == '': # skip mask with empty fill even 1 target info component in mask 
                        # like Q?d?dA -> if even Q is '' then Q?d?dA is not valid mask this time 
                        invalid_mask = True
                        break
                    new += format_dict[raw[i]]
                else:
                    new += raw[i]
            if invalid_mask:
                continue
            raw_lst.append(raw)
            new_lst.append(new)
            count += 1
            print ('count valid mask :', count)
            print (raw, '\t', new)
            # print (raw, '\t', new)
    return raw_lst, new_lst

def create_mask(trans_format):
    mask = trans_format.replace('D', '?d').replace('L', '?l').replace('S', '?s')
    return mask 


class Mask:
    def __init__(self, mask_after_train, mask_after_fill, mask_final, prob=0.0):
        self.mask_after_train = mask_after_train
        self.mask_after_fill = mask_after_fill
        self.mask_final = mask_final
        self.prob = float(prob)


def generate_mask_file(mask_file_path, file_path):
    mask_ls = []
    mask_file = open(mask_file_path, 'w')
    with open (file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            mask_after_train, trans_format = line.split('\t')
            
            
            if 'D' in trans_format or 'L' in trans_format or 'S' in trans_format:
                final_mask = create_mask(trans_format)
                
                mask_file.write(final_mask + '\n')
            else:
                final_mask = trans_format
                mask_file.write(final_mask + '\n')
            new_mask = Mask(mask_after_train = mask_after_train, 
                            mask_after_fill = trans_format, 
                            mask_final = final_mask)
            mask_ls.append(new_mask)
    return mask_ls
    

def main():
    parser = argparse.ArgumentParser(description="parse input data")
    parser.add_argument('--mask_file_path', type=str)
    parser.add_argument('--target_info_file', type=str)
    parser.add_argument('--max_mask_generate', type=str) # max mask can generate if full all information 
    # less mask if less information 
    parser.add_argument('--train_result_refined_path', type=str)
    parser.add_argument('--mask_prob_path', type=str)

    args = parser.parse_args()
    mask_file_path = args.mask_file_path
    target_info_file = args.target_info_file
    mask_prob_path = args.mask_prob_path
    train_result_refined_path = args.train_result_refined_path
    max_mask_generate = int(args.max_mask_generate)
    os.makedirs(os.path.dirname(mask_file_path), exist_ok=True)
    t = os.path.join('GUESS_MASK','format_translation')
    os.makedirs(t, exist_ok=True)
    f = os.path.join(t, str(uuid.uuid4()) + '.txt')
    info_dict = read_input(target_info_file)
    print ('train_result_refined_path :', train_result_refined_path)

    with open(f, 'w') as file:
        raw_lst, new_lst = replace_format(max_mask_generate, info_dict, train_result_refined_path)
        
        for raw, new in zip(raw_lst, new_lst):
            file.write(f"{raw}\t{new}\n")
    # t = {}
    # with open (train_result_refined_path, 'r') as file:
    #     lines = file.readlines()
    #     for line in lines:
    #         line = line.strip('\n').strip()
    #         raw, prob = line.split('\t')
    #         t[raw] = prob
    print ('--------------------------------------------')



    print ('intermediate file created', f)
    # f is just intermediate file to store format translation
    mask_ls = generate_mask_file(mask_file_path, f)
    with open (train_result_refined_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n').strip()
            raw, prob = line.split('\t')
            for mask in mask_ls:
                if mask.mask_after_train == raw and mask.prob == 0.0:
        
                    
                    mask.prob = prob
                    break
    t = {}
    for mask in mask_ls:
        t[mask.mask_final] = mask.prob
    print ('writing into mask_prob_path :', mask_prob_path)
    with open(mask_prob_path, 'w') as file:
        json.dump(t, file, indent=4)

if __name__ == '__main__':
    main()





