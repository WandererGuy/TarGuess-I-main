from GUESS_MASK.format_finder import create_format_dict
from utils.train import (deduplicate_dict, 
                         create_pattern, 
                         check_trawling_mask, 
                         collect_clue, 
                        find_fill, 
                        sort_dict_by_occurence)
import sys
from tqdm import tqdm
import os



def training(data, 
             target_train_output_path, 
             extra_target_train_output_path
            ) -> str:
    '''
    Function:
        from a person info and his/her password 
        find the target mask for that password 
    Process:
        A person info can extract format dictionary 
        from this format dictionary + person password, can find: target mask + trawling fill dictionary
        to find the target mask:
            by slowly replace part > 2 char, and following order of replace follow by 
            cluster_dict = {'phone': ['C'], 
                            'account': ['A', 'u', 'v'],
                            'name': ['N', 'a', 'b', 'c', 'd', 'f', 'g', 'V', 'W', 'X'],
                            'birth': ['O', 'Q', 'R', 'F', 'H', 'I', 'J', 'K', 'Y', 'Z', 'M'],
                            'email': ['E', 's', 't'],
                            'gid': ['G', 'w']}
        to find trawling fill dictionary:

    
    '''

    fail = 0 
    fill_class_dict = {}
    fill_dict = {}
    all_pattern = {}
    tmp_ls = []


    print ('Start training ...')
    for index, (key, value) in tqdm(enumerate(data.items()), 
                                              total = len(data)):
        total = len(data)
        if index == total - 1:
            print ('finished loop')
        try:
            email = key
            password = value['password']
            name = value['name'].lower()
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
    print ('total fail person info for training : ', fail)

    for item in tqdm(tmp_ls, total = len(tmp_ls)):
        password = item[0]
        all_dict = item[1]
        # keep non-empty format and group format into 6 groups


        better_cluster = deduplicate_dict(collect_clue(all_dict))
        '''
        function: find clearer mask to find trawling strings that fill in target mask 
        clearer mask : mask have no format mask key
        example:
            racingboycrazy123 -> clearer mask is: ---------crazy--- 
            (where v, u is format mask key, v is account letter, u is account digit), 
            'crazy' dont belong to any format so NOT be replaced by '-' 
        '''
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
    with open (extra_target_train_output_path, 'w', encoding='utf-8', errors='ignore') as f_extra:
        with open (target_train_output_path, 'w', encoding='utf-8', errors='ignore') as f:
            for key, value in sorted_dict.items():
                f.write(f'{key}\t{float(value/total)}\n')
                f_extra.write(f'{key}\t{value}\n')

    # sorted_dict = dict(sorted(fill_dict.items(), key=lambda item: item[1], reverse=True))
    # with open('clearer_mask.txt', 'w') as file:
    #     for key, value in sorted_dict.items():
    #         file.write(f'{key}\t{value}\n')

    # with open('clearer_mask_better.txt', 'w') as file:
    res, res_prob = sort_dict_by_occurence(fill_class_dict)
    with open (target_train_output_path, 'a', encoding='utf-8', errors='ignore') as file:
        file.write('\n')
        for i in ['D', 'L', 'S']:
            for j in range (1, 50):
                for key, value in res_prob.items():
                    if key == i+str(j):
                        for item in value:
                            first_key = next(iter(item))
                            first_value = item[first_key]
                            file.write(f'{key}\t{first_key}\t{first_value}\n')

    with open(extra_target_train_output_path, 'a', encoding='utf-8', errors='ignore') as file_extra:
        file_extra.write('\n')
        for i in ['D', 'L', 'S']:
            for j in range (1, 50):
                for key, value in res.items():
                    if key == i+str(j):
                        for item in value:
                            first_key = next(iter(item))
                            first_value = item[first_key]
                            file_extra.write(f'{key}\t{first_key}\t{first_value}\n')


    return 'Done'