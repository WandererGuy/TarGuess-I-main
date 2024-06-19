'''
for 1 character there is 10 digits + 26 lower case + 26 uppercase + 32 special char = 94 possibilities

so a 8 character password have 94^8 = 6.1 * 10^15 possibilities , with advance computer takes about 2.6 days 

for 9 character password, however takes more than 9 years
https://www.password-depot.de/en/know-how/brute-force-attacks.htm#:~:text=Combination%20and%20length%20of%20the%20password&text=When%20creating%20a%20password%2C%20the,Special%20characters%20(32%20different).
'''

possi_dict = {'L': 52, 'D': 10, 'S': 32 }

def collect_mask(text):
    tmp = []
    for i in range(len(text)):
        char = text[i]
        if char in possi_dict.keys():
            tmp.append(char)
    return tmp 
def estimate(tmp):
    possi = 1 
    for item in tmp:
        possi *= possi_dict[item]
    return possi

def cal_trials(text):
    tmp = collect_mask(text)
    possi = estimate(tmp)
    return possi``