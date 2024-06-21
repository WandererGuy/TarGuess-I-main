from format_finder import create_format_dict

name_str = ['ynhi', 'nguyen', 'luu']
birth = '20001231'
email = 'nhi30k@gmail.com'
phone = '0383962428'
account = 'ynhiluu3112'
gid = '001201000681'


def replace_format():
    global select_num
    format_dict = create_format_dict(name_str, birth, email, phone, account, gid)
    raw_lst = []
    new_lst = []
    with open ('test.txt', 'r') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            if index == select_num:
                break
            line = line.strip('\n')
            raw = line.split('\t')[0]
            new = ''
            for i in range(len(raw)):
                if raw[i] in format_dict.keys():
                    new += format_dict[raw[i]]
                else:
                    new += raw[i]
            raw_lst.append(raw)
            new_lst.append(new)
            # print (raw, '\t', new)
    return raw_lst, new_lst


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



def ploting(probabilities_ls, labels_ls):
    global num_elements
    # Sort the data by probabilities and select the top 'num_elements' items
    sorted_labels = [label for _, label in sorted(zip(probabilities_ls, labels_ls), reverse=True)]
    sorted_probabilities = sorted(probabilities_ls, reverse=True)


    # Example usage
  # Assuming 20 elements in the plot
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
    plt.savefig('top_labels.png')

select_num = 30
num_elements = select_num
# analyze format samples (from new_order) , translate format & plot 
if __name__ == '__main__':

    probabilities_ls = []
    labels_ls = []
    with open ('test.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            label, prob = line.split('\t')


            prob = round(round(float(prob), 8)*10000000,8) 
            probabilities_ls.append(prob)
            labels_ls.append(label)


    from estimate_trials import cal_trials
    for item in labels_ls[:select_num]:
        print (item, '\t',cal_trials(item))

    ploting(probabilities_ls[:select_num], labels_ls[:select_num])

    replace_format()

    