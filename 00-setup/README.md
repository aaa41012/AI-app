# Stage 0 — 環境設定

你的系統內建 Python 是 3.9.6，太舊了（這套練習用 3.12：`int | None`、`StrEnum`、泛型 `def f[T]()` 都要新版）。
不要去動系統的 Python，交給 **uv** 管理 —— 它就是 Python 世界的 `nvm + pnpm`，一個工具全包。

## 1. 安裝 uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# 裝完開一個新的終端機視窗
uv --version
```

不要用 `brew install uv`：macOS 13 已經沒有 Homebrew 預先編好的套件，brew 會從原始碼編譯 Rust 等一整串相依，要好幾個小時。官方安裝程式是直接下載編好的執行檔，幾秒就好。

## 2. 安裝依賴

```bash
cd ~/Desktop/ai-app-engineer
uv sync
```

這一步會做三件事（對照 Node）：

1. 讀 `.python-version`，自動下載 Python 3.12（≈ `nvm install`）
2. 建立 `.venv/`（≈ `node_modules/`，但連 Python 直譯器都放在裡面）
3. 安裝 `pyproject.toml` 裡的 pytest、ruff，產生 `uv.lock`（≈ `pnpm install`）

確認：

```bash
uv run python --version   # 應該顯示 Python 3.12.x
```

## 3. 確認可以跑測試

```bash
uv run pytest 01-python-for-ts-devs
```

看到一整排 `FAILED`（`NotImplementedError`）就對了 —— 那些就是你接下來要寫的。

## 4. 編輯器（Cursor / VS Code）

1. 安裝擴充：**Python**（Microsoft）、**Ruff**；型別檢查在 VS Code 用 **Pylance**，在 Cursor 用 **Cursor Pyright**（Pylance 不能在 Cursor 上用，裝 Python 擴充時會自動帶入）
2. `Cmd+Shift+P` → `Python: Select Interpreter` → 選 `./.venv/bin/python`
3. 這個資料夾已經有 `.vscode/settings.json`（Cursor 也讀這個）：存檔自動 format、左側 Testing 面板可以一個一個點測試來跑（像 Jest 擴充）

建議直接開 `~/Desktop/ai-app-engineer` 這個資料夾當 workspace。

## 5. Git

```bash
git init
git add .
git commit -m "init learning path"
```

在 GitHub 開一個 repo 推上去 —— 你的 commit 紀錄本身就是「持續學習」的證據。

## 6. 先註冊起來（之後才會用到）

| 什麼 | 哪一關要用 |
|---|---|
| Docker Desktop | Stage 2 後半（Postgres）、Stage 4（Qdrant） |
| LLM API key（Anthropic / OpenAI / Google 選一家當主力） | Stage 3 |
| Intuit Developer 帳號（QuickBooks 沙盒） | Stage 7 |

API key 放在 `.env`（`cp .env.example .env` 再填），`.env` 已在 `.gitignore`。

## 工具對照表

| Node 世界 | Python 世界 |
|---|---|
| nvm | `uv python install` |
| npm / pnpm | `uv` |
| package.json | `pyproject.toml` |
| pnpm-lock.yaml | `uv.lock` |
| node_modules | `.venv` |
| `pnpm add x` / `pnpm add -D x` | `uv add x` / `uv add --dev x` |
| `npx x` / `pnpm exec x` | `uv run x` |
| eslint + prettier | `ruff check` + `ruff format` |
| `tsc --noEmit` | Pylance（內建 pyright，在編輯器裡即時檢查） |
| jest / vitest | pytest |

## 完成標準

- [ ] `uv --version` 有輸出
- [ ] `uv run python --version` 顯示 3.12.x
- [ ] `uv run pytest 01-python-for-ts-devs` 能跑（失敗是正常的）
- [ ] VS Code 狀態列顯示 `.venv` 的 Python
- [ ] 第一次 git commit

完成後直接進 [Stage 1](../01-python-for-ts-devs/)。
