pos_dict = {
    "?a" :94,
    "?l": 26,
    "?d": 10,
    "?u": 26,
    "?s": 32
    # "?x": 10  # most common symbol
}


def check_short_pass(line, min_pass_len):

    for key, value in pos_dict.items():
        new_line = line
        new_line = new_line.replace(key, 'X')
    if len(new_line) > min_pass_len:
        return False
    else:
        return True


# def cal_complexity(line):
def count_substring(main_string, sub_string):
    return main_string.count(sub_string)



def deduplicate_file_lines(mask_file_path):
    """
    Removes duplicate lines from the specified file while preserving the original order.

    Parameters:
    - mask_file_path (str): The path to the file to be deduplicated.

    Returns:
    - None
    """
    seen = set()
    unique_lines = []

    # Read all lines from the file
    with open(mask_file_path, 'r') as f:
        for line in f:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)

    # Write the unique lines back to the file
    with open(mask_file_path, 'w') as f:
        f.writelines(unique_lines)

def sort_by_complexity(mask_file_path, 
                       sorted_mask_file_path, 
                       min_pass_len):
    '''
    sort by complexity (aka number keyspaces)
    then with the masks have the same complexity,  sort by probability
    '''
    with open (mask_file_path, 'r') as f:
        lines = f.readlines()
        raw = {}
        for index, line in enumerate(lines):
            line = line.strip('\n')
            if line == '':
                continue
            if check_short_pass(line, min_pass_len): # skip min_pass_len char lenghth
                continue 
            total = 1
            for key, value in pos_dict.items():
                sub_string = key
                occurrences = count_substring(line, sub_string)
                if occurrences == 0:
                    continue
                combination = value ** occurrences             
                total = total*combination
            raw[index] = total


    # sort by complex then by probabilty 
    sorted_dict = dict(sorted(raw.items(), key=lambda item: item[1]))
    with open (sorted_mask_file_path, 'w') as f:
        for key, value in sorted_dict.items():
            line = lines[key].strip('\n')
            f.write(f'{line}\n')

