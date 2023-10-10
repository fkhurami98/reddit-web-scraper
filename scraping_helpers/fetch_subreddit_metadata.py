"""
fetch_subreddit_metadata.py

This script focuses on scraping metadata of posts from Reddit's subreddit landing pages.
The key functionalities are:
- Scrape the HTML content of a subreddit page using a headless browser.
- Parse the HTML to extract metadata for individual posts.
- Save the metadata of posts as JSON files.
- Delete JSON files when needed.
- Offer concurrent scraping for multiple subreddit URLs for efficiency.
"""
import json
import os
import re
import time
from urllib.parse import urlparse
from utils.functions import get_random_user_agent

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright


def clear_json_files_in_folder(folder_path: str):
    """
    Remove all JSON files in the specified folder.
    """
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)
                print(f"Deleted: {filename}")
            else:
                print("Folder is empty")
                break
    except Exception as e:
        print(f"An error occurred: {e}")


def scrape_subreddit_page_html(url: str) -> str:
    """
    Retrieves the HTML content of a subreddit page using a headless browser.

    Args:
        url (str): Subreddit URL.

    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(user_agent=get_random_user_agent())
        page = context.new_page()

        page.goto(
            url, timeout=60000
        )  # Increase timeout in case the page takes longer to load

        page.wait_for_load_state("networkidle")  # Wait for the page to load completely

        # Handle cookies button if it exists
        accept_button = page.query_selector(
            "button._1tI68pPnLBjR1iHcL7vsee._2iuoyPiKHN3kfOoeIQalDT._10BQ7pjWbeYP63SAPNS8Ts.HNozj_dKjQZ59ZsfEegz8"
        )
        if accept_button:
            accept_button.click()

        page.wait_for_load_state(
            "networkidle"
        )  # Wait for the page to load completely after accepting cookies

        page.evaluate(
            "window.scrollBy(0, window.innerHeight);"
        )  # Scroll down by the height of the viewport

        page.wait_for_load_state(
            "networkidle"
        )  # Wait for the page to load completely after scrolling down

        html_content = page.content()  # Get the entire HTML content of the page

        browser.close()  # Close the browser

    return html_content


def extract_posts_from_html(html: str) -> list:
    """
    Extracts post elements from the subreddit's HTML.

    Args:
        html (str): HTML content of the subreddit page.
    """
    soup = BeautifulSoup(html, "html.parser")
    post_elements = soup.select("shreddit-post")
    return post_elements


def extract_post_details(post_element) -> dict:
    """
    Extracts post information from a BeautifulSoup element representing a post.

    Args:
        post_element (bs4.element.Tag): BeautifulSoup element representing a post.
    """
    post_title_element = post_element.select_one('[slot="title"]')
    post_title = post_title_element.text.strip() if post_title_element else "N/A"

    permalink_element = post_element.get("permalink")
    permalink = (
        "https://www.reddit.com" + permalink_element if permalink_element else "N/A"
    )

    subreddit_elem = post_element.get("subreddit-prefixed-name")
    subreddit = subreddit_elem if subreddit_elem else "N/A"

    author_element = post_element.get("author")
    author = author_element if author_element else "N/A"

    comment_count_element = post_element.get("comment-count")
    comment_count = int(comment_count_element) if comment_count_element else 0

    post_score_element = post_element.get("score")
    post_score = int(post_score_element) if post_score_element else 0

    post_data = {
        "Post Title": post_title,
        "Permalink": permalink,
        "Subreddit": subreddit,
        "Author": author,
        "Number of Comments": comment_count,
        "Post Score": post_score,
    }

    return post_data


def clean_url_for_filename(url) -> str:
    """
    Cleans a URL to be used as a filename.

    Args:
        url (str): The URL to be sanitized.
    """
    path = urlparse(url).path  # Use the urlparse function to get the path from the URL
    return re.sub(
        r"[^a-zA-Z0-9-_.]", "_", path
    )  # Replace characters that are not allowed in filenames with underscores


def scrape_subreddit_metadata(reddit_url, max_retry=10, retry_delay=3):
    """
    Attempts to scrape post metadata from a subreddit page and save it as JSON.

    Args:
        reddit_url (str): The Reddit URL to scrape.
        max_retry (int, optional): Maximum number of retry attempts. Defaults to 10.
        retry_delay (int, optional): Delay in seconds between retries. Defaults to 3.
    """
    filename = f"json_data_folder/{clean_url_for_filename(reddit_url)}.json"

    retry_count = 0
    homepage_post_list = []

    while retry_count < max_retry:
        try:
            html_data = scrape_subreddit_page_html(reddit_url)
            post_elements = extract_posts_from_html(html_data)

            homepage_post_list = []
            for element in post_elements:
                post_data = extract_post_details(element)
                homepage_post_list.append(post_data)

            if homepage_post_list:
                break
        except Exception as e:
            print(f"An error occurred while scraping {reddit_url}: {e}")

        retry_count += 1
        print(f"Retry {retry_count}/{max_retry}. Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)

    if homepage_post_list:
        print(f"Scraped {reddit_url}:")
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(homepage_post_list, json_file, indent=4)
    else:
        print(f"Failed to scrape {reddit_url} even after retries.")


def scrape_multiple_subreddits_concurrently(
    url_list: list, max_attempts=10, wait_between_attempts=3, concurrency_limit=6
):
    """
    Scrapes multiple Reddit URLs concurrently using threads.

    Args:
        urls (list): A list of Reddit URLs to scrape.
        max_attempts (int, optional): Maximum number of retry attempts. Defaults to 10.
        wait_between_attempts (int, optional): Delay in seconds between retries. Defaults to 3.
        num_threads (int, optional): Number of threads to use for concurrent scraping. Defaults to 4.
        concurrency_limit (int, optional): Number of concurrent scraping tasks. Defaults to 6.
    """
    with ThreadPoolExecutor(max_workers=concurrency_limit) as executor:
        executor.map(
            lambda url: scrape_subreddit_metadata(
                url, max_attempts, wait_between_attempts
            ),
            url_list,
        )
