'''
template 
,id,username,password,email,firstname,lastname,birthday,gender,address,tel
0,,rinocococ,e10adc3949ba59abbe56e057f20f883e,vtailieu@gmail.com,Minh Trâm,Từ,19-1-1985,1.0,"56 vancao, phuong tan loi, tp.bmt , tinh daklak",0973276483
1,,lamfriends2000,c640856549e3cf8dfd35274ad9e62736,lamfriends2000@yahoo.com,Lam,Thai Xuan,,1.0,,
2,,hanguyen,a667f8ec02cb7d3f205a36658367169e,congha76@yahoo.com,Ha,Nguyen,,0.0,,
3,,ngocanhcdtk5,e2f5bbdb11e0089051185fe540227f85,ngocanhcdtk5@gmail.com,Anh,Nguyen Ngoc,,0.0,,
4,,manh_sanh_co_don,e2f5bbdb11e0089051185fe540227f85,ngocanha3@gmail.com,Anh,Nguyen Ngoc,,0.0,,
5,,manh_sanh_co_don_cdt,e2f5bbdb11e0089051185fe540227f85,ngocanh_hy87@yahoo.com,Anh,Nguyen Ngoc,,0.0,,
6,,nonameteam,d48b279000cc65c062cb1e1d4a979ba3,nnt@gmail.com,Noname,Team,,0.0,,
7,,myphuong,e71c617b3b17ecc166a6a5a8eccf0302,cdspthk1142@qtttc.edu.vn,Mỹ Phương,Nguyễn Thị,,0.0,,
8,,phuong_my,e71c617b3b17ecc166a6a5a8eccf0302,giotlesau_872000@yahoo.com,Mỹ Phương,Nguyễn Thị,,0.0,,
9,,dangquangtai,11c0e20f98e63cc8049a7c6168f1f483,haiauvocanh_goikevodanh2005@yahoo.com,Tai,Dang Quang,,0.0,,
10,,daiquangtang,11c0e20f98e63cc8049a7c6168f1f483,haiauvocanh_goikevodanh2005@gmail.com,Tang,Dai Quang,,0.0,,
11,,nhatchinh,de03ebd7140cd135176bbc0ddae1f30e,nhatchinhbc@hotmail.com,Chinh,Luong Nguyen Nhat,,0.0,,
12,,vnguyen,6f918ecea9faca2b62a17b2ec4eff8f9,pickajob@gmail.com,Vu,Nguyen,,0.0,,
'''
import pandas as pd
import os 
from routers.model import MyHTTPException
report_str = r"""
where:
    first_name: First name (e.g., Nam)
    last_name: Last name and middle name (e.g., Nguyen Hoai)
    birthday: Birthday in this form (e.g., 19-1-1985)
    username: Username used on a website (e.g., manhsuperman99)
    password: plaintext or hash password , if hash password with plaintext value is in hash_dict_path (e.g. e10adc3949ba59abbe56e057f20f883e)
    id: Unique identifier starting from 1 and incrementing
    email: Email address (e.g., manh30k@gmail.com)
"""

necessary_columns = ['id', 'username', 'password', 'email', 'firstname', 'lastname', 'birthday', 'tel']
no_necessary_columns = ['gender', 'address'] # still include to match template but left blank all 
# turn all dataset to be this form 

def check_password_type(pass_ls):
    print ('check password type')
    # print (pass_ls)
    # print (type(pass_ls))
    print ('first password to check as the standard quality hash to compare others  ', pass_ls[0])
    len_pass = len(pass_ls[0])
    thres_error = len(pass_ls)*0.1
    error_password = 0
    error_dict = {}
    for i,item in enumerate(pass_ls):
        if item == '' or item == None or item.lower() == 'nan':
            continue
        else:
            if len(item) != len_pass:
                error_password += 1
                # password at index 0 is row 2 in excel , or index excel 1
                # so to remove password at index 0 , we must drop row excel index 1 
                error_dict[i+1] = item
        if error_password > thres_error:
                print ('detect password as plaintext because')
                print ('all password if hash must have same length')
                print (r'threshold error allow is 10% of all password')
                print ('while first item has length of ', len_pass)
                return 'plaintext'
    print ('dict of error password at index to be remove')
    # print (error_dict)
    return 'hash', error_dict


def check_valid_and_refine(filepath):
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    else:
        message = f"Unsupported file format: {filepath}. \
                         Support filepath for training \
                        dataset is .csv or .xlsx"
        raise MyHTTPException(status_code=400,
                              message = message
        )

    for item in necessary_columns:
        if item not in df.columns:
            message = f"Column \'{item}\' not found in the dataset. Table must have columns for training dataset are {necessary_columns}.\
                {report_str}"
            raise MyHTTPException(status_code=400,
                                message = message)

    # drop error passwords
    password_type, error_dict = check_password_type(df["password"].to_list())
    print ('detect password as ', password_type)
    # password at index 0 is row 2 in excel , or index excel 1
    # so to remove password at index 0 , we must drop row excel index 1 
    drop_rows = list(error_dict.keys())
    index_row_to_drop = df.index[drop_rows]
    df = df.drop(index_row_to_drop)
    new_df = df[necessary_columns]
    new_df = new_df.dropna(subset=['password'])
    for item in no_necessary_columns:
        new_df[item] = ''
    new_df = new_df.fillna('')
    raw_path = os.path.join('TRAIN','src','tailieuvn_data','raw.csv')
    new_df.to_csv(raw_path, sep = ',', index=False)
    return raw_path, password_type
