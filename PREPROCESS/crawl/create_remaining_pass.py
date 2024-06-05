def split_line(different_set):
    """
    Splits a set of passwords into groups and writes them to an output file.

    Args:
        different_set (set): A set of passwords to be written to the output file.

    This function writes the passwords from the set to the specified output file in groups of size `group_size`.
    """
    pass_list = list(different_set)

    with open(output_file_path, 'w') as f:
        num_lines = len(pass_list)
        for i in range(0, num_lines, group_size):
            # Extract passwords as a list and filter out None values
            passwords = pass_list[i:i+group_size]
            # Write passwords to the file
            for item in passwords:
                f.write(item)
            f.write('\n')

def remove_None(sample_list):
    """
    Removes None values from a list.

    Args:
        sample_list (list): A list potentially containing None values.

    Returns:
        list: A new list with None values removed.
    """
    filtered_list = [element for element in sample_list if element is not None]
    return filtered_list

def filter_and_split(big_file_path, small_file_path, output_file_path):
    """
    Filters out passwords from a big file that are present in a small file and splits the remaining passwords.

    Args:
        big_file_path (str): Path to the big file containing all passwords.
        small_file_path (str): Path to the small file containing already processed passwords.
        output_file_path (str): Path to the output file where remaining passwords will be written.

    This function reads passwords from the big file and small file, filters out the passwords from the big file that
    are present in the small file, and writes the remaining passwords to the output file in groups.
    """
    from time import sleep
    try:
        with open(big_file_path, 'r') as big_file:
            big_set = set(remove_None(big_file.readlines()))
            print ('original unique element: ' , len(big_set))
        with open(small_file_path, 'r') as small_file:
            small_list = remove_None([str(line.split(':')[0] + '\n') for line in small_file.readlines()])
            print ('crack messy all element:',len(small_list))
            small_set = set(small_list)
            print ('crack unique element',len(small_set))
        difference = big_set.difference(small_set)
        print ('remaining unique element to crack:', len(difference))
        split_line(difference)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Example usage:
big_file_path = 'DONE_PASS/ORIGINAL_PASS.txt'
small_file_path = 'DONE_PASS/first_crack.txt'
output_file_path = 'REMAINING_PASS.txt'
group_size = 25

filter_and_split(big_file_path, small_file_path, output_file_path)
