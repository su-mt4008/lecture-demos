"""Download the three data sources for "Is AI a bubble?".

Run once:  uv run ai-bubble/fetch.py
Saves to ai-bubble/data/; the report reads only those files.

1. Robert Shiller's monthly US stock market data (S&P composite, earnings, CAPE), 1871-.
   https://shillerdata.com (the old Yale page stopped updating in 2023; if this link breaks,
   take the "ie_data.xls" link from that page).
2. The NASDAQ Composite index, daily, from FRED (St. Louis Fed), series NASDAQCOM.
3. Hacker News: per month, how many story titles there were in total and how many
   mention each term. From the HN Search API by Algolia (hn.algolia.com/api).
"""
from datetime import date, datetime, timezone
from pathlib import Path
import time

import pandas as pd
import requests

DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)
session = requests.Session()
# (No custom User-Agent: FRED refuses requests that send one.)


def save(url: str, name: str) -> None:
    r = session.get(url, timeout=60)
    r.raise_for_status()
    (DATA / name).write_bytes(r.content)
    print(f"{name}: {len(r.content) // 1000} kB")


save("https://img1.wsimg.com/blobby/go/e5e77e0b-59d1-44d9-ab25-4763ac982e53/downloads/"
     "1449043e-a1ed-4e2e-8e9c-7b9a2a064493/ie_data.xls", "shiller-ie_data.xls")
save("https://fred.stlouisfed.org/graph/fredgraph.csv?id=NASDAQCOM", "fred-nasdaqcom.csv")

# Hacker News. Words are matched exactly in the title (no prefixes, no typos),
# so "AI" does not match "aim" or "air".
TERMS = ["", "AI", "LLM", "GPT", "blockchain", "bitcoin", "crypto"]
LAST = date(2026, 10, 1)


def stamp(d: date) -> int:
    return int(datetime(d.year, d.month, 1, tzinfo=timezone.utc).timestamp())


def count(term: str, start: int, end: int) -> int:
    """Number of stories from `start` to `end` (Unix seconds) whose title has `term`.
    For large result sets the API only estimates the count (exhaustiveNbHits is false, and the
    estimate can be off by a factor of 100), so we split the window in half until it is exact."""
    params = {
        "query": term, "tags": "story", "hitsPerPage": 0,
        "numericFilters": f"created_at_i>={start},created_at_i<{end}",
        "restrictSearchableAttributes": "title", "typoTolerance": "false",
        "queryType": "prefixNone",
    }
    for attempt in range(5):
        r = session.get("https://hn.algolia.com/api/v1/search_by_date", params=params, timeout=30)
        if r.status_code == 200:
            break
        time.sleep(2 ** attempt)
    r.raise_for_status()
    time.sleep(0.1)  # be polite to a free API
    result = r.json()
    if result["exhaustiveNbHits"]:
        return result["nbHits"]
    middle = (start + end) // 2
    return count(term, start, middle) + count(term, middle, end)


months = pd.date_range("2007-03-01", LAST, freq="MS").date
rows = []
for start in months:
    end = (pd.Timestamp(start) + pd.offsets.MonthBegin()).date()
    row = {"month": start.isoformat()}
    for term in TERMS:
        row[term or "all_stories"] = count(term, stamp(start), stamp(end))
    rows.append(row)
pd.DataFrame(rows).to_csv(DATA / "hn-title-mentions.csv", index=False)
print(f"hn-title-mentions.csv: {len(rows)} months")
