import feedparser
import requests
import datetime
import time
import os

# --- ⚙️ SETTINGS ---
WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

# RSS Feed: "Web Scraping" & "Python" (Sorted by Newest)
RSS_URL = "https://www.upwork.com/ab/feed/jobs/rss?q=web%20scraping+python&sort=recency&paging=0%3B10&api_params=1"

# --- 🎯 FILTERS ---
KEYWORDS = ['python', 'scraping', 'selenium', 'automation', 'bot', 'script', 'extraction','scrape','a']
BAD_WORDS = ['expert', 'senior', 'java', 'php', 'wordpress', 'design', 'manager']

def send_discord_alert(title, link, date):
    if not WEBHOOK_URL:
        print("❌ Error: Discord Webhook URL is missing!")
        return

    data = {
        "content": "🚨 **NEW JOB FOUND!** @here",
        "embeds": [{
            "title": title,
            "url": link,
            "description": f"**Posted:** {date}\n\n[⚡ Click to Apply Immediately]({link})",
            "color": 5763719,
            "footer": {"text": "Upwork Sniper • Machine 3"}
        }]
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
        print("✅ Discord alert sent.")
    except Exception as e:
        print(f"❌ Error sending Discord: {e}")

def check_jobs():
    print("👀 Sniper woke up! Checking Upwork RSS...")
    now = datetime.datetime.utcnow()
    
    try:
        feed = feedparser.parse(RSS_URL)
    except Exception as e:
        print(f"❌ Error reading RSS feed: {e}")
        return

    found_any = False
    
    for entry in feed.entries:
        published_time = datetime.datetime(*entry.published_parsed[:6])
        minutes_old = (now - published_time).total_seconds() / 60
        
        if minutes_old < 2000000:
            desc = entry.description.lower()
            title = entry.title
            
            if any(good in desc for good in KEYWORDS):
                if not any(bad in desc for bad in BAD_WORDS):
                    print(f"🎯 FOUND MATCH: {title}")
                    send_discord_alert(title, entry.link, str(published_time))
                    found_any = True
                    time.sleep(1)

    if not found_any:
        print("💤 No new jobs found this cycle.")

if __name__ == "__main__":
    check_jobs()
