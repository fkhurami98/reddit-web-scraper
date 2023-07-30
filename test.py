import time
from bs4 import BeautifulSoup
from pprint import pprint
from main import get_reddit_page


def extract_individual_post_info(html_code):
    soup = BeautifulSoup(html_code, "html.parser")

    parent_div = soup.select_one("div.mb-sm.mb-xs.px-md.xs\\:px-0")

    if not parent_div:
        post_info = {
            "Opinions": "Post content not found. Likely to be blanks",
        }
    else:
        post_text = parent_div.find_all("p")

        opinions = [paragraph.text.strip() for paragraph in post_text]

        post_info = {
            "Opinions": opinions,
        }

    return post_info




if __name__ == "__main__":
    post_data_list = [
        {
            "Author": "One_Tumbleweed_565",
            "Number of Comments": 626,
            "Permalink": "https://www.reddit.com/r/AskUK/comments/15dlmz9/am_i_a_snob_for_thinking_benidorm_is_a_cheap/",
            "Post Score": 1239,
            "Post Title": "Am I a snob for thinking Benidorm is a cheap, tacky, pish holiday?",
            "Subreddit": "r/AskUK",
        },
        {
            "Author": "StartheBulldog",
            "Number of Comments": 8816,
            "Permalink": "https://www.reddit.com/r/AskReddit/comments/15diop1/which_profession_has_the_most_fked_up_people_in_it/",
            "Post Score": 8570,
            "Post Title": "Which profession has the most f**ked up people in it?",
            "Subreddit": "r/AskReddit",
        },
        {
            "Author": "tylerthe-theatre",
            "Number of Comments": 477,
            "Permalink": "https://www.reddit.com/r/AskUK/comments/15dpnmy/what_are_some_unpopular_opinions_you_have_about/",
            "Post Score": 114,
            "Post Title": "What are some unpopular opinions you have about the uk?",
            "Subreddit": "r/AskUK",
        },
    ]

    for post_data in post_data_list:
        permalink = post_data["Permalink"]
        print(f"Extracting HTML from {permalink}")
        html_content = get_reddit_page(permalink)
        data = extract_individual_post_info(html_content)
        pprint(data)
        time.sleep(60)
