from GUESS_MASK.format_finder import create_format_dict
import json
from utils.train import deduplicate_dict, create_pattern, check_trawling_mask, collect_clue, \
find_fill, sort_dict_by_occurence
import sys
from tqdm import tqdm
import os
# import argparse

# # Create the parser
# parser = argparse.ArgumentParser(description="something")

# # Add arguments
# parser.add_argument('--save_folder_path', type=str)
# parser.add_argument('--train_input_path', type=str)
# parser.add_argument('--target_train_output_path', type=str)
# parser.add_argument('--extra_target_train_output_path', type=str)
# parser.add_argument('--trawling_train_output_path', type=str)
# parser.add_argument('--extra_trawling_train_output_path', type=str)


# Parse the arguments
# args = parser.parse_args()

# save_folder_path = args.save_folder_path
# train_input_path = args.train_input_path

# target_train_output_path = args.target_train_output_path
# extra_target_train_output_path = args.extra_target_train_output_path
# trawling_train_output_path = args.trawling_train_output_path
# extra_trawling_train_output_path = args.extra_trawling_train_output_path
'''
from a password 
find mask 
find trawling fill dict 
'''


def training(data, 
             save_folder_path, 
             train_input_path, 
             target_train_output_path, 
             extra_target_train_output_path, 
             trawling_train_output_path,
             extra_trawling_train_output_path):  

    os.makedirs(save_folder_path, exist_ok = True)
    fail = 0 
    fill_class_dict = {}
    fill_dict = {}
    all_pattern = {}
    tmp_ls = []


    print ('Start training ...')
    for index, (key, value) in tqdm(enumerate(data.items()), 
                                              total = len(data)):
        # if index > 10000:
        #     break
        # if index % 1000 == 0:
        #     print ('index : ', key)
        
        try:
            email = key
            password = value['password']
            name = value['name']
            gid = value['gid']
            account = value['account']
            phone = value['phone']
            birth = value['birth']
            name_ls = name.split(' ')
            all_dict = create_format_dict(name_str = name_ls,
                                birth = birth,
                                email = email,
                                phone = phone,
                                account = account,
                                gid = gid
                                )
            tmp_ls.append((password, all_dict))
        except Exception as e:
            print (e) 
            fail += 1
            continue
    print ('total fail : ', fail)

    for item in tqdm(tmp_ls, total = len(tmp_ls)):
        password = item[0]
        all_dict = item[1]
        better_cluster = deduplicate_dict(collect_clue(all_dict))
        python_pattern, clearer_mask = create_pattern(password, better_cluster)
        if check_trawling_mask(python_pattern) == False:

            if python_pattern not in all_pattern:
                all_pattern[python_pattern] = 1
            else:
                all_pattern[python_pattern] += 1
        # print ('------------------python pattern ------------------')
        # print (python_pattern)
        # print ('------------------clearer mask ------------------')
        # print (clearer_mask)
        # print ('------------------collect fill ------------------')
        # print (find_fill(clearer_mask))

        if check_trawling_mask(python_pattern) == False:
                # check fill target mask only 
                res = find_fill(clearer_mask)
                for key, value in res.items():
                    if key not in fill_dict:
                        fill_dict[key] = 0 
                        fill_dict[key] += value[1]
                    else:
                        fill_dict[key] += value[1]
                    fill_class_dict[key] = (value[0], fill_dict[key])

        
                        
    sorted_dict = dict(sorted(all_pattern.items(), key=lambda item: item[1], reverse=True))
    total = 0 
    for key, value in sorted_dict.items():
        total += value
    with open (extra_target_train_output_path, 'w') as f_extra:
        with open (target_train_output_path, 'w') as f:
            for key, value in sorted_dict.items():
                f.write(f'{key}\t{float(value/total)}\n')
                f_extra.write(f'{key}\t{value}\n')

    # sorted_dict = dict(sorted(fill_dict.items(), key=lambda item: item[1], reverse=True))
    # with open('clearer_mask.txt', 'w') as file:
    #     for key, value in sorted_dict.items():
    #         file.write(f'{key}\t{value}\n')



    # with open('clearer_mask_better.txt', 'w') as file:
    res, res_prob = sort_dict_by_occurence(fill_class_dict)
    with open (target_train_output_path, 'a') as file:
        file.write('\n')
        for i in ['D', 'L', 'S']:
            for j in range (1, 50):
                for key, value in res_prob.items():
                    if key == i+str(j):
                        for item in value:
                            first_key = next(iter(item))
                            first_value = item[first_key]
                            file.write(f'{key}\t{first_key}\t{first_value}\n')

    with open(extra_target_train_output_path, 'a') as file_extra:
        file_extra.write('\n')
        for i in ['D', 'L', 'S']:
            for j in range (1, 50):
                for key, value in res.items():
                    if key == i+str(j):
                        for item in value:
                            first_key = next(iter(item))
                            first_value = item[first_key]
                            file_extra.write(f'{key}\t{first_key}\t{first_value}\n')

            
    
    print ('Done')
    return 'Done'