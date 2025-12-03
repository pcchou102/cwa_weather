# Weather UI Specification

## ADDED Requirements

### Requirement: Web-based User Interface
系統 SHALL 提供基於 Streamlit 的網頁使用者介面，讓使用者可以透過瀏覽器查看天氣資訊。

#### Scenario: 成功啟動 Web UI
- **GIVEN** 使用者已安裝所有必要套件
- **WHEN** 使用者執行 `streamlit run weather_app.py`
- **THEN** 瀏覽器應自動開啟並顯示天氣應用程式首頁
- **AND** 頁面標題應顯示「中央氣象署天氣資訊」

### Requirement: Location Selector
系統 SHALL 提供下拉式選單讓使用者選擇想查看的地點。

#### Scenario: 顯示所有可用地點
- **GIVEN** Web UI 已成功載入
- **WHEN** 頁面渲染完成
- **THEN** 下拉選單應顯示所有從 API 取得的地點名稱
- **AND** 地點清單應按字母順序或地區順序排列
- **AND** 預設應選擇第一個地點

#### Scenario: 選擇不同地點
- **GIVEN** 使用者在下拉選單中看到多個地點
- **WHEN** 使用者從下拉選單選擇一個地點
- **THEN** 系統應立即更新顯示該地點的溫度資訊
- **AND** 不需要按下任何按鈕或重新整理頁面

### Requirement: Temperature Information Display
系統 SHALL 顯示選定地點的詳細溫度資訊。

#### Scenario: 顯示完整溫度資訊
- **GIVEN** 使用者已選擇一個地點
- **WHEN** 系統成功取得該地點的天氣資料
- **THEN** 應顯示以下資訊：
  - 地點名稱
  - 當前溫度（°C）
  - 最高溫度（°C）
  - 最低溫度（°C）
  - 資料更新時間
- **AND** 溫度數值應使用清晰的格式與單位
- **AND** 應使用圖示增強視覺效果（如 🌡️ 📍 ↗️ ↘️）

#### Scenario: 資料載入中
- **GIVEN** 使用者剛開啟應用程式或選擇地點
- **WHEN** 系統正在從 API 取得資料
- **THEN** 應顯示載入指示器（spinner）
- **AND** 應顯示「正在載入天氣資料...」訊息

#### Scenario: 無可用資料
- **GIVEN** API 成功回應但該地點無溫度資料
- **WHEN** 系統嘗試顯示溫度資訊
- **THEN** 應顯示友善的「暫無該地點的溫度資料」訊息
- **AND** 不應顯示錯誤或崩潰

### Requirement: Error Handling and User Feedback
系統 SHALL 優雅地處理錯誤並提供清晰的使用者回饋。

#### Scenario: API 連線失敗
- **GIVEN** 網路連線中斷或 API 無法存取
- **WHEN** 系統嘗試取得天氣資料
- **THEN** 應顯示錯誤訊息：「無法連線到氣象署 API，請檢查網路連線」
- **AND** 應提供重試機制或建議

#### Scenario: API 金鑰無效
- **GIVEN** 環境變數中的 API 金鑰無效或過期
- **WHEN** 系統嘗試呼叫 API
- **THEN** 應顯示錯誤訊息：「API 金鑰無效，請檢查環境變數設定」
- **AND** 應提供設定指引連結或說明

#### Scenario: JSON 解析錯誤
- **GIVEN** API 回應格式異常或損壞
- **WHEN** 系統嘗試解析回應資料
- **THEN** 應顯示錯誤訊息：「資料格式異常，請稍後再試」
- **AND** 系統應記錄詳細錯誤訊息到 console

### Requirement: Performance Optimization
系統 SHALL 使用快取機制避免重複的 API 呼叫，提升效能與使用者體驗。

#### Scenario: 資料快取
- **GIVEN** 使用者首次載入應用程式
- **WHEN** 系統從 API 取得天氣資料
- **THEN** 資料應被快取 10 分鐘
- **AND** 在快取期間內，切換地點不應觸發新的 API 呼叫
- **AND** 快取過期後，下次請求應重新取得資料

#### Scenario: 快取更新提示
- **GIVEN** 快取的資料已過期
- **WHEN** 系統重新取得資料
- **THEN** 應顯示「正在更新資料...」提示
- **AND** 資料更新時間應反映最新的 API 回應時間

### Requirement: Responsive Design
UI SHALL 在不同螢幕尺寸下都能正常顯示與操作。

#### Scenario: 桌面瀏覽器顯示
- **GIVEN** 使用者使用桌面瀏覽器（1920x1080）
- **WHEN** 頁面載入
- **THEN** 所有元件應合理排列，留有適當間距
- **AND** 文字應清晰可讀

#### Scenario: 行動裝置顯示
- **GIVEN** 使用者使用手機瀏覽器（375x667）
- **WHEN** 頁面載入
- **THEN** 下拉選單應可正常點擊與選擇
- **AND** 溫度資訊應垂直排列，避免水平捲動
- **AND** 所有文字與按鈕應大小適中，易於點擊
