"""Download SMHI weather for Malmö (zone SE4) and Luleå (zone SE1).

Run once:  uv run electricity/fetch_weather.py
Saves SMHI's files unchanged to electricity/data/ (CC BY 4.0, SMHI open data):
daily mean temperature (parameter 2) and hourly wind speed (parameter 4).
"""
from pathlib import Path

import requests

DATA = Path(__file__).parent / "data"
STATIONS = {"malmo": 52350, "lulea": 162860}
PARAMETERS = {"temperature": 2, "wind": 4}
BASE = "https://opendata-download-metobs.smhi.se/api/version/1.0"

for place, station in STATIONS.items():
    for what, parameter in PARAMETERS.items():
        for period in ["corrected-archive"]:
            url = f"{BASE}/parameter/{parameter}/station/{station}/period/{period}/data.csv"
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            out = DATA / f"smhi-{place}-{what}-{period}.csv"
            out.write_bytes(r.content)
            print(f"{out.name}: {len(r.content) // 1000} kB")
