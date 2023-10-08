import os
from fake_useragent import UserAgent


def get_save_path(caller_file):
    """
    Get the save path for a directory named 'json_data_folder' relative to the directory of the caller's file.

    Args:
        caller_file (str): The path of the file that is calling this function.

    Returns:
        str: The relative save path to 'json_data_folder'.
    """
    current_directory = os.path.dirname(os.path.abspath(caller_file))
    save_path = os.path.join(current_directory, "json_data_folder")
    return save_path


def get_random_user_agent():
    """
    Gets a random user agent from the fake_useragent library.

    Returns:
       ua (str): A random user agent string.
    """
    ua = UserAgent().random
    return ua
