#!/usr/bin/env python3
"""Patch notebook for RunPod + unified paths."""
import json
from pathlib import Path

NB = Path(__file__).resolve().parent.parent / "human_kidney_scrna_atlas_reproduction.ipynb"
OLD_ROOT = "/content/drive/MyDrive/human-kidney-scrna-atlas-reproduction"
FALLBACK = """if 'PROCESSED_DATA_DIR' not in globals():
    import kidney_atlas_paths as kap
    kap.ensure_importable()
    kap.bind_notebook_globals(globals())
"""

nb = json.loads(NB.read_text())

# --- intro ---
intro = nb["cells"][0]["source"]
if isinstance(intro, list):
    text = "".join(intro)
    text = text.replace(
        "> **存储策略**：数据、缓存、图片、中间结果一律保存在 **Google Drive**，不使用 Colab 临时盘。",
        "> **存储策略**：数据与缓存保存在项目根目录（**RunPod** `/workspace/kidney-atlas` 或 **Colab** Google Drive）。路径由 `kidney_atlas_paths.py` 自动检测。",
    )
    nb["cells"][0]["source"] = [text]

# --- module 0 drive cell -> runtime detect ---
nb["cells"][3]["source"] = [
    "# 运行环境检测（Colab 挂载 Drive；RunPod 跳过）\n",
    "from pathlib import Path\n",
    "import os\n",
    "\n",
    "if Path('/content/drive/MyDrive').exists() or Path('/content/drive').exists():\n",
    "    try:\n",
    "        from google.colab import drive\n",
    "        if not Path('/content/drive/MyDrive').exists():\n",
    "            drive.mount('/content/drive')\n",
    "            print('Drive mounted at /content/drive')\n",
    "        else:\n",
    "            print('Drive 已挂载，跳过')\n",
    "    except ImportError:\n",
    "        print('非 Colab，跳过 Drive 挂载')\n",
    "else:\n",
    "    root = os.environ.get('KIDNEY_ATLAS_ROOT', '/workspace/kidney-atlas')\n",
    "    print('RunPod/本地模式 — 项目根:', root)\n",
    "    print('首次请运行: bash runpod/setup.sh')\n",
]

nb["cells"][4]["source"] = [
    "---\n",
    "## 模块 1 — 项目初始化\n",
    "\n",
    "创建目录结构，配置路径常量（Colab / RunPod / 本地 自动检测）。\n",
]

nb["cells"][5]["source"] = [
    "### 模块 1a — 创建目录结构\n",
    "\n",
    "**RunPod / 本地**：`mkdir` 创建 `data/`、`figures/` 等。\n",
    "\n",
    "**Colab**：可选 Google Drive API 创建（下方 `setup_project_dirs_colab()`）。\n",
]

nb["cells"][6]["source"] = [
    "# 模块 1a — 创建目录\n",
    "import kidney_atlas_paths as kap\n",
    "\n",
    "kap.setup_project_dirs()\n",
    "\n",
    "# Colab 专用：需要 Drive 网页可见目录时再运行\n",
    "def setup_project_dirs_colab():\n",
    "    \"\"\"Colab + Google Drive API（可选）。\"\"\"\n",
    "    from google.colab import auth\n",
    "    from googleapiclient.discovery import build\n",
    "    from google.auth import default\n",
    "    auth.authenticate_user()\n",
    "    creds, _ = default()\n",
    "    service = build('drive', 'v3', credentials=creds)\n",
    "    print('Colab Drive API 就绪 — 可按需扩展 create_folder 逻辑')\n",
    "\n",
    "if kap.runtime_name() == 'colab':\n",
    "    print('Colab：本地路径已 mkdir；Drive API 可选 setup_project_dirs_colab()')\n",
]

nb["cells"][7]["source"] = [
    "### 模块 1b — 路径配置\n",
    "\n",
    "加载 `kidney_atlas_paths.py`；声明 Figure 1/2 输出路径。\n",
]

nb["cells"][8]["source"] = [
    "# 模块 1b — 路径配置（Colab / RunPod / 本地）\n",
    "import kidney_atlas_paths as kap\n",
    "kap.ensure_importable()\n",
    "kap.bind_notebook_globals(globals())\n",
    "kap.print_paths()\n",
]

# --- bulk replace hardcoded drive paths ---
for cell in nb["cells"]:
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell.get("source", []))
    if OLD_ROOT not in src:
        continue
    src = src.replace(f"Path('{OLD_ROOT}')", "kap.PROJECT_ROOT")
    src = src.replace(f'Path("{OLD_ROOT}")', "kap.PROJECT_ROOT")
    src = src.replace(f"DRIVE_ROOT = Path('{OLD_ROOT}')", "kap.bind_notebook_globals(globals())")
    src = src.replace(f'DRIVE_ROOT = Path("{OLD_ROOT}")', "kap.bind_notebook_globals(globals())")
    # fix cells that set many vars from DRIVE_ROOT after bind
    if "kap.bind_notebook_globals(globals())" in src and "DATA_DIR = DRIVE_ROOT" in src:
        src = src.split("kap.bind_notebook_globals(globals())")[0] + "kap.bind_notebook_globals(globals())\n"
    if "if 'PROCESSED_DATA_DIR' not in globals():" in src:
        # replace whole fallback block start
        lines = src.splitlines()
        new_lines = []
        i = 0
        while i < len(lines):
            if lines[i].strip().startswith("if 'PROCESSED_DATA_DIR' not in globals():"):
                new_lines.append(FALLBACK.strip())
                i += 1
                while i < len(lines) and (lines[i].startswith("    ") or lines[i].strip() == ""):
                    i += 1
                continue
            new_lines.append(lines[i])
            i += 1
        src = "\n".join(new_lines)
    if "kap.PROJECT_ROOT" in src or "kap.bind_notebook_globals" in src or FALLBACK.strip() in src:
        if "import kidney_atlas_paths" not in src and "kap." in src:
            src = "import kidney_atlas_paths as kap\n" + src
    cell["source"] = [src]

NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1))
print("Patched", NB)
