import csv

def read_first_n_lines(file_path, n, output_file):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        lines = []
        for i, row in enumerate(reader):
            if i >= n:
                break
            lines.append(row)

    with open(output_file, mode='w', encoding='utf-8') as out_file:
        for line in lines:
            out_file.write(','.join(line) + '\n')

# Example usage:
file_path = '28M_zing.csv'
output_file = 'read_output.txt'
num_lines = 50  # You can change this to any number of lines you want to read
read_first_n_lines(file_path, num_lines, output_file)

print(f"The first {num_lines} lines have been written to {output_file}")
