"""Colab / RunPod / 本地 统一项目路径（Lake et al. Nature 2023 复现）。"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def detect_project_root() -> Path:
    if env := os.environ.get("KIDNEY_ATLAS_ROOT"):
        return Path(env).expanduser().resolve()
    for candidate in (
        Path("/workspace/kidney-atlas"),
        Path("/runpod-volume/kidney-atlas"),
        Path("/content/drive/MyDrive/human-kidney-scrna-atlas-reproduction"),
    ):
        if candidate.exists():
            return candidate
    here = Path(__file__).resolve().parent
    if (here / "human_kidney_scrna_atlas_reproduction.ipynb").exists():
        return here
    return here


def runtime_name() -> str:
    if Path("/workspace").exists() and not Path("/content/drive").exists():
        return "runpod"
    if Path("/content/drive").exists():
        return "colab"
    return "local"


PROJECT_ROOT = detect_project_root()
DRIVE_ROOT = PROJECT_ROOT  # 兼容旧变量名
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FIGURES_DIR = PROJECT_ROOT / "figures"
CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"

CELLXGENE_DIR = RAW_DATA_DIR / "cellxgene"
GSE183279_RAW_DIR = RAW_DATA_DIR / "GSE183279_RAW"
VISIUM_DIR = RAW_DATA_DIR / "visium" / "GSE183456"
SLIDESEQ_DIR = RAW_DATA_DIR / "slideseq" / "GSE183274"

CACHED_FIG1 = PROCESSED_DATA_DIR / "fig1_umap_light.h5ad"
FIG1C_OUTPUT = FIGURES_DIR / "figure1c_labeled.png"
FIG1C_MODALITIES_OUTPUT = FIGURES_DIR / "figure1c_modalities.png"
FIG1C_COLOR_KEY = "subclass.l3"

CACHED_FIG2B = PROCESSED_DATA_DIR / "fig2b_sn_light.h5ad"
FIG2B_MAIN_OUTPUT = FIGURES_DIR / "figure2b_sncv3_celltypes.png"
FIG2B_STATES_OUTPUT = FIGURES_DIR / "figure2b_sncv3_altered_states.png"
FIG2B_REGIONS_OUTPUT = FIGURES_DIR / "figure2b_sncv3_regions.png"
FIG2B_COLOR_KEY = "subclass.l3"


def setup_project_dirs() -> None:
    """创建标准目录（RunPod / 本地用 mkdir；Colab 可选 Drive API）。"""
    dirs = [
        DATA_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        FIGURES_DIR,
        CHECKPOINT_DIR,
        CELLXGENE_DIR,
        VISIUM_DIR,
        SLIDESEQ_DIR / "pucks",
        SLIDESEQ_DIR / "metadata",
        RAW_DATA_DIR / "geo" / "GSE183277",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    readme = RAW_DATA_DIR / "README.txt"
    if not readme.exists():
        readme.write_text(
            "Place raw data here.\n"
            "- cellxgene/kidney_integrated_sc_snRNA.h5ad\n"
            "- visium/GSE183456/*.tar.gz\n"
            "- slideseq/GSE183274/pucks/*.rds.gz\n",
            encoding="utf-8",
        )
    print(f"目录已就绪 ({runtime_name()}): {PROJECT_ROOT}")


def print_paths() -> None:
    print("Runtime:           ", runtime_name())
    print("PROJECT_ROOT:      ", PROJECT_ROOT)
    print("DATA_DIR:          ", DATA_DIR)
    print("PROCESSED_DATA_DIR:", PROCESSED_DATA_DIR)
    print("FIGURES_DIR:       ", FIGURES_DIR)
    if CELLXGENE_DIR.exists():
        n = len(list(CELLXGENE_DIR.glob("*.h5ad")))
        print(f"CELLxGENE: {n} 个 h5ad")
    else:
        print("CELLxGENE 目录待创建")


def prefer_local_h5ad(src_path: Path, cache_name: str | None = None) -> Path:
    """Colab 上把 Drive 大文件复制到 /content/local_cache；RunPod/本地直接读。"""
    src_path = Path(src_path)
    if runtime_name() != "colab" or not str(src_path).startswith("/content/drive"):
        return src_path
    local_dir = Path("/content/local_cache")
    local_dir.mkdir(exist_ok=True)
    local_path = local_dir / (cache_name or src_path.name)
    if local_path.exists() and local_path.stat().st_size == src_path.stat().st_size:
        print("使用 Colab 本地副本:", local_path)
        return local_path
    print("复制到 Colab 本地盘（一次性，约 3GB 磁盘，不占 RAM）...")
    import shutil
    shutil.copy2(src_path, local_path)
    return local_path


def bind_notebook_globals(g: dict) -> None:
    """把路径常量注入 notebook global，供 `if PROCESSED_DATA_DIR not in globals()` 回退使用。"""
    keys = [
        "PROJECT_ROOT", "DRIVE_ROOT", "DATA_DIR", "RAW_DATA_DIR", "PROCESSED_DATA_DIR",
        "FIGURES_DIR", "CHECKPOINT_DIR", "CELLXGENE_DIR", "GSE183279_RAW_DIR",
        "VISIUM_DIR", "SLIDESEQ_DIR", "CACHED_FIG1", "FIG1C_OUTPUT", "FIG1C_MODALITIES_OUTPUT",
        "FIG1C_COLOR_KEY", "CACHED_FIG2B", "FIG2B_MAIN_OUTPUT", "FIG2B_STATES_OUTPUT",
        "FIG2B_REGIONS_OUTPUT", "FIG2B_COLOR_KEY",
    ]
    mod = sys.modules[__name__]
    for k in keys:
        g[k] = getattr(mod, k)


def ensure_importable() -> None:
    root = str(PROJECT_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
