# Cursor ↔ RunPod 连接指南

## 1. 在 RunPod 获取 SSH 信息

RunPod 控制台 → 你的 Pod → **Connect** → **SSH over exposed TCP**

记下：

- `Host`（如 `xxx.runpod.io`）
- `Port`（如 `12345`）
- SSH 公钥（需先把你的公钥加到 RunPod 账户）

## 2. 本地 `~/.ssh/config`

```sshconfig
Host runpod-kidney
  HostName YOUR_POD_HOST.runpod.io
  User root
  Port YOUR_SSH_PORT
  IdentityFile ~/.ssh/id_ed25519
  StrictHostKeyChecking accept-new
```

测试：

```bash
ssh runpod-kidney "ls -la /workspace/kidney-atlas"
```

## 3. Cursor 连接

1. 安装扩展 **Remote - SSH**（若尚未安装）
2. `Cmd+Shift+P` → **Remote-SSH: Connect to Host…** → 选 `runpod-kidney`
3. 打开文件夹 **`/workspace/kidney-atlas`**（或你的 `KIDNEY_ATLAS_ROOT`）
4. 打开 `human_kidney_scrna_atlas_reproduction.ipynb`，选 Jupyter 内核（Python 3）

## 4. 推荐 Pod 目录布局

```
/workspace/kidney-atlas/          ← git 仓库 + notebook
├── data/raw/                     ← 原始数据（不进 git）
├── data/processed/               ← 缓存（不进 git）
├── figures/
├── kidney_atlas_paths.py
└── runpod/setup.sh
```

持久化：把 Network Volume 挂载到 `/workspace`，Pod 重启后数据仍在。

## 5. 环境变量（可选）

在 `~/.bashrc` 或 Pod 模板里：

```bash
export KIDNEY_ATLAS_ROOT=/workspace/kidney-atlas
```

## 6. 与 GitHub 工作流

在 Pod 内：

```bash
cd /workspace/kidney-atlas
git pull
# 改 notebook / 代码后
git add -p && git commit -m "..." && git push
```

Cursor Remote 里可直接改代码、跑 notebook、提交 push（需配置 git credential 或 SSH key）。

## 7. 不再使用 Colab MCP

迁移完成后：

- 数据在 RunPod Volume，不再依赖 Google Drive 挂载
- Cursor 通过 SSH 直接编辑 + 运行，无需 Colab proxy MCP
