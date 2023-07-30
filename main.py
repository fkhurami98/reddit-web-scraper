from bs4 import BeautifulSoup
import requests

# The URL of the web page you want to fetch
url = "https://www.reddit.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
}


# Sending a GET request with a User-Agent header to mimic a web browser
response = requests.get(url, headers=headers)
print(response.status_code)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the HTML content from the response
    html = response.text
else:
    print("Failed to fetch the page:", response.status_code)
    exit()

# Parse the larger HTML page using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all elements with the shreddit-post class (the provided HTML snippet)
post_elements = soup.find_all('div', {'class': 'rpBJOHq2PR60pnwJlUyP0'})

# Loop through all the post elements found
for post_element in post_elements:
    # Convert the element back to a string representation
    extracted_html_snippet = str(post_element)

    soup_post = BeautifulSoup(extracted_html_snippet, 'html.parser')

    # Extracting post details
    post_title_elem = soup_post.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'})
    post_title = post_title_elem.text.strip() if post_title_elem else "N/A"

    permalink_elem = soup_post.find('a', {'class': 'SQnoC3ObvgnGjWt90zD9Z'})
    permalink = "https://www.reddit.com" + permalink_elem['href'] if permalink_elem else "N/A"
    subreddit = permalink.split('/')[4] if permalink != "N/A" else "N/A"

    author_elem = soup_post.find('a', {'class': '_2tbHP6ZydRpjI44J3syuqC _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE'})
    author = author_elem.text.strip() if author_elem else "N/A"

    # Extracting the number of comments
    comment_count_elem = soup_post.find('span', {'class': 'FHCV02u6Cp2zYL0fhQPsO'})
    comment_count = int(comment_count_elem.text.split()[0]) if comment_count_elem else 0

    post_score_elem = soup_post.find('div', {'class': '_1rZYMD_4xY3gRcSS3p8ODO'})
    post_score = int(post_score_elem.text) if post_score_elem else 0

    # Printing the extracted information for each post
    print("--------------")
    print("Post Title:", post_title)
    print("Permalink:", permalink)
    print("Subreddit:", subreddit)
    print("Author:", author)
    print("Number of Comments:", comment_count)
    print("Post Score:", post_score)

# Separator between snippets
print("--------------")
