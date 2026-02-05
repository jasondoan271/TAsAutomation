import re
import unicodedata
from html import unescape

# this was low hanging fruit

def clean_html(text):
    if not text:
        return ""
    text = unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_cves(text):
    return sorted(set(
        re.findall(r"CVE-\d{4}-\d{4,7}", text, re.IGNORECASE)
    ))

# ts below is not mine bro I am NOT looking through allat to fix it - don't mess with perfection

def sanitize(text):
    if not text:
        return ""

    # Normalize Unicode
    text = unicodedata.normalize("NFKC", text)

    # Remove control characters except newline and tab
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Replace Windows CRLF with LF
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Escape backslashes so JSON is valid/safe
    text = text.replace("\\", "\\\\")

    # Collapse weird whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()

