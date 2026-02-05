from datetime import datetime

def format_newsletter(body):
    today = datetime.utcnow().strftime("%Y-%m-%d")

    return f"""
Cyber Threat Advisory — {today}
================================

{body}

--------------------------------
Sources:
• The Hacker News
• Krebs on Security
• 0day Fans

This advisory was generated automatically using local AI analysis.
"""


