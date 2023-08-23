from scraping_scripts.scrape_subreddit import scrape_subreddits
from scraping_scripts.scrape_post_info import scrape_post_info
from database.db import insert_to_db
import os


if __name__ == "__main__":
    scrape_subreddits(
        url_list=[
            "https://www.reddit.com/r/Jokes/",
            "https://www.reddit.com/r/explainlikeimfive/",
            "https://www.reddit.com/r/LifeProTips/",
            "https://www.reddit.com/r/TrueOffMyChest/",
            "https://www.reddit.com/r/talesfromtechsupport/",
            "https://www.reddit.com/r/AskUK/",
            "https://www.reddit.com/r/tifu/",
            "https://www.reddit.com/r/tifu/",
            "https://www.reddit.com/r/AmItheAsshole/",
            "https://www.reddit.com/r/legaladvice/",
            "https://www.reddit.com/r/whowouldwin/",
            "https://www.reddit.com/r/AskReddit/",
            "https://www.reddit.com/r/HFY/",
            "https://www.reddit.com/r/AskHistorians/",
            "https://www.reddit.com/r/talesfromretail/",
            "https://www.reddit.com/r/talesfromtechsupport/",
            "https://www.reddit.com/r/wouldyourather/"
        ]
    )

    scrape_post_info(folder_path="subreddit_page_data")

    insert_to_db(
        database_url="postgresql://postgres:password@localhost:5432/reddit_scraper_1",
        json_folder_path="subreddit_page_data",
    )

# Need to handle private communities
