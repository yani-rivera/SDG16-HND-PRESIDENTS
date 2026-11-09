"""Usage: python -m presidents_viz config.toml"""
import csv, sys, tomllib
from pathlib import Path
from .io import read_terms, read_geojson, write_json
from .clean import terms_to_records
from .validate import check, norm
from .geo import departments, neighbors
from .provenance import record


def run(cfg_path):
    base = Path(cfg_path).parent
    cfg = tomllib.loads(Path(cfg_path).read_text())
    i = cfg["input"]
    out = base / cfg["output"]["dir"]
    out.mkdir(parents=True, exist_ok=True)

    recs = terms_to_records(read_terms(base / i["workbook"], i["sheet"]))
    dep = departments(read_geojson(base / i["departments"]))
    names = [f["properties"]["name"] for f in dep["features"]]
    unknown = cfg["unknown"]
    for r in recs:
        r["dept_key"] = norm(r["department"]) if r["country_of_birth"] == "Honduras" and r["department"] not in unknown["labels"] else None
        r["person_key"] = norm(r["name"])
    issues = check(recs, names, unknown["labels"])

    countries = cfg["countries"]["birth"] + cfg["countries"]["context"]
    nb = neighbors(base / i["neighbors_topojson"], countries)

    prov = record({"workbook": base / i["workbook"], "departments": base / i["departments"],
                   "neighbors": base / i["neighbors_topojson"]}, cfg)
    write_json({"terms": recs, "issues": issues, "provenance": prov}, out / "presidents.json")
    write_json(dep, out / "departments.geojson")
    write_json(nb, out / "neighbors.geojson")
    with open(out / "quality_report.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["seq", "field", "issue"]); w.writeheader(); w.writerows(issues)
    print(f"{len(recs)} terms, {len(issues)} issues, {len(nb['features'])} neighbor countries -> {out}")
    for x in issues:
        print("  ", x)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    run(sys.argv[1])
