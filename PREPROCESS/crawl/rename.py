import os
folder_path = './capcha_img'
for filename in os.listdir(folder_path):
    new_filename = filename.replace('_','_.')
    os.rename (os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))