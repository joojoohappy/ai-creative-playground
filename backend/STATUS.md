# Person 2 後端｜進度記錄

**更新：** 2026-09-20 — v2 架構已實作並實測
**狀態：** HTTP layer 實際跑過，所有文件宣告的 status code 都驗證過。**live provider 仍未接。**

---

## 已驗證（實際跑過，不是「應該可以」）

| 檢查 | 結果 |
|---|---|
| `GET /api/health` | `{"ok":true}` |
| 未知 recipe | `404 unknown_recipe` |
| 缺 recipeId | `400 missing_recipe_id` |
| 缺圖片 | `400 missing_image` |
| `.txt` 改名 `.jpg` | `400 unsupported_type`（magic bytes 擋下） |
| 9MB 檔案 | `400 too_large` |
| `resultId=../../etc/passwd` | `404`，沒有碰到檔案系統 |
| 正常流程 | 回 32 字元 hex resultId，`/api/results/{id}` 讀得回來 |
| cached 模式 | sidecar 存在時 `mode: "cached"`，`sourceNote` 帶出 provider/model/日期/測試照片檔名 |
| `/static/results/<id>.png` | HTTP 200 |
| timeout 由 sidecar 推導 | `durationSec 23.4 × 1.5 = 35s`（無資料時用上限 60） |
| **慢速生成不會凍住 server** | 8 秒 blocking 呼叫進行中，`/api/health` 仍即時回應 |
| 壞掉的 sidecar | 降級成 `mock`，不拋例外 |

```bash
cd backend && ./.venv/bin/python test_generate.py
```

---

## 未驗證 / 未完成

| 項目 | 卡在哪 |
|---|---|
| **live provider** | `_call_provider()` 仍是 `NotImplementedError`。沒選 provider、沒有 key |
| **cached fallback 素材** | `storage/fallback/` 是空的。要 `pregen.py` 跑過才有 |
| **Next.js rewrite proxy** | `next.config.js` 已寫好，但 `mosaic/` 還沒有 `package.json`，無法實測 |
| **長連線是否被 proxy 切斷** | 需要 Next 跑起來才測得到。這是 T+30 的必測項 |
| HTML 視覺化溝通文件 | 之前被中斷，仍未產出 |

> **注意：** 測試時建立的 `storage/fallback/` 假 sidecar（標示 google / demo-model-id）已刪除。
> 那是捏造的來源資訊，留著會讓 `sourceNote` 說出不實的 provider 和日期。

---

## 這次對 `mosaic/` 的改動（Person 1 要知道）

| 動作 | 檔案 | 理由 |
|---|---|---|
| **刪除** | `app/api/generate/route.ts` | **會遮蔽 rewrite proxy。** Next rewrites 是 afterFiles，實體 route 檔優先；該檔沒有 export POST，`/api/generate` 會回 405 而不是轉給 Python。已 `git rm`，要還原：`git checkout mosaic/app/api/generate/route.ts` |
| 新增 | `next.config.js` | `/api/*` 和 `/static/*` 轉發到 `localhost:8000` |
| 填入 | `types/recipe.ts`、`types/generation.ts` | 共用 contract。`GenerationResult` 就是前端要吃的形狀 |
| 未動 | `data/recipes.ts`、`services/generation-client.ts` | 標記 Owner: user |
| 未動 | `services/generation-server.ts` | 標記 Owner: teammate 但目前 inert。FastAPI 是唯一 API owner，這個檔案已無用途 |

---

## 三條不變量（改 code 前先讀）

1. **`_call_provider()` 只回傳 bytes，絕不寫檔案。** 所有寫入都在 `_write_result()`，在 mode 決定之後發生一次。超時後的殭屍 thread 因此不可能覆寫 cached 結果。
2. **`mode: "live"` 代表真的拿到一張圖。** provider 輸出過的是跟上傳同一套 `_is_image()`。回 200 但是文字 → 當作失敗 → fallback。
3. **使用者照片不保留。** bytes → provider → 丟掉。
   *誠實的但書：* Starlette 會把大的 multipart 上傳先 spool 到暫存檔，request 結束時刪除。我們沒有複製到任何地方，但「完全不落地」不精確。

---

## 下一步（照順序）

1. **選 provider、拿 key** ← 唯一的關鍵路徑
2. 實作 `_call_provider()`（讀線上文件，不憑記憶寫）
3. `MOSAIC_API_KEY=... python pregen.py seed-01 <照片>` ×3 → 產生 fallback + sidecar
4. 等 Person 1 跑 `create-next-app` → 實測 proxy 與長連線
5. 核對三則 Threads 貼文的作者 / IG（目前全是 `null`）
