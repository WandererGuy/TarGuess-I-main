# pcfg 
from tqdm import tqdm

from utils.fill_mask import single_mask_analysis
from itertools import product
import time 

MAX_VOCAB = 10
MAX_MASK_NUM = 1000
def create_wordlist_single_mask(single_mask, mask_fill_dictionary, mask_prob):
    # single_mask = '?d?dbombay?d'
    res = single_mask_analysis(single_mask, mask_fill_dictionary)
    new_res = []
    
    for item in res:
        
        if len(item) > MAX_VOCAB:
            item = item[:MAX_VOCAB]
 
        new_res.append(item)
    # Generate the Cartesian product
    combinations = list(product(*new_res))
    pcfg_ls = {}
    # Calculate and display probabilities
    for combo in combinations:
        password = ''
        prob = 1
        for component in combo:
            password += component[0]
            prob *= float(component[1])
        if password not in pcfg_ls:
            pcfg_ls[password] = prob
        pcfg_ls[password] += prob
    for key, value in pcfg_ls.items():
        pcfg_ls[key] = value * float(mask_prob)
    return pcfg_ls


def add_to_dict(key, value, all_pcfg_wordlist):
    if key in all_pcfg_wordlist:
        all_pcfg_wordlist[key] += value
    else:
        all_pcfg_wordlist[key] = value

    return all_pcfg_wordlist


import json 

def make_pcfg_wordlist(mask_fill_dictionary, mask_prob_path, destination_pcfg_wordlist_path):
    all_pcfg_wordlist = {}
    print ('creating pcfg wordlist ...')
    with open(mask_prob_path, 'r') as f:
        t = json.load(f)
        for key, value in tqdm(t.items(), total = len(t.keys())):
            key = key.strip('\n').strip()
            single_mask = key
            mask_prob = value
            single_mask_wordlist_dict = create_wordlist_single_mask(single_mask, mask_fill_dictionary, mask_prob)
            for key, value in single_mask_wordlist_dict.items():
                all_pcfg_wordlist = add_to_dict(key, value, all_pcfg_wordlist)
            
    sorted_items_desc = sorted(all_pcfg_wordlist.items(), key=lambda item: item[1], reverse=True)


    print ('finished creating pcfg wordlist, writing to file ...')
    print ('total len of pcfg wordlist: ', len(sorted_items_desc))
    with open(destination_pcfg_wordlist_path, 'w') as f:
        for key, value in tqdm(sorted_items_desc, total = len(sorted_items_desc)):
            f.write(f'{key}\t{value}\n')


# class Mask():
#     def __init__(self, mask, fill_mask_dict):
#         self.mask = mask
#         self.fill_mask_dict = fill_mask_dict

#     def create