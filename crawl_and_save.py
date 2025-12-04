"""
完整天氣資料爬蟲腳本
從 CWA API 取得所有地點的天氣資料並儲存到資料庫
"""
from weather_crawler import WeatherAPIClient
from database import WeatherDatabase


def crawl_all_weather_data():
    """爬取並儲存所有天氣資料"""
    print("=" * 60)
    print("開始爬取天氣資料")
    print("=" * 60)
    
    # 初始化客戶端（啟用資料庫）
    client = WeatherAPIClient(use_database=True)
    
    # 取得所有地點清單
    print("\n📍 取得地點清單...")
    locations = client.get_locations()
    
    if not locations:
        print("✗ 無法取得地點清單")
        return
    
    print(f"✓ 找到 {len(locations)} 個地點")
    print(f"地點列表: {', '.join(locations)}")
    
    # 逐一取得每個地點的天氣資料
    print(f"\n🌤️ 開始爬取所有地點的天氣資料...")
    success_count = 0
    fail_count = 0
    
    for i, location in enumerate(locations, 1):
        print(f"\n[{i}/{len(locations)}] 正在處理: {location}")
        temp_info = client.get_temperature_info(location)
        
        if temp_info:
            print(f"  ✓ 成功: {location}")
            print(f"    日期: {temp_info['date']}")
            print(f"    溫度: {temp_info['min_temp']}°C ~ {temp_info['max_temp']}°C")
            print(f"    天氣: {temp_info['weather']}")
            success_count += 1
        else:
            print(f"  ✗ 失敗: {location}")
            fail_count += 1
    
    # 顯示摘要
    print("\n" + "=" * 60)
    print("爬取完成")
    print("=" * 60)
    print(f"✓ 成功: {success_count} 筆")
    print(f"✗ 失敗: {fail_count} 筆")
    print(f"📊 總計: {success_count + fail_count} 筆")
    
    # 顯示資料庫統計
    if client.db:
        print("\n📈 資料庫統計...")
        stats = client.db.get_statistics()
        print(f"  總記錄數: {stats.get('total_records', 0)}")
        print(f"  地點數: {stats.get('unique_locations', 0)}")
        print(f"  資料庫大小: {stats.get('db_size_kb', 0)} KB")


if __name__ == "__main__":
    crawl_all_weather_data()
