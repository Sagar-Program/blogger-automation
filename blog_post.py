import os
import requests
from datetime import datetime
import openai  # Make sure you install openai: pip install openai

# -----------------------
# 1. CONFIGURATION
# -----------------------
BLOG_ID = os.environ.get("BLOG_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # Add this secret in GitHub

if not BLOG_ID or not CLIENT_ID or not CLIENT_SECRET or not REFRESH_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Please set BLOG_ID, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, and OPENAI_API_KEY in GitHub Secrets")

openai.api_key = OPENAI_API_KEY

# -----------------------
# 2. GET ACCESS TOKEN
# -----------------------
def get_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    response = requests.post(url, data=data)
    result = response.json()
    if "access_token" not in result:
        print("Failed to get access_token. Response:", result)
        raise ValueError("access_token not found")
    return result["access_token"]

# -----------------------
# 3. GENERATE BLOG CONTENT
# -----------------------
def generate_blog_post(topic):
    prompt = f"""
    You are an expert blogger. Write a full blog post on the topic: "{topic}".
    Requirements:
    - 900–1300 words
    - Include H1, H2, H3 sections
    - TL;DR of 3–5 bullets after intro
    - One callout box ("Pro Tip")
    - Example scenario (3–6 sentences)
    - Images with Markdown placeholders
    - Meta title ≤ 60 chars, meta description 150–160 chars
    - Conclusion with 4–6 sentences
    - Two CTAs: comment & follow/subscribe
    Output ONLY in Markdown.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content

# -----------------------
# 4. POST TO BLOGGER
# -----------------------
def post_to_blogger(title, content):
    access_token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"✅ Blog posted successfully: {title}")
    else:
        print(f"❌ Failed to post. Status: {response.status_code}, Response: {response.text}")

# -----------------------
# 5. MAIN LOGIC
# -----------------------
if __name__ == "__main__":
    # You can modify topics or pick randomly
    topics = [
        "Using Pomodoro for Deep Work",
        "Top 10 Healthy Breakfast Recipes",
        "Budget Travel Tips for Europe",
        "How to Start a Productivity Journal",
        "Review: The Latest Noise-Cancelling Headphones"
    ]
    
    # Pick the next topic (rotate or random)
    topic = topics[0]  # Replace with rotation logic if needed

    print("Generating blog content...")
    content = generate_blog_post(topic)

    print("Posting to Blogger...")
    post_to_blogger(topic, content)
