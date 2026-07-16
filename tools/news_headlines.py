"""
news_headlines.py

Tool for fetching current news headlines using Google News' public
RSS feed. No API key required.
"""

try:
    import requests
except ImportError:
    requests = None

import xml.etree.ElementTree as ET

TOP_HEADLINES_URL = "https://news.google.com/rss"
SEARCH_URL = "https://news.google.com/rss/search"
MAX_HEADLINES = 5


def execute(arguments: dict):
    if requests is None:
        return "News error: requests library is not installed"

    topic = arguments.get("topic") or arguments.get("query")

    try:
        if topic:
            response = requests.get(
                SEARCH_URL,
                params={"q": topic, "hl": "en-IN", "gl": "IN", "ceid": "IN:en"},
                timeout=10,
            )
        else:
            response = requests.get(
                TOP_HEADLINES_URL,
                params={"hl": "en-IN", "gl": "IN", "ceid": "IN:en"},
                timeout=10,
            )
        response.raise_for_status()

        root = ET.fromstring(response.content)
        items = root.findall(".//item")[:MAX_HEADLINES]

        if not items:
            label = f" about '{topic}'" if topic else ""
            return f"No news headlines found{label}"

        headlines = []
        for item in items:
            title_el = item.find("title")
            if title_el is not None and title_el.text:
                headlines.append(title_el.text)

        if not headlines:
            return "News error: could not parse headlines from feed"

        label = f" about '{topic}'" if topic else ""
        formatted = "\n".join(f"- {h}" for h in headlines)
        return f"Top headlines{label}:\n{formatted}"

    except ET.ParseError:
        return "News error: could not parse the news feed"
    except Exception as e:
        return f"News error: {e}"