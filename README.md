# 前端 → AI 應用工程師

10 年前端轉 AI Application Engineer 的學習路線。一次一關，每關都有能跑的程式和明確的完成標準。

## 學習目標

- **Python 後端**：FastAPI、Pydantic、SQL，寫出可測試的 API
- **LLM 應用**：結構化輸出、Tool use、Vision、Prompt 設計與 eval
- **RAG**：Embedding、向量資料庫、Hybrid search、多模態文件、ETL
- **Agent**：用 LangGraph 設計 workflow，加入人工審核（HITL）
- **可靠性**：外部系統串接、Retry、Idempotency
- **安全與成本**：Guardrails、Prompt injection 防護、PII、多模型路由、可觀測性
- **部署**：Docker、CI、雲端、MCP

**最終作品：採購單 AI 助理**

上傳供應商報價單（PDF / 圖片）→ AI 抽取欄位 → 比對產品目錄 → 人工審核 → 寫入 ERP。
每個 Stage 學到的東西都會用在這個作品上。

```
報價單 → [輸入防護] → [Agent：分類 → 抽取 → RAG 比對 → 路由] → [HITL 審核介面] → [寫入 ERP + retry]
```

## 怎麼用這個資料夾

1. 一次只做一個 Stage，照該資料夾裡的 README 走
2. 做完勾下面的清單，回來跟 Claude 說「**Stage N 做完了**」→ review 你的程式碼，再產生下一關
3. 觀念題隨進度累積在 [INTERVIEW.md](INTERVIEW.md)，每關做完回去用自己的話寫答案

**AI 工具使用原則**

- **Stage 1 自己手寫。** 目的是讓 Python 語法進到手指裡，之後看 AI 產的程式才看得出問題
- **Stage 2 之後可以大量用 AI 寫**，但每一行都要能解釋「為什麼這樣寫」

## 進度總覽

| Stage | 主題 | 預估 | 重點 |
|---|---|---|---|
| 0 | 環境設定 | 半天 | uv、VS Code、git |
| 1 | Python for TS devs | 3–5 天 | 語法、型別、async、decorator |
| 2 | FastAPI + Pydantic + SQL | 1 週 | REST API、資料驗證、SQL |
| 3 | LLM API 與結構化輸出 | 1 週 | Tool use、JSON Schema、Vision |
| 4 | RAG 與向量資料庫 | 1.5 週 | Embedding、Hybrid search、ETL |
| 5 | Agent 與 LangGraph | 1.5 週 | Agentic workflow、路由、狀態持久化 |
| 6 | HITL 審核介面 | 1 週 | 審核流程、SSE、Audit log |
| 7 | 企業系統整合與可靠性 | 1 週 | ERP 串接、Retry、Idempotency |
| 8 | MCP | 3–4 天 | MCP server / client |
| 9 | Guardrails 與資安 | 1 週 | Prompt injection、PII、紅隊測試 |
| 10 | 多模型、成本、可觀測性 | 1 週 | Model routing、成本、Tracing |
| 11 | 部署與作品包裝 | 1 週 | Docker、CI、雲端部署 |

下班時間做大約 3 個月；全職投入約 6–8 週。

---

## 詳細清單

### Stage 0 — 環境設定 → [00-setup/](00-setup/)

- [ ] 安裝 uv，`uv sync` 成功
- [ ] VS Code 裝好 Python / Pylance / Ruff 擴充，選到 `.venv` 的 Python
- [ ] `uv run pytest 01-python-for-ts-devs` 能跑（全部失敗是正常的）
- [ ] git init + 推到 GitHub

### Stage 1 — Python for TS devs → [01-python-for-ts-devs/](01-python-for-ts-devs/)

- [ ] Ex01 基本語法：字串、f-string、函式、keyword-only 參數、`None`
- [ ] Ex02 集合：list / dict、推導式、排序、slicing、**RAG chunking 雛形**
- [ ] Ex03 型別：dataclass、Enum、`@property`、`@classmethod`、**審核狀態機雛形**
- [ ] Ex04 JSON 與例外：**解析不聽話的 LLM 輸出**、自訂 Exception、`raise ... from`
- [ ] Ex05 async：`gather`（≈ Promise.all）、timeout、Semaphore 限制併發
- [ ] Ex06 decorator：自己寫 **retry + 指數退避**
- [ ] 挑戰題：把 1–6 組成第一個迷你 pipeline

### Stage 2 — FastAPI + Pydantic + SQL

從這關開始寫真正的作品，程式碼放在 `project/`，一路長大到最後。

- [ ] Pydantic v2：`BaseModel`、`Field` 驗證、`field_validator` / `model_validator`、`model_validate_json`、`model_json_schema()`
- [ ] FastAPI：路由、path / query / body、`Depends` 依賴注入、async endpoint、`UploadFile`、`HTTPException`、自動產生的 `/docs`
- [ ] SQL：SQLModel 或 SQLAlchemy 2.0，先 SQLite 再換 Postgres（Docker）；JOIN、GROUP BY、transaction
- [ ] 用 pytest + `TestClient` 寫 API 測試
- **產出**：報價單 CRUD API（建立、列表、查詢、更新狀態）

### Stage 3 — LLM API 與結構化輸出

- [ ] Messages API 基本：system prompt、多輪對話、token 與 `max_tokens`、stop reason
- [ ] Streaming（SSE）—— 你在前端接過，這次寫後端
- [ ] Tool use / function calling：**先不靠框架，自己寫一次 agent loop**
- [ ] Structured outputs：用 JSON Schema 約束輸出 → Pydantic 驗證 → 失敗時把錯誤回饋給模型重試
- [ ] Instructor 套件
- [ ] Vision：直接把 PDF / 圖片丟給模型抽取
- [ ] Prompt 基本功：清楚的指令、few-shot 範例、用 XML 標籤把指令和資料分開
- [ ] 第一個 eval：20 份測試報價單 + 正確答案，算欄位準確率
- **產出**：`POST /quotes/extract` 上傳 PDF / 圖片 → 回傳通過驗證的 Quote JSON

### Stage 4 — RAG 與向量資料庫

- [ ] Embedding 是什麼、cosine similarity
- [ ] Chunking 策略：固定長度、依段落 / 標題、overlap
- [ ] Qdrant（Docker）：collection、upsert、search、payload filter；ChromaDB 看一下 API 差異
- [ ] Hybrid search（BM25 + 向量）—— 料號、型號這種精確字串，純向量搜尋會失敗
- [ ] Reranker
- [ ] 多模態：PDF 解析（文字 / 表格 / 圖片）、圖片轉描述或多模態 embedding
- [ ] ETL：產品目錄 → Qdrant 的同步 job（增量更新、idempotent upsert、失敗可重跑）
- [ ] RAG eval：recall@k；分清楚是「檢索失敗」還是「生成失敗」
- **產出**：`match_products(line_item)` 回傳最可能的料號 + 信心分數

### Stage 5 — Agent 與 LangGraph

- [ ] 先搞懂 workflow（你寫死流程）vs agent（模型決定下一步），什麼時候該用哪個
- [ ] LangGraph：State、Node、Edge、conditional edge（決策路由）
- [ ] Tools 綁定
- [ ] Checkpointer（狀態持久化）
- [ ] `interrupt()` —— 暫停等人審核，這就是 HITL 的後端
- [ ] 節點失敗的處理：重試、fallback
- [ ] 看一眼 Agno、AutoGen 的寫法，知道差在哪
- **產出**：報價處理 graph：分類 → 抽取 → 比對 → 路由（正常 → 待審 / 異常 → 加警示）

### Stage 6 — HITL 審核介面（你的主場）

- [ ] Next.js（或你最熟的框架）+ Stage 2 的 API
- [ ] 審核佇列：待審 / 已核准 / 已駁回
- [ ] 原始文件 vs AI 抽取結果並排對照、欄位可編輯、低信心欄位醒目標示
- [ ] 用 SSE 即時顯示 agent 執行到哪一步
- [ ] 核准 → resume LangGraph；駁回 → 記錄原因（之後拿來改 prompt）
- [ ] Audit log：誰、何時、改了什麼
- [ ] 分流設計：依金額 / 信心分數決定要不要人審（全部都審會審核疲勞）

### Stage 7 — 企業系統整合與可靠性

- [ ] httpx（async HTTP client）
- [ ] OAuth 2.0 授權流程（QuickBooks Online 開發者沙盒）
- [ ] 自己做一個 mock ERP，可以設定隨機 500 / 429 / timeout
- [ ] tenacity：重試、指數退避 + jitter、只重試可重試的錯誤
- [ ] Idempotency key —— 重試不會重複下單
- [ ] Timeout、circuit breaker、dead letter queue（失敗任務另存待處理）
- **產出**：核准後寫入 ERP；在 30% 失敗率下壓測，不重複、不遺失

### Stage 8 — MCP

- [ ] MCP 概念：tools / resources / prompts、stdio vs Streamable HTTP
- [ ] 寫一個 MCP server：`search_products`、`create_purchase_order`
- [ ] 接到 Claude Desktop / Claude Code 測試
- [ ] 讓自己的 agent 當 MCP client 去呼叫它

### Stage 9 — Guardrails 與資安

- [ ] 讀一遍 OWASP Top 10 for LLM Applications
- [ ] Prompt injection：直接注入 vs 間接注入（藏在 PDF 裡的指令）—— 自己做一份惡意報價單
- [ ] 防護：指令 / 資料分離、工具最小權限、寫入動作必經 HITL、輸出驗證
- [ ] PII：Microsoft Presidio 偵測與遮蔽（送雲端模型前）、可還原的 token 化
- [ ] Guardrails AI 或 NeMo Guardrails 選一個試
- [ ] 紅隊測試集：20 個攻擊案例，自動化跑

### Stage 10 — 多模型、成本、可觀測性

- [ ] 接第二家雲端模型 + Ollama 地端模型，統一成同一個介面
- [ ] Model router：依任務難度選模型
- [ ] 每次呼叫記錄 token 用量與成本；prompt caching
- [ ] Langfuse tracing：看到每一步的輸入、輸出、延遲
- [ ] 用 Stage 3 的 eval 比較不同模型的準確率 / 成本 / 延遲 → 做成表格放 README

### Stage 11 — 部署與作品包裝

- [ ] Dockerfile（multi-stage）+ docker-compose（api、web、qdrant、postgres）
- [ ] GitHub Actions：push 時自動跑測試 + eval
- [ ] 部署到雲端（Cloud Run / Fly.io / Railway 選一個）
- [ ] （選修）Kubernetes 基本概念：Pod、Deployment、Service
- [ ] 作品 README：架構圖、eval 結果表、失敗注入展示、demo 影片
