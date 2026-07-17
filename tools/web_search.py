"""
web_search.py

General-purpose web search tool. No API key required.

Strategy:
  1. Try DuckDuckGo's Instant Answer API first -- fast, structured,
     good for direct factual questions ("who is...", "what is...").
  2. If there's no instant answer, fall back to scraping DuckDuckGo's
     plain HTML results page and return the top few organic results
     (title, snippet, link) -- this covers general "search the web"
     style questions across many sites, similar to a normal search
     engine.
"""

try:
    import requests
except ImportError:
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

INSTANT_ANSWER_URL = "https://api.duckduckgo.com/"
HTML_SEARCH_URL = "https://html.duckduckgo.com/html/"

MAX_RESULTS = 5

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def _try_instant_answer(query: str):
    response = requests.get(
        INSTANT_ANSWER_URL,
        params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
        headers=HEADERS,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    abstract = data.get("AbstractText")
    if abstract:
        source = data.get("AbstractSource") or "DuckDuckGo"
        url = data.get("AbstractURL")
        suffix = f" (source: {source}{', ' + url if url else ''})"
        return f"{abstract}{suffix}"

    answer = data.get("Answer")
    if answer:
        return answer

    return None


def _fallback_html_search(query: str):
    if BeautifulSoup is None:
        return "Web search error: beautifulsoup4 is not installed"

    response = requests.get(
        HTML_SEARCH_URL,
        params={"q": query},
        headers=HEADERS,
        timeout=10,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    result_blocks = soup.select(".result")[:MAX_RESULTS]

    if not result_blocks:
        return f"No web results found for '{query}'"

    lines = []
    for block in result_blocks:
        title_el = block.select_one(".result__title a") or block.select_one("a.result__a")
        snippet_el = block.select_one(".result__snippet")

        if not title_el:
            continue

        title = title_el.get_text(strip=True)
        link = title_el.get("href", "")
        snippet = snippet_el.get_text(strip=True) if snippet_el else ""

        entry = f"- {title}"
        if snippet:
            entry += f": {snippet}"
        if link:
            entry += f" ({link})"

        lines.append(entry)

    if not lines:
        return f"No web results found for '{query}'"

    formatted = "\n".join(lines)
    return f"Top web results for '{query}':\n{formatted}"


def execute(arguments: dict):
    if requests is None:
        return "Web search error: requests library is not installed"

    query = arguments.get("query") or arguments.get("q")

    if not query:
        return "Web search error: 'query' is required"

    clean_query = str(query).strip()

    try:
        instant = _try_instant_answer(clean_query)
        if instant:
            return instant
    except Exception:
        pass

    try:
        return _fallback_html_search(clean_query)
    except Exception as e:
        return f"Web search error: {e}"


if __name__ == "__main__":
    print("Web search tool\n")
    print(execute({"query": "who is the current prime minister of India"}))
    print()
    print(execute({"query": "best budget laptops 2026"}))