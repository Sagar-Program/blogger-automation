import os
import requests
import json
import datetime
import openai

# Load secrets from environment variables
BLOG_ID = os.environ.get("BLOG_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not all([BLOG_ID, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, OPENAI_API_KEY]):
    raise RuntimeError("Please set all required secrets: BLOG_ID, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Step 1: Get access token from Google OAuth
def get_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    response = requests.post(url, data=data)
    resp_json = response.json()
    if "access_token" not in resp_json:
        print("Failed to get access_token:", resp_json)
        raise ValueError("access_token not found")
    return resp_json["access_token"]

# Step 2: Generate blog content from OpenAI
def generate_blog_content():
    prompt = """You are an expert blog writer.
Follow these rules:
- H1: 28–34px, bold, 8–12 words
- H2/H3 for sections and subpoints
- TL;DR 3–5 bullets after intro
- Include callouts, example scenario, checklist
- Include 1–2 images with captions
- Meta title <=60 chars, meta desc 150–160 chars
- Conclusion + 2 CTAs
- Output HTML for Blogger
- Length: 900–1300 words

Topic set: Personal Life, Food, Travel, How-To, Reviews, Finance, Productivity, Health, Fashion, Lists/Roundups

Write a fresh, original post and provide:
Title, MetaTitle, MetaDescription, HTML content, images with captions, CTAs.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content": prompt}],
        temperature=0.7,
        max_tokens=2500
    )
    content = response['choices'][0]['message']['content']
    return content

# Step 3: Post to Blogger
def post_to_blogger(html_content, title, meta_title, meta_desc):
    access_token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    data = {
        "kind": "blogger#post",
        "title": title,
        "content": html_content
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Post successful:", title)
    else:
        print("Failed to post:", response.text)

# Step 4: Main execution
if __name__ == "__main__":
    blog_html = generate_blog_content()

    # Extract Title, MetaTitle, MetaDescription from generated content
    # For simplicity, assume HTML contains <!--TITLE: ...--> etc.
    def extract_field(content, field):
        start = f"<!--{field}:"
        end = "-->"
        if start in content:
            return content.split(start)[1].split(end)[0].strip()
        return field

    title = extract_field(blog_html, "TITLE")
    meta_title = extract_field(blog_html, "META_TITLE")
    meta_desc = extract_field(blog_html, "META_DESC")

    post_to_blogger(blog_html, title, meta_title, meta_desc)
