import os
import requests
import datetime
import random

# ✅ Step 1: Get access token safely
def get_access_token():
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    refresh_token = os.environ["REFRESH_TOKEN"]

    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.post(token_url, data=payload)
    data = response.json()

    # Debugging log for GitHub Actions
    print("Google OAuth response:", data)

    if "access_token" not in data:
        raise ValueError("❌ Failed to get access_token. Check your CLIENT_ID, CLIENT_SECRET, and REFRESH_TOKEN in GitHub secrets.")
    
    return data["access_token"]

# ✅ Step 2: Generate a blog post (simple example – can be expanded with your rules)
def generate_post():
    topics = [
        "5 Easy Recipes for Busy Weeknights",
        "Top Travel Hacks for 2025",
        "How to Stay Productive While Working from Home",
        "Beginner’s Guide to Investing in Crypto Safely",
        "10 Fashion Trends to Watch This Fall"
    ]
    title = random.choice(topics)
    content = f"""
    <h2>{title}</h2>
    <p>This is an auto-generated blog post created on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.</p>
    <p>Stay tuned for more updates every Monday, Wednesday, and Friday at 10:00 AM!</p>
    """
    return title, content

# ✅ Step 3: Publish to Blogger
def publish_post(access_token, blog_id, title, content):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    post_data = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }

    response = requests.post(url, headers=headers, json=post_data)
    if response.status_code == 200:
        print("✅ Post published successfully:", response.json()["url"])
    else:
        print("❌ Failed to publish post:", response.text)
        response.raise_for_status()

# ✅ Step 4: Main script
if __name__ == "__main__":
    BLOG_ID = os.environ["BLOG_ID"]  # comes from GitHub Secrets
    access_token = get_access_token()
    title, content = generate_post()
    publish_post(access_token, BLOG_ID, title, content)
