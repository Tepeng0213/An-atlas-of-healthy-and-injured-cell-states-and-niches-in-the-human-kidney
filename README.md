# Kidney Atlas Figure Reproduction

复现 [Lake et al., Nature 2023](https://doi.org/10.1038/s41586-023-05769-3) — *An atlas of healthy and injured cell states and niches in the human kidney* 的论文图表。

**GitHub 仓库**：[Tepeng0213/An-atlas-of-healthy-and-injured-cell-states-and-niches-in-the-human-kidney](https://github.com/Tepeng0213/An-atlas-of-healthy-and-injured-cell-states-and-niches-in-the-human-kidney)

本项目支持 **两种工作流自由切换**：

| 方式 | 用途 |
|------|------|
| **Cursor + Colab MCP** | AI 在 Colab 云端自动写代码、执行、调参 |
| **GitHub + Colab 网页** | 手动运行 notebook，稳定可视化，适合作品集展示 |

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Tepeng0213/An-atlas-of-healthy-and-injured-cell-states-and-niches-in-the-human-kidney/blob/main/notebooks/00_setup_colab.ipynb)

## 项目结构

```
├── .cursor/mcp.json          # Cursor ↔ Colab MCP 配置
├── notebooks/
│   ├── 00_setup_colab.ipynb  # Colab 环境初始化
│   ├── 01_data_loading.ipynb # 数据加载
│   └── 02_figure1_umap.ipynb # Figure 1 骨架
├── src/                      # 可复用 Python 模块
├── figures/                  # 输出图片
├── data/                     # 数据目录（大文件不入库）
├── docs/WORKFLOW.md          # 双工作流切换指南
└── requirements.txt
```

## 快速开始

### 方式 A：Colab 网页（推荐首次验证）

1. 点击上方 **Open in Colab** 徽章
2. 依次运行 `00` → `01` → `02`

### 方式 B：Cursor + Colab MCP

1. 运行本地初始化脚本：

   ```bash
   bash scripts/setup_local.sh
   ```

2. **重启 Cursor**（加载 `.cursor/mcp.json`）
3. 在 Cursor 对话中说：「连接 Colab，打开 `00_setup_colab.ipynb` 并运行」
4. 首次使用会弹出 Google OAuth 授权

详细切换说明见 [docs/WORKFLOW.md](docs/WORKFLOW.md)。

## 数据下载

| 来源 | 链接 |
|------|------|
| KPMP Atlas | https://www.kpmp.org/doi-collection/10-48698-3z31-8924 |
| CZ CELLxGENE | https://cellxgene.cziscience.com/ |
| CAP | https://celltype.info/project/588 |
| 原始代码 | https://github.com/KPMP/Cell-State-Atlas-2022 |

建议将 `.h5ad` 放在 Google Drive，在 Colab 中挂载后读取（见 `00_setup_colab.ipynb`）。

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

MIT — 分析代码可自由使用；数据请遵循 KPMP / 各数据平台的原始许可。
