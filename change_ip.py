import socket
import os

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def update_config_host(config_path, new_host):
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"The configuration file {config_path} does not exist.")

    with open(config_path, 'r') as file:
        lines = file.readlines()

    with open(config_path, 'w') as file:
        for line in lines:
            stripped_line = line.strip()
            # Skip empty lines and comments
            if stripped_line.startswith('#') or stripped_line.startswith(';') or not stripped_line:
                file.write(line)
                continue

            # Check if the line contains the 'host' key
            if '=' in line:
                key, value = line.split('=', 1)
                if key.strip().lower() == 'host':
                    # Replace the value while preserving any inline comments
                    if '#' in value:
                        value_part, comment = value.split('#', 1)
                        new_line = f"{key.strip()} = {new_host}  # {comment}"
                    elif ';' in value:
                        value_part, comment = value.split(';', 1)
                        new_line = f"{key.strip()} = {new_host}  ; {comment}"
                    else:
                        new_line = f"{key.strip()} = {new_host}\n"
                    file.write(new_line)
                    continue

            # Write the original line if no changes are made
            file.write(line)
import time 
def main():
    # Define the path to your config.ini file
    config_file = os.path.join('config', 'config.ini')  # Update this path if necessary

    # Get the local IP address dynamically
    new_ip = get_local_ip()

    try:
        update_config_host(config_file, new_ip)
        time.sleep(3)
        print(f"Host IP address dynamically updated to: {new_ip}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
