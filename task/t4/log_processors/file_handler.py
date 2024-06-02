import os

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_log_files(log_directory):
    log_files = []
    for root, _, files in os.walk(log_directory):
        for file in files:
            if file.endswith(".log"):
                log_files.append(os.path.join(root, file))
    return log_files

def read_log_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_log_file(file_path, log_entries):
    with open(file_path, 'w') as file:
        for entry in log_entries:
            file.write(entry + "\n")
