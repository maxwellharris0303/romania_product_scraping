import os

def get_file_names(directory):
    file_names = []
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            file_names.append(file_name)
    return file_names

# # Specify the directory path
# directory_path = 'assets'

# # Get the file names in the directory
# files = get_file_names(directory_path)

# print(files)