import os
import random
import requests

# -----------------------
# CONFIGURATION
# -----------------------
BLOG_ID = os.environ.get("BLOG_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")

if not BLOG_ID or not CLIENT_ID or not CLIENT_SECRET or not REFRESH_TOKEN:
    raise RuntimeError("Set BLOG_ID, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN in GitHub Secrets")

TEMPLATE_FOLDER = "blog_templates"

# -----------------------
# GET ACCESS TOKEN
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
# LOAD RANDOM TEMPLATE
# -----------------------
def load_random_template():
    files = [f for f in os.listdir(TEMPLATE_FOLDER) if f.endswith(".txt")]
    if not files:
        raise RuntimeError("No template files found in blog_templates/")
    chosen_file = random.choice(files)
    with open(os.path.join(TEMPLATE_FOLDER, chosen_file), "r") as f:
        return f.read()

# -----------------------
# FORMAT BLOG CONTENT
# -----------------------
def parse_template(template_text):
    # Very simple parsing: split by lines starting with keywords
    lines = template_text.splitlines()
    content = ""
    title = ""
    meta_title = ""
    meta_desc = ""
    for line in lines:
        if line.startswith("Title:"):
            title = line.replace("Title:", "").strip()
        elif line.startswith("MetaTitle:"):
            meta_title = line.replace("MetaTitle:", "").strip()
        elif line.startswith("MetaDescription:"):
            meta_desc = line.replace("MetaDescription:", "").strip()
        else:
            content += line + "\n"
    return title, meta_title, meta_desc, content

# -----------------------
# POST TO BLOGGER
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
# MAIN
# -----------------------
if __name__ == "__main__":
    template = load_random_template()
    title, meta_title, meta_desc, content = parse_template(template)
    post_to_blogger(title, content)
