import requests

with open('test.txt', 'w', encoding = 'utf-8') as f:
    url = "http://192.168.1.4:4003/preprocess-train-dataset/"
    for number in ['0']:
        t = f'C:\\Users\\Admin\\CODE\\work\\PASSWORD_CRACK\\TarGuess-I-main\\PREPROCESS\\{number}.csv'
        payload = {'dataset_path': t,
        'hash_dict_path': 'C:\\Users\\Admin\\CODE\\work\\PASSWORD_CRACK\\cracking_server_v1.0\\wordlist_samples\\potfile_tailieuvn_zing.txt'}
        files=[

        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        data = response.json()
        f.write(str(data))
        f.write('\n')
