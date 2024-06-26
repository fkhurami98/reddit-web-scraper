"""
fetch_post_details.py

This script is designed to scrape detailed content from individual Reddit posts.
The process includes:
- Fetching the content of a post given its permalink.
- Parsing HTML to extract specific details like post content and timestamp.
- Processing JSON files that contain post metadata to augment them with detailed post content.
"""

import json
import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def extract_post_content_from_html(html_code: str) -> dict:
    """
    Parses the given HTML to extract post content and its timestamp.

    Args:
        html_code (str): The HTML code of the post page.

    """
    soup = BeautifulSoup(html_code, "html.parser")
    parent_div = soup.select_one("div.mb-sm.mb-xs.px-md.xs\\:px-0")

    # Initialize created_timestamp with a default value
    created_timestamp = ""

    # Find timestamp when post was created
    time_element = soup.find(attrs={"created-timestamp": True})
    if time_element:
        created_timestamp = time_element["created-timestamp"]

    if not parent_div:
        post_info = {
            "Post Content": "Post content not found. Likely to be blank, an image, or a URL",
            "Time Stamp": created_timestamp,
        }
    else:
        post_text = parent_div.find_all("p")
        # opinions = [paragraph.text.strip() for index, paragraph in enumerate(post_text)]

        opinions = ""
        for paragraph in post_text:
            opinions += paragraph.text.strip()

        post_info = {"Post Content": opinions, "Time Stamp": created_timestamp}

    return post_info


def fetch_post_content_from_permalink(permalink: str) -> dict:
    """
    Scrapes post content from a given permalink.

    Args:
        permalink (str): The permalink of the post.

    Returns:
        dict or None: A dictionary containing the extracted post content,
                      or None if an error occurred during scraping.
    """
    try:
        response = requests.get(permalink)
        response.raise_for_status()

        post_info = extract_post_content_from_html(response.content)
        return post_info

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while scraping {permalink}: {e}")
        return None


def update_post_content_in_json(json_file_path: str):
    """
    Enhances a given JSON file with content details of the Reddit posts.

    Args:
        json_file_path (str): The path to the JSON file.
    """
    with open(json_file_path, "r") as json_file:
        original_posts = json.load(json_file)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(fetch_post_content_from_permalink, post["Permalink"])
            for post in original_posts
        ]

        for future, post in zip(futures, original_posts):
            post_info = future.result()
            if post_info:
                post.update(post_info)

    with open(json_file_path, "w") as json_file:
        json.dump(original_posts, json_file, indent=4)


def process_all_json_files_in_folder(folder_path: str):
    """
    Processes all JSON files in a folder.

    Args:
        folder_path (str): The path to the folder containing JSON files.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            json_file_path = os.path.join(folder_path, filename)
            update_post_content_in_json(json_file_path)
