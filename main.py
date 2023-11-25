"""

This branch needs alot of the plumbing stripped out to accomodate the HTML/CSS structure of old.reddit.com
Might be worth rewriting the whole lot.

"""









# import os
# import sys
# from db_handler.db import insert_to_db
# from utils.constants import URL_LIST
# from utils.functions import (
#     get_save_path,
#     get_ip_addresses,
#     setup_data_folder,
#     determine_access_path,
# )
# from scraping_helpers.fetch_post_details import process_all_json_files_in_folder
# from scraping_helpers.fetch_subreddit_metadata import (
#     scrape_multiple_subreddits_concurrently,
#     clear_json_files_in_folder,
# )


# if __name__ == "__main__":
#     JSON_SAVE_PATH = get_save_path(__file__)

#     #--------------------------------------------------------------
#     # current_tailscale_ip = get_ip_addresses()["tailscale_ipv4"]
#     # print(current_tailscale_ip)

#     # # Determine the database URL based on the machine's IP
#     # database_url = determine_access_path(current_tailscale_ip)

#     # print(database_url)
#     #--------------------------------------------------------------

#     # Creates /json_data_folder folder if not exists
#     setup_data_folder("json_data_folder")

#     # Clean up JSON files before initiating scraping
#     clear_json_files_in_folder(folder_path=JSON_SAVE_PATH)

#     # Scrapes a Reddit URL, extracts post information, and saves the results to a JSON file.
#     scrape_multiple_subreddits_concurrently(url_list=URL_LIST)

#     # Processes all JSON files in /json_data_folder
#     process_all_json_files_in_folder(folder_path=JSON_SAVE_PATH)

#     # # Reads JSON files from /json_data_folder and sends to db
#     # insert_to_db(
#     #     database_url="postgresql://postgres:password@localhost:5432/reddit_scraper_1",
#     #     json_folder_path=JSON_SAVE_PATH,
#     # )
