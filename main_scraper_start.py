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

Usage:
Run the script directly to initiate the scraping process: `python3 main_reddit_scraper.py`
"""

import os
from fake_useragent import UserAgent
from db_handler.db import insert_to_db
from utils.constants import URL_LIST, DATABASE_URL_HOME, DATABASE_URL_VPN
from utils.functions import get_save_path
from scraping_helpers.fetch_post_details import process_all_json_files_in_folder
from scraping_helpers.fetch_subreddit_metadata import (
    scrape_multiple_subreddits_concurrently,
    clear_json_files_in_folder,
)


if __name__ == "__main__":
    JSON_SAVE_PATH = get_save_path(__file__)

    # Creates /json_data_folder folder if not exists
    if not os.path.exists("json_data_folder"):
        os.makedirs("json_data_folder")

    # Clean up JSON files before initiating scraping
    clear_json_files_in_folder(folder_path=JSON_SAVE_PATH)

    # Scrapes a Reddit URL, extracts post information, and saves the results to a JSON file.
    scrape_multiple_subreddits_concurrently(url_list=URL_LIST)

    # Processes all JSON files in /json_data_folder
    process_all_json_files_in_folder(folder_path=JSON_SAVE_PATH)

    # Reads JSON files from /json_data_folder and sends to db
    insert_to_db(database_url=DATABASE_URL_HOME, json_folder_path=JSON_SAVE_PATH)
