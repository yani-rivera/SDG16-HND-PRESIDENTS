# hnd_presidents_viz

Interactive map + timeline of every Honduran head of state since 1824 (131 terms).

## Layout
```
config.toml          inputs, countries, unknown-birthplace rule, output folder
data/                source files (workbook, geoBoundaries ADM1, Natural Earth countries-50m)
presidents_viz/      Python package: io, clean, validate, geo, provenance
docs/index.html      the page (D3 7.9.0); reads docs/data/
docs/data/           built by the pipeline: presidents.json, departments.geojson, neighbors.geojson, quality_report.csv
```

## Run
```
pip install pandas openpyxl
npm i topojson-client@3.1.0        # used to extract neighbor countries
TOPOJSON_CLIENT=$(pwd)/node_modules/topojson-client python -m presidents_viz config.toml
cd docs && python3 -m http.server 8000
```

## Rules
- Source values are never rewritten; dates are parsed from both real dates and dd-mm-yyyy text.
- Unknown birthplace department -> point at the centre of Honduras (15.0, -86.3), dashed ring.
- Born abroad (Nicaragua, El Salvador, Panama) -> the country is shaded; Panama sits off the map frame and is pinned to its edge.
- Department colour = distinct people born there, counted up to the selected term.
- `presidents.json` carries provenance: script version, input SHA-256, config, UTC time.
- `debt_end_of_term` is reserved for the external-debt series.

## GitHub Pages
Settings → Pages → Deploy from a branch → `main`, folder `/docs`.
The page and its `data/` folder must stay together inside `docs/`; there must be no other `index.html` at the repo root.

## Licences
- Code: MIT.
- Terms: Wikipedia, "List of presidents of Honduras" (CC BY-SA 4.0); birthplaces researched and validated by Yanira A. Rivera.
- Departments: geoBoundaries ADM1 (CC BY 4.0). Neighbouring countries: Natural Earth (public domain).
