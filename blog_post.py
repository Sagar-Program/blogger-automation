import os
import requests
import openai
from datetime import datetime

# ---------- CONFIGURATION ----------
BLOG_ID = os.environ.get("BLOG_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not all([BLOG_ID, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, OPENAI_API_KEY]):
    raise RuntimeError("Missing one or more required secrets. Set BLOG_ID, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, OPENAI_API_KEY in GitHub Secrets.")

openai.api_key = OPENAI_API_KEY

# ---------- FUNCTION TO GET ACCESS TOKEN ----------
def get_access_token():
    url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=payload)
    data = response.json()
    if "access_token" not in data:
        print("Failed to get access_token. Response:", data)
        raise ValueError("access_token not found in response")
    return data["access_token"]

# ---------- FUNCTION TO GENERATE BLOG CONTENT ----------
def generate_blog_content():
    prompt = """
    You are an expert blog writer. Generate a fully formatted Markdown post including:
    - H1, H2, H3 headings
    - TL;DR bullets
    - Callout box ("Pro tip")
    - Example scenario
    - Images with captions
    - Conclusion and blog-specific CTAs
    Topic: Productivity
    Word count: 900-1300 words
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )
    return response['choices'][0]['message']['content']

# ---------- FUNCTION TO POST BLOG ----------
def post_blog(title, content):
    access_token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    post_data = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    response = requests.post(url, json=post_data, headers=headers)
    if response.status_code != 200:
        print("Failed to post blog:", response.text)
    else:
        print("Blog posted successfully!")

# ---------- MAIN ----------
if __name__ == "__main__":
    print("Generating blog content...")
    blog_content = generate_blog_content()
    blog_title = f"Automated Blog Post - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    post_blog(blog_title, blog_content)
