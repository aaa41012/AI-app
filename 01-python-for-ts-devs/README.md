# Stage 1 — Python for TS devs

**目標**：3–5 天內能流暢寫 Python，同時熟悉之後每天都會用的模式：JSON 解析、async 併發、retry。

每一題的主題都跟最終作品有關 —— 你在練語法的同時，也在寫報價單處理的零件。

## 怎麼做

每個 `exNN_*.py` 檔開頭有 TS 對照表，函式的 docstring 就是規格。
把 `raise NotImplementedError` 換成你的實作，讓對應的 `test_exNN_*.py` 變綠。**測試檔不用改。**

```bash
# 一題一題來（建議）
uv run pytest 01-python-for-ts-devs/test_ex01_basics.py

# 只跑名稱含 normalize 的測試
uv run pytest 01-python-for-ts-devs/test_ex01_basics.py -k normalize

# 全部跑
uv run pytest 01-python-for-ts-devs

# 風格檢查（≈ eslint）；--fix 自動修 import 排序之類的小問題
uv run ruff check 01-python-for-ts-devs --fix
```

也可以用 VS Code 左側的 Testing 面板，一個一個點來跑。

想試語法時開 REPL：`uv run python`（≈ 在終端機打 `node`）。

## 練習順序

| # | 檔案 | 學什麼 | 跟作品的關係 |
|---|---|---|---|
| 1 | `ex01_basics.py` | 字串、f-string、函式、keyword-only 參數、`None` | 料號正規化、金額格式 |
| 2 | `ex02_collections.py` | list / dict、推導式、排序、slicing | line items 計算、**RAG chunking** |
| 3 | `ex03_dataclass.py` | dataclass、Enum、`@property`、`@classmethod` | Quote 資料模型、**審核狀態機** |
| 4 | `ex04_json_errors.py` | json、例外處理、自訂 Exception | **解析不聽話的 LLM 輸出** |
| 5 | `ex05_async.py` | async / await、gather、timeout、Semaphore | **同時呼叫 LLM 又不撞 rate limit** |
| 6 | `ex06_retry_decorator.py` | decorator、closure、指數退避 | **第三方 API retry** |
| ★ | 挑戰題（見下方） | 把 1–6 組起來 | 第一個迷你 pipeline |

## TS → Python 速查

### 基本

| TypeScript | Python |
|---|---|
| `const x = 1` / `let x = 1` | `x = 1` |
| `// 註解` | `# 註解` |
| `null` / `undefined` | `None` |
| `true` / `false` | `True` / `False` |
| `&&` `\|\|` `!` | `and` `or` `not` |
| `===` | `==`（判斷 None 用 `x is None`） |
| `cond ? a : b` | `a if cond else b` |
| `a ?? b` | `a if a is not None else b` |
| `` `Hi ${name}` `` | `f"Hi {name}"` |
| `typeof x === "string"` | `isinstance(x, str)` |
| `console.log(x)` | `print(x)` |
| `x++` | `x += 1`（沒有 `++`） |
| `Math.floor(a / b)` | `a // b` |
| `for (const x of arr)` | `for x in arr:` |
| `for (let i = 0; i < n; i++)` | `for i in range(n):` |

### 函式

| TypeScript | Python |
|---|---|
| `function f(a: number, b = 2): number` | `def f(a: int, b: int = 2) -> int:` |
| `(x) => x * 2` | `lambda x: x * 2`（只能寫一行運算式） |
| `f(name, { unit: "盒" })` | `f(name, unit="盒")` 關鍵字參數 |
| `(...args) => {}` | `def f(*args, **kwargs):` |
| `f(...arr)` | `f(*arr)`；物件展開成參數用 `f(**obj)` |
| `function f<T>(x: T): T` | `def f[T](x: T) -> T:` |

### 集合

| TypeScript | Python |
|---|---|
| `arr.length` | `len(arr)` |
| `arr.push(x)` | `arr.append(x)` |
| `arr.map(x => x * 2)` | `[x * 2 for x in arr]` |
| `arr.filter(x => x > 0)` | `[x for x in arr if x > 0]` |
| `arr.includes(x)` | `x in arr` |
| `arr.slice(1, 3)` | `arr[1:3]` |
| `arr.at(-1)` | `arr[-1]` |
| `arr.forEach((x, i) => …)` | `for i, x in enumerate(arr):` |
| `arr.some(…)` / `arr.every(…)` | `any(…)` / `all(…)` |
| `Object.keys(o)` / `Object.entries(o)` | `o.keys()` / `o.items()` |
| `o.key ?? "預設"` | `o.get("key", "預設")` |
| `{ ...a, ...b }` | `{**a, **b}` 或 `a \| b` |
| `const [a, ...rest] = arr` | `a, *rest = arr` |
| `const { a, b } = o` | 沒有物件解構：`a, b = o["a"], o["b"]` |
| `new Set(arr)` | `set(arr)` |
| `Object.fromEntries(…)` | `{k: v for k, v in …}` |

### 類別與型別

| TypeScript | Python |
|---|---|
| `interface User { name: string }` | `@dataclass class User: name: str`（Stage 2 換成 Pydantic） |
| `this.name` | `self.name`（方法的第一個參數要寫 `self`） |
| `constructor(…)` | `__init__(self, …)`（dataclass 會自動產生） |
| `string \| null` | `str \| None` |
| `string[]` | `list[str]` |
| `Record<string, number>` | `dict[str, int]` |
| `[string, number]` | `tuple[str, int]` |
| `"a" \| "b"` | `Literal["a", "b"]` |
| `any` | `Any` |

### 模組

| TypeScript | Python |
|---|---|
| `import { a } from "./utils"` | `from utils import a` |
| `import * as u from "./utils"` | `import utils as u` |
| `export` | 不用寫，模組裡的名字都能被 import（`_` 開頭代表「私有」的慣例） |
| `if (require.main === module)` | `if __name__ == "__main__":` |

## JS 開發者最常踩的坑

1. **縮排就是區塊**。沒有 `{}`，縮排錯了就是語法錯誤或邏輯錯誤
2. **空的 list / dict 是 falsy**。JS 的 `[]` 是 truthy；Python 的 `[]`、`{}`、`""`、`0`、`None` 全都是 falsy
3. **dict 取不存在的 key 會丟 `KeyError`**，不會回 `undefined`。不確定有沒有就用 `.get()`
4. **呼叫 `async def` 不會執行**，只會拿到 coroutine，要 `await` 才會跑（Ex05）
5. **預設參數只建立一次**：`def f(items=[])` 每次呼叫都共用同一個 list（Ex03 說明）
6. **`"a" + 1` 是 TypeError**，不會自動轉型，用 f-string
7. **`/` 永遠回傳 float**：`7 / 2 == 3.5`，整除要用 `//`
8. **在內層函式要改外層的變數**，要宣告 `nonlocal`（測試檔裡就有例子）

## ★ 挑戰題：第一個迷你 pipeline（選做，但很推薦）

`fake_llm.py` 是一個假的 LLM：會隨機 503、回覆格式亂七八糟、有幾份輸出被截斷。
先跑一次看看它會回什麼：

```bash
uv run python 01-python-for-ts-devs/fake_llm.py
```

然後自己建一個 `pipeline.py`（放在這個資料夾），完成：

1. 用 Ex06 的 `@retry` 包住 `fake_llm`（`max_attempts=3`、`base_delay=0.2`）
2. 處理 `DOC_IDS` 全部 20 份報價單，**同時最多 5 個**（Ex05）
3. 每份回覆 → `extract_json`（Ex04）→ `Quote.from_dict`（Ex03）
4. 單一份失敗不能讓整批中斷，要記錄是哪份、為什麼失敗
5. 印出報告：

```
處理 20 份報價單，耗時 4.1 秒
成功 16 份，失敗 4 份
  Q-004  LLMOutputError: 無法從 LLM 輸出解析出 JSON 物件
  Q-009  LLMOutputError: 無法從 LLM 輸出解析出 JSON 物件
  Q-014  LLMOutputError: 無法從 LLM 輸出解析出 JSON 物件
  Q-019  LLMOutputError: 無法從 LLM 輸出解析出 JSON 物件
各供應商總金額：
  北辰五金  TWD 135,075.49
  南星電子  TWD 69,144.44
  西岳材料  TWD 77,656.31
```

**對答案**：失敗的那 4 份和三個金額應該跟上面一模一樣（偶爾某份剛好連續 3 次 503，會多一筆 `RetryableError`，再跑一次就好）。

執行：`uv run python 01-python-for-ts-devs/pipeline.py`

提示：
- 寫一個 `async def process(doc_id)`，自己在裡面 try / except，回傳 `(doc_id, quote, error)`，再交給 `fetch_all_limited`
- 最外層用 `asyncio.run(main())`，放在 `if __name__ == "__main__":` 底下
- 一個一個跑要 12 秒以上；做對的話大約 3–5 秒

這其實就是 Stage 3 之後真實系統的縮小版：換成真的 LLM、換成 Pydantic，骨架都一樣。

## 完成標準

- [ ] `uv run pytest 01-python-for-ts-devs` 全部通過
- [ ] `uv run ruff check 01-python-for-ts-devs` 沒有錯誤
- [ ] （選做）挑戰題能跑出報告

做完跟 Claude 說「**Stage 1 做完了**」，會幫你 review，然後開 Stage 2。
