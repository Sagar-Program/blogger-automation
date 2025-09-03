import os
import requests
import json
import openai
from datetime import datetime

# Load environment variables from GitHub Secrets
BLOG_ID = os.environ.get("BLOG_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not all([BLOG_ID, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, OPENAI_API_KEY]):
    raise RuntimeError("One or more required environment variables are missing. Add them to GitHub Secrets.")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Function to get access token from Google
def get_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=data)
    res_json = response.json()
    if "access_token" not in res_json:
        print("Failed to get access token. Response:", res_json)
        raise ValueError("access_token not found")
    return res_json["access_token"]

# Generate blog content using OpenAI
def generate_blog():
    prompt = """
    You are an expert blog writer. Generate a full blog post in Markdown according to this Master Prompt:
    - 900–1300 words
    - H1, H2, H3 formatting
    - TL;DR bullets
    - Meta title and description
    - Callout boxes, example scenario, images with captions and credits
    - Schedule post for Monday, Wednesday, Friday 10:00 AM
    - Follow SEO, freshness, and topic rules
    Output only Markdown.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

# Post blog to Blogger
def post_blog(content):
    access_token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    data = {"kind": "blogger#post", "title": "Automated Blog Post", "content": content}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code not in [200, 201]:
        print("Failed to post. Response:", response.text)
        raise ValueError("Failed to post blog")
    print("Blog posted successfully!")

# Main execution
if __name__ == "__main__":
    blog_content = generate_blog()
    post_blog(blog_content)
