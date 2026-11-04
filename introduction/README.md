# Three example projects (MT4008 introduction)

The three projects from the first session of MT4008 Statistical Data Processing,
Stockholm University. Each is a complete report in the same seven sections your
assignments use: question, data, cleaning, exploration, analysis, conclusions and
limitations, and how to reproduce. Slides and a write-up are on the
[course site](https://su-mt4008.github.io/lectures/introduction).

| Project | Ambition | Data |
|:--|:--|:--|
| [Are baby names a fashion?](names/report.md) | small, about E | SCB: the 200 most common first names by year of birth |
| [Why does electricity cost more in Malmö than in Luleå?](electricity/report.md) | medium, about C | Nord Pool spot prices (elprisetjustnu.se API), SMHI weather |
| [Is AI a bubble?](ai-bubble/report.md) | ambitious, about A | Shiller's CAPE, FRED NASDAQ index, Hacker News Search API |

## Reproduce

You need [uv](https://docs.astral.sh/uv/) and [Quarto](https://quarto.org). From this folder:

```bash
uv sync                    # installs the locked environment
uv run quarto render       # renders all three reports from the saved data
```

The raw data is saved in each project's `data/` folder, so rendering works offline. To
download it again, run the project's fetch script, for example `uv run names/fetch.py`
(the AI project's takes about ten minutes).

## Data and licences

- SCB (Statistics Sweden): open data, cite the source.
- SMHI: CC BY 4.0.
- Spot prices: Nord Pool day-ahead prices via elprisetjustnu.se.
- Shiller data: from shillerdata.com; FRED series NASDAQCOM (St. Louis Fed).
- Hacker News: counts from the HN Search API by Algolia.
