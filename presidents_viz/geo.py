"""Boundary layers for the page."""
import os, subprocess, json
from .validate import norm


def departments(gj):
    feats = []
    for f in gj["features"]:
        p = f["properties"]
        feats.append({"type": "Feature", "geometry": _round(f["geometry"]),
                      "properties": {"name": p["shapeName"], "iso": p["shapeISO"], "key": norm(p["shapeName"])}})
    return {"type": "FeatureCollection", "features": feats}


def neighbors(topo_path, names):
    """Extract named countries from Natural Earth TopoJSON with topojson-client (node)."""
    script = (
        "const tc=require(process.argv[1]);const t=require(process.argv[2]);"
        "const want=new Set(JSON.parse(process.argv[3]));"
        "const fc=tc.feature(t,t.objects.countries);"
        "fc.features=fc.features.filter(f=>want.has(f.properties.name));"
        "process.stdout.write(JSON.stringify(fc));"
    )
    mod = os.environ.get("TOPOJSON_CLIENT", "topojson-client")
    out = subprocess.run(["node", "-e", script, mod, os.path.abspath(topo_path), json.dumps(names)],
                         capture_output=True, text=True, check=True).stdout
    fc = json.loads(out)
    for f in fc["features"]:
        f["geometry"] = _round(f["geometry"])
        f["properties"] = {"name": f["properties"]["name"]}
    return fc


def _round(g, nd=4):
    def r(c):
        return [round(c[0], nd), round(c[1], nd)] if isinstance(c[0], (int, float)) else [r(x) for x in c]
    return {"type": g["type"], "coordinates": r(g["coordinates"])}
