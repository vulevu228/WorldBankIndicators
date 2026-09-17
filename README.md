# World Bank Health Indicators

Global health outcomes across 217 countries (1960–2024), pulled directly from
the [World Bank Indicators API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392)
— no API key or account required.

## Why health

This project is a deliberate pivot toward worldwide-scale datasets, following
[GBIFBiodiversityTracker](https://github.com/vulevu228/GBIFBiodiversityTracker).
Health outcomes are universally relatable, have decades of consistent
country-level reporting, and sit outside this portfolio's existing
weather/climate/energy cluster.

## Indicators

| Code | Indicator |
|---|---|
| `SP.DYN.LE00.IN` | Life expectancy at birth (years) |
| `SH.DYN.MORT` | Under-5 mortality rate (per 1,000 live births) |
| `SH.STA.MMRT` | Maternal mortality ratio (per 100,000 live births) |
| `SH.XPD.CHEX.GD.ZS` | Current health expenditure (% of GDP) |
| `SH.MED.PHYS.ZS` | Physicians (per 1,000 people) |
| `SP.DYN.TFRT.IN` | Fertility rate (births per woman) |
| `SH.DYN.AIDS.ZS` | HIV prevalence, ages 15-49 (%) |
| `SH.TBS.INCD` | Tuberculosis incidence (per 100,000 people) |
| `SH.IMM.MEAS` | Measles immunization (% of children ages 12-23 months) |

## Data

- `data/health_indicators.csv` — tidy long-format panel: one row per
  country/indicator/year (~76,000 rows).
- Aggregate entities (World, income-group buckets, EU, etc.) are excluded —
  only actual countries are included, using the World Bank country list's
  `region` field to tell them apart.

## Pipeline

```
pip install -r requirements.txt
python scripts/fetch_indicators.py
```

Fetches the full history for each indicator across all real countries and
writes `data/health_indicators.csv`.

## Source

World Bank Open Data / World Development Indicators.
https://data.worldbank.org/
