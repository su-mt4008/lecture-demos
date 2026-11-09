# Week 2
Taariq Nazar

``` python
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

raw = pd.read_csv("election-2018-municipalities.csv", sep=";", decimal=",", encoding="utf-8-sig")

raw.shape
raw.dtypes
```

    LÄNSKOD              int64
    KOMMUNKOD            int64
    LÄNSNAMN               str
    KOMMUNNAMN             str
    M                  float64
    C                  float64
    L                  float64
    KD                 float64
    S                  float64
    V                  float64
    MP                 float64
    SD                 float64
    FI                 float64
    AfS                float64
    BASIP              float64
    CSIS               float64
    DD                 float64
    DjuP               float64
    EAP                float64
    ENH                float64
    FHS                float64
    Gup                float64
    INI                float64
    KLP                float64
    KrVP               float64
    LPo                float64
    MED                float64
    NMR                float64
    NORRP              float64
    NYREF              float64
    PP                 float64
    RNP                float64
    S-FRP              float64
    SKP                float64
    SKÅ                float64
    TRP                float64
    VL-S               float64
    ÖVR                float64
    OGEJ               float64
    BLANK              float64
    OG                 float64
    RÖSTER GILTIGA       int64
    RÖSTANDE             int64
    RÖSTBERÄTTIGADE      int64
    VALDELTAGANDE      float64
    dtype: object

``` python
raw.dtypes
```

    LÄNSKOD              int64
    KOMMUNKOD            int64
    LÄNSNAMN               str
    KOMMUNNAMN             str
    M                  float64
    C                  float64
    L                  float64
    KD                 float64
    S                  float64
    V                  float64
    MP                 float64
    SD                 float64
    FI                 float64
    AfS                float64
    BASIP              float64
    CSIS               float64
    DD                 float64
    DjuP               float64
    EAP                float64
    ENH                float64
    FHS                float64
    Gup                float64
    INI                float64
    KLP                float64
    KrVP               float64
    LPo                float64
    MED                float64
    NMR                float64
    NORRP              float64
    NYREF              float64
    PP                 float64
    RNP                float64
    S-FRP              float64
    SKP                float64
    SKÅ                float64
    TRP                float64
    VL-S               float64
    ÖVR                float64
    OGEJ               float64
    BLANK              float64
    OG                 float64
    RÖSTER GILTIGA       int64
    RÖSTANDE             int64
    RÖSTBERÄTTIGADE      int64
    VALDELTAGANDE      float64
    dtype: object

``` python
raw.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|  | LÄNSKOD | KOMMUNKOD | LÄNSNAMN | KOMMUNNAMN | M | C | L | KD | S | V | ... | TRP | VL-S | ÖVR | OGEJ | BLANK | OG | RÖSTER GILTIGA | RÖSTANDE | RÖSTBERÄTTIGADE | VALDELTAGANDE |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | 1 | 14 | Stockholms län | Upplands Väsby | 23.11 | 6.26 | 5.66 | 6.71 | 26.97 | 8.01 | ... | NaN | NaN | NaN | 0.04 | 0.69 | 0.06 | 25830 | 26036 | 30740 | 84.70 |
| 1 | 1 | 15 | Stockholms län | Vallentuna | 28.29 | 10.11 | 7.73 | 7.58 | 18.91 | 4.47 | ... | 0.0 | NaN | 0.00 | 0.02 | 0.59 | 0.08 | 20952 | 21099 | 23438 | 90.02 |
| 2 | 1 | 17 | Stockholms län | Österåker | 29.68 | 9.35 | 7.48 | 7.13 | 19.71 | 4.97 | ... | NaN | NaN | 0.01 | 0.03 | 0.69 | 0.13 | 27711 | 27947 | 31309 | 89.26 |
| 3 | 1 | 20 | Stockholms län | Värmdö | 27.49 | 9.76 | 6.40 | 5.89 | 20.48 | 6.02 | ... | NaN | NaN | 0.01 | 0.04 | 0.67 | 0.07 | 28115 | 28335 | 31371 | 90.32 |
| 4 | 1 | 23 | Stockholms län | Järfälla | 23.96 | 6.31 | 6.04 | 6.29 | 27.68 | 8.75 | ... | 0.0 | NaN | 0.02 | 0.04 | 0.53 | 0.07 | 45654 | 45948 | 53230 | 86.32 |

<p>5 rows × 45 columns</p>
</div>

``` python
votes = (
  raw.rename(columns={
    "LÄNSNAMN": "county", "KOMMUNNAMN": "municipality",
    "RÖSTANDE": "voters", "RÖSTBERÄTTIGADE": "electorate",
    "VALDELTAGANDE": "turnout"
  })[["county", "municipality", "voters", "electorate", "turnout"]]
  .assign(county=lambda d: d["county"].str.removesuffix("s län"))
)

votes.tail()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | county     | municipality | voters | electorate | turnout |
|-----|------------|--------------|--------|------------|---------|
| 285 | Norrbotten | Luleå        | 53589  | 60185      | 89.04   |
| 286 | Norrbotten | Piteå        | 29719  | 33094      | 89.80   |
| 287 | Norrbotten | Boden        | 19291  | 21934      | 87.95   |
| 288 | Norrbotten | Haparanda    | 4454   | 6120       | 72.78   |
| 289 | Norrbotten | Kiruna       | 14991  | 17468      | 85.82   |

</div>

``` python
votes: pd.DataFrame = votes.assign(check = 100* votes["voters"]/votes["electorate"])
(votes["check"] - votes["turnout"]).abs().max()
```

    np.float64(0.00498599439777081)

``` python
votes.sort_values("turnout").head(3)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | county     | municipality | voters | electorate | turnout | check     |
|-----|------------|--------------|--------|------------|---------|-----------|
| 288 | Norrbotten | Haparanda    | 4454   | 6120       | 72.78   | 72.777778 |
| 17  | Stockholm  | Södertälje   | 48684  | 62783      | 77.54   | 77.543284 |
| 7   | Stockholm  | Botkyrka     | 45719  | 58436      | 78.24   | 78.237730 |

</div>
