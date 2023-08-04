from scripts.scrape_subreddit import scrape_subreddits
from scripts.scrape_post_info import scrape_post_info
import time

if __name__ == "__main__":
    """
    If i run the code of the two functions below in one file,
    post content is not written to the json file properly.

    - Post content only supports text. Support for URLs and Images needed.
    - Date time needs to be added to the json
    """
    scrape_subreddits()
    time.sleep(1)
    scrape_post_info()