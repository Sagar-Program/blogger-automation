import os
import requests
import random
from datetime import datetime

# === Blogger Blog ID ===
BLOG_ID = os.environ.get("BLOG_ID")
if not BLOG_ID:
    raise RuntimeError("❌ BLOG_ID environment variable is not set. Please add it to GitHub Secrets.")

# === OAuth 2.0 credentials ===
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")

if not CLIENT_ID or not CLIENT_SECRET or not REFRESH_TOKEN:
    raise RuntimeError("❌ CLIENT_ID, CLIENT_SECRET, or REFRESH_TOKEN is missing. Please add them to GitHub Secrets.")

# === Step 1: Get Access Token ===
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
        print("❌ Failed to get access_token. Response:", data)
        raise ValueError("access_token not found in response")
    return data["access_token"]

# === Step 2: Generate Blog Content ===
def generate_blog_content():
    titles = [
        "The Future of AI: What’s Next?",
        "Top 5 Tools Every Developer Should Know",
        "How Automation is Changing Our World",
        "The Rise of Smart Tourism in 2025",
        "Why Coding is the New Literacy"
    ]
    paragraphs = [
        "Technology is evolving at an incredible pace, and artificial intelligence is at the forefront.",
        "Developers today have access to powerful tools that make coding faster and smarter.",
        "Automation is not just about efficiency; it's about reshaping industries.",
        "Tourism is entering a new era with smart cities and AI-driven experiences.",
        "Learning to code is becoming as important as reading and writing in today’s world."
    ]
    title = random.choice(titles)
    body = f"""
<h2>{title}</h2>
<p>{random.choice(paragraphs)}</p>
<p>Published on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""
    return title, body

# === Step 3: Post to Blogger ===
def post_to_blogger(access_token, title, content):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"✅ Blog posted successfully: {title}")
    else:
        print(f"❌ Failed to post. Status: {response.status_code}, Response: {response.text}")
        response.raise_for_status()

# === Step 4: Run Script ===
if __name__ == "__main__":
    token = get_access_token()
    title, content = generate_blog_content()
    post_to_blogger(token, title, content)
