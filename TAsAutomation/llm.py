import os
import requests
from utils import sanitize

LM_STUDIO_URL = "http://127.0.0.1:1234" # this is ur own local LM Studio instance
MODEL_NAME    = "gpt-oss-20b"
API_KEY       = os.getenv("OPENAI_API_KEY") # doesn't have to be OpenAI btw

headers = {}
if API_KEY:
    headers["Authorization"] = f"Bearer {API_KEY}"  # just for use outside local llm - scalability fr (cybernetic upgrades ;d)

def analyze_threats(threats):
    items = []

    # threats: (id, source, title, summary, clean_content, cves, links)
    for _, source, title, summary, clean_content, cves, link in threats:
        items.append(f"""
SOURCE: {source}
TITLE: {title}
CVEs: {cves or "None"}
SUMMARY: {summary}
DETAILS: {clean_content}
LINK: {link}
""")

    prompt = f"""
You are writing a short threat intelligence newsletter for SOC analysts. 
Summarize each article concisely and as detailed as possible, providing at least 2-3 sentences in the summary.

For EACH item in the Threats list, write in this exact format:

SOURCE: {{source}}
TITLE: {{title}}
CVEs: {{cves}}
SUMMARY: {{your_summary_here}}
LINK: {{link}}

Use a concise, newsletter‑friendly tone.

Threats:
{"".join(items)}
"""


    # Sanitizes the final prompt BEFORE sending to LM Studio
    prompt = sanitize(prompt)

    # Debug prints (only for testing)

    print(repr(prompt[:10000]))

    print("FULL PROMPT LENGTH:", len(prompt))

    for i, ch in enumerate(prompt):
        if ord(ch) < 32 and ch not in ("\n", "\t"):
            print("BAD CHAR:", repr(ch), "at index", i)

    response = requests.post(
    f"{LM_STUDIO_URL}/v1/chat/completions",
    json={
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You analyze cybersecurity threats. "
                    "Do not explain your reasoning. "
                    "Do not show chain-of-thought. "
                    "You will provide a quick summary for the summary section, given in the threats listed. "
                    "Only output the final newsletter entries in the required format."
                )
            },
            {
                "role": "user",
                "content": prompt + 
                    "\n\nDo not restate the instructions. "
                    "Do not analyze the format. "
                    "Only output the formatted newsletter entries. "
                    "Begin now."
            }
        ],
        "temperature": 0.3, # low temp for more focused output
        "top_p": 0.9, # accuracy over creativity (90% of probable output)
        "max_tokens": 2000
    },
    headers=headers,
    timeout=600
)


    response.raise_for_status()
    llm_output = response.json()["choices"][0]["message"]["content"]
    return llm_output


