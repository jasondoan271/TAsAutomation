from db import init_db, get_unprocessed_per_source, mark_processed
from rss_ingest import ingest_feeds
from llm import analyze_threats
from formatter import format_newsletter
from mailer import send_email

EMAIL_LIST = [
    "cybersaiko@proton.me" # -- prob have EMAIL_LIST in env variable or config file later
]

def main():
    init_db()
    ingest_feeds()

    # limit this so LLM can can handle it, its per source
    threats = get_unprocessed_per_source(limit_per_source=1)
    if not threats:
        print("No new threats.") # -- rare case tbh most RSS feeds updated quickly + I doubt we can exhaust the feeds
        return

    analysis = analyze_threats(threats)
    newsletter = format_newsletter(analysis)

    
    send_email(EMAIL_LIST, newsletter)
    mark_processed([t[0] for t in threats]) # -- for loop counter to mark processed
    print("Threat advisory sent.")

    
    print(newsletter)  # For debugging

if __name__ == "__main__":
    main()

