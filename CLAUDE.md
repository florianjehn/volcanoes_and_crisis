# CLAUDE.md — Volcanoes and Crisis

## Project Overview

This project analyzes how volcanic eruptions impact human societies across history. The core question: **do societies closer to large volcanic eruptions experience more crises, and do outcomes differ by proximity?**

The analysis is done in two tracks:
1. **Global track**: using the Seshat Crisis Consequences dataset (general crises across many polities worldwide)
2. **Egypt track**: using Egyptian power-transition data (same structure as similar regional files for other civilizations)

The Cliopatria geospatial dataset provides polygon geometries for historical polities, allowing proximity calculations between eruptions and societies.

## Data Sources

All data files live in `data/`. The `data/` folder is **not committed to git** (too large).

| File | Description |
|------|-------------|
| `cliopatria_polities_only.geojson` | Cliopatria geo-polygons for historical polities — **must be downloaded separately** from [Zenodo](https://zenodo.org/records/14714684) |
| `CrisisConsequencesData_NavigatingPolycrisis_2023.03.csv` | Seshat crisis consequences data (169 crises across many polities, with crisis type, severity, and outcomes) |
| `EgyptPT Data.csv` | Egyptian power transitions with regime-change metadata (same structure as other regional PT files from Seshat) |
| `volcano_list.csv` | Large volcanic eruptions (VEI ≥ 6) over the last several thousand years with lat/lon, year, and impact data |

### Key Column Notes

**CrisisConsequencesData**: `Polity.Name`, `Polity.Date.From`, `Polity.Date.To`, `Polity.Continent`, `Crisis.Period`, outcome columns (`decline`, `collapse`, `epidemic`, `downw.mob`, `extermination`, `uprising`, `civil.war`, `century.plus`, `fragmentation`, `conquest`, `assassin`, `depose`), `Severity`

**EgyptPT Data**: `Region`, `CultureGroup`, `MacroPolity`, `PolID`, `Start.reign.predecessor`, `End.reign.Transition`, `Overturn`, `Assassination.Predecessor`, `Intra.elite`, `Military.revolt`, `Popular.uprising`, `Separatist.rebellion`, `External.invasion`, `External.interference`

**volcano_list.csv**: `Year`, `Name`, `Location`, `Country`, `Latitude`, `Longitude`, `Elevation (m)`, `VEI`, `Deaths`, `Total Deaths`

**cliopatria_polities_only.geojson**: `Name`, `FromYear`, `ToYear`, `Area`, `Type`, `SeshatID` — polygon geometries in WGS84 (CRS84)

## Analysis Approach

1. **Spatial join**: For each crisis/transition event, identify which volcanic eruptions occurred within a configurable time window (e.g., ±50 years) and compute the distance from the polity centroid (or polygon) to the nearest eruption.
2. **Distance bands**: Classify societies as "near" / "far" from eruptions using distance thresholds.
3. **Outcome comparison**: Compare crisis frequencies, severity scores, and specific outcome types (collapse, civil war, etc.) between near and far groups.
4. **Two-track analysis**: Run the above separately for the Seshat global dataset and the Egypt PT dataset.
5. **Notebook**: Compile all findings into a clean, narrative Jupyter notebook.

## Coding Conventions

### Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) strictly. Code is auto-formatted with **black** and checked with **flake8** (without E203).
- All functions must have docstrings in this format:
  ```python
  def my_function(arg1, arg2):
      """
      One-line summary.

      Arguments:
          arg1 (type): description
          arg2 (type): description

      Returns:
          type: description
      """
  ```
- Write decoupled code — functions do exactly one thing and are as short as possible.
- **Delete dead code.** Never comment out unused code; use git to recover it.

### Naming
- `snake_case` for variables and module files (e.g., `volcano_distance.py`)
- `CamelCase` for class names (e.g., `PolityMatcher`)
- `Camel Case With Spaces` for Jupyter notebook filenames (e.g., `Volcano Crisis Analysis.ipynb`)

### Structure
- **Jupyter Notebooks** are for explanation and visualization only. All logic lives in `.py` files in `src/`.
- Tests go in `tests/` using **pytest**. Every non-trivial function should have an assert-based test.
- Results (plots, CSVs) go in `results/`.

### Plotting
- Use the ALLFED matplotlib style:
  ```python
  plt.style.use("https://raw.githubusercontent.com/allfed/ALLFED-matplotlib-style-sheet/main/ALLFED.mplstyle")
  ```
- For maps, use the **Winkel Tripel projection**: reproject geopandas CRS to `+proj=wintri`.
  ```python
  def plot_winkel_tripel_map(ax):
      import geopandas as gpd
      border_geojson = gpd.read_file('https://raw.githubusercontent.com/ALLFED/ALLFED-map-border/main/border.geojson')
      border_geojson.plot(ax=ax, edgecolor='black', linewidth=0.1, facecolor='none')
      ax.set_axis_off()
  ```
  Note: Winkel Tripel is visual only — do distance calculations in an appropriate equal-area or equidistant CRS, not in Winkel Tripel.

## Environment

Always work in a virtual environment managed by **uv** (not conda).

```bash
# Create environment
uv venv

# Activate
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Add a new dependency
uv pip install <package>
# then update requirements.txt
```

## License

Apache 2.0 — see `LICENSE`.
