



def colab_plotting(points): 
    import matplotlib.pyplot as plt

    # Extract x and y values
    x, y = zip(*points)

    # Create the plot
    plt.figure(figsize=(12, 6))  # Larger figure size for better visibility
    plt.plot(x, y, marker='o', linestyle='-', markersize=4, label='Data Points')

    # Customize the plot
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Dot and Line Plot for Large Dataset')
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.show()

def convert():
    path = r'TRAIN\src\training_output.txt'
    from tqdm import tqdm 
    person_dict = {}
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for index, line in tqdm(enumerate (lines), total=len(lines)):
            if line.startswith('Email:'):
                email = line.split(': ')[1].strip('\n')
                password = lines[index + 1].split(': ')[1].strip('\n')
                name = lines[index + 2].split(': ')[1].strip('\n')
                gid = lines[index +3].split(': ')[1].strip('\n')
                account = lines[index + 4].split(': ')[1].strip('\n')
                phone = lines[index + 5].split(': ')[1].strip('\n')
                birth = lines[index + 6].split(': ')[1].strip('\n')
                pattern = lines[index + 8].split(': ')[1].strip('\n')
                person_dict[email] = {'password': password, 
                                    'name': name, 
                                    'gid': gid, 
                                    'account': account, 
                                    'phone': phone, 
                                    'birth': birth, 
                                    'pattern': pattern}
            continue 
    import json
    with open('train_output_result.json', 'w') as json_file:
        json.dump(person_dict, json_file, indent=4)
    import time 
    time.sleep(5)



def chunk_list(lst, n):
    """
    Splits the list `lst` into `n` chunks.
    The first few chunks will have one more element if `lst` isn't divisible by `n`.
    """
    '''
    usage 
    # chunks = chunk_list(name_ls, cpu_count)
    # with Pool(cpu_count) as p:
    #     p.map(process_all_name, chunks) # all cpu will together take care of this list 

    '''
    if n <= 0:
        raise ValueError("Number of chunks 'n' must be a positive integer.")
    length = len(lst)
    chunk_size = length // n
    excess = length % n
    chunks = []
    start = 0
    for i in range(n):
        # If there are excess elements, distribute one to this chunk
        end = start + chunk_size + (1 if i < excess else 0)
        chunks.append(lst[start:end])
        start = end
    return chunks

from tqdm import tqdm
def convert_txt_to_json(txt_path, json_path):
    import json
    print ('Converting txt to json')
    error_line = []
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        person_dict = {}
        for line in tqdm(lines, total=len(lines)):
            line = line.strip('\n').strip()
            if line:
                data = line.split('\t')
                if len(data) != 7:
                    error_line.append(line)
                    continue
                # email, password, name, gid, account, phone, birth = line.split('\t')
                email, password, name, gid, account, phone, birth = data
                person_dict[email] = {'password': password,
                                    'name': name,
                                    'gid': gid,
                                    'account': account,
                                    'phone': phone,
                                    'birth': birth}
    print ('error line:', len(error_line))
    for item in error_line:
        print (item)
    with open(json_path, 'w') as json_file:
        json.dump(person_dict, json_file, indent=4)
