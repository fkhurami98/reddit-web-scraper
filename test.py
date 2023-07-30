import time
from bs4 import BeautifulSoup
from pprint import pprint
from main import get_reddit_page
import json

def extract_individual_post_info(html_code):
    soup = BeautifulSoup(html_code, "html.parser")

    parent_div = soup.select_one("div.mb-sm.mb-xs.px-md.xs\\:px-0")

    if not parent_div:
        post_info = {
            "Opinions": "Post content not found. Likely to be blank",
        }
    else:
        post_text = parent_div.find_all("p")
        opinions = [paragraph.text.strip() for paragraph in post_text]
        post_info = {
            "Opinions": opinions,
        }

    return post_info

if __name__ == "__main__":
    # Read post_data_list from the JSON file
    with open("posts_metadata.json", "r") as file:
        post_data_list = json.load(file)

    for post_data in post_data_list:
        permalink = post_data["Permalink"]
        print(f"Extracting HTML from {permalink}")
        html_content = get_reddit_page(permalink)
        data = extract_individual_post_info(html_content)
        pprint(data)
        time.sleep(60)
