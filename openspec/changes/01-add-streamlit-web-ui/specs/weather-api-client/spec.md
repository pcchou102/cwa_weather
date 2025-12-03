# Weather API Client Specification

## ADDED Requirements

### Requirement: Reusable API Client Class
系統 SHALL 提供可重用的 API 客戶端類別，封裝所有與中央氣象署 API 的互動邏輯。

#### Scenario: 初始化 API 客戶端
- **GIVEN** 使用者需要存取天氣 API
- **WHEN** 使用者建立 `WeatherAPIClient` 實例
- **THEN** 客戶端應從環境變數 `CWA_API_KEY` 讀取 API 金鑰
- **AND** 如果環境變數未設定，應使用預設金鑰
- **AND** 應初始化 HTTP session 供後續請求使用

#### Scenario: 使用自訂 API 金鑰
- **GIVEN** 使用者有特定的 API 金鑰
- **WHEN** 使用者建立 `WeatherAPIClient(api_key="custom-key")`
- **THEN** 客戶端應使用提供的金鑰，忽略環境變數

### Requirement: Fetch Raw Weather Data
API 客戶端 SHALL 能取得完整的天氣資料 JSON。

#### Scenario: 成功取得天氣資料
- **GIVEN** API 金鑰有效且網路連線正常
- **WHEN** 呼叫 `fetch_weather_data()` 方法
- **THEN** 應回傳完整的 JSON 字典
- **AND** JSON 應包含 `cwaopendata` 根節點
- **AND** 應設定 30 秒逾時

#### Scenario: API 請求失敗
- **GIVEN** 網路連線中斷或 API 無法存取
- **WHEN** 呼叫 `fetch_weather_data()` 方法
- **THEN** 應回傳 `None`
- **AND** 應記錄錯誤訊息到 console
- **AND** 不應拋出未捕捉的例外

#### Scenario: JSON 解析失敗
- **GIVEN** API 回應非 JSON 格式
- **WHEN** 呼叫 `fetch_weather_data()` 方法
- **THEN** 應回傳 `None`
- **AND** 應記錄 JSON 解析錯誤訊息

### Requirement: Extract Location List
API 客戶端 SHALL 能提取所有可用地點的清單。

#### Scenario: 取得地點清單
- **GIVEN** 已成功取得天氣資料
- **WHEN** 呼叫 `get_locations()` 方法
- **THEN** 應回傳包含所有地點名稱的字串清單
- **AND** 清單應按字母順序排序
- **AND** 不應包含重複的地點

#### Scenario: 資料結構異常時取得地點
- **GIVEN** API 資料格式與預期不符
- **WHEN** 呼叫 `get_locations()` 方法
- **THEN** 應回傳空清單 `[]`
- **AND** 應記錄警告訊息

### Requirement: Extract Temperature Information
API 客戶端 SHALL 能提取特定地點的溫度資訊。

#### Scenario: 取得特定地點溫度
- **GIVEN** 使用者指定地點名稱（如「臺北市」）
- **WHEN** 呼叫 `get_temperature_info(location_name)` 方法
- **THEN** 應回傳包含以下欄位的字典：
  - `location`: 地點名稱
  - `date`: 預報日期
  - `max_temp`: 最高溫度（數字）
  - `min_temp`: 最低溫度（數字）
  - `weather`: 天氣現象描述
- **AND** 溫度數值應為浮點數或整數
- **AND** 如果溫度資料為 "-"，應轉換為 `None`

#### Scenario: 地點不存在
- **GIVEN** 使用者指定的地點名稱不存在於資料中
- **WHEN** 呼叫 `get_temperature_info("不存在的地點")` 方法
- **THEN** 應回傳 `None`
- **AND** 應記錄地點找不到的訊息

#### Scenario: 溫度資料缺失
- **GIVEN** 指定地點存在但溫度資料欄位為空或無效
- **WHEN** 呼叫 `get_temperature_info(location_name)` 方法
- **THEN** 應回傳字典，但溫度欄位為 `None`
- **AND** 仍應包含地點名稱與可用資訊
- **AND** 不應拋出例外

### Requirement: Environment Variable Support
API 客戶端 SHALL 支援從環境變數讀取設定。

#### Scenario: 從環境變數讀取 API 金鑰
- **GIVEN** 環境變數 `CWA_API_KEY` 已設定
- **WHEN** 建立 `WeatherAPIClient()` 實例（無參數）
- **THEN** 應使用環境變數中的 API 金鑰
- **AND** 應優先使用環境變數，而非硬編碼預設值

#### Scenario: 環境變數未設定時使用預設值
- **GIVEN** 環境變數 `CWA_API_KEY` 未設定
- **WHEN** 建立 `WeatherAPIClient()` 實例
- **THEN** 應使用預設的 API 金鑰（向下相容）
- **AND** 應在 console 顯示使用預設金鑰的提示（選用）

### Requirement: Error Handling
API 客戶端 SHALL 優雅地處理所有可能的錯誤情況。

#### Scenario: HTTP 錯誤處理
- **GIVEN** API 回應 HTTP 錯誤狀態碼（如 401, 403, 500）
- **WHEN** 呼叫任何 API 方法
- **THEN** 應捕捉並記錄錯誤
- **AND** 應回傳 `None` 或空清單（視方法而定）
- **AND** 不應導致程式崩潰

#### Scenario: 逾時處理
- **GIVEN** API 回應時間超過 30 秒
- **WHEN** 呼叫 `fetch_weather_data()` 方法
- **THEN** 應拋出逾時錯誤並捕捉
- **AND** 應記錄逾時訊息
- **AND** 應回傳 `None`

#### Scenario: 資料結構變更
- **GIVEN** API 回應的 JSON 結構與預期不同
- **WHEN** 呼叫資料提取方法（如 `get_locations()`）
- **THEN** 應使用 `.get()` 安全存取欄位
- **AND** 應記錄資料結構異常的警告
- **AND** 應回傳空值而非崩潰
