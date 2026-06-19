# 双工作流切换指南

本项目以 **GitHub 仓库** 为唯一真相来源（source of truth）。  
Cursor 本地编辑、Colab MCP 自动执行、Colab 网页手动运行 —— 三者操作的是同一套文件。

```
                    ┌─────────────────┐
                    │  GitHub 仓库     │
                    │  (.ipynb / src)  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        Cursor 本地编辑   Colab MCP       Colab 网页
        (写代码/重构)     (AI 自动跑)     (手动调试)
```

---

## 1. Cursor + Colab MCP

### 前置条件

- 已运行 `bash scripts/setup_local.sh`（安装 `uv`）
- 已重启 Cursor，`.cursor/mcp.json` 已加载
- 有 Google 账号（首次 OAuth 授权）

### 典型用法

在 Cursor 对话中直接说：

- 「连接 Colab，创建 notebook 并安装 scanpy」
- 「在 Colab 运行 `01_data_loading.ipynb`」
- 「根据论文 Figure 2 写代码并执行」

### 注意

- MCP 操作的是 **Google Drive / Colab 中的 notebook**，改完后需 sync 回 GitHub
- 若工具不可见，在浏览器中打开 Colab 并点击 Connect
- 社区修复版（可选）：将 `mcp.json` 中的 URL 换为 `git+https://github.com/ashtad63/colab-mcp`

---

## 2. GitHub + Colab 网页

### 典型用法

1. 在 Cursor 中编辑代码 → `git push`
2. 打开 README 中的 **Open in Colab** 链接
3. `00_setup_colab.ipynb` 会自动 `git clone` 你的仓库
4. 手动 Run All 或逐 cell 调试

### 适合场景

- MCP 连接不稳定
- 需要细看中间变量、交互式调参
- 长时间 GPU 任务
- 给面试官演示

---

## 3. 如何在两种方式之间同步

| 你做了什么 | 需要同步什么 |
|-----------|-------------|
| Cursor 本地改了代码 | `git push` → Colab 里 `git pull` 或重新 clone |
| Colab 网页改了 notebook | 下载 `.ipynb` 或用 `git` → `git push` |
| MCP 在 Colab 改了 notebook | 从 Drive 下载 / Colab「在 GitHub 中打开」→ push |

### 推荐习惯

```bash
# 每次开始工作前
git pull

# 每次结束工作后
git add -A && git commit -m "..." && git push
```

在 Colab 中可在 notebook 开头加：

```python
!git pull origin main
```

---

## 4. 故障排查

| 问题 | 解决 |
|------|------|
| Cursor 看不到 Colab MCP 工具 | 重启 Cursor；检查 `~/.local/bin/uvx` 是否存在 |
| OAuth 失败 | 确认浏览器未拦截弹窗；删除 `~/.colab-mcp-auth-token.json` 重试 |
| Colab 断连 | Runtime → Reconnect；长任务考虑 Colab Pro |
| 数据文件找不到 | 挂载 Drive 或检查 `data/raw/` 路径 |
| notebook 与本地不一致 | 以 GitHub 为准，强制 pull 覆盖 |

---

## 5. 求职展示建议

- README 放 **Open in Colab** 徽章 + 复现进度表
- `figures/` 放最终出图（小图可入库，大图用 Release 附件）
- 每个 figure 对应一个 notebook，commit message 写清楚对应论文图号
