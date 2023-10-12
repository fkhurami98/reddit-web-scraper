import os
import requests
import sys
from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright


def get_save_path(caller_file) -> str:
    """
    Get the save path for a directory named 'json_data_folder' relative to the directory of the caller's file.

    Args:
        caller_file (str): The path of the file that is calling this function.

    Returns:
        save_path (str): The relative save path to 'json_data_folder'.
    """
    current_directory = os.path.dirname(os.path.abspath(caller_file))
    save_path = os.path.join(current_directory, "json_data_folder")
    return save_path


def get_random_user_agent() -> str:
    """
    Gets a random user agent from the fake_useragent library.

    Returns:
       ua (str): A random user agent string.
    """
    ua = UserAgent().random
    return ua


def get_request_details():
    """
    Fetches the current IP address and headers used by the scraper.
    """
    try:
        response = requests.get("https://httpbin.org/get")
        details = {
            "origin": response.json().get("origin"),
            "headers": response.json().get("headers"),
        }
        return details
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None

def check_browser_installation():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
    except Exception as e:
        if "Executable doesn't exist" in str(e):
            print("Browser/executable for Playwright not installed. Exiting program...")
            sys.exit(1)


def queue_worker(url):
    """
    Read from a list of urls and put into a queue. Will be run with multi-threads, to ensure thread safety.

    Args:

    """
    pass


if __name__ == "__main__":
    pass
