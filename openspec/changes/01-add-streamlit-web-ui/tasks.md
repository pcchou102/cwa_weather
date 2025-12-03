# Implementation Tasks

## 1. 重構 API 客戶端
- [x] 1.1 建立 `weather_client.py` 模組
- [x] 1.2 實作 `WeatherAPIClient` 類別，封裝 API 呼叫邏輯
- [x] 1.3 新增方法：`fetch_weather_data()` 取得原始資料
- [x] 1.4 新增方法：`get_locations()` 取得所有地點清單
- [x] 1.5 新增方法：`get_temperature_info(location_name)` 取得特定地點溫度資訊
- [x] 1.6 新增環境變數支援：從 `CWA_API_KEY` 讀取 API 金鑰
- [x] 1.7 測試 API 客戶端的所有方法

## 2. 建立 Streamlit Web UI
- [x] 2.1 建立 `weather_app.py` 檔案
- [x] 2.2 設定 Streamlit 頁面配置與標題
- [x] 2.3 實作地點下拉選單（使用 `st.selectbox`）
- [x] 2.4 實作溫度資訊顯示區塊
- [x] 2.5 新增載入狀態指示器
- [x] 2.6 新增錯誤處理與使用者提示訊息
- [x] 2.7 優化 UI 排版與樣式
- [x] 2.8 測試所有互動功能

## 3. 依賴套件管理
- [x] 3.1 建立或更新 `requirements.txt`
- [x] 3.2 新增 `streamlit` 套件
- [x] 3.3 新增 `pandas` 套件（選用）
- [x] 3.4 確保 `requests` 已列出
- [x] 3.5 測試套件安裝流程

## 4. 文件更新
- [x] 4.1 建立或更新 `README.md`
- [x] 4.2 記錄 Web UI 使用方式
- [x] 4.3 記錄環境變數設定方式
- [x] 4.4 提供使用範例與截圖（選用）

## 5. 測試與驗證
- [x] 5.1 測試 CLI 爬蟲功能（確保未破壞）
- [x] 5.2 測試 Web UI 在本機啟動
- [x] 5.3 測試地點選擇功能
- [x] 5.4 測試溫度資訊顯示
- [x] 5.5 測試錯誤情境（網路錯誤、API 錯誤）
- [x] 5.6 測試環境變數設定
