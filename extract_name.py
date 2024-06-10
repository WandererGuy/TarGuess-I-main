import pandas as pd

# Replace 'yourfile.csv' with the path to your CSV file
file_path = 'TRAIN/src/tailieuvn_data/final.csv'
df = pd.read_csv(file_path)

# Print the column names
print(df.columns.tolist())

name_list = df['Name'].tolist()
name_list = list(set(name_list))

# Write the list to a text file
with open('train_names.txt', 'w') as file:
    for name in name_list:
        file.write(f"{name}\n")
