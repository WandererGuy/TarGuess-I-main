import copy

digit_lst = '0123456789'
letter_lst = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def find_class(char):
    if char in digit_lst:
        return 'D'
    elif char in letter_lst:
        return 'L'
    else:
        return 'S'



def collect_clue(all_dict):
    '''
    given a target format dict 
    group relevant format into groups, then keep only the format not empty 
    
        all_dict: target format dict
        better_cluster: format dict in group and each format not empty 
    '''
    ''' 
        learn from cpp targuess
        they respectively replace in this order they resspectively replace in this order 
        not by max length , 
        but by this order only 

        if (PI.find(email) != PI.end()) {
            person pp = PI[email];
            /// phone
            pp.processPhone(pat_str, psw);

            // account name
            pp.processAccount(pat_str, psw);

            ///name
            pp.processName(pat_str, psw);

            //birth
            pp.processBirth(pat_str, psw);

            //email
            pp.processEmail(pat_str, psw);

            // gid
            pp.processGid(pat_str, psw);

    '''
    cluster_dict = {'phone': ['C'], 
                    'account': ['A', 'u', 'v'],
                    'name': ['N', 'a', 'b', 'c', 'd', 'f', 'g', 'V', 'W', 'X'],
                    'birth': ['O', 'Q', 'R', 'F', 'H', 'I', 'J', 'K', 'Y', 'Z', 'M'],
                    'email': ['E', 's', 't'],
                    'gid': ['G', 'w']}
    better_cluster = {}

    for key, value in cluster_dict.items():
        better_cluster[key] = []
        for i in value: # 'C'
            if i not in all_dict.keys():
                continue
            if all_dict[i]  == '': 
                continue
            better_cluster[key].append({i:all_dict[i]})
    return better_cluster


def find_substring_indices(main_str, sub_str):
    start_indices = []
    sub_len = len(sub_str)
    i = 0  # Initialize the starting index

    while i <= len(main_str) - sub_len:
        # Check if the substring matches
        if main_str[i:i+sub_len] == sub_str:
            start_indices.append(i)
            i += sub_len  # Move past this substring to prevent overlapping
        else:
            i += 1  # Move to the next character
    return start_indices


    

def create_pattern(pwd, better_cluster):
    # better_cluster :{ account: [{'A': 'hoatrangnguyen_05'}, {'u': '05'}, {'v': 'hoatrangnguyen'} = {}
    '''
    function: find clearer mask to find trawling strings that fill in target mask 
    clearer mask : mask have no format mask key
    example:
        racingboycrazy123 -> clearer mask is: ---------crazy--- 
        (where v, u is format mask key, v is account letter, u is account digit), 
        'crazy' dont belong to any format so NOT be replaced by '-' 
    '''

    note = {}
    for key, value in better_cluster.items():
        for i in value:
            for k, v in i.items():
                if len(v) >= 2: # longer more than 1 can be consider format
                    start_indices = find_substring_indices(pwd, v)
                    
                    
                    note[k] = (start_indices, len(v))
                    pwd = pwd.replace(v, '-'*len(v)) # only replace once
                    # print ('changed: ', pwd)
    clearer_mask = ''
    pattern = ''
    i = 0 
    while i < len(pwd):
            exit_flag = False
            for key, value in note.items():
                start_indices, len_v = value
                for start_index in start_indices:
                    if i == start_index:
                        pattern += key
                        right_len = len_v
                        clearer_mask += len_v*'-'
                        exit_flag = True
            if exit_flag:
                i += right_len
            if not exit_flag:
                clearer_mask += pwd[i]
                pattern += find_class(pwd[i])
                i += 1
    
    return pattern, clearer_mask


def deduplicate_dict(dict1):
    tmp = set()
    res_dict = {}
    for key1, value1 in dict1.items():
        res_dict[key1] = []
        for item in value1:
        
            for key2, value2 in item.items():
                if value2 in tmp:
                    continue
                else:
                    tmp.add(value2)
                    res_dict[key1].append({key2: value2})
    return res_dict


def find_class_fill(text):
    '''
    given a string , find the trawling fill class of that string
    deptrai : D6
    278 : L3
    '''
    return find_class(text[0]) + str(len(text))

def find_fill(clearer_mask):
    '''
    function: find clearer mask to find trawling strings that fill in target mask 
    clearer mask : mask have no format mask key
    example:
        racingboycrazy123 -> clearer mask is: ---------crazy--- 
        (where v, u is format mask key, v is account letter, u is account digit), 
        'crazy' dont belong to any format so NOT be replaced by '-' 
    '''
    '''
    collect trawling strings then find their class (trawling fill class)
    '''
    res = {}
    tmp_str = ''
    for i in range (len(clearer_mask)):
        if clearer_mask[i] == '-':
            continue 
        else:
            tmp_str += clearer_mask[i]
            if i == len(clearer_mask)-1:
                if tmp_str not in res: res[tmp_str] = 1
                else: res[tmp_str] += 1

            elif find_class(clearer_mask[i]) != find_class(clearer_mask[i+1]):
                if tmp_str not in res: res[tmp_str] = 1
                else: res[tmp_str] += 1
                tmp_str = ''
                
    new_res = {}
    for key, value in res.items():
        new_res[key] = (find_class_fill(key), value)

    return new_res

def check_trawling_mask(mask:str) -> bool:
    '''
    check whether a mask is a trawling mask or target mask 
    '''
    trawling_symbol = ['D', 'L', 'S']
    for i in range (len(mask)):
        if mask[i] in trawling_symbol:
            continue
        else:
            return False
    return True

def sort_dict_by_occurence(fill_class_dict):
    
    t = {}
    for key, value in fill_class_dict.items():
        class_fill = value[0]
        count = value[1]
        if class_fill not in t:
            t[class_fill] = []
        t[class_fill].append({key:count})
    for class_fill, value in t.items():
        t[class_fill].sort(key=lambda item: list(item.values())[0], reverse=True)
    w = {}
    u = copy.deepcopy(t)
    for class_fill, value in u.items():
        single_class_fill_sum = 0 
        for index, item in enumerate(value):
            first_key = next(iter(item))
            first_value = item[first_key]
            single_class_fill_sum += first_value
        w[class_fill] = single_class_fill_sum

    for class_fill, value in u.items():
        for index, item in enumerate(value):
            first_key = next(iter(item))
            first_value = item[first_key]
            u[class_fill][index][first_key] = first_value / w[class_fill] 
            
    return t, u 