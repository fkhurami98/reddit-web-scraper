import time
from bs4 import BeautifulSoup
from pprint import pprint
import random
import json
from playwright.sync_api import sync_playwright, TimeoutError
from urllib.parse import urlparse
import re
from pprint import pprint


def save_reddit_html_to_file(url, output_file):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto(
            url, timeout=60000
        )  # Increase timeout in case the page takes longer to load

        # Wait for the page to load completely
        page.wait_for_load_state("networkidle")

        # Handle cookies button if it exists
        accept_button = page.query_selector(
            "button._1tI68pPnLBjR1iHcL7vsee._2iuoyPiKHN3kfOoeIQalDT._10BQ7pjWbeYP63SAPNS8Ts.HNozj_dKjQZ59ZsfEegz8"
        )
        if accept_button:
            accept_button.click()

        # Wait for the page to load completely after accepting cookies
        page.wait_for_load_state("networkidle")

        # Scroll down by the height of the viewport
        page.evaluate("window.scrollBy(0, window.innerHeight);")

        # Wait for the page to load completely after scrolling down
        page.wait_for_load_state("networkidle")

        # Wait for one second
        page.wait_for_timeout(1000)

        # Get the entire HTML content of the page
        html_content = page.content()

        browser.close()

    # Save the HTML content to a file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"HTML content saved to {output_file}")


def read_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    return html_content


def parse_reddit_html(html):
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
    # Use the urlparse function to get the path from the URL
    path = urlparse(url).path

    # Replace characters that are not allowed in filenames with underscores
    return re.sub(r"[^a-zA-Z0-9-_.]", "_", path)


if __name__ == "__main__":
    reddit_url = "https://www.reddit.com/r/Python/"
    output_file_json = f"{sanitize_url_for_filename(reddit_url)}.json"
    output_file_html = f"{sanitize_url_for_filename(reddit_url)}.html"

    max_retry = 3
    retry_count = 0
    homepage_post_list = []

    while retry_count < max_retry:
        try:
            save_reddit_html_to_file(reddit_url, output_file_html)

            html_data = read_html_file(output_file_html)
            post_elements = parse_reddit_html(html_data)

            homepage_post_list = []
            for element in post_elements:
                post_data = extract_post_metadata(element)
                homepage_post_list.append(post_data)

            if homepage_post_list:
                break
        except Exception as e:
            print(f"An error occurred while scraping: {e}")

        retry_count += 1
        print(f"Retry {retry_count}/{max_retry}. Retrying in 5 seconds...")
        time.sleep(5)

    if homepage_post_list:
        print(homepage_post_list)
        # Save the post list as JSON
        with open(output_file_json, "w", encoding="utf-8") as json_file:
            json.dump(homepage_post_list, json_file, indent=4)
    else:
        print("Failed to scrape the subreddit even after retries.")