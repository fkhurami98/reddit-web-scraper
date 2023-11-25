import os
import requests
import subprocess
import sys
from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright
from utils.constants import  DATABASE_URLS
from pprint import pprint


def get_ip_addresses() -> dict:
    """
    Get Tailscale and public facing IP addresses.
    """
    # Get Tailscale IPv4 address
    try:
        tailscale_ips = subprocess.check_output(['tailscale', 'ip']).decode('utf-8').strip().split('\n')
        tailscale_ipv4 = next((ip for ip in tailscale_ips if '.' in ip), 'Unable to fetch Tailscale IPv4')
    except Exception as e:
        tailscale_ipv4 = f'Unable to fetch Tailscale IPv4 due to: {str(e)}'

    # Get public facing IP address
    try:
        public_ip = requests.get('https://httpbin.org/ip').json()['origin']
    except Exception as e:
        public_ip = f'Unable to fetch public IP due to: {str(e)}'

    return {
        "public_ipv4": public_ip,
        "tailscale_ipv4": tailscale_ipv4
    }


def get_save_path(caller_file: str) -> str:
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


def get_random_user_agent() -> str:
    """
    Gets a random user agent from the fake_useragent library.

    Returns:
       str: A random user agent string.
    """
    ua = UserAgent().random
    return ua


def check_browser_installation() -> None:
    """
    Verifies if the Chromium executable for Playwright is installed.
    On failure due to missing executable, exits the program with a status code of 1.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
    except Exception as e:
        if "Executable doesn't exist" in str(e):
            print("Browser/executable for Playwright not installed. Exiting program...")
            sys.exit(1)


def determine_access_path(current_ip: str) -> str:
    """
    Determine the appropriate database access path (URL) based on the given IP address.

    Args:
        current_ip (str): The current machine's IP address.

    Returns:
        str: The appropriate database URL for the given IP.
    """
    
    DATABASE_URL_VPN = "postgresql://postgres:password@100.68.124.90:5432/reddit_scraper_1"
    DATABASE_URL_HOME = "postgresql://postgres:password@192.168.1.129:5432/reddit_scraper_1"
    
    # This dictionary maps known IP addresses to their corresponding database URLs.
    IP_DATABASE_MAPPING = {
        '100.68.124.90': DATABASE_URL_VPN, 
        '192.168.1.129': DATABASE_URL_HOME
    }
    
    return IP_DATABASE_MAPPING.get(current_ip, DATABASE_URL_HOME)

def setup_data_folder(folder_path: str) -> None:
    """
    Ensures the existence of a directory at a given path.
    If the directory doesn't exist, it creates it.
    
    Args:
        folder_path (str): Path to the directory.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


if __name__ == "__main__":
    pprint(get_ip_addresses())
