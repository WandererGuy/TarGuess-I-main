import os 
import json 
import re
from tqdm import tqdm
import itertools

print_flag = False
# LIMIT_COMBINATION_NUM = 50 * (10**6)
LIMIT_COMBINATION_NUM = 10**5 # total combination allow for each mask class  
MAX_LENGTH_CLASS_NUM = 50 # up to D50, L50, S50 for scanning
print ('LIMIT_COMBINATION_NUM', LIMIT_COMBINATION_NUM)


def create_scan_ls():
    scan_ls = []
    s = ['?l','?d', '?s']
    for i in range(MAX_LENGTH_CLASS_NUM,0,-1):
        for item in s:
            scan_ls.append(item*i)
    return scan_ls

SCAN_LS = create_scan_ls()    

def generate_combinations(nested_lst):
    combinations = list(itertools.product(*nested_lst))
    return combinations

def limit_transform_components(transform_components, limit_each_class):
    res = []
    for item in transform_components:
        if len(item) > limit_each_class:
            for index, fill in enumerate(item):
                if index == limit_each_class:
                    res.append(item[0:index])
                    break    
        else: 
            res.append(item)
    return res

def find_all_substring_indices(main_string, substring):
    # Find all range [start indices, len(substring) of the substring in the main string
    return [[match.start(), match.start() + len(substring)] for match in re.finditer(re.escape(substring), main_string)]

def translate_format(class_type):
    '''
    mapping from D3 to ?d?d?d
    '''
    letter = class_type[0].lower()
    num = class_type[1:]
    trans = ('?' + letter)*int(num)
    return trans

def extract_content(text):
    '''
    extract content from text with ' '  or '\t'
    return list of strings
    '''
    ls = text.split(' ')
    res = []
    for item in ls:
        res.extend(item.split('\t'))
    new_res = [item for item in res if item != '']
    return new_res 

def sort_by_start_index(nested_lst):
    '''
    sort nested list by first element of each list 
    '''
    return sorted(nested_lst, key=lambda x: x[0])

def cal_num_combination(ls):
    '''
    given nested list , calculate total number of combination
    '''
    total = 1 
    for item in ls:
        total *= len(item)
    return total

def form_range(sorted_index_ls):
    '''
    args: ex: [6, 7, 8, 9, 10, 11, 20, 21, 23, 36,37]
    return [6, 7, 8, 9, 10, 11], [20, 21], [23], [36, 37]
    '''
    res = []
    temp = []
    for index, item in enumerate(sorted_index_ls):
        if temp == []:
            temp.append(item)
        else: 
            if sorted_index_ls[index - 1] == item - 1:
                temp.append(item)
            else:
                res.append(temp)
                temp = []
                temp.append(item)
    if temp != []:
        res.append(temp)
    return res 

def find_missing_range(occupy_index, max_len):
    all_index = [i for i in range(0,max_len)]
    for ls in occupy_index:
         for i in ls:
             all_index.remove(i)
    all_index.sort()
    return all_index
def break_down_component(text, scan_ls):
    '''
    args: 
        ?l?l?lgaymen?d?d?l?s?l?l?liknow
    process:
        tmp , in each loop becomes
        ------gaymen?d?d?l?s------iknow
        ------gaymen----?l?s------iknow
        ------gaymen------?s------iknow
        ------gaymen--------------iknow
        ------gaymen--------------iknow
    d =  {'?l?l?l': [[0, 6], [20, 26]], '?d?d': [[12, 16]], '?l': [[16, 18]], '?s': [[18, 20]]}
    place_holder_occupy_index = [[0, 1, 2, 3, 4, 5], [20, 21, 22, 23, 24, 25], [12, 13, 14, 15], [16, 17], [18, 19]]
    non_place_holder_occy_index = [[6, 7, 8, 9, 10, 11], [26, 27, 28, 29, 30]]
    use string slice 
    expect return:
    ['?l?l?l', 'gaymen','?d?d','?l', '?s','?l?l?l', 'iknow']
    '''
    res = []
    d = {}
    pseudo_replace = '-'
    tmp = text 
    for item in scan_ls:
        main_string = tmp
        substring = item
        if item in tmp:
            ls_start_to_len_indices = find_all_substring_indices(main_string, substring)
            d[item] = ls_start_to_len_indices
            tmp = tmp.replace(substring, pseudo_replace*len(substring))
            if print_flag:print (tmp)

    place_holder_occupy_index = []
    for _, value in d.items():
        for item in value:
            start = item[0]
            end = item[1]
            t = []
            for i in range(start, end):
                t.append(i)
            place_holder_occupy_index.append(t)
    non_place_holder_occupy_index = find_missing_range(place_holder_occupy_index, len(text))
    non_place_holder_occupy_index = form_range(non_place_holder_occupy_index)
    all_range = place_holder_occupy_index
    all_range.extend(non_place_holder_occupy_index)
    sorted_all_range = sort_by_start_index(nested_lst = all_range)
    for index_range in sorted_all_range:
        res.append(text[index_range[0]:index_range[-1]+1])

    if print_flag:print ('text')
    if print_flag:print (text)
    if print_flag:print ('tmp')
    if print_flag:print (tmp)
    if print_flag:print ('d')
    if print_flag:print (d)
    if print_flag:print ('place_holder_occupy_index')
    if print_flag:print (place_holder_occupy_index)
    if print_flag:print ('non_place_holder_occupy_index')
    if print_flag:print (non_place_holder_occupy_index)
    if print_flag:print ('sorted_all_range')
    if print_flag:print (sorted_all_range)
    if print_flag:print ('res')
    if print_flag:print (res)
    return res

def create_fill_json(fill_mask_path, fill_mask_json_path):
    '''
    create json dictionary for filling into mask 
    '''
    thres_prob = 0
    success = 0
    json_dict = {}
    error = 0
    with open(fill_mask_path, 'r') as file:
        data = file.readlines()
        for item in data:
            item = item.strip('\n')
            res = extract_content(item)
            if len(res) != 3:
                error += 1
                continue
            else:
                success += 1
            class_type, value_fill, prob = res
            trans_type = translate_format(class_type)
            if trans_type not in json_dict.keys():
                json_dict[trans_type] = []
            if float(prob) > thres_prob:
                json_dict[trans_type].append(value_fill)
    with open (fill_mask_json_path, 'w') as file:
        json.dump(json_dict, file, indent=4)
    # with open(fill_mask_json_path, 'r') as f:
    #     dictionary = json.load(f)
    return json_dict

def check_line_have_target_info(components, scan_ls):
    # line must have at least one target info, not trawling mask 
    '''
    remove mask have no target info (since user dont provide that info field)
    '''
    for item in components:
        if item not in scan_ls:
            return True
    return False




def create_wordlist(mask_file, dictionary, limit_each_class):
    '''
    prioritize replace by longest pattern like ?l?l?l over ?l?l, 
    so scan from longest class to shortest
    limit_each_class is the max vocab for fill each class deserve (classes are xmen?l?l?l, ?d?dbombay?d, ?l, ?s, ...)
    '''
    scan_ls = SCAN_LS
    wordlist = {}
    decreasing_factor = 0.9 # slowly lower limit bar 
    lim_count = 8 # allow to fail limit bar 
    with open(mask_file, 'r') as f:
        lines = f.readlines()
        for line in tqdm(lines, total = len(lines)):
            line = line.strip('\n')
            wordlist[line] = []
            components = break_down_component(line, scan_ls) # ?d?dbombay?d -> ?d?d, bombay, ?d
            # if check_line_have_target_info(components, scan_ls) == False:
            #     continue 
            transform_components = []
            for item in components:
                if item in dictionary.keys():
                    value = dictionary[item]
                    transform_components.append(value)
                else:
                    transform_components.append([item])
            '''
            add some if else cases so that combination dont get too large
            ?d?d?d or ?l or ?s?s each have their vocab with certain number of word, descend in prob
            this decreasing_factor will cut down on limit number of in their vocab after every try
            if combination dont meet LIMIT_COMBINATION_NUM, reduce limit_each_class
            so vocab have more will be cut down more since the number limit bar keep decrease
            this allow fair for each class to have vocab with certain number of words
            '''        
            new_limit = limit_each_class
            count = 0 
            discard = False
            while True:  
                if count == lim_count:
                    discard = True
                    break
                # update every new_limit 
                tmp = limit_transform_components(transform_components, 
                                                new_limit)
                if cal_num_combination(tmp) < LIMIT_COMBINATION_NUM:
                    combinations = generate_combinations(tmp)
                    break
                else:
                    print ('doing again with lower limit_each_class to lower combination. please wait ...')
                    print ('current combinations num',cal_num_combination(tmp))
                    new_limit *= decreasing_factor 
                    count += 1
            
            if discard: continue 
            '''
            only mask with LIMIT_COMBINATION_NUM can survive, also known as not 
            high entropy / highly variated password / hard to guess
            0.9 decay so that low entropy can benefit from more choices in ?d?d / ?l?l?l / ?s
            '''
            for combo in combinations:
                # end = time.time()
                # if end - start > 10:
                #     raise TimeoutError
                join = ''.join(combo)  # Join the tuple into a string
                wordlist[line].append(join)
    return wordlist



def main_fill_mask(mask_fill_dictionary, mask_file_path, target_wordlist_path, only_wordlist = False):
    '''
    main usage: a target mask file , for each mask class , create wordlist no exceed LIMIT_COMBINATION_NUM
    create wordlist from fill_mask.txt + mask_file
    example: total short wordlist < 100 M for each mask file with 5000 mask with low , high entropy
    though high entropy class can be discarded due to not meet LIMIT_COMBINATION_NUM
    '''

    unique_set = set()

    print ('start making wordlist for each line in mask file')
    # mask_file = 'C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/generated_target_masklist/5ac50029-d881-4157-bc58-8eb9c91a9b24.hcmask'
    wordlist = create_wordlist(mask_file_path, 
                    mask_fill_dictionary, 
                    limit_each_class = 20)
    # discard mask have value []
    discard_mask_ls = []
    f = open(target_wordlist_path, 'a')
    ### write first item of mask for good representation to show people , then write the rest 
    for index, (key, value) in tqdm(enumerate(wordlist.items()), total=len(wordlist)):
        if index % 5 == 0 and index != 0:
            f.close()
            f = open(target_wordlist_path, 'a')
        if value == []:
            discard_mask_ls.append(key)
            continue
        if not only_wordlist:
            f.write(key)
            f.write('\n')
        if value[0] in unique_set:
            continue
        f.write(value[0])
        unique_set.add(value[0])
        f.write('\n')
        if not only_wordlist:f.write('--------------------------------------------------------------------\n')
    f.write('------------------------------------------------------------------------------------\n')
    print ('------------------------------------------------------------------------------------')
    end_flag = False
    for index, (key, value) in tqdm(enumerate(wordlist.items()), total=len(wordlist)):
        
        if index % 5 == 0 and index != 0:
            f.close()
            f = open(target_wordlist_path, 'a')
        if value == []:
            discard_mask_ls.append(key)
            continue
        if not only_wordlist:
            f.write(key)
            f.write('\n')
        for index, item in enumerate(value[1:]):
            if index == len(value) - 2:
                end_flag = True
            if item in unique_set:
                continue
            f.write(item)
            f.write('\n')
            unique_set.add(item)
        if end_flag:
            f.write('\n\n')
            end_flag = False
        if not only_wordlist:f.write('--------------------------------------------------------------------\n')
    print ("number of discarded mask class")
    print (len(discard_mask_ls))
    # print (discard_mask_ls)


# for each mask , there exist a wordlist for it , each with own prob
# this is for pcfg 
def single_mask_analysis(mask, dictionary):
    
    scan_ls = SCAN_LS
    components = break_down_component(mask, scan_ls) # ?d?dbombay?d -> ?d?d, bombay, ?d
    # if check_line_have_target_info(components, scan_ls) == False:
    #     continue 
    print ('components', components)
    require_mask_fill = []
    for item in components:
        if item in dictionary.keys():
            value = dictionary[item] # 
            require_mask_fill.append(value)
        else:
            require_mask_fill.append([item])
    return require_mask_fill