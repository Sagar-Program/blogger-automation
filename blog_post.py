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

# === Step 2: Generate Full Blog Content ===
def generate_blog_content():
    # --- Example topics ---
    topics = [
        {"category": "Personal Life", "angle": "Morning routine for productivity"},
        {"category": "Food & Recipes", "angle": "Quick 20-min healthy meals"},
        {"category": "Travel", "angle": "Weekend mini-itinerary for Bangkok"},
        {"category": "Productivity", "angle": "Using Pomodoro for deep work"},
        {"category": "Health & Fitness", "angle": "Home HIIT workout for beginners"}
    ]
    topic = random.choice(topics)

    # --- Meta info ---
    meta_title = f"{topic['angle']} - {topic['category']}"
    meta_description = f"Learn {topic['angle']} in {topic['category']} to boost your life. Practical tips and examples included."

    # --- TL;DR bullets ---
    tldr = [
        "- Quick overview of the topic",
        "- Step-by-step actionable tips",
        "- Practical example included"
    ]

    # --- H1 title ---
    h1_title = topic['angle']

    # --- H2 sections with H3 subpoints ---
    sections = [
        {"h2": "Introduction", "content": f"This post explores {topic['angle']} in detail for readers interested in {topic['category']}."},
        {"h2": "Step 1: Preparation", "h3": ["Gather necessary tools", "Plan your approach"]},
        {"h2": "Step 2: Execution", "h3": ["Follow steps carefully", "Avoid common mistakes"]},
        {"h2": "Pro Tips", "content": "Always track your progress and adjust as needed."},
    ]

    # --- Callout box ---
    callout = {
        "title": "Pro Tip",
        "bullets": ["Be consistent", "Use small steps", "Track results"]
    }

    # --- Example scenario ---
    example = "Imagine you start your morning with a 15-minute focused task session, followed by a quick review of your daily goals."

    # --- Images ---
    images = [
        {"url": "https://via.placeholder.com/600x400", "alt": "Example image", "caption": "Illustrative image of the topic", "credit": "Photo: Unsplash"}
    ]

    # --- Conclusion ---
    conclusion = "Following these steps consistently will help you master the topic. Remember, practice and reflection are key."

    # --- CTAs ---
    ctas = [
        "Enjoyed this? Leave a comment with your thoughts or questions.",
        "Follow the blog for three new posts every week.",
        "Get fresh guides in your inbox—subscribe to never miss Monday, Wednesday, and Friday drops."
    ]

    # --- Internal & external links placeholders ---
    links = [
        "[Link: Related Post Title]",
        "[External Reference 1]",
        "[External Reference 2]"
    ]

    # --- Construct Markdown ---
    content = f"<!-- Angle: {topic['angle']} -->\n"
    content += f"# {h1_title}\n\n"
    content += f"**Meta Title:** {meta_title}\n\n"
    content += f"**Meta Description:** {meta_description}\n\n"
    content += "**TL;DR:**\n"
    for bullet in tldr:
        content += f"- {bullet}\n"
    content += "\n"

    for sec in sections:
        content += f"## {sec['h2']}\n"
        if "content" in sec:
            content += f"{sec['content']}\n"
        if "h3" in sec:
            for sub in sec['h3']:
                content += f"### {sub}\n"
                content += "Explanation goes here.\n"
        content += "\n"

    # Callout
    content += f"### {callout['title']}\n"
    for b in callout['bullets']:
        content += f"- {b}\n"
    content += "\n"

    # Example
    content += f"**Example Scenario:** {example}\n\n"

    # Images
    for img in images:
        content += f"![{img['alt']}]({img['url']})\n"
        content += f"*{img['caption']}*\n"
        content += f"{img['credit']}\n\n"

    # Conclusion
    content += f"## Conclusion\n{conclusion}\n\n"

    # CTAs
    for cta in ctas:
        content += f"{cta}\n"

    # Links
    content += "\n".join(links)

    return h1_title, content

# === Step 3: Post to Blogger ===
def post_to_blogger(access_token, title, content):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
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
