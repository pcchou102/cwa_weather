"""
中央氣象署天氣資料 API 客戶端
可重用的 API 呼叫類別，供 CLI 和 Web UI 使用
"""
import os
import requests
import json
import urllib3
from typing import Optional, List, Dict, Any

# 停用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WeatherAPIClient:
    """中央氣象署開放資料 API 客戶端"""
    
    BASE_URL = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi"
    DEFAULT_API_KEY = "CWA-EED186C4-DA85-4467-8C6F-F87B1111AA87"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 API 客戶端
        
        Args:
            api_key: CWA API 授權金鑰，若未提供則從環境變數讀取
        """
        self.api_key = api_key or os.getenv("CWA_API_KEY", self.DEFAULT_API_KEY)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WeatherCrawler/1.0'
        })
    
    def fetch_weather_data(self) -> Optional[Dict[str, Any]]:
        """
        取得完整的天氣預報資料
        
        Returns:
            Dict: 完整的 JSON 資料，失敗則返回 None
        """
        url = f"{self.BASE_URL}/F-A0010-001"
        params = {
            "Authorization": self.api_key,
            "downloadType": "WEB",
            "format": "JSON"
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            response.raise_for_status()
            data = response.json()
            return data
            
        except requests.exceptions.Timeout:
            print(f"✗ API 請求逾時（超過 30 秒）")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"✗ HTTP 錯誤: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"✗ 請求失敗: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"✗ JSON 解析失敗: {e}")
            return None
        except Exception as e:
            print(f"✗ 未預期的錯誤: {e}")
            return None
    
    def get_locations(self) -> List[str]:
        """
        取得所有可用地點的清單
        
        Returns:
            List[str]: 地點名稱清單，按字母順序排序
        """
        data = self.fetch_weather_data()
        if not data:
            return []
        
        try:
            # 導航到 location 清單
            root = data.get('cwaopendata', {})
            resources = root.get('resources', {})
            resource = resources.get('resource', {})
            data_node = resource.get('data', {})
            agr_forecasts = data_node.get('agrWeatherForecasts', {})
            weather_forecasts = agr_forecasts.get('weatherForecasts', {})
            locations = weather_forecasts.get('location', [])
            
            if not locations:
                print("⚠ 找不到地點資料，資料結構可能已變更")
                return []
            
            # 提取地點名稱並排序
            location_names = [loc.get('locationName', '') for loc in locations if loc.get('locationName')]
            return sorted(location_names)
            
        except Exception as e:
            print(f"✗ 提取地點清單時發生錯誤: {e}")
            return []
    
    def get_temperature_info(self, location_name: str) -> Optional[Dict[str, Any]]:
        """
        取得特定地點的溫度資訊
        
        Args:
            location_name: 地點名稱（如「臺北市」）
        
        Returns:
            Dict: 包含溫度資訊的字典，失敗則返回 None
            {
                'location': str,
                'date': str,
                'max_temp': float or None,
                'min_temp': float or None,
                'weather': str
            }
        """
        data = self.fetch_weather_data()
        if not data:
            return None
        
        try:
            # 導航到 location 清單
            root = data.get('cwaopendata', {})
            resources = root.get('resources', {})
            resource = resources.get('resource', {})
            data_node = resource.get('data', {})
            agr_forecasts = data_node.get('agrWeatherForecasts', {})
            weather_forecasts = agr_forecasts.get('weatherForecasts', {})
            locations = weather_forecasts.get('location', [])
            
            # 找到指定的地點
            target_location = None
            for loc in locations:
                if loc.get('locationName') == location_name:
                    target_location = loc
                    break
            
            if not target_location:
                print(f"✗ 找不到地點: {location_name}")
                return None
            
            # 提取溫度資訊
            elements = target_location.get('weatherElements', {})
            
            # 最高溫
            max_t_data = elements.get('MaxT', {}).get('daily', [])
            first_day_max = max_t_data[0] if max_t_data else {}
            max_temp_str = first_day_max.get('temperature', '-')
            max_temp = self._parse_temperature(max_temp_str)
            
            # 最低溫
            min_t_data = elements.get('MinT', {}).get('daily', [])
            first_day_min = min_t_data[0] if min_t_data else {}
            min_temp_str = first_day_min.get('temperature', '-')
            min_temp = self._parse_temperature(min_temp_str)
            
            # 日期
            date = first_day_max.get('dataDate', '-')
            
            # 天氣現象
            wx_data = elements.get('Wx', {}).get('daily', [])
            first_day_wx = wx_data[0] if wx_data else {}
            weather = first_day_wx.get('weather', '-')
            
            return {
                'location': location_name,
                'date': date,
                'max_temp': max_temp,
                'min_temp': min_temp,
                'weather': weather
            }
            
        except Exception as e:
            print(f"✗ 提取溫度資訊時發生錯誤: {e}")
            return None
    
    def _parse_temperature(self, temp_str: str) -> Optional[float]:
        """
        解析溫度字串為浮點數
        
        Args:
            temp_str: 溫度字串
        
        Returns:
            float or None: 溫度數值，無效則返回 None
        """
        if temp_str == '-' or not temp_str:
            return None
        try:
            return float(temp_str)
        except (ValueError, TypeError):
            return None


if __name__ == "__main__":
    # 測試 API 客戶端
    print("=" * 50)
    print("測試 WeatherAPIClient")
    print("=" * 50)
    
    client = WeatherAPIClient()
    
    # 測試取得地點清單
    print("\n📍 取得地點清單...")
    locations = client.get_locations()
    if locations:
        print(f"✓ 找到 {len(locations)} 個地點")
        print(f"前 5 個地點: {locations[:5]}")
    else:
        print("✗ 無法取得地點清單")
    
    # 測試取得特定地點溫度
    if locations:
        test_location = locations[0]
        print(f"\n🌡️ 取得「{test_location}」的溫度資訊...")
        temp_info = client.get_temperature_info(test_location)
        if temp_info:
            print(f"✓ 成功取得資訊:")
            print(f"  地點: {temp_info['location']}")
            print(f"  日期: {temp_info['date']}")
            print(f"  最高溫: {temp_info['max_temp']}°C")
            print(f"  最低溫: {temp_info['min_temp']}°C")
            print(f"  天氣: {temp_info['weather']}")
        else:
            print("✗ 無法取得溫度資訊")
