digit_lst = '0123456789'
letter_lst = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def check_class(char):
    if char in digit_lst:
        return 'D'
    elif char in letter_lst:
        return 'L'
    else:
        return 'S'
def kw_ls_check(new_kw_ls):
    for kw in new_kw_ls:
        ref_class = check_class(kw[0])
        for char in kw:
            if check_class(char) != ref_class:
                return False, kw 
    return True, None            


def find_class_fill(kw):
    ref_class = check_class(kw[0])
    return ref_class + str(len(kw))



def main(new_kw_ls, train_fill_mask, target_fill_mask):
    t = {}
    for new_kw in new_kw_ls:
        c = find_class_fill(new_kw)
        if c not in t:
            t[c] = []
        t[c].append(new_kw)

    res = []
    used_mask = []
    with open (train_fill_mask, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            class_fill, fill_data, prob = line.split('\t')
            if class_fill not in used_mask:
                if class_fill in t:
                    used_mask.append(class_fill)
                    for kw in t[class_fill]:
                        res.append(f'{class_fill}\t{kw}\t1.0\n')
            res.append(line)
            res.append('\n')

    with open (target_fill_mask, 'w') as f:    
        for line in res:
            f.write(line)

