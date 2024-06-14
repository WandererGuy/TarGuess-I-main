
def read_file_to_list(filename):
    with open(filename, encoding="utf8") as file:
        return [line.strip() for line in file]

word_list = read_file_to_list('name_dict.txt')
name_list = read_file_to_list('Vietnamese_transform_dict.txt')
english_list = read_file_to_list('english_popular.txt')

letter_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
digit_list = '0123456789'
symbol_list = '!@#$%^&*()-_=+[]{};’:”,./<>?'

def transform_string(str): 
    sequence = ""
    for i in range(len(str)): 
        if (str[i].isdigit()): 
            sequence += 'D'
        elif((str[i] >= 'A' and str[i] <= 'Z') or
                (str[i] >= 'a' and str[i] <= 'z')): 
            sequence += 'L'
        else:
            sequence += 'S'
    return sequence


def chunk_string(s, sequence):
    chunk_list = []
    temp_sequence = ""
    for index, i in enumerate(range(len(s))): 
        if index >= 1:
            if sequence[i] == sequence[i-1] and index == len(s)-1:
                temp_sequence += s[i]
                chunk_list.append(temp_sequence)
            elif sequence[i] == sequence[i-1]:
                temp_sequence += s[i]
            elif sequence[i] != sequence[i-1] and index == len(s)-1:
                chunk_list.append(s[i])
            else:
                chunk_list.append(temp_sequence)
                temp_sequence = ''
                temp_sequence += s[i]
        else: 
            temp_sequence += s[i]
    return chunk_list





def flatten(nested):
    flat = []
    def helper(nested):
        for e in nested:
            if isinstance(e, list):
                helper(e)
            else:
                flat.append(e)
    helper(nested)
    return flat

# for index, item in update_df['NickName'].items():
#     # extract clue from nickname -> create nickname clue list
#     clue_segment_ls = extract_meaningful_chunks_WORD_NAME_CHAR_NEW(item, word_list, name_list, english_list)
#     clue = flatten(clue_segment_ls)
#     # remove 1 letter in clue
#     clue = [item for item in clue if len(item) > 1]
#     update_df.at[index, 'PossibleNickNameClue'] = clue


def extract_meaningful_chunks_WORD_NAME_CHAR_NEW(input_str, word_list, name_list, english_list):
    # Assuming the transformation and chunking functions are defined elsewhere and are correct
    sequence = transform_string(input_str)
    chunk_list = chunk_string(input_str, sequence)
    
    new_word_list = [item.replace('\n', '') for item in word_list]
    new_name_list = [item.replace('\n', '') for item in name_list]
    new_english_list = [item.strip().replace('\n', '') for item in english_list]
    all_meaningful_chunk_list = []
    total_list = []

    
    # break down chunk (based priority max length substring match name, dict, rest word)
    for item in chunk_list:
        item = item.lower()
        flag_text = False
        for i in range(len(letter_list)):
            if letter_list[i] in item:
                flag_text = True
                meaning_chunk_list = []
                ori_item = item
                flag = True
                english_flag = False
                while True:

                    ### find all possible name from substring
                    res = [ori_item[i: j] for i in range(len(ori_item))
                    for j in range(i + 1, len(ori_item) + 1)]
                    substring_descend = sorted(res, key=len, reverse=True)
                    first_substring = substring_descend[0] #longest substring
                    if first_substring in new_english_list and len(first_substring) > 4:
                        
                        repeat = ori_item.count(first_substring)
                        ori_item = ori_item.replace(first_substring, ';')
                        for i in range(repeat):
                            meaning_chunk_list.append(first_substring)
                        # print ('Found first english ', first_substring)
                    elif first_substring not in new_english_list and english_flag == False:
                        for i in range(len(substring_descend)):
                            if i > 0:
                                substring = substring_descend[i]
                                if substring in new_english_list and len(substring) > 4:
                                    repeat = ori_item.count(substring)
                                    ori_item = ori_item.replace(substring, ';')
                                    for i in range(repeat):
                                        meaning_chunk_list.append(substring)
                                    # print ('Found english ', substring) 
                        english_flag = True

                    # if all substring > 4  dont have english word, still 
                    # return english flag = True to continue while loop for < 4 english word first substring
                    elif first_substring in new_english_list and english_flag == False and len(first_substring) <= 4:
                        english_flag = True
                    elif first_substring in new_name_list and english_flag:
                        repeat = ori_item.count(first_substring)
                        ori_item = ori_item.replace(first_substring, ';')
                        for i in range(repeat):
                            meaning_chunk_list.append(first_substring)
                    elif len(ori_item) > 0 and english_flag: 
                        found = False
                        for i in range(len(substring_descend)):
                            if i > 0:
                                substring = substring_descend[i]
                                if substring in new_name_list:
                                    repeat = ori_item.count(substring)
                                    ori_item = ori_item.replace(substring, ';')
                                    for i in range(repeat):
                                        meaning_chunk_list.append(substring)
                                    found = True
                                    break 
                        ### no name can be found from remaining substring, switch to find words
                        if first_substring in new_word_list and found == False:
                            repeat = ori_item.count(first_substring)
                            ori_item = ori_item.replace(first_substring, ';')
                            for i in range(repeat):
                                meaning_chunk_list.append(first_substring)
                            found = True
                        if first_substring not in new_word_list and found == False:
                            for i in range(len(substring_descend)):
                                if i > 0:
                                    substring = substring_descend[i]

                                    if substring in new_name_list:
                                        repeat = ori_item.count(substring)
                                        ori_item = ori_item.replace(substring, ';')
                                        for i in range(repeat):
                                            meaning_chunk_list.append(substring)
                                        found = True
                                        break 
                            if found == False:
                                ### find in word list 
                                for i in range(len(substring_descend)):
                                    if i > 0:
                                        substring = substring_descend[i]

                                        if substring in new_word_list:
                                            repeat = ori_item.count(substring)
                                            ori_item = ori_item.replace(substring, ';')
                                            for i in range(repeat):
                                                meaning_chunk_list.append(substring)
                                            found = True
                                            break 
                        if found == False :
                            flag = False
                            if ';' not in first_substring:
                                repeat = ori_item.count(first_substring)
                                ori_item = ori_item.replace(first_substring, ';')
                                for i in range(repeat):
                                    meaning_chunk_list.append(first_substring)

                            else:
                                for i in range(len(substring_descend)):
                                    if i > 0:
                                        substring = substring_descend[i]
                                        if ';' not in substring:

                                            repeat = ori_item.count(substring)
                                            ori_item = ori_item.replace(substring, ';')
                                            for i in range(repeat):
                                                meaning_chunk_list.append(substring)
                                            flag = True ### found substring not ;
                                            break 
                            if flag == False: ### only ; left                
                                # print ('no more can be found from substring')
                                break
                sorted_meaning_chunk_list = meaning_chunk_list
                all_meaningful_chunk_list.append(sorted_meaning_chunk_list)
        # for item in all_meaningful_chunk_list:
        #     all_meaningful_chunk_list = [ [i for i in item if i != ';'] for item in all_meaningful_chunk_list]
                total_list.append(all_meaningful_chunk_list)
                break
        if flag_text == False:
            total_list.append(item)
# Sorting the list
    return total_list
