"""
main_reddit_scraper.py

This script orchestrates the end-to-end process of scraping metadata and details of posts from Reddit subreddits.
Steps included are:
- Set up and prepare the directory for saving scraped data.
- Clear pre-existing data to avoid redundancy.
- Invoke scraping for multiple subreddit URLs to fetch post metadata.
- Further process the scraped metadata to fetch detailed post content.
- Transfer the final aggregated data into a designated database.

Dependencies:
- db_handler: Contains methods for interacting with the database.
- utils: Consists of utility functions and constants used in scraping and data processing.
- scraping_helpers: Provides specific methods for scraping Reddit and processing data.
- distributed_helpers: (WIP) Provides functionality to run scrapers on distributed nodes.
Usage:
Run the script directly to initiate the scraping process: `python3 main_reddit_scraper.py`
"""

import os
import sys
from db_handler.db import insert_to_db
from utils.constants import URL_LIST
from utils.functions import get_save_path,  get_ip_addresses, setup_data_folder, determine_access_path
from scraping_helpers.fetch_post_details import process_all_json_files_in_folder
from scraping_helpers.fetch_subreddit_metadata import (
    scrape_multiple_subreddits_concurrently,
    clear_json_files_in_folder,
)


if __name__ == "__main__":
    JSON_SAVE_PATH = get_save_path(__file__)
    
    current_tailscale_ip = get_ip_addresses()["tailscale_ipv4"]
    print(current_tailscale_ip)
    
    # Determine the database URL based on the machine's IP
    database_url = determine_access_path(current_tailscale_ip)

    print(database_url)
    # Creates /json_data_folder folder if not exists
    setup_data_folder('json_data_folder')

    # Clean up JSON files before initiating scraping
    clear_json_files_in_folder(folder_path=JSON_SAVE_PATH)

    # Scrapes a Reddit URL, extracts post information, and saves the results to a JSON file.
    scrape_multiple_subreddits_concurrently(url_list=URL_LIST)

    # Processes all JSON files in /json_data_folder
    process_all_json_files_in_folder(folder_path=JSON_SAVE_PATH)

    # Reads JSON files from /json_data_folder and sends to db
    insert_to_db(database_url="postgresql://postgres:password@localhost:5432/reddit_scraper_1", json_folder_path=JSON_SAVE_PATH)
