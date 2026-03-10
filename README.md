# Volcanoes and Crisis

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## What is this?

This repository investigates how large volcanic eruptions affect human societies across history. Using geospatial data on historical polities (Cliopatria), volcanic eruption records, and two crisis datasets from the Seshat Global History Databank, we test whether societies in closer proximity to major eruptions experienced more crises, more severe outcomes, and different types of societal stress.

The analysis has two tracks:
- **Global**: 169 crisis cases from the Seshat Crisis Consequences dataset across many polities worldwide
- **Egypt**: Egyptian power transitions from ~3000 BCE to the modern era, using a detailed regional dataset from Seshat

## Data

Data files live in `data/`. Most are included in the repo, but the Cliopatria geospatial file must be downloaded separately (too large for GitHub):

| File | Source | Notes |
|------|--------|-------|
| `cliopatria_polities_only.geojson` | [Zenodo](https://zenodo.org/records/14714684) | **Download manually** — polygon boundaries for historical polities |
| `CrisisConsequencesData_NavigatingPolycrisis_2023.03.csv` | Seshat / Navigating Polycrisis project | Crisis outcomes for 169 polity-crisis pairs |
| `EgyptPT Data.csv` | Seshat Databank | Egyptian power transitions with regime-change metadata |
| `volcano_list.csv` | NOAA / compiled | Large eruptions (VEI ≥ 6) over the last ~6000 years with coordinates |

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for environment management.

```bash
# Clone the repo
git clone https://github.com/your-org/volcanoes_and_crisis.git
cd volcanoes_and_crisis

# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Download Cliopatria data manually and place in data/
# https://zenodo.org/records/14714684
```

## Usage

All analysis logic lives in `src/`. To explore the full analysis narrative:

```bash
jupyter notebook "notebooks/Volcano Crisis Analysis.ipynb"
```

To run tests:

```bash
pytest tests/
```

## Repository Structure

```
volcanoes_and_crisis/
├── data/                  # Input data (Cliopatria must be downloaded separately)
├── src/                   # Python modules with all analysis logic
├── notebooks/             # Jupyter notebooks for exploration and visualization
├── tests/                 # pytest tests
├── results/               # Output plots and result CSVs
├── requirements.txt       # Python dependencies
└── CLAUDE.md              # Coding conventions and project context for AI assistants
```

## License

[Apache 2.0](LICENSE)
