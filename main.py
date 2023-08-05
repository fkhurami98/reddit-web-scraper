from scraping_scripts.scrape_subreddit import scrape_subreddits
from scraping_scripts.scrape_post_info import scrape_post_info
from database.db import insert_to_db

if __name__ == "__main__":
    SUBREDDIT_URL_LIST = [
        "https://www.reddit.com/r/Jokes/",
        "https://www.reddit.com/r/explainlikeimfive/",
        "https://www.reddit.com/r/LifeProTips/",
        "https://www.reddit.com/r/TrueOffMyChest/"
    ]
    scrape_subreddits(url_list=SUBREDDIT_URL_LIST)

    scrape_post_info()

    insert_to_db(
        database_url="postgresql://postgres:password@localhost:5432/reddit_scraper_1",
        json_folder_path="subreddit_page_data",
    )

# Need to handle private communities