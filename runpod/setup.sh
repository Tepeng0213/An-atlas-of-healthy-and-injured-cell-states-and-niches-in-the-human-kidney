#!/usr/bin/env bash
# RunPod 首次初始化：克隆 GitHub、安装 Python/R 依赖、创建目录
set -euo pipefail

PROJECT="${KIDNEY_ATLAS_ROOT:-/workspace/kidney-atlas}"
REPO="${KIDNEY_ATLAS_REPO:-https://github.com/Tepeng0213/An-atlas-of-healthy-and-injured-cell-states-and-niches-in-the-human-kidney.git}"

echo "==> 项目目录: $PROJECT"
mkdir -p "$(dirname "$PROJECT")"

if [[ ! -d "$PROJECT/.git" ]]; then
  echo "==> 克隆 GitHub 仓库..."
  git clone "$REPO" "$PROJECT"
else
  echo "==> 仓库已存在，拉取最新..."
  git -C "$PROJECT" pull --ff-only || true
fi

export KIDNEY_ATLAS_ROOT="$PROJECT"
cd "$PROJECT"

echo "==> Python 依赖..."
python3 -m pip install -q -U pip
python3 -m pip install -q -r requirements.txt pyarrow scikit-learn rdata

echo "==> 创建 data/ figures/ 目录..."
python3 -c "import kidney_atlas_paths as k; k.setup_project_dirs(); k.print_paths()"

if ! command -v Rscript >/dev/null 2>&1; then
  echo "==> 安装 R（Seurat TransferData 需要）..."
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq r-base r-base-dev libcurl4-openssl-dev libssl-dev libxml2-dev
fi

echo "==> 安装 Seurat R 包（首次较慢）..."
Rscript -e "
  pkgs <- c('Seurat','Matrix','sp')
  miss <- pkgs[!sapply(pkgs, requireNamespace, quietly=TRUE)]
  if (length(miss)) install.packages(miss, repos='https://cloud.r-project.org')
  cat('Seurat OK\n')
"

echo ""
echo "完成。下一步："
echo "  1. 迁移 Google Drive 数据: bash runpod/migrate_from_gdrive.sh"
echo "  2. Cursor SSH 连接本 Pod，打开文件夹: $PROJECT"
echo "  3. 在 notebook 模块 0→1b 后按模块运行"
