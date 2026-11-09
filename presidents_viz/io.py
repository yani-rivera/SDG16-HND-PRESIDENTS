"""Read the presidents workbook and boundary files."""
import json
import pandas as pd


def read_terms(path, sheet):
    return pd.read_excel(path, sheet_name=sheet)


def read_geojson(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
