
import os 
import requests
test_ls = ['xak', 'xal', 'xam', 'xan']
with open('test.txt', 'w', encoding = 'utf-8') as f:
    url = "http://192.168.1.2:4003/preprocess-train-dataset/"
    for filename in os.listdir('processed_csv'):
        # if 'xai' in filename or 'xan' in filename:
            print ('-------------------------------')
            print (filename)
            path = os.path.join('processed_csv', filename)
            # for item in test_ls:
                # if item in filename:
            payload = {
            'dataset_path': f'C:\\Users\\Admin\\CODE\\work\\PASSWORD_CRACK\\TarGuess-I-main\\processed_csv\\{filename}',
            'hash_dict_path': 'C:\\Users\\Admin\\CODE\\work\\PASSWORD_CRACK\\cracking_server_v1.0\\wordlist_samples\\potfile_tailieuvn_zing.txt'}
            files=[

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            data = response.json()
            f.write(path)
            f.write('\n')
            f.write(str(data))
            f.write('\n')
            f.write('\n')