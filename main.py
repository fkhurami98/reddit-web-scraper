from scraping_helpers.fetch_post_info import process_all_json_files
from scraping_helpers.fetch_subreddit_info import fetch_subreddits
from db_handler.db import insert_to_db
from utils.constants import URL_LIST, DATABASE_URL
import os


if __name__ == "__main__":
    if not os.path.exists('subreddit_page_data'):
        os.makedirs('subreddit_page_data')
    
    # PATH = "/home/farhadkhurami/reddit-web-scraper/subreddit_page_data"
    
    # fetch_subreddits(url_list=URL_LIST)

    # process_all_json_files(folder_path=PATH)

    # insert_to_db(database_url=DATABASE_URL, json_folder_path=PATH)

