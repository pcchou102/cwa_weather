"""
中央氣象署天氣資訊 Streamlit Web 應用
顯示各地點的溫度資訊，提供下拉式選單選擇地點
參考 CWA 官網設計的美化版本
"""
import streamlit as st
from weather_client import WeatherAPIClient


# 設定頁面配置
st.set_page_config(
    page_title="中央氣象署天氣資訊",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="expanded"
)


def get_weather_icon(weather_description: str) -> str:
    """
    根據天氣描述返回對應的 emoji 圖示
    
    Args:
        weather_description: 天氣描述文字
    
    Returns:
        str: 對應的 emoji 圖示
    """
    weather_map = {
        '晴': '☀️',
        '多雲時晴': '🌤️',
        '多雲': '⛅',
        '陰': '☁️',
        '陰天': '☁️',
        '雨': '🌧️',
        '陣雨': '🌦️',
        '雷': '⛈️',
        '雷雨': '⛈️',
        '雪': '❄️',
        '霧': '🌫️',
    }
    
    # 檢查描述中是否包含關鍵字
    for keyword, icon in weather_map.items():
        if keyword in weather_description:
            return icon
    
    # 預設圖示
    return '🌤️'


def get_temperature_color(temp: float) -> str:
    """
    根據溫度返回對應的顏色代碼
    
    Args:
        temp: 溫度值（攝氏）
    
    Returns:
        str: CSS 顏色代碼
    """
    if temp < 10:
        return '#2196F3'  # 藍色 - 寒冷
    elif temp < 20:
        return '#4CAF50'  # 綠色 - 涼爽
    elif temp < 28:
        return '#FFC107'  # 黃色 - 舒適
    elif temp < 32:
        return '#FF9800'  # 橙色 - 炎熱
    else:
        return '#F44336'  # 紅色 - 酷熱


def inject_custom_css():
    """注入自訂 CSS 樣式"""
    st.markdown("""
        <style>
        /* 全域樣式 */
        .main {
            background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%);
        }
        
        /* 頁首樣式 */
        .header-banner {
            background: linear-gradient(135deg, #1E88E5 0%, #42A5F5 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .header-banner h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        .header-banner p {
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
            opacity: 0.95;
        }
        
        /* 資訊卡片樣式 */
        .info-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .info-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Metric 卡片優化 */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
        }
        
        /* 移除 metric 的 delta 空白區域 */
        [data-testid="stMetricDelta"] {
            display: none;
        }
        
        /* 調整 metric 間距 */
        [data-testid="stMetric"] {
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* 溫度範圍條 */
        .temp-range-bar {
            height: 30px;
            border-radius: 15px;
            background: linear-gradient(90deg, 
                #2196F3 0%,
                #4CAF50 25%,
                #FFC107 50%,
                #FF9800 75%,
                #F44336 100%);
            position: relative;
            margin: 1.5rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .temp-marker {
            position: absolute;
            top: -5px;
            width: 4px;
            height: 40px;
            background: white;
            border: 2px solid #212121;
            border-radius: 2px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        /* 天氣圖示 */
        .weather-icon {
            font-size: 4rem;
            text-align: center;
            margin: 1rem 0;
        }
        
        /* 頁尾樣式 */
        .footer {
            text-align: center;
            padding: 2rem 0 1rem 0;
            color: #666;
            font-size: 0.9rem;
            border-top: 1px solid #e0e0e0;
            margin-top: 3rem;
        }
        
        /* 選擇器優化 */
        .stSelectbox {
            margin-bottom: 1.5rem;
        }
        
        /* 移除 Streamlit 預設的上邊距 */
        .block-container {
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)


@st.cache_data(ttl=600)  # 快取 10 分鐘
def fetch_all_locations():
    """取得所有地點清單（帶快取）"""
    client = WeatherAPIClient()
    return client.get_locations()


@st.cache_data(ttl=600)  # 快取 10 分鐘
def fetch_temperature_info(location_name: str):
    """取得特定地點的溫度資訊（帶快取）"""
    client = WeatherAPIClient()
    return client.get_temperature_info(location_name)


def main():
    """主應用程式"""
    
    # 注入自訂 CSS
    inject_custom_css()
    
    # 頁首橫幅
    st.markdown("""
        <div class="header-banner">
            <h1>🌤️ 中央氣象署天氣資訊</h1>
            <p>即時天氣預報・溫度查詢・全台覆蓋</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 取得地點清單
    with st.spinner("🔄 正在載入地點清單..."):
        locations = fetch_all_locations()
    
    if not locations:
        st.error("❌ 無法取得地點清單，請檢查網路連線或稍後再試")
        st.info("💡 提示：請確認您的網路連線正常，且 CWA API 服務可用")
        return
    
    # 地點選擇器
    st.markdown("### 📍 選擇查詢地點")
    selected_location = st.selectbox(
        "請選擇想查看的地點：",
        options=locations,
        index=0,
        label_visibility="collapsed"
    )
    
    # 取得並顯示溫度資訊
    if selected_location:
        with st.spinner(f"🔄 正在載入 {selected_location} 的天氣資料..."):
            temp_info = fetch_temperature_info(selected_location)
        
        if temp_info:
            # 地點標題
            st.markdown(f"## 📍 {temp_info['location']}")
            
            # 天氣圖示
            weather_icon = get_weather_icon(temp_info['weather'])
            st.markdown(f'<div class="weather-icon">{weather_icon}</div>', unsafe_allow_html=True)
            
            # 天氣現象
            st.markdown(f"### {temp_info['weather']}")
            
            st.markdown("---")
            
            # 溫度 metrics
            col1, col2, col3 = st.columns(3)
            
            max_temp = temp_info['max_temp']
            min_temp = temp_info['min_temp']
            
            with col1:
                if max_temp is not None:
                    st.metric(
                        label="🌡️ 最高溫",
                        value=f"{max_temp}°C"
                    )
                else:
                    st.metric(label="🌡️ 最高溫", value="無資料")
            
            with col2:
                if min_temp is not None:
                    st.metric(
                        label="❄️ 最低溫",
                        value=f"{min_temp}°C"
                    )
                else:
                    st.metric(label="❄️ 最低溫", value="無資料")
            
            with col3:
                if max_temp is not None and min_temp is not None:
                    avg_temp = (max_temp + min_temp) / 2
                    st.metric(
                        label="📊 平均溫度",
                        value=f"{avg_temp:.1f}°C"
                    )
                else:
                    st.metric(label="📊 平均溫度", value="無資料")
            
            # 溫度範圍視覺化
            if max_temp is not None and min_temp is not None:
                st.markdown("### 🌡️ 溫度範圍")
                avg_temp = (max_temp + min_temp) / 2
                
                # 計算平均溫度在 0-40°C 範圍內的相對位置
                marker_position = ((avg_temp - 0) / (40 - 0)) * 100
                marker_position = max(0, min(100, marker_position))  # 限制在 0-100%
                
                st.markdown(f"""
                    <div class="temp-range-bar">
                        <div class="temp-marker" style="left: {marker_position}%;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #666;">
                        <span>💙 {min_temp}°C</span>
                        <span>📊 {avg_temp:.1f}°C</span>
                        <span>❤️ {max_temp}°C</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # 預報日期
            st.markdown("### 📅 預報資訊")
            st.info(f"📆 預報日期：{temp_info['date'] if temp_info['date'] != '-' else '無資料'}")
            
            # 資料來源說明
            st.caption("📡 資料來源：中央氣象署開放資料平台")
            st.caption("⏱️ 資料每 10 分鐘自動更新")
            
        else:
            st.error(f"❌ 無法取得「{selected_location}」的溫度資訊")
            st.info("💡 提示：資料可能暫時無法使用，請稍後再試")
    
    # 頁尾
    st.markdown("""
        <div class="footer">
            <p>© 2025 AIoT 天氣資料專案 | 資料來源：中央氣象署開放資料平台</p>
            <p>本服務僅供參考，實際天氣狀況請以中央氣象署官方發布為準</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 側邊欄：使用說明
    with st.sidebar:
        st.markdown("## 📖 使用說明")
        st.markdown("""
        <div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <p style="margin: 0.5rem 0;"><strong>1️⃣</strong> 從下拉選單選擇地點</p>
            <p style="margin: 0.5rem 0;"><strong>2️⃣</strong> 檢視該地點的溫度資訊</p>
            <p style="margin: 0.5rem 0;"><strong>3️⃣</strong> 資料每 10 分鐘自動更新</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🌡️ 溫度等級說明")
        st.markdown("""
        <div style="font-size: 0.9rem;">
            <p>💙 <strong style="color: #2196F3;">10°C 以下</strong> - 寒冷</p>
            <p>💚 <strong style="color: #4CAF50;">10-20°C</strong> - 涼爽</p>
            <p>💛 <strong style="color: #FFC107;">20-28°C</strong> - 舒適</p>
            <p>🧡 <strong style="color: #FF9800;">28-32°C</strong> - 炎熱</p>
            <p>❤️ <strong style="color: #F44336;">32°C 以上</strong> - 酷熱</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ⚙️ 環境設定")
        with st.expander("🔑 設定 API 金鑰（選用）"):
            st.code("""
# Windows PowerShell
$env:CWA_API_KEY="your-api-key"

# 或永久設定
setx CWA_API_KEY "your-api-key"
            """, language="bash")
            st.caption("若未設定，將使用預設金鑰")
        
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <p style="font-size: 0.85rem; color: #666;">Made with ❤️ using</p>
                <p style="font-size: 1rem; font-weight: bold; color: #FF4B4B;">Streamlit</p>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
