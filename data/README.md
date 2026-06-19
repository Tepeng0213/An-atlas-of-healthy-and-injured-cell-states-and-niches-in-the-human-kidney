# Data directory

Do **not** commit large raw/processed files to Git.

## Recommended workflow

1. Download processed `.h5ad` from [CZ CELLxGENE](https://cellxgene.cziscience.com/) or [KPMP Atlas](https://www.kpmp.org/doi-collection/10-48698-3z31-8924)
2. Place files under `data/raw/` or mount Google Drive in Colab
3. Notebooks read from `src/config.py` paths

## Suggested layout

```
data/
├── raw/          # downloaded h5ad / mtx (gitignored)
└── processed/    # intermediate AnnData objects (gitignored)
```
