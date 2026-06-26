#!/usr/bin/env bash
# 从 Google Drive 同步 Colab 项目到 RunPod（需先配置 rclone）
set -euo pipefail

PROJECT="${KIDNEY_ATLAS_ROOT:-/workspace/kidney-atlas}"
REMOTE="${RCLONE_REMOTE:-gdrive}"
REMOTE_PATH="${RCLONE_PATH:-human-kidney-scrna-atlas-reproduction}"

echo "目标: $PROJECT"
echo "来源: ${REMOTE}:${REMOTE_PATH}"
mkdir -p "$PROJECT"

if ! command -v rclone >/dev/null 2>&1; then
  echo "安装 rclone..."
  curl -fsSL https://rclone.org/install.sh | bash
fi

if ! rclone listremotes | grep -q "^${REMOTE}:"; then
  cat <<'EOF'
尚未配置 rclone。在 Pod 上运行一次交互式配置：

  rclone config
  # n) New remote
  # name: gdrive
  # Storage: drive (Google Drive)
  # 按提示 OAuth 授权（RunPod 终端里会给出链接）

然后重新运行:
  RCLONE_REMOTE=gdrive bash runpod/migrate_from_gdrive.sh
EOF
  exit 1
fi

echo "==> 同步 data/ processed 缓存与 figures（跳过 raw 大文件可手动加 --exclude）..."
rclone sync "${REMOTE}:${REMOTE_PATH}" "$PROJECT" \
  --progress \
  --transfers 8 \
  --checkers 16 \
  --exclude ".git/**" \
  --exclude "**/.ipynb_checkpoints/**"

echo "==> 同步完成"
du -sh "$PROJECT/data" "$PROJECT/figures" 2>/dev/null || true
echo "设置环境变量: export KIDNEY_ATLAS_ROOT=$PROJECT"
