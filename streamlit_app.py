import streamlit as st

# Title
st.title("Welcome to PassGuess Model !!!")
st.title("Generating WORDLIST for Target API !!!")

st.write("Please enter your target's information below:")

import requests
import configparser
import os 
# can only achieve max mask if all information is provided 
config = configparser.ConfigParser()
config.read(os.path.join('config','config.ini'))
host_ip = config['DEFAULT']['host'] 
TARGUESS_PORT_NUM = int(config['DEFAULT']['port'])
TARGUESS_URL_WORDLIST = f"http://{host_ip}:{TARGUESS_PORT_NUM}/generate-target-wordlist/"

def targuess_generate_wordlist_for_app(targuess_train_result_refined_path, 
                      targuess_url, 
                      target_info: dict, 
                      max_mask_generate: int):
    '''
    return 
        {
    "status_code": 200,
    "message": "Result saved successfully",
    "result": {
        "path": "C:/Users/Admin/CODE/work/PASSWORD_CRACK/TarGuess-I-main/static/generated_target_wordlist/1da75da8-fc05-4aa8-8424-486ba44182b0.txt",
        "url": "http://192.168.1.5:4003/static/generated_target_wordlist/1da75da8-fc05-4aa8-8424-486ba44182b0.txt"
    }
}
    '''
    payload = {
    'full_name': target_info['full_name'],
    'birth': target_info['birth'], 
    'email': target_info['email'],
    'account_name': target_info['account_name'],
    'id_num': target_info['id_num'],
    'phone': target_info['phone'],
    'max_mask_generate': max_mask_generate,
    'train_result_refined_path': targuess_train_result_refined_path,
    'other_keywords': target_info['other_keywords']}
    files=[
    ]
    headers = {}
    response = requests.request("POST", targuess_url, headers=headers, data=payload, files=files)
    return response


def process_data(data):
        final_data = {}
        target_info = {
            "full_name": data["full_name"],
            "birth": data["birth"],
            "email": data["email"],
            "account_name": data["account_name"],
            "id_num": data["id_num"],
            "phone": data["phone"],
            "other_keywords": data["other_keywords"]
        }

        if data["max_mask_generate"] == '' or data["max_mask_generate"] == None :
            max_mask_generate = 5000 
        else:
            max_mask_generate = int(max_mask_generate)
        final_data["target_info"] = target_info
        final_data["max_mask_generate"] = max_mask_generate
        final_data["train_result_refined_path"] = data["train_result_refined_path"]
        return final_data


def send_to_api(data):
        targuess_url = TARGUESS_URL_WORDLIST
        final_res = targuess_generate_wordlist_for_app(
                                targuess_train_result_refined_path = data["train_result_refined_path"],
                                targuess_url = targuess_url, 
                                target_info = data["target_info"], 
                                max_mask_generate = data["max_mask_generate"])
        
        return final_res

def create_data_form():
        # Create a form for input
        with st.form("target_info_form"):
            full_name = st.text_input("Full Name", placeholder="Enter full name")
            birth = st.text_input("Birth Date", placeholder="DD-MM-YYYY or your format")
            email = st.text_input("Email", placeholder="Enter email address")
            account_name = st.text_input("Account Name", placeholder="Enter account name")
            id_num = st.text_input("ID Number", placeholder="Enter ID number")
            phone = st.text_input("Phone", placeholder="Enter phone number")
            
            # You can use number_input if you expect an integer value for max_mask_generate.
            # Here, we use text_input to keep consistency with other fields.
            max_mask_generate = st.text_input("Max Mask Generate", placeholder="Enter maximum mask generate value. Default is 5000")
            
            train_result_refined_path = st.text_input("Train Result Refined Path", placeholder="Enter name of refined train result folder")
            other_keywords = st.text_input("Other Keywords", placeholder="Enter additional keywords (optional). Seperate each keyword by comma")
            
            # Submit button for the form
            submitted = st.form_submit_button("Submit")

        # Process the form submission
        if submitted:
            st.success("Information Submitted Successfully!")
            # Display the entered information
            st.write("### Submitted Information:")
            st.write(f"**Full Name:** {full_name}")
            st.write(f"**Birth Date:** {birth}")
            st.write(f"**Email:** {email}")
            st.write(f"**Account Name:** {account_name}")
            st.write(f"**ID Number:** {id_num}")
            st.write(f"**Phone:** {phone}")
            st.write(f"**Max Mask Generate:** {max_mask_generate}")
            st.write(f"**Train Result Refined Path:** {train_result_refined_path}")
            st.write(f"**Other Keywords:** {other_keywords}")


        data = {
            "full_name": full_name,
            "birth": birth,
            "email": email,
            "account_name": account_name,
            "id_num": id_num,
            "phone": phone,
            "max_mask_generate": max_mask_generate,
            "train_result_refined_path": train_result_refined_path,
            "other_keywords": other_keywords
        }

        return data
def main(): 
        data = create_data_form()
        final_data = process_data(data)
        final_res = send_to_api(final_data)
        if str(final_res.json()['status_code']) == '200':
            st.write("### Model Output:")
            st.write(final_res.json())

        else:
            st.write("### An Error have occured while validating input:")
            st.write(final_res.json())
            st.write("Please try again.")

if __name__ == "__main__":
    main()