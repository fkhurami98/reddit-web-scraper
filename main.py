from scripts.scrape_subreddit import scrape_subreddits
from scripts.scrape_post_info import scrape_post_info

if __name__ == "__main__":
    """
    If i run the code of the two functions below in one file,
    post content is not written to the json file properly.
    """
    scrape_subreddits()
    scrape_post_info()