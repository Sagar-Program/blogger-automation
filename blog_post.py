import os
import random
import datetime
import requests

# Blogger API details (your Blog ID is hardcoded here)
BLOG_ID = "4221948764114299957"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

# ==== BLOG GENERATION SETTINGS ====
CATEGORIES = [
    "Personal Life and Stories",
    "Food and Recipes",
    "Travel",
    "How-To Guides and Tutorials",
    "Product Reviews",
    "Money and Finance",
    "Productivity",
    "Health and Fitness",
    "Fashion",
    "Lists and Roundups",
]

# Simple memory of recent topics to avoid duplicates (30 days logic would need persistence in a real DB)
recent_titles = []

def get_access_token():
    """Get access token using refresh token"""
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    response = requests.post(url, data=data)
    return response.json()["access_token"]

def generate_blog_post():
    """Generate structured blog content based on Master Prompt rules"""
    today = datetime.datetime.now().strftime("%B %d, %Y")
    category = random.choice(CATEGORIES)

    # Example dynamic angle
    angles = {
        "Travel": "Budget-friendly destinations in 2025",
        "Food and Recipes": "Quick, healthy weekday meals",
        "Health and Fitness": "Beginner-friendly home workouts",
        "Money and Finance": "Simple tips to save money in 2025",
        "Productivity": "Habits that improve focus",
        "Fashion": "Trendy outfits for this season",
        "Personal Life and Stories": "A personal growth story",
        "Lists and Roundups": "Top 10 style list",
        "Product Reviews": "Testing a new gadget",
        "How-To Guides and Tutorials": "Step-by-step beginner guide",
    }

    chosen_angle = angles.get(category, "Fresh perspective for readers")
    title = f"{category}: {chosen_angle} ({today})"

    # Ensure no duplicate titles (basic safeguard)
    if title in recent_titles:
        title += " [New Edition]"
    recent_titles.append(title)

    # Structured content
    content = f"""
<h1>{title}</h1>
<p><b>By Auto Blogger</b> | {today}</p>

<h2>Introduction</h2>
<p>Welcome! This post dives into <i>{chosen_angle}</i>.  
If you’re looking for practical advice, inspiration, or simply a fresh perspective, you’re in the right place.  
By the end of this read, you’ll walk away with actionable takeaways you can use immediately.</p>

<h2>Main Content</h2>
<h3>Why this matters</h3>
<p>{chosen_angle} is becoming more important than ever. Readers today want fresh insights, not recycled advice. This blog brings you that freshness.</p>

<h3>Key Insights</h3>
<ul>
  <li>Easy to apply tips</li>
  <li>Focused on real-world use</li>
  <li>Designed for today’s needs</li>
</ul>

<div style="border:1px solid #ccc; padding:10px; margin:15px 0;">
<b>Pro Tip:</b> Keep experimenting and note what works for you.  
Consistency is more powerful than intensity.
</div>

<h2>Example Scenario</h2>
<p>For example, if someone applies {chosen_angle.lower()}, within just 30 days they can see noticeable improvement.  
This isn’t theory — it’s been tested and shared by many readers.</p>

<h2>Quick Checklist</h2>
<ul>
  <li>Step 1: Identify your current habits</li>
  <li>Step 2: Pick one small change</li>
  <li>Step 3: Apply it for one week</li>
  <li>Step 4: Reflect and adjust</li>
</ul>

<h2>Conclusion</h2>
<p>Thanks for reading! This post explored <b>{chosen_angle}</b> under the category <i>{category}</i>.  
The goal is to help you take a small but meaningful step forward.  
Remember — big results come from small, consistent actions.</p>

<h2>Engage with us</h2>
<p>Enjoyed this? Leave a comment with your thoughts or questions.</p>
<p><i>Love practical reads like this? Follow the blog for three new posts every week (Mon, Wed, Fri).</i></p>

<h2>What to read next</h2>
<ul>
  <li>[Link: Related Post 1]</li>
  <li>[Link: Related Post 2]</li>
  <li>[Link: Related Post 3]</li>
</ul>
"""
    return title, content

def post_to_blogger():
    """Post generated blog to Blogger"""
    access_token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"

    title, content = generate_blog_post()
    headers = {"Authorization": f"Bearer {access_token}"}
    body = {"kind": "blogger#post", "title": title, "content": content}

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        print("✅ Post published:", title)
    else:
        print("❌ Error:", response.text)

if __name__ == "__main__":
    post_to_blogger()
