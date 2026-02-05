import feedparser
from utils import clean_html, extract_cves, sanitize
from db import insert_threat

# Again, this can be set via config/env vars later

FEEDS = [
    ("The Hacker News", "https://feeds.feedburner.com/TheHackersNews?format=xml"),
    ("Krebs on Security", "https://krebsonsecurity.com/feed/"),
    ("0day Fans", "https://0dayfans.com/feed.rss")
]

def ingest_feeds():
    for source, url in FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            raw_content = entry.content[0].value if "content" in entry and entry.content else entry.get("summary", "") # if no content, use summary, else use content starting from beginning

            # Clean HTML first, then sanitize for LLM safety
            clean_html_content = clean_html(raw_content)
            clean_content = sanitize(clean_html_content)

            summary = clean_html(entry.get("summary", ""))

            categories = [t.term for t in entry.tags if hasattr(t, "term")] if "tags" in entry else [] # I did NOT write ts, but categories could help w other agents down the line ig
            cves = extract_cves(clean_content + " " + " ".join(categories)) # Some CVEs are put in tags/categories too apparently but I just manually parsed raw content (idk if its faster)

            threat = {
                "source": source,
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": summary,
                "raw_content": raw_content,                 # used ONLY for hashing
                "clean_content": clean_content[:5000],      # stored + used for LLM (set limit properly or LLM WILL implode, for reference usually 1000 tokens is 4000 chars, or around 750 words)
                "categories": categories,
                "cves": cves
            }

            insert_threat(threat)

