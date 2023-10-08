import os


def get_save_path(caller_file):
    current_directory = os.path.dirname(os.path.abspath(caller_file))
    save_path = os.path.join(current_directory, "json_data_folder")
    return save_path
