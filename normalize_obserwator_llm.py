"""
Utility to normalize the `variable` names inside forecasts_json for
obserwatorfinansowy_llm_extracted.csv.

It maps common Polish/English synonyms to the canonical set used in the
analysis code: gdp, unemployment, inflation, interest_rate, deficit,
public_debt, fx, wages. Unknown variables are dropped.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Optional

import pandas as pd

SRC = Path("obserwatorfinansowy_llm_extracted.csv")
DEST = Path("obserwatorfinansowy_llm_extracted_clean.csv")


def normalize_var(raw: str) -> Optional[str]:
    """Map messy variable labels to canonical ones."""
    v = (raw or "").strip().lower()

    if any(key in v for key in ("pkb", "gdp")):
        return "gdp"
    if "bezroboc" in v or "unemployment" in v:
        return "unemployment"
    if "inflac" in v or "hicp" in v:
        return "inflation"
    if "stopa" in v and "procent" in v or "interest" in v:
        return "interest_rate"
    if "deficyt" in v or "budget balance" in v or "deficit" in v:
        return "deficit"
    if "dług" in v or "public debt" in v or ("debt" in v and "public" in v):
        return "public_debt"
    if "kurs" in v or "fx" in v or "exchange rate" in v:
        return "fx"
    if "płac" in v or "wyna" in v or "wages" in v:
        return "wages"

    return None


def clean_forecasts(raw_json: str) -> str:
    """Return cleaned forecasts_json with normalized variables."""
    try:
        items = json.loads(raw_json)
    except Exception:
        return "[]"

    cleaned = []
    for item in items:
        if not isinstance(item, dict):
            continue
        norm = normalize_var(str(item.get("variable", "")))
        if not norm:
            continue
        new_item = dict(item)
        new_item["variable"] = norm
        cleaned.append(new_item)

    return json.dumps(cleaned, ensure_ascii=False)


def main() -> None:
    df = pd.read_csv(SRC)
    df["forecasts_json"] = df["forecasts_json"].fillna("[]").apply(clean_forecasts)
    df.to_csv(DEST, index=False)

    # Quick sanity report.
    counter = Counter()
    for raw in df["forecasts_json"]:
        try:
            for item in json.loads(raw):
                counter[item.get("variable")] += 1
        except Exception:
            continue
    print("Saved cleaned file to", DEST)
    print("Variable counts:", counter)


if __name__ == "__main__":
    main()
