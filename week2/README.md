# Week 2


``` python
import pandas as pd
import numpy as np
import matplotlib.pyplot
```

``` python
raw = pd.read_csv("election-2018-municipalities.csv", sep=";", decimal=",", encoding="utf-8-sig")
raw.head(5)
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
raw.shape
```

    (290, 45)

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
raw[["LÄNSNAMN", "KOMMUNNAMN"]]
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

|     | LÄNSNAMN        | KOMMUNNAMN     |
|-----|-----------------|----------------|
| 0   | Stockholms län  | Upplands Väsby |
| 1   | Stockholms län  | Vallentuna     |
| 2   | Stockholms län  | Österåker      |
| 3   | Stockholms län  | Värmdö         |
| 4   | Stockholms län  | Järfälla       |
| ... | ...             | ...            |
| 285 | Norrbottens län | Luleå          |
| 286 | Norrbottens län | Piteå          |
| 287 | Norrbottens län | Boden          |
| 288 | Norrbottens län | Haparanda      |
| 289 | Norrbottens län | Kiruna         |

<p>290 rows × 2 columns</p>
</div>

``` python
votes = (
    raw.rename(columns={
        "LÄNSNAMN": "county", "KOMMUNNAMN": "municipality",
        "RÖSTANDE": "voters", "RÖSTBERÄTTIGADE": "electorate",
        "VALDELTAGANDE": "turnout",
    })[["county", "municipality", "electorate", "voters", "turnout"]]
    .assign(county=lambda d: d["county"].str.removesuffix("s län") )
)

votes.head(5)
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

|     | county    | municipality   | electorate | voters | turnout |
|-----|-----------|----------------|------------|--------|---------|
| 0   | Stockholm | Upplands Väsby | 30740      | 26036  | 84.70   |
| 1   | Stockholm | Vallentuna     | 23438      | 21099  | 90.02   |
| 2   | Stockholm | Österåker      | 31309      | 27947  | 89.26   |
| 3   | Stockholm | Värmdö         | 31371      | 28335  | 90.32   |
| 4   | Stockholm | Järfälla       | 53230      | 45948  | 86.32   |

</div>

``` python
# Check validity
(votes["turnout"] - 100*(votes["voters"]/votes["electorate"])).abs().max()
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

|     | county     | municipality | electorate | voters | turnout |
|-----|------------|--------------|------------|--------|---------|
| 288 | Norrbotten | Haparanda    | 6120       | 4454   | 72.78   |
| 17  | Stockholm  | Södertälje   | 62783      | 48684  | 77.54   |
| 7   | Stockholm  | Botkyrka     | 58436      | 45719  | 78.24   |

</div>

``` python
by_county = (
    votes.groupby("county")["turnout"]
    .agg(n="size", mean="mean", median="median", sd="std")
    .sort_values("mean")
)

by_county
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

|                 | n   | mean      | median | sd       |
|-----------------|-----|-----------|--------|----------|
| county          |     |           |        |          |
| Norrbotten      | 14  | 84.326429 | 85.270 | 4.259152 |
| Västerbotten    | 15  | 85.240667 | 84.950 | 2.056889 |
| Gävleborg       | 10  | 85.578000 | 85.815 | 1.302415 |
| Jämtland        | 8   | 86.247500 | 85.505 | 1.804667 |
| Värmland        | 16  | 86.265000 | 86.115 | 2.380552 |
| Västmanland     | 10  | 86.401000 | 86.320 | 1.329649 |
| Skåne län       | 33  | 86.879697 | 86.670 | 3.122502 |
| Västernorrland  | 7   | 87.122857 | 87.300 | 1.075077 |
| Örebro län      | 12  | 87.294167 | 87.350 | 1.955870 |
| Kronoberg       | 8   | 87.403750 | 87.320 | 1.114322 |
| Dalarna         | 15  | 87.450000 | 87.080 | 1.166227 |
| Stockholm       | 26  | 87.520385 | 87.620 | 3.818309 |
| Södermanland    | 9   | 87.617778 | 88.430 | 1.752475 |
| Blekinge län    | 5   | 87.730000 | 87.790 | 1.748657 |
| Kalmar län      | 12  | 87.879167 | 88.015 | 1.703261 |
| Västra Götaland | 49  | 87.981020 | 87.970 | 1.826171 |
| Uppsala län     | 8   | 88.252500 | 87.620 | 1.606938 |
| Halland         | 6   | 88.308333 | 87.840 | 2.347913 |
| Jönköping       | 13  | 88.353846 | 88.210 | 1.961566 |
| Gotland         | 1   | 88.750000 | 88.750 | NaN      |
| Östergötland    | 13  | 88.866923 | 89.080 | 1.135726 |

</div>
