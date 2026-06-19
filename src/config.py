"""Project-wide paths and constants."""

from pathlib import Path

# Repo root (works in local dev and Colab after cloning)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FIGURES_DIR = PROJECT_ROOT / "figures"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Paper reference
PAPER_TITLE = (
    "An atlas of healthy and injured cell states and niches in the human kidney"
)
PAPER_DOI = "10.1038/s41586-023-05769-3"
ORIGINAL_CODE_REPO = "https://github.com/KPMP/Cell-State-Atlas-2022"

# Public data sources
DATA_SOURCES = {
    "kpmp_atlas": "https://www.kpmp.org/doi-collection/10.48698-3z31-8924",
    "cellxgene": "https://cellxgene.cziscience.com/",
    "cap": "https://celltype.info/project/588",
    "geo": "https://www.ncbi.nlm.nih.gov/geo/",
}

# Default scanpy settings
SCANPY_FIGDIR = str(FIGURES_DIR)
SCANPY_VERBOSITY = 1
