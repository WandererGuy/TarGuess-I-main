'''
write to txt new rule , 
old rule filter out only D,L,S format 
(so keep only personal info included format )
remove duplicate element 
analyze new_order format in graph 
'''

import matplotlib.pyplot as plt



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
                            new_line += item
                        else: 
                            new_line += prob
                    content.append(new_line)
                else:
                    content.append(line)
                    
        with open (file_path, 'w') as new_file:
            for item in content:
                new_file.write(item)

def resolve_conflict():
    '''
    mechanism of produce 
    '''

if __name__ == '__main__':
    rule_file_path = 'GUESS/src/result_folder/OUTPUT_TRAIN.txt'
    new_order_path = 'GUESS/src/result_folder/new_order.txt'
    trawling_path = 'GUESS/src/result_folder/trawling.txt'
    better_new_order_path = 'GUESS/src/result_folder/better_new_order.txt'
    write_new_order(rule_file_path, new_order_path)
    remove_duplicate_elements(rule_file_path, new_order_path)
    format_prob(new_order_path)

    targuess_trawling_rule(rule_file_path, new_order_path, trawling_path)
    remove_duplicate_elements(rule_file_path, trawling_path)
    format_prob(trawling_path)

