'''
write to txt new rule , 
old rule filter out only D,L,S format 
(so keep only personal info included format )
remove duplicate element 
analyze new_order format in graph 
'''

# import matplotlib.pyplot as plt
import os 



def calculate_figsize(num_elements, base_width=6, base_height=4, scale_factor=0.5):
    """
    Calculate dynamic figure size based on number of elements.
    
    Parameters:
        num_elements (int): Number of elements in the plot.
        base_width (float): Base width of the figure in inches.
        base_height (float): Base height of the figure in inches.
        scale_factor (float): Factor to scale the size of the figure per element.
    
    Returns:
        tuple: A tuple containing the width and height of the figure.
    """
    # Scale width dynamically based on the number of elements
    width = base_width + num_elements * scale_factor
    # Keep the height relatively constant unless very large number of elements
    height = base_height if num_elements <= 10 else base_height + (num_elements - 10) * 0.1
    return (width, height)

def filter(label):
     flag = False
     for i in range (len(label)):
          if label[i] !='L' and label[i] !='D' and label[i] != 'S':
               flag = True
               break
     return flag

def write_new_order(rule_file_path, new_order_path):
    labels_ls = []
    probabilities_ls = []

    first_ls_label = []
    first_ls_prob = []
    second_ls_label = []
    second_ls_prob = []
    number = ['0','1','2','3','4','5','6','7','8','9','.']
    file_path = rule_file_path
    with open (file_path, 'r') as file:
        data = file.readlines()
        for index, item in enumerate(data):
            if item == '\n':
                final_data = data[:index]
                break 
    data = final_data
    for index,item in enumerate(data):
                line = item.strip()

            # if line == '':
            #     fill_ls = data[index+1:]
            #     break
            # else:
                prob = ''
                labels = ''
                # for i in range(len(line)):  
                i = 0
                while i < len(line):
                    if line[i] in number:
                        prob = prob + line[i]
                        i += 1
                    elif line[i]+line[i+1]=='e-':
                        prob = prob + line[i] + line[i+1]
                        i += 2
                    else: 
                        labels = labels + line[i]
                        i += 1
                prob = float(prob)


                labels = labels.replace(' ','').replace('\t','').strip()
                if filter(labels) == False:
                    second_ls_label.append(labels)
                    second_ls_prob.append(prob)
                    continue
                labels_ls.append(labels)
                probabilities_ls.append(prob)
                first_ls_label.append(labels)
                first_ls_prob.append(prob)
                print (labels,prob)

            # label, prob = line.split("\t")
            # labels_probs.append((label, float(prob)))

    # Number of elements to plot



    with open(new_order_path, 'w', encoding='utf-8') as f:
        print ('start write to new order')
        for i in range(len(first_ls_label)):
            f.write(first_ls_label[i] + '\t' + str(first_ls_prob[i])+'\n')
        print ('done write to new order')
        f.close()
        # for i in range(len(second_ls_label)):
        #     f.write(second_ls_label[i] + '\t' + str(second_ls_prob[i])+'\n')
        # f.write('\n')
        # print ('******************************')
        # for i in range(len(fill_ls)):
        #     f.write(fill_ls[i])
        #     print (fill_ls[i])
'''

    # Sort the data by probabilities and select the top 'num_elements' items
    sorted_labels = [label for _, label in sorted(zip(probabilities_ls, labels_ls), reverse=True)]
    sorted_probabilities = sorted(probabilities_ls, reverse=True)


    # Example usage
    num_elements = 20  # Assuming 20 elements in the plot
    figsize = calculate_figsize(num_elements)

    # Slicing the lists to get only the top specified elements
    top_labels = sorted_labels[:num_elements]
    top_probabilities = sorted_probabilities[:num_elements]

    # Create the bar plot for the top elements
    plt.figure(figsize=figsize)
    plt.bar(top_labels, top_probabilities, color='green')
    plt.xlabel('Labels')
    plt.ylabel('Probability')
    plt.title(f'Top {num_elements} Labels by Probability')
    plt.xticks(rotation=90)
    plt.savefig('GUESS/src/result_folder/top_labels.png')

'''


def remove_duplicate_elements(input_file, output_file):
    # Example data
    final_data = []
    with open (input_file, 'r') as file:
        data = file.readlines()
        for index, item in enumerate(data):
            if item == '\n':
                final_data = data[index+1:]
                break 
    
    sample_class_ls = []
    keep_ls = []
    for item in final_data:
        item_detail = item.split('\t')
        sample_class = item_detail[1]
        if sample_class not in sample_class_ls:
            sample_class_ls.append(sample_class)
            keep_ls.append(item)

    with open (output_file, 'a') as file:
        file.write('\n')
        for item in keep_ls:
            file.write(item)

def targuess_trawling_rule(rule_file_path, new_order_path, trawling_path):
    with open (rule_file_path, 'r') as file:
        data = file.readlines()
        for index, item in enumerate(data):
            if item == '\n':
                final_data_1 = data[:index-1]
                break 
    with open (new_order_path, 'r') as file:
        data = file.readlines()
        for index, item in enumerate(data):
            if item == '\n':
                final_data_2 = data[:index-1]
                break
    list3 = [item for item in final_data_1 if item not in final_data_2]
    with open (trawling_path, 'w') as file:
        for item in list3:
            file.write(item)
        
def format_prob(file_path):
        content = []
        with open (file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line != '\n':
                    data = line.strip('\n').split('\t')
                    old_prob = data[len(data)-1]
                    prob = float(old_prob)
                    prob = "{:.10f}".format(prob)
                    new_line = ''
                    for index, item in enumerate(data): 
                        if index != len(data)-1:
                            new_line += item + '\t'
                        else: 
                            new_line += prob + '\n'
                    content.append(new_line)
                else:
                    content.append(line)
                    
        with open (file_path, 'w') as new_file:
            for item in content:
                new_file.write(item)

def resolve_conflict(file_path):
    '''
    mechanism PCFG for extract D,L,S with length 
    is independent of format extract from targuess  
    so if L19 missing by FPCG, and uDDDD.. extracted from targuess needs filling 
    it cause bug, so a simple solution is to tackle this rare missing what to fill problem
    ex: 
    manhhandsome
    PCFG: L12
    Targuess: ALLLLLLLL (acount + L5)
    so no L5 is pick up but rather L12 word pick up
    this really need to pick up the L8 that needs to fill , in the meantime , lets 
    fill this with random string
    though 
    PCFG pick up L12 is really misleading (only good for trawling)
    PCFG should pick up L8 that needs to fill (this is real FPCG)
    ok lemme cook , test it out , first FPCG wordlist contains general , then my method , then combine 
    need to test 

    only need to fill lesser length , this phenonmenon caused by len (letter, 
    symbol, digit string) that PCFG pick up 
    longer than length format Targuess pick up (which tells diffrent kind of L,D,S)

    needed to fill     
    

    for example result 
    highest letter len 27
    highest digit len 30
    highest symbol len 11
    missing letter for fill ['L23', 'L25']
    missing digit for fill ['D19', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29']
    missing symbol for fill ['S10']
    '''
    available_list = [str(i) for i in range(1, 50)]
    existing_letter_length_for_fill = []
    existing_digit_length_for_fill = []
    existing_symbol_length_for_fill = []
    missing_letter_for_fill = []
    missing_digit_for_fill = []
    missing_symbol_for_fill = []

# diagnose which is potential , so can fill by random thing or take 1 substring from longest 
    with open (file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            data = line.split('\t')
            if len(data) == 3:
                mask = data[0]
                if 'L' in mask:
                    existing_letter_length_for_fill.append(mask.replace('L', ''))
                if 'D' in mask:
                    existing_digit_length_for_fill.append(mask.replace('D', ''))
                if 'S' in mask:
                    existing_symbol_length_for_fill.append(mask.replace('S', ''))
        for item in available_list:
            if item in existing_letter_length_for_fill:
                highest_letter_len = item
            if item in existing_digit_length_for_fill:
                highest_digit_len = item
            if item in existing_symbol_length_for_fill:
                highest_symbol_len = item
        available_list = [str(i) for i in range(1, int(highest_letter_len))]
        for item in available_list:                          
            if item not in existing_letter_length_for_fill:
                missing_letter_for_fill.append('L'+item)
        available_list = [str(i) for i in range(1, int(highest_digit_len))]
        for item in available_list:                          
            if item not in existing_digit_length_for_fill:
                missing_digit_for_fill.append('D'+item)
                
        available_list = [str(i) for i in range(1, int(highest_symbol_len))]
        for item in available_list:                          
            if item not in existing_symbol_length_for_fill:
                missing_symbol_for_fill.append('S'+item)
        print ('highest letter len', highest_letter_len)
        print ('highest digit len', highest_digit_len)
        print ('highest symbol len', highest_symbol_len)
        print ('missing letter for fill', missing_letter_for_fill)
        print ('missing digit for fill', missing_digit_for_fill)
        print ('missing symbol for fill', missing_symbol_for_fill)

    new_pcfg_value_ls = []
    for item in missing_letter_for_fill:
        times = int(item.replace('L', ''))
        new_pcfg_value_ls.append(item + '\t' + 'x'* times + '\t1') # 100% for its category
    for item in missing_digit_for_fill:
        times = int(item.replace('D', ''))
        new_pcfg_value_ls.append(item + '\t' + '0'* times + '\t1') # 100% for its category
    for item in missing_symbol_for_fill:
        times = int(item.replace('S', ''))
        new_pcfg_value_ls.append(item + '\t' + '@'* times + '\t1') # 100% for its category

    print ('Putting non sense to fill missing')
    with open(file_path, 'a') as new_file:
        for value in new_pcfg_value_ls:
            new_file.write(value + '\n')

def finalize(new_order_path, final_path):
    with open (new_order_path, 'r') as file:
        data = file.readlines()
        for i, item in enumerate(data):
            if item == '\n':
                final_data = data[:i]
                break 
    with open (final_path, 'w') as file:
        for item in final_data:
            file.write(item)

def extract_fill_mask(file_path, dest_path):
    with open (file_path, 'r') as file:
        data = file.readlines()
        for i, item in enumerate(data):
            if item == '\n':
                final_data = data[i+1:]
                break 
    with open (dest_path, 'w') as file:
        for item in final_data:
            file.write(item)

if __name__ == '__main__':
    f = os.path.join('GUESS', 'src', 'train_result')
    rule_file_path = os.path.join(f,'OUTPUT_TRAIN.txt')
    new_order_path = os.path.join(f,'new_order.txt')
    trawling_path = os.path.join(f,'trawling.txt')
    final_path = os.path.join(f,'train_result_refined.txt')
    
    fill_mask_path = os.path.join(f,'fill_mask.txt')
    write_new_order(rule_file_path, new_order_path)
    remove_duplicate_elements(rule_file_path, new_order_path)
    resolve_conflict(new_order_path)
    targuess_trawling_rule(rule_file_path, new_order_path, trawling_path)
    remove_duplicate_elements(rule_file_path, trawling_path)
    finalize(new_order_path, final_path)
    extract_fill_mask(file_path = new_order_path, dest_path = fill_mask_path)
    print ('done training and write refined result at ', final_path)

    '''
    OUTPUT_TRAIN.txt: target mask + trawling mask + pcfg word fill mask
    new_order_path: target mask + pcfg word fill mask
    trawling_path: trawling mask
    train_result_refined.txt: target mask sorted by keyspace then probability sorted
    '''