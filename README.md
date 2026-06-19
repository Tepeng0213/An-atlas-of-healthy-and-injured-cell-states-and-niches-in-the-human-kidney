# Kidney Atlas 论文复现

复现 [Lake et al., Nature 2023](https://doi.org/10.1038/s41586-023-05769-3) — *An atlas of healthy and injured cell states and niches in the human kidney* 的论文图表。

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Tepeng0213/An-atlas-of-healthy-and-injured-cell-states-and-niches-in-the-human-kidney/blob/main/kidney_atlas_reproduction.ipynb)

## 仓库内容

| 路径 | 说明 |
|------|------|
| `kidney_atlas_reproduction.ipynb` | **唯一** Colab notebook，包含全部复现代码（分模块） |
| `figures/` | 复现产出图 |
| `requirements.txt` | Python 依赖 |

## 快速开始

1. 点击上方 **Open in Colab**
2. **Runtime → Run all**（或按模块依次运行）
3. 在 notebook「模块 1」中配置数据路径（Google Drive 或本地上传）

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
