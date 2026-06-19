#!/usr/bin/env bash
# One-time local setup: uv (for Colab MCP) + optional Python venv
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
export PATH="$HOME/.local/bin:$PATH"

echo "==> Checking uv (required for Colab MCP in Cursor)..."
if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
uv --version

echo ""
echo "==> Optional: create local Python venv for editing notebooks offline"
if [ ! -d "$ROOT/.venv" ]; then
  uv venv "$ROOT/.venv"
  # shellcheck disable=SC1091
  source "$ROOT/.venv/bin/activate"
  uv pip install -r "$ROOT/requirements.txt"
  echo "Created .venv and installed requirements."
else
  echo ".venv already exists — skip."
fi

echo ""
echo "==> Done. Next steps:"
echo "  1. Restart Cursor (loads .cursor/mcp.json)"
echo "  2. In Cursor chat, ask the agent to connect Colab via MCP"
echo "  3. Push to GitHub: https://github.com/Tepeng0213/An-atlas-of-healthy-and-injured-cell-states-and-niches-in-the-human-kidney"
