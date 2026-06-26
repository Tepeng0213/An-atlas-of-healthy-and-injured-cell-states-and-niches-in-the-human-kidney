# Kidney Atlas 论文复现

复现 [Lake et al., Nature 2023](https://doi.org/10.1038/s41586-023-05769-3) — *An atlas of healthy and injured cell states and niches in the human kidney* 的论文图表。

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Tepeng0213/An-atlas-of-healthy-and-injured-cell-states-and-niches-in-the-human-kidney/blob/main/human_kidney_scrna_atlas_reproduction.ipynb)

## 仓库内容

| 路径 | 说明 |
|------|------|
| `human_kidney_scrna_atlas_reproduction.ipynb` | 主 notebook（Figure 1–3、2d 等） |
| `kidney_atlas_paths.py` | Colab / RunPod / 本地 统一路径 |
| `runpod/` | RunPod 初始化、Drive 迁移、Cursor SSH 说明 |
| `figures/` | 复现产出图 |
| `requirements.txt` | Python 依赖 |

## 推荐：RunPod + Cursor（主工作流）

1. **创建 RunPod**：建议 Network Volume 挂载到 `/workspace`（≥250 GB），模板选 CPU 大内存或带 GPU 均可（当前 pipeline 主要用 CPU/RAM）。
2. **Pod 内首次初始化**：
   ```bash
   export KIDNEY_ATLAS_ROOT=/workspace/kidney-atlas
   bash runpod/setup.sh
   ```
3. **从 Google Drive 同步 Colab 缓存**（可选，跳过重复下载）：
   ```bash
   rclone config   # 一次性配置 gdrive remote
   bash runpod/migrate_from_gdrive.sh
   ```
4. **Cursor Remote-SSH**：见 [`runpod/CURSOR_SSH.md`](runpod/CURSOR_SSH.md)，打开 `/workspace/kidney-atlas`，运行 notebook 模块 0 → 1b → 后续模块。
5. **GitHub**：在 Pod 或 Cursor 内 `git pull` / `git push` 同步代码；`data/` 与 `figures/` 不进 git，留在 Volume。

环境变量（可选）：

```bash
export KIDNEY_ATLAS_ROOT=/workspace/kidney-atlas
```

## 备选：Google Colab

1. 点击上方 **Open in Colab**
2. **Runtime → Run all**（或按模块依次运行）
3. 模块 0 挂载 Drive；路径自动指向 `MyDrive/human-kidney-scrna-atlas-reproduction`

## 数据来源

| 来源 | 链接 |
|------|------|
| KPMP Atlas | https://www.kpmp.org/doi-collection/10-48698-3z31-8924 |
| CZ CELLxGENE | https://cellxgene.cziscience.com/ |
| CAP | https://celltype.info/project/588 |
| 原始代码 | https://github.com/KPMP/Cell-State-Atlas-2022 |

## 引用

```bibtex
@article{lake2023atlas,
  title={An atlas of healthy and injured cell states and niches in the human kidney},
  author={Lake, Blue B and others},
  journal={Nature},
  volume={619},
  pages={585--594},
  year={2023},
  doi={10.1038/s41586-023-05769-3}
}
```

## License

MIT
