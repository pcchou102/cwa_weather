# 中央氣象署天氣資料爬蟲與 Web UI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cwa-weather.streamlit.app)

> 🌐 **線上體驗：** [https://cwa-weather.streamlit.app](https://cwa-weather.streamlit.app)

從中央氣象署開放資料平台獲取鄉鎮天氣預報資料，提供 CLI 和 Web UI 兩種使用方式。

## 功能特色

- 🌐 **Web UI**：使用 Streamlit 建構的友善網頁介面
- 📍 **地點選擇**：下拉式選單選擇全台各地
- 🌡️ **溫度資訊**：顯示最高溫、最低溫與平均溫度
- ☁️ **天氣現象**：顯示天氣狀況描述
- 💾 **CLI 工具**：命令列介面，可儲存 JSON 資料
- ⚡ **快取機制**：10 分鐘快取，減少 API 呼叫

## 專案結構

```
.
├── weather_crawler.py   # CLI 爬蟲工具（原有功能）
├── weather_client.py    # 可重用的 API 客戶端類別
├── weather_app.py       # Streamlit Web UI
├── requirements.txt     # Python 套件依賴
└── README.md           # 專案說明文件
```

## 安裝

### 前置需求
- Python 3.8 或更新版本
- Git（如需部署到 GitHub）

### 1. 安裝 Python 套件

```bash
pip install -r requirements.txt
```

或手動安裝：

```bash
pip install requests streamlit
```

### 2. 設定 API 金鑰（選用）

預設已內建 API 金鑰，但建議使用自己的金鑰：

**Windows PowerShell:**
```powershell
# 暫時設定（當前工作階段）
$env:CWA_API_KEY="your-api-key-here"

# 永久設定
setx CWA_API_KEY "your-api-key-here"
```

**Windows CMD:**
```cmd
setx CWA_API_KEY "your-api-key-here"
```

**Linux / macOS:**
```bash
export CWA_API_KEY="your-api-key-here"
```

> 💡 如何取得 API 金鑰：前往 [中央氣象署開放資料平台](https://opendata.cwa.gov.tw/) 註冊並申請金鑰

## 使用方式

### 方式 1: Web UI（推薦）

啟動 Streamlit 應用：

```bash
streamlit run weather_app.py
```

瀏覽器會自動開啟 `http://localhost:8501`，然後：

1. 從下拉選單選擇地點
2. 檢視該地點的溫度與天氣資訊
3. 資料每 10 分鐘自動更新

### 方式 2: CLI 爬蟲

執行命令列爬蟲並儲存 JSON 檔案：

```bash
python weather_crawler.py
```

資料會儲存為 `weather_data.json` 並在終端顯示表格。

### 方式 3: Python 程式中使用

```python
from weather_client import WeatherAPIClient

# 建立客戶端
client = WeatherAPIClient()

# 取得所有地點
locations = client.get_locations()
print(f"可用地點: {locations[:5]}")

# 取得特定地點溫度
temp_info = client.get_temperature_info("臺北市")
if temp_info:
    print(f"地點: {temp_info['location']}")
    print(f"最高溫: {temp_info['max_temp']}°C")
    print(f"最低溫: {temp_info['min_temp']}°C")
    print(f"天氣: {temp_info['weather']}")
```

## API 說明

### WeatherAPIClient 類別

#### 初始化

```python
client = WeatherAPIClient(api_key="optional-api-key")
```

- `api_key` (選用): API 金鑰，未提供則從環境變數 `CWA_API_KEY` 讀取

#### 方法

**`fetch_weather_data() -> Optional[Dict]`**
- 取得完整的天氣預報 JSON 資料
- 返回：完整 JSON 字典或 `None`（失敗時）

**`get_locations() -> List[str]`**
- 取得所有可用地點的清單
- 返回：地點名稱清單（已排序）

**`get_temperature_info(location_name: str) -> Optional[Dict]`**
- 取得特定地點的溫度資訊
- 參數：`location_name` - 地點名稱（如「臺北市」）
- 返回：包含以下欄位的字典：
  - `location`: 地點名稱
  - `date`: 預報日期
  - `max_temp`: 最高溫度（°C）
  - `min_temp`: 最低溫度（°C）
  - `weather`: 天氣現象描述

## 資料來源

- **API**: 中央氣象署開放資料平台
- **資料集**: F-A0010-001（鄉鎮天氣預報資料）
- **更新頻率**: 依氣象署發布時間

## 技術棧

- **Python**: 3.13
- **Streamlit**: Web UI 框架
- **Requests**: HTTP 客戶端
- **CWA Open Data API**: 資料來源

## 疑難排解

### 問題：無法連線到 API

**解決方式：**
1. 檢查網路連線
2. 確認 API 金鑰有效
3. 檢查中央氣象署服務狀態

### 問題：Streamlit 無法啟動

**解決方式：**
```bash
# 重新安裝 streamlit
pip install --upgrade streamlit

# 檢查 Python 版本（需 3.8+）
python --version
```

### 問題：找不到地點資料

**解決方式：**
- API 資料結構可能已變更
- 查看終端錯誤訊息
- 確認 API 回應格式

## 授權

本專案僅供學習與研究用途。資料版權歸中央氣象署所有。

## 部署到雲端

想要將應用部署到網路上？查看 [DEPLOY.md](DEPLOY.md) 了解如何部署到 Streamlit Cloud。

**快速部署步驟：**
1. 將程式碼推送到 GitHub
2. 前往 [Streamlit Cloud](https://share.streamlit.io/)
3. 連結您的 GitHub 儲存庫
4. 設定 `weather_app.py` 為主檔案
5. 點擊部署！

詳細步驟請參考 [DEPLOY.md](DEPLOY.md)。

## 作者

pcchou102

## 更新日誌

### v1.2.0 (2025-12-03)
- ✨ UI 大幅美化，參考 CWA 官網設計
- 🎨 新增專業配色與漸層效果
- 🌡️ 新增溫度範圍視覺化條形圖
- 🌤️ 新增天氣圖示系統
- 📱 優化響應式設計
- 🎴 改為卡片式佈局

### v1.1.0 (2025-12-03)
- ✨ 新增 Streamlit Web UI
- ✨ 新增可重用的 API 客戶端類別
- ✨ 新增環境變數支援
- ✨ 新增資料快取機制
- 📝 完善文件說明

### v1.0.0
- 🎉 初始版本
- ✨ CLI 爬蟲功能
