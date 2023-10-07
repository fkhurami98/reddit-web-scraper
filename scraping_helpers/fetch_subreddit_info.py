import json
import os
import random
import re
import time
from urllib.parse import urlparse
from utils.constants import USER_AGENTS

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright



def save_reddit_html_to_variable(url: str):
    """
    Saves the HTML content of a given Reddit URL to a file.

    Args:
        url (str): The Reddit URL to scrape.

    Returns:
        str: The HTML content of the page.
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

        page.wait_for_timeout(1000)  # Wait for one second

        html_content = page.content()  # Get the entire HTML content of the page

        browser.close()  # Close the browser

    return html_content


def get_random_user_agent():
    """
    Gets a random user agent from a list of common user agents.

    Returns:
        str: A random user agent string.
    """

    return random.choice(USER_AGENTS)


def parse_reddit_html(html: str):
    """
    Parses the HTML of a Reddit page using BeautifulSoup and extracts post elements.

    Args:
        html (str): The HTML content of the Reddit page.

    Returns:
        list: A list of BeautifulSoup elements representing post elements.
    """
    soup = BeautifulSoup(html, "html.parser")
    post_elements = soup.select("shreddit-post")
    return post_elements


def extract_post_metadata(post_element):
    """
    Extracts post information from a BeautifulSoup element representing a post.

    Args:
        post_element (bs4.element.Tag): BeautifulSoup element representing a post.

    Returns:
        dict: A dictionary containing post information.
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


def sanitize_url_for_filename(url):
    """
    Sanitizes a URL to create a valid filename by replacing characters that are not allowed in filenames with underscores.

    Args:
        url (str): The URL to be sanitized.

    Returns:
        str: The sanitized filename.
    """
    path = urlparse(url).path  # Use the urlparse function to get the path from the URL
    return re.sub(
        r"[^a-zA-Z0-9-_.]", "_", path
    )  # Replace characters that are not allowed in filenames with underscores


def fetch_reddit_url(reddit_url, max_retry=10, retry_delay=3):
    """
    Scrapes a Reddit URL, extracts post information, and saves the results to a JSON file.

    Args:
        reddit_url (str): The Reddit URL to scrape.
        max_retry (int, optional): Maximum number of retry attempts. Defaults to 10.
        retry_delay (int, optional): Delay in seconds between retries. Defaults to 3.

    Returns:
        None
    """
    filename = f"subreddit_page_data/{sanitize_url_for_filename(reddit_url)}.json"

    retry_count = 0
    homepage_post_list = []

    while retry_count < max_retry:
        try:
            html_data = save_reddit_html_to_variable(reddit_url)
            post_elements = parse_reddit_html(html_data)

            homepage_post_list = []
            for element in post_elements:
                post_data = extract_post_metadata(element)
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


def fetch_reddit_urls_with_threads(urls, max_retry=10, retry_delay=3, num_threads=6):
    """
    Scrapes multiple Reddit URLs concurrently using threads.

    Args:
        urls (list): A list of Reddit URLs to scrape.
        max_retry (int, optional): Maximum number of retry attempts. Defaults to 10.
        retry_delay (int, optional): Delay in seconds between retries. Defaults to 3.
        num_threads (int, optional): Number of threads to use for concurrent scraping. Defaults to 4.

    Returns:
        None
    """
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(lambda url: fetch_reddit_url(url, max_retry, retry_delay), urls)


def delete_json_files(folder_path: str):
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


def fetch_subreddits(url_list: list):
    """
    Initiates the scraping process for a list of Reddit URLs.

    Returns:
        None
    """

    delete_json_files(folder_path="/home/farhadkhurami/reddit-web-scraper/subreddit_page_data")

    # Call the function to scrape Reddit URLs using threads
    fetch_reddit_urls_with_threads(url_list)


if __name__ == "__main__":
    pass
