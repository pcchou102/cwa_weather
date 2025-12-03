# Add Streamlit Web UI for Weather Visualization

## Why
目前的天氣爬蟲只能透過 CLI 執行並將資料儲存為 JSON 檔案，使用者無法即時視覺化查看各地區的溫度資訊。需要一個友善的網頁介面讓使用者可以選擇地點並查看溫度資料。

## What Changes
- 新增 Streamlit 網頁應用程式
- 實作下拉式選單來選擇地點
- 顯示所選地點的溫度資訊（當前溫度、最高/最低溫）
- 保留原有的 CLI 爬蟲功能
- 新增依賴套件：streamlit, pandas（選用，用於資料處理）
- 建立獨立的 `weather_app.py` 檔案

## Impact
- **受影響的規格**：
  - 新增 `weather-ui` capability
  - 新增 `weather-api-client` capability（將爬蟲邏輯模組化）
  
- **受影響的程式碼**：
  - `weather_crawler.py` - 保持不變（CLI 功能）
  - 新增 `weather_app.py` - Streamlit 應用程式
  - 新增 `weather_client.py` - 可重用的 API 客戶端類別
  - 更新 `requirements.txt` 或建立 `requirements.txt`

- **使用者體驗**：
  - 使用者可以選擇透過 CLI (`python weather_crawler.py`) 或 Web UI (`streamlit run weather_app.py`) 使用
  - Web UI 提供更直觀的資料檢視方式

## Non-Goals
- 不包含歷史資料分析
- 不包含天氣預報圖表（僅顯示溫度數值）
- 不包含多語言支援（僅繁體中文）
