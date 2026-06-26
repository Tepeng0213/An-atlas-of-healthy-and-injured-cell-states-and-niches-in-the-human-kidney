# RunPod 迁移清单

从 **Colab + Google Drive** 迁到 **RunPod + Cursor SSH** 的逐步操作。

## 前置

| 项目 | 建议 |
|------|------|
| RunPod Volume | 挂载到 `/workspace`，≥250 GB |
| Pod 规格 | 125 GB RAM / 32 vCPU 足够 Fig.1–3；GPU 非必需 |
| SSH 公钥 | 加到 RunPod 账户 → Settings → SSH Public Keys |
| GitHub | 仓库 push 权限（Pod 内 git push 需 SSH key 或 token） |

## 步骤 1 — 启动 Pod 并 SSH 登录

RunPod 控制台 → Connect → **SSH over exposed TCP**，记下 Host 与 Port。

本地 `~/.ssh/config` 见 [CURSOR_SSH.md](./CURSOR_SSH.md)。

## 步骤 2 — 克隆仓库并装环境

```bash
export KIDNEY_ATLAS_ROOT=/workspace/kidney-atlas
cd /workspace
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Tepeng0213/An-atlas-of-healthy-and-injured-cell-states-and-niches-in-the-human-kidney/main/runpod/setup.sh)" \
  || git clone https://github.com/Tepeng0213/An-atlas-of-healthy-and-injured-cell-states-and-niches-in-the-human-kidney.git "$KIDNEY_ATLAS_ROOT" && bash "$KIDNEY_ATLAS_ROOT/runpod/setup.sh"
```

若仓库尚未 push 最新代码，可先在 Pod 上 `git clone` 后 `scp` 本地文件，或 push 后再 `git pull`。

## 步骤 3 — 同步 Google Drive 数据

Colab 项目路径：`MyDrive/human-kidney-scrna-atlas-reproduction/`

```bash
# 安装并配置 rclone（首次）
rclone config
# name: gdrive, type: drive, 按提示 OAuth

export KIDNEY_ATLAS_ROOT=/workspace/kidney-atlas
bash /workspace/kidney-atlas/runpod/migrate_from_gdrive.sh
```

**优先同步的缓存**（有则可跳过大量重算）：

- `data/processed/fig1_umap_light.h5ad`
- `data/processed/fig2b_sn_light.h5ad`
- `data/processed/fig2f_visium_raw.h5ad`
- `data/processed/fig3c_subclass_scores/`（23 个 parquet）
- `data/processed/fig2d_spots_master.parquet`
- `figures/figure2d_dotplot.png`

若只同步 processed，可：

```bash
rclone sync gdrive:human-kidney-scrna-atlas-reproduction/data/processed \
  /workspace/kidney-atlas/data/processed --progress
```

## 步骤 4 — Cursor 连接

1. Cursor → Remote-SSH → `runpod-kidney`
2. 打开 `/workspace/kidney-atlas`
3. 打开 `human_kidney_scrna_atlas_reproduction.ipynb`
4. 选 Python 3 内核，运行 **模块 0 → 1a → 1b**

`kidney_atlas_paths.py` 会自动识别 RunPod，打印 `Runtime: runpod`。

## 步骤 5 — 继续复现

| 已有缓存 | 可跳过 |
|----------|--------|
| fig3c 23 样本 scores | 10c/10d |
| fig2f_visium_raw.h5ad | 7c 大部分 |
| fig2d_spots_master.parquet | 11a |

直接跑 **11b → 11c** 重绘 Figure 2d，或从 Figure 3 模块继续。

## 步骤 6 — GitHub 同步

```bash
cd /workspace/kidney-atlas
git pull
# 修改后
git status
git add human_kidney_scrna_atlas_reproduction.ipynb kidney_atlas_paths.py
git commit -m "..."
git push
```

`data/`、`figures/` 在 `.gitignore`，只留在 Volume。

## 故障排查

| 问题 | 处理 |
|------|------|
| 盘满 | 删 `data/raw/**/*.tar.gz` 解压后；Slide-seq 勿一次下 67 puck |
| Seurat 缺包 | `Rscript -e "install.packages('Seurat')"` |
| 路径不对 | `export KIDNEY_ATLAS_ROOT=/workspace/kidney-atlas` |
| notebook 找不到 kap | 确保在项目根运行，或模块 1b 已执行 |

## 不再依赖

- Colab MCP / Drive 挂载（可选保留 Colab 作为备份）
- `/content/drive/MyDrive/...` 硬编码（已改为 `kidney_atlas_paths`）
