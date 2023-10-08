import os
from db_handler.db import insert_to_db
from utils.constants import URL_LIST, DATABASE_URL
from utils.functions import CurrentPath
from scraping_helpers.fetch_post_info import process_all_json_files
from scraping_helpers.fetch_subreddit_info import fetch_reddit_with_threads, delete_json_files


if __name__ == "__main__":
    JSON_SAVE_PATH = CurrentPath(__file__).get_save_path()

    # Creates /json_data_folder folder if not exists
    if not os.path.exists("json_data_folder"):
        os.makedirs("json_data_folder")

    # Clean up JSON files before initiating scraping
    delete_json_files(folder_path=JSON_SAVE_PATH)

    # Scrapes a Reddit URL, extracts post information, and saves the results to a JSON file.
    fetch_reddit_with_threads(url_list=URL_LIST)

    # Processes all JSON files in /json_data_folder
    process_all_json_files(folder_path=JSON_SAVE_PATH)

    # Reads JSON files from /json_data_folder and sends to db
    insert_to_db(database_url=DATABASE_URL, json_folder_path=JSON_SAVE_PATH)
