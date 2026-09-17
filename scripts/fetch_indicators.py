"""
Pulls a curated set of World Bank Health indicators for all countries/years
via the World Bank Indicators API (no API key required) and writes a single
tidy long-format CSV to data/health_indicators.csv.

API docs: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
"""

import csv
import time
from pathlib import Path

import requests

BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/{code}"
COUNTRY_LIST_URL = "https://api.worldbank.org/v2/country"
PER_PAGE = 20000

INDICATORS = {
    "SP.DYN.LE00.IN": "Life expectancy at birth (years)",
    "SH.DYN.MORT": "Under-5 mortality rate (per 1,000 live births)",
    "SH.STA.MMRT": "Maternal mortality ratio (per 100,000 live births)",
    "SH.XPD.CHEX.GD.ZS": "Current health expenditure (% of GDP)",
    "SH.MED.PHYS.ZS": "Physicians (per 1,000 people)",
    "SP.DYN.TFRT.IN": "Fertility rate (births per woman)",
    "SH.DYN.AIDS.ZS": "HIV prevalence, ages 15-49 (%)",
    "SH.TBS.INCD": "Tuberculosis incidence (per 100,000 people)",
    "SH.IMM.MEAS": "Measles immunization (% of children ages 12-23 months)",
}

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "health_indicators.csv"


def fetch_real_country_codes() -> set[str]:
    """World Bank's country/all list mixes real countries with aggregates
    (World, income-group buckets, EU, etc). Aggregates have region.value
    == "Aggregates"; real countries have an actual region name."""
    resp = requests.get(COUNTRY_LIST_URL, params={"format": "json", "per_page": 400}, timeout=60)
    resp.raise_for_status()
    _, rows = resp.json()
    return {row["id"] for row in rows if row["region"]["value"] != "Aggregates"}


def fetch_indicator(code: str, valid_codes: set[str]) -> list[dict]:
    records = []
    page = 1
    while True:
        resp = requests.get(
            BASE_URL.format(code=code),
            params={"format": "json", "per_page": PER_PAGE, "page": page},
            timeout=60,
        )
        resp.raise_for_status()
        payload = resp.json()

        if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
            break

        meta, rows = payload
        for row in rows:
            if row.get("value") is None:
                continue
            if row["countryiso3code"] not in valid_codes:
                continue
            records.append(
                {
                    "country": row["country"]["value"],
                    "country_code": row["countryiso3code"],
                    "indicator_code": code,
                    "indicator_name": INDICATORS[code],
                    "year": int(row["date"]),
                    "value": float(row["value"]),
                }
            )

        if page >= meta["pages"]:
            break
        page += 1

    return records


def main() -> None:
    print("Fetching valid country list (excluding aggregates)...")
    valid_codes = fetch_real_country_codes()
    print(f"  {len(valid_codes)} real countries")

    all_records: list[dict] = []
    for code, name in INDICATORS.items():
        print(f"Fetching {code} ({name})...")
        records = fetch_indicator(code, valid_codes)
        print(f"  {len(records)} rows")
        all_records.extend(records)
        time.sleep(0.5)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["country", "country_code", "indicator_code", "indicator_name", "year", "value"],
        )
        writer.writeheader()
        writer.writerows(all_records)

    print(f"\nWrote {len(all_records)} total rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
