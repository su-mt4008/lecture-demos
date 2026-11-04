"""Download SCB's 100 most common first names, by year of birth.

Run once:  uv run names/fetch.py
Saves SCB's CSV unchanged to names/data/scb-names-by-birth-year.csv.
Source: Statistics Sweden (SCB), table BE0001T100, "First names normally used, the 100 most
common for women and men 31 December 2021. Year of birth 1922 - 2021".
"""
from pathlib import Path

import requests

URL = "https://api.scb.se/OV0104/v1/doris/en/ssd/BE/BE0001/BE0001G/BE0001T100"
OUT = Path(__file__).parent / "data" / "scb-names-by-birth-year.csv"

# An empty query asks for every name and every year.
r = requests.post(URL, json={"query": [], "response": {"format": "csv"}}, timeout=60)
r.raise_for_status()
OUT.write_bytes(r.content)
print(f"{OUT.name}: {len(r.content) // 1000} kB")
