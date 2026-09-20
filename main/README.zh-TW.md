# AI Creative Playground｜Build Day Starter Kit

**狀態：活動前準備文件，尚未建立產品。** 目前預計整理三份創作者分享的圖片生成 prompt，讓使用者在同一平台看預覽、找到原作者，並用自己的照片試用。專案目標見 [PROJECT.md](PROJECT.md)。Fable5 示範後，團隊再決定 prototype 的畫面、技術與分工。

## 建議閱讀順序

1. [PROJECT.md](PROJECT.md)：本次 prototype 的目標與使用流程。
2. [BUILD-DAY.zh-TW.md](BUILD-DAY.zh-TW.md)：現場決策、三人分工、checkpoints、feature freeze 與備案。活動中先填決策表，再開始實作。對應的[英文版](archive/BUILD-DAY.md)目前存放在 archive。
3. [CREATIVE-RECIPE.md](CREATIVE-RECIPE.md)：**資料格式**，定義一份 recipe 要記錄哪些欄位，例如原貼文、原作者 IG、預覽圖與 prompt。
4. [SEED-RECIPES.md](SEED-RECIPES.md)：**實際內容**，存放已選的三份 prompt 原文與 Threads 連結，以及作者、IG、預覽圖等待核對項目。
5. [WIREFRAMES.zh-TW.md](WIREFRAMES.zh-TW.md)：畫面資訊架構參考；包含早期構想，須依現場決策取捨。

**資料格式與實際內容的差別：** CREATIVE-RECIPE.md 說明每張資料卡要有哪些欄位；SEED-RECIPES.md 提供目前選出的三張卡要填入的內容。程式中的 Gallery、Recipe、Create 與 Result 應使用同一組 recipe ID 與欄位。

## 文件狀態

| 文件 | 用途與狀態 |
|---|---|
| [PROJECT.md](PROJECT.md) | 本次 prototype 目標；目前版本 |
| [CREATIVE-RECIPE.md](CREATIVE-RECIPE.md) | 共用資料欄位約定；實作前可由團隊簡化 |
| [SEED-RECIPES.md](SEED-RECIPES.md) | 三份已選 prompt 與來源；作者、IG、預覽圖等尚未全數核對 |
| [BUILD-DAY.zh-TW.md](BUILD-DAY.zh-TW.md) | 中文團隊執行計畫；現場填入決策 |
| [WIREFRAMES.zh-TW.md](WIREFRAMES.zh-TW.md) | 中文畫面參考；尚待依現場結果決定採用範圍 |
| [README.md](README.md)、[WIREFRAMES.md](WIREFRAMES.md) | 保留的英文版本 |
| [archive/BUILD-DAY.md](archive/BUILD-DAY.md) | 對應目前中文 Build Day 的英文版，現存於 archive |
| [archive/BUILD-DAY.en-early-draft.md](archive/BUILD-DAY.en-early-draft.md) | 較早、範圍較廣的英文 Build Day 草稿 |
| [AI-PROMPTS.md](AI-PROMPTS.md)、[archive/AI-PROMPTS.zh-TW.md](archive/AI-PROMPTS.zh-TW.md) | AI session 提示草稿；使用前須對照現場決策、實際路徑與分工 |
| [archive/PITCH.md](archive/PITCH.md)、[archive/YOUR-NEXT-STEPS.md](archive/YOUR-NEXT-STEPS.md) | 已存檔的較早期準備文件 |

較早的 PROJECT 草稿也保留在 [英文版本](archive/PROJECT-vision-en-v0.1.md)及[中文擴充版](archive/PROJECT-vision-zh-v0.2.md)。根目錄的 PROJECT.md 是目前版本。

## 文件與決策的分工

- **PROJECT.md：**本次 prototype 的目標。
- **CREATIVE-RECIPE.md：**候選 recipe 的共用資料欄位。
- **SEED-RECIPES.md：**三份候選 prompt 的原文、來源與素材準備狀態。
- **BUILD-DAY.zh-TW.md：**Fable5 示範後決定的最終流程、功能、負責人與時間。



## 活動日尚需填入

- 活動時間、規則、允許的事前準備與提交要求：**[待確認]**
- Repo 位址、可見範圍與三位成員權限：**[團隊決定]**
- 技術架構、執行版本與套件管理方式：**[看完示範後決定]**
- 實際安裝、執行、檢查與建置指令：**[建立產品後補入]**
- 生成服務、費用或額度、金鑰取得方式：**[技術負責人確認；此處不填金鑰]**
- 可展示的原作者預覽圖、已核對的 IG、測試照片與備用結果：**[素材負責人補入]**
- 展示網址或經驗證的本機展示方式：**[實作後補入]**

目前沒有可執行的應用程式或安裝指令。各成員開始平行開發前，應先建立共同可運行的最小版本，確認 recipe ID、資料欄位與檔案負責範圍。

## Build Day 結束後補入

實際完成的功能、live／事先生成／示意部分、操作與執行方式、展示截圖或錄影、已知限制、參與成員，以及活動中觀察到的問題。截圖與素材的展示方式應與各自來源紀錄一致。
