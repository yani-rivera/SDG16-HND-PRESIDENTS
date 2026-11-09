"""Report data issues; never rewrite source values."""
import unicodedata


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return s.lower().strip()


def check(records, dept_names, unknown_labels):
    issues = []
    for r in records:
        if r["department"] in unknown_labels and r["code"] and r["code"].startswith("HN") and r["code"] != "HND":
            issues.append({"seq": r["seq"], "field": "code",
                           "issue": f"department unknown ('{r['department']}') but coded {r['code']}"})
    for r in records:
        if not r["took_office"]:
            issues.append({"seq": r["seq"], "field": "took_office", "issue": f"unparsed date '{r['took_office_raw']}'"})
        if r["left_office_raw"] and not r["left_office"]:
            issues.append({"seq": r["seq"], "field": "left_office", "issue": f"unparsed date '{r['left_office_raw']}'"})
        if r["country_of_birth"] == "Honduras":
            known = norm(r["department"]) in {norm(n) for n in dept_names}
            if not known and r["department"] not in unknown_labels:
                issues.append({"seq": r["seq"], "field": "department", "issue": f"no polygon named '{r['department']}'"})
            if known and r["code"] == "HND":
                issues.append({"seq": r["seq"], "field": "code", "issue": f"department '{r['department']}' coded HND (unknown)"})
        if r["lat"] is None or r["lon"] is None:
            issues.append({"seq": r["seq"], "field": "lat/lon", "issue": "missing coordinates"})
    return issues
