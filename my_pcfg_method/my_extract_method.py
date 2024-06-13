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

def making_my_pcfg():
    with open ('my_method_result.txt', 'r') as file:

        lines = file.readlines()


        class_dict = {}
        for line in lines:
            if line != '\n':
                class_type = line.split('\t')[0]
                if class_type not in class_dict:
                    class_dict[class_type] = []
                class_dict[class_type].append(line.split('\t')[1].strip('\n'))

    # we have key : [value1 , value 2 , value 1 ]
    # we have key , value , prob 
    # prob value 1 = number of value 1 / total number of value (aka len of list )
    with open ('my_method_final.txt', 'w') as file:
        for key, value in class_dict.items():
            ls  = list(set(value))
            for item in ls:
                # print (item,value.count(item))
                prob_item = value.count(item) / len(value)
                file.write (f'{key}\t{item}\t{prob_item}\n')

######### SORT BY CLASS #########
def finalize_my_pcfg():
    with open ('my_method_final.txt', 'r') as file:
        # arrange key 
        # arrange key in dict in descending alphabt order
        new_dict = {}
        sorted_new_dict = {}
        lines = file.readlines()
        for line in lines:
            if line != '\n':
                line = line.strip('\n')
                cls = line.split('\t')[0]
                value = line.split('\t')[1]
                prob = line.split('\t')[2]
                if cls not in new_dict.keys():
                    new_dict[cls] = []
                new_dict[cls].append({value:prob})

        # create list of keys on priority
        # create new dict with the list  
        # see what key available 
        # sort by number 
        
        overall_priority_queue = []
        for main_key in ['D', 'L', 'S']:
            temp_ls = []
            priority_queue = []
            for key in new_dict.keys():
                if main_key in key:
                    num = int(key.replace(main_key, ''))
                    temp_ls.append(num)
            temp_ls = sorted(temp_ls)
            for item in temp_ls:
                priority_queue.append(main_key+str(item))
            overall_priority_queue.extend(priority_queue)

        for key in overall_priority_queue:
            sorted_new_dict[key] = new_dict[key]

    with open ('my_method_better_final.txt', 'w') as file:
        for key, value in sorted_new_dict.items():
            for item in value:
                    for key_item, value_item in item.items():
                        file.write (f'{key}\t{key_item}\t{value_item}\n')

    ######### SORT BY PROB #########
    with open ('my_method_last_final.txt', 'w') as last_file:

        with open ('my_method_better_final.txt', 'r') as file:
            # solve prob descend for each section class one by one 
            lines = file.readlines()
            last = lines[0].strip('\n').split('\t')[0]
            temp_dict = {}

            for index, line in enumerate(lines):
                if line != '\n':
                    line = line.strip('\n')
                    cls = line.split('\t')[0]
                    value = line.split('\t')[1]
                    prob = line.split('\t')[2]
                    if cls == last:
                        temp_dict[value] = prob
                        if index == len(lines)-1:
                            sorted_temp_dict = dict(sorted(temp_dict.items(), key=lambda x:x[1], reverse=True))
                            for key, prob_value in sorted_temp_dict.items():
                                last_file.write (f'{last}\t{key}\t{prob_value}\n')
                    else:
                        sorted_temp_dict = dict(sorted(temp_dict.items(), key=lambda x:x[1], reverse=True))
                        for key, prob_value in sorted_temp_dict.items():
                            last_file.write (f'{last}\t{key}\t{prob_value}\n')
                        temp_dict = {}
                        last = cls
                        if index == len(lines)-1:
                            last_file.write (f'{last}\t{key}\t{value}\n')
                        
                        temp_dict[value] = prob

    ### check quality by total preserve -> Done 
    ### the more better extract formate correct , the better my 


            
if __name__ == '__main__':
    print ('from train_output : TRAIN/src/training_output.txt\n\
             produce my_method_result.txt')
    extract_all_things()
    print ('from my_method_result.txt\n\
           produce my_method_final.txt')
    making_my_pcfg()
    print ('group and sort by class then prob ')
    finalize_my_pcfg()
