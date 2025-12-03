import requests
import json
from datetime import datetime

def fetch_weather_data():
    """
    從中央氣象署開放資料平台獲取天氣預報資料
    API: F-A0010-001 (鄉鎮天氣預報資料)
    """
    url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001"
    params = {
        "Authorization": "CWA-EED186C4-DA85-4467-8C6F-F87B1111AA87",
        "downloadType": "WEB",
        "format": "JSON"
    }
    
    try:
        print("正在獲取氣象資料...")
        response = requests.get(url, params=params, timeout=30)
        
        # 檢查回應狀態
        response.raise_for_status()
        
        # 解析 JSON 資料
        data = response.json()
        
        print(f"✓ 資料獲取成功！")
        print(f"狀態碼: {response.status_code}")
        print(f"回應時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 儲存資料到檔案
        output_filename = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 資料已儲存至: {output_filename}")
        
        # 顯示部分資料摘要
        if 'cwaopendata' in data:
            dataset = data['cwaopendata']
            print(f"\n=== 資料摘要 ===")
            print(f"資料集識別碼: {dataset.get('identifier', 'N/A')}")
            print(f"資料更新時間: {dataset.get('datasetInfo', {}).get('update', 'N/A')}")
            
            # 顯示位置資訊
            locations = dataset.get('dataset', {}).get('locations', [])
            if locations:
                location_count = len(locations[0].get('location', []))
                print(f"包含地點數量: {location_count}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"✗ 請求失敗: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"✗ JSON 解析失敗: {e}")
        return None
    except Exception as e:
        print(f"✗ 發生錯誤: {e}")
        return None

def main():
    print("=" * 50)
    print("中央氣象署天氣資料爬蟲")
    print("=" * 50)
    
    data = fetch_weather_data()
    
    if data:
        print("\n程式執行完成！")
    else:
        print("\n程式執行失敗！")

if __name__ == "__main__":
    main()
