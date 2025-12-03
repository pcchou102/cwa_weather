# Technical Design

## Architecture

### Component Structure
```
weather_crawler.py    # 現有 CLI 工具（保持不變）
weather_client.py     # 新增：可重用的 API 客戶端類別
weather_app.py        # 新增：Streamlit Web UI
requirements.txt      # 依賴套件清單
```

### Data Flow
```
使用者選擇地點
    ↓
Streamlit UI (weather_app.py)
    ↓
WeatherAPIClient (weather_client.py)
    ↓
CWA Open Data API
    ↓
解析並提取溫度資訊
    ↓
顯示在 Web UI
```

## Key Design Decisions

### 1. API 客戶端模組化
**決策**: 建立獨立的 `WeatherAPIClient` 類別，而非直接在 Streamlit 中呼叫 API

**理由**:
- 可重用性：CLI 和 Web UI 都能使用
- 可測試性：easier to unit test
- 關注點分離：UI 邏輯與 API 邏輯分離
- 快取友善：Streamlit 可使用 `@st.cache_data` 裝飾器

### 2. Streamlit 作為 Web 框架
**決策**: 使用 Streamlit 而非 Flask/FastAPI

**理由**:
- 快速原型開發
- 內建 UI 元件（下拉選單、載入狀態）
- 自動重載與互動性
- 適合資料視覺化應用
- 學習曲線低

### 3. 環境變數管理
**決策**: API 金鑰從環境變數 `CWA_API_KEY` 讀取，有預設值作為備援

**理由**:
- 安全性：避免將金鑰硬編碼
- 彈性：不同環境可使用不同金鑰
- 向下相容：提供預設值確保現有功能不中斷

### 4. 資料快取策略
**決策**: 使用 Streamlit 的 `@st.cache_data` 裝飾 API 呼叫函數

**理由**:
- 效能：避免重複 API 呼叫
- 使用者體驗：減少載入時間
- API 限制：減少對氣象署 API 的負擔

**實作**:
```python
@st.cache_data(ttl=600)  # 快取 10 分鐘
def fetch_cached_weather_data():
    client = WeatherAPIClient()
    return client.fetch_weather_data()
```

### 5. UI 設計模式
**決策**: 單頁應用，上方選擇地點，下方顯示結果

**佈局**:
```
┌─────────────────────────────────┐
│  標題：中央氣象署天氣資訊       │
├─────────────────────────────────┤
│  選擇地點: [下拉選單 ▼]         │
├─────────────────────────────────┤
│  📍 地點名稱                    │
│  🌡️ 當前溫度: XX°C             │
│  ↗️  最高溫: XX°C                │
│  ↘️  最低溫: XX°C                │
│  🕐 更新時間: YYYY-MM-DD HH:MM  │
└─────────────────────────────────┘
```

## Data Model

### WeatherAPIClient 類別結構
```python
class WeatherAPIClient:
    def __init__(self, api_key: str = None)
    def fetch_weather_data(self) -> Optional[Dict]
    def get_locations(self) -> List[str]
    def get_temperature_info(self, location_name: str) -> Optional[Dict]
```

### 溫度資訊結構
```python
{
    "location": "臺北市",
    "current_temp": 25,      # 當前溫度
    "max_temp": 28,          # 最高溫
    "min_temp": 22,          # 最低溫
    "update_time": "2025-12-03 14:30:00",
    "time_range": "今天白天"  # 時間範圍描述
}
```

## Error Handling

### API 錯誤
- HTTP 錯誤：顯示友善錯誤訊息，建議使用者檢查網路
- JSON 解析錯誤：提示 API 回應格式異常
- 逾時錯誤：提示伺服器回應過慢，稍後再試

### UI 錯誤
- 無資料：顯示「暫無資料」提示
- 地點不存在：顯示「找不到該地點」訊息
- 環境變數未設定：使用預設值並顯示警告

## Dependencies

### Required
- `streamlit >= 1.28.0` - Web UI 框架
- `requests >= 2.31.0` - HTTP 客戶端

### Optional
- `pandas >= 2.0.0` - 資料處理（如果需要進階資料操作）

## Testing Strategy

### Manual Testing Checklist
1. 啟動 Streamlit 應用 (`streamlit run weather_app.py`)
2. 驗證下拉選單顯示所有地點
3. 選擇不同地點，驗證溫度資訊更新
4. 測試網路錯誤情境（中斷網路）
5. 測試 API 金鑰錯誤情境
6. 驗證快取機制運作

### Future Improvements
- 單元測試：使用 pytest + mock
- E2E 測試：使用 Selenium 測試 UI 互動
- 效能測試：驗證快取效果
