# CLAUDE.md

使用者的學習專案：10 年前端轉 AI 應用工程師。路線與進度在 README.md，面試題在 INTERVIEW.md。

- 用繁體中文（台灣用語）回覆，技術名詞保留英文
- 使用者熟 TS / React / 前端，用 TS 類比解釋 Python 與後端概念最有效
- 練習題不要直接給完整解答：先給提示，使用者明確要求才給答案
- 使用者說「Stage N 做完了」時：
  1. 跑該 stage 的測試和 `uv run ruff check`
  2. Review 程式碼：指出不夠 Pythonic 的寫法、潛在 bug，說明理由（拿 TS 對照）
  3. 在 README.md 的清單幫忙打勾
  4. 建立下一個 stage 的資料夾（README + 練習或骨架 + 測試），維持跟前面相同的格式
- Stage 2 起開始寫最終作品（採購單 AI 助理），程式碼放在 `project/`
