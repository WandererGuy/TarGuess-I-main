import gradio as gr
import subprocess
from dateutil import parser
import os 
import time 

# Function to handle the file download
# input_file = 'mask.hcmask'  # Replace with your actual input file path
output_file = 'generated_target_masklist/mask.hcmask'  # Replace with your desired output file path

# def format_text_file(input_filepath, output_filepath):
#     # Read lines from the input file
#     with open(input_filepath, 'r') as file:
#         lines = file.readlines()

#     # Determine the maximum length of the password for formatting
#     max_length = max(len(line.split('\t')[0]) for line in lines if line.strip())

#     # Prepare to write formatted text to the output file
#     with open(output_filepath, 'w') as file:
#         # Writing header and separator
#         file.write(f"{'Password':<{max_length}} Probability\n")
#         file.write('-' * (max_length + 12) + '\n')
        
#         # Formatting each line and writing to the file
#         for line in lines:
#             if line.strip():
#                 password, probability = line.split('\t')
#                 file.write(f"{password:<{max_length}} {probability}\n")


def download_file(output_file):
    # Provide the path to your file
    file_path = output_file
    # print ('**********', input_file)
    print ('**********', output_file)
    # format_text_file(input_file, output_file)

    
    # Make sure the file exists to avoid errors
    if os.path.exists(file_path):
        return file_path
    else:
        return 'Fail generate'
    
def process_birthday(birthday):
    try:
        # Attempt to parse the birthday in various formats
        parsed_date = parser.parse(birthday)
        # Convert to a standard format e.g., YYYY-MM-DD
        formatted_date = parsed_date.strftime("%Y%m%d")
        return formatted_date
    except ValueError:
        return "Invalid date. Please enter a valid date (e.g., DD-MM-YYYY)."
import unidecode

def main(name='', birth='', email='', accountName='', id='', phone=''):
    # Initializes an empty string for the full name
    print ('Receiving inputs')
    fullName = ''
    password = ''
    # Splits the name into a list and rearranges to last name first
    if name != '':
        name = name.lower()
        name = unidecode.unidecode(name)

        my_list = name.split(' ')
        my_list = [my_list[-1]] + my_list[:-1]
        # Joins elements with '|' and avoids extra '|' at the end
        for index, item in enumerate(my_list):
            if index == len(my_list) - 1:
                fullName += item
                break
            fullName += item
            fullName += ' '
    print (birth)
    print (fullName)
    birth = process_birthday(birth)
    if birth == "Invalid date. Please enter a valid date (e.g., DD-MM-YYYY).":
        return birth
    print ('write input to files')
    with open ("GUESS/src/result_folder/test.txt", "w") as f:
        f.write(email + '\\t' + password + '\\t' + fullName + '\\t' + id + '\\t' + accountName + '\\t' + phone + '\\t' + birth)
    
    current_directory = os.getcwd()
# Print the current working directory
    print("Current Working Directory:", current_directory)

    python_file = "automate_cracking.py"
# eragonkisyrong96@gmail.com	buiduymanh1996	manh		wantedbyzeus	01647732700	14-3-1995

    # Run the batch file
    print ('running batch file to generate guesses')
    result = subprocess.run(['python', python_file], capture_output=True, text=True)
    print("Output:", result.stdout)
    if result.stderr != None and result.stderr != '':
        print("Errors:", result.stderr)   
    # with open ("GUESS/src/result_folder/output.txt", "r") as f_output:
    # output = f_output.read()
    # print (output)
    output = download_file(output_file)
    return output 


# Example usage:
demo = gr.Interface(
    fn=main,

    inputs=[
        gr.Textbox(label="WELCOME TO PASS GUESSING MODEL, please enter person's information to guess password. Full Name", placeholder="Duong Van Phu"),
        gr.Textbox(label="Enter your birth date in DD-MM-YYYY format. Date of Birth", placeholder="DD-MM-YYYY"),
        gr.Textbox(label="Email", placeholder="example@email.com"),
        gr.Textbox(label="Account Name", placeholder="YourAccountName123"),
        gr.Textbox(label="Citizen ID", placeholder="1234567890"),
        gr.Textbox(label="Phone Number", placeholder="+1234567890")
    ],
    # outputs="text"
    outputs=gr.File(label="Download Output File"),
    title="File Download Example",
    description="Click the button below to download the output file."

)

demo.launch(share=True)
# name = 'duong van phu'
# birth = '19591004'
# email = 'phuduong37@gmail.com'
# accountName = 'phudv123'
# id = ''
# phone = '0904172428'

# print (output = main(name, birth, email, accountName, id, phone))