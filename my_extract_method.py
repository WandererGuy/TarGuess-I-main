'''
create new pcfg wordlist better than original 
'''

def find_groups(password, text):
    temp_strings = []
    pass_list = []
    last =  text[0]
    last_index = 0 
    for i in range (len(text)):

        if text[i] == last:
            pass
        # keep a temp last in task of continous string 
        else:
            last = text[i]
            temp = text[last_index:i]
            temp_strings.append(temp)

            temp_pass = password[last_index:i]
            pass_list.append(temp_pass)
            last_index = i 

        # build case for only last string  
        if i == len(text) - 1:
            temp = text[last_index:]
            temp_strings.append(temp)

            temp_pass = password[last_index:]
            pass_list.append(temp_pass)
    return pass_list, temp_strings

def shorten (text):
    return text[0]+str(len(text))


def final_group(password, real_pattern):
    pass_list, temp_strings = find_groups(password, real_pattern)
    temp_ls = []
    for i in range (len(temp_strings)):
        for item in ['L','S','D']:
            if item in temp_strings[i]:
                temp_ls.append(shorten(temp_strings[i]) + '\t' + pass_list[i])


    return temp_ls


# real_pattern = 'DDLDDL'

# password = '53b57a'

# print (final_group(password, real_pattern))
def extract_all_things():
    with open ('my_method_result.txt', 'w') as output_file:
        with open ('TRAIN/src/training_output.txt', 'r') as file:
                lines = file.readlines()
                pass_flag = False
                pattern_flag = False 
                for line in lines:
                    if 'Password: ' in line:
                        password = line.split('Password: ')[1].strip('\n').replace(' ','')
                        pass_flag = True 
                    if 'real pattern: ' in line:
                        real_pattern = line.split('real pattern: ')[1].strip('\n').replace(' ','')
                        pattern_flag = True 
                    if pass_flag == True and pattern_flag == True:
                        # got a pair pass and pattern
                        temp_ls = final_group(password, real_pattern)
                        # for 1 password and 1 pattern of that, i can extract my own D,L,S
                        for item in temp_ls:
                            output_file.write(f'{item}\n')
                        output_file.write('\n')
                        pass_flag = False
                        pattern_flag = False

with open ('my_method_result.txt', 'r') as file:
    class_ls = []

    lines = file.readlines()
    for line in lines:
        if line != '\n':
            class_ls.append(line.split('\t')[0])

