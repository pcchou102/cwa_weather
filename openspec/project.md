# Project Context

## Purpose
AIoT 天氣資料爬蟲專案 - 從中央氣象署開放資料平台獲取並處理鄉鎮天氣預報資料，用於 AIoT 應用整合。

## Tech Stack
- Python 3.13
- requests (HTTP 客戶端)
- JSON (資料格式)
- 中央氣象署開放資料 API (F-A0010-001)

## Project Conventions

### Code Style
- 使用繁體中文註解與文件字串
- 函數與變數使用 snake_case 命名
- 類別使用 PascalCase 命名
- 保持 4 空格縮排
- 檔案編碼使用 UTF-8
- 字串格式化優先使用 f-string

### Architecture Patterns
- 功能導向設計：每個函數專注於單一職責
- 錯誤處理：使用 try-except 捕捉並記錄所有 HTTP 與解析錯誤
- 資料持久化：將 API 回應儲存為帶時間戳記的 JSON 檔案
- 環境變數：敏感資訊（如 API 金鑰）應從環境變數讀取

### Testing Strategy
- 手動測試：執行腳本驗證 API 呼叫與資料儲存
- 錯誤處理測試：確保網路錯誤、逾時、JSON 解析錯誤都有適當處理
- 資料驗證：檢查回應格式與必要欄位是否存在

### Git Workflow
- 主分支開發
- 有意義的 commit 訊息（繁體中文）
- 功能完成後再提交

### OpenSpec Change Conventions
- **變更編號**：所有變更提案必須使用兩位數字前綴，格式為 `NN-change-name`
  - 範例：`01-add-streamlit-web-ui`, `02-add-database-support`, `03-refactor-api-client`
  - 編號從 `01` 開始，依序遞增
  - 編號協助追蹤變更順序與歷史
  - 即使變更已封存，編號不可重複使用
- **命名規則**：kebab-case，動詞開頭（`add-`, `update-`, `remove-`, `refactor-`）
- **目錄結構**：`openspec/changes/NN-change-name/`
- **下一個可用編號**：03（請在建立新變更時更新此編號）

## Domain Context
- 中央氣象署開放資料平台 API 規範
- 天氣預報資料結構：包含 cwaopendata、dataset、locations 等巢狀物件
- API 授權：需使用個人 API 金鑰（CWA-XXXXXXXX 格式）
- 資料更新頻率：依氣象署發布時間更新

## Important Constraints
- API 呼叫限制：遵守氣象署 API 使用規範與頻率限制
- 網路依賴：需要穩定的網路連線
- 資料時效性：天氣預報資料有時效性，需定期更新
- Windows 環境：開發環境為 Windows + PowerShell

## External Dependencies
- 中央氣象署開放資料平台 (https://opendata.cwa.gov.tw)
- API 端點：F-A0010-001 (鄉鎮天氣預報資料)
- 需要有效的 CWA API 授權金鑰
