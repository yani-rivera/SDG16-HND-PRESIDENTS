"""Normalize dates and fields without changing the source values."""
import datetime as dt
import math
import pandas as pd


def parse_date(v):
    """Accept datetime cells and 'dd-mm-yyyy' text; return ISO 'yyyy-mm-dd' or None."""
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    if isinstance(v, (dt.datetime, pd.Timestamp)):
        return v.strftime("%Y-%m-%d")
    s = str(v).strip()
    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None


def text(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    return str(v).strip()


def num(v):
    try:
        f = float(v)
        return None if math.isnan(f) else f
    except (TypeError, ValueError):
        return None


def terms_to_records(df):
    out = []
    for r in df.itertuples(index=False):
        out.append({
            "seq": int(r.seq),
            "name": text(r.name),
            "era": text(r.era),
            "took_office": parse_date(r.took_office),
            "left_office": parse_date(r.left_office),
            "took_office_raw": text(r.took_office),
            "left_office_raw": text(r.left_office),
            "mandate_days": num(r.mandate_days),
            "status": text(r.status),
            "party": text(r.party),
            "birthplace": text(r.birthplace),
            "department": text(r.department),
            "country_of_birth": text(r.country_of_birth),
            "code": text(r.code),
            "lat": num(r.lat),
            "lon": num(r.lon),
            "source_url": text(getattr(r, "pre_url", None)),
            "debt_end_of_term": None,   # slot for the external-debt series
        })
    return out
