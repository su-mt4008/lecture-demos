"""Download spot prices for the four Swedish price zones, 2023-2025.

Run once:  uv run electricity/fetch_prices.py
Saves every price interval to electricity/data/prices.csv. The report reads that file,
so it renders without the network. Source: elprisetjustnu.se (Nord Pool day-ahead prices).
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path
import time

import pandas as pd
import requests

OUT = Path(__file__).parent / "data" / "prices.csv"
ZONES = ["SE1", "SE2", "SE3", "SE4"]
START, END = date(2023, 1, 1), date(2025, 12, 31)
session = requests.Session()
session.headers["User-Agent"] = "MT4008 course demo (Stockholm University)"


def fetch(day: date, zone: str) -> list[dict]:
    url = f"https://www.elprisetjustnu.se/api/v1/prices/{day:%Y}/{day:%m-%d}_{zone}.json"
    for attempt in range(5):
        r = session.get(url, timeout=30)
        if r.status_code == 200:
            return [{"zone": zone, "start": p["time_start"], "end": p["time_end"],
                     "sek_per_kwh": p["SEK_per_kWh"]} for p in r.json()]
        time.sleep(2 ** attempt)
    raise RuntimeError(f"{url}: HTTP {r.status_code}")


days = [START + timedelta(d) for d in range((END - START).days + 1)]
jobs = [(d, z) for d in days for z in ZONES]
with ThreadPoolExecutor(4) as pool:
    rows = [row for chunk in pool.map(lambda j: fetch(*j), jobs) for row in chunk]
pd.DataFrame(rows).to_csv(OUT, index=False)
print(f"{len(rows)} rows -> {OUT}")
