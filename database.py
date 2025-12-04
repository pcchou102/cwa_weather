"""
中央氣象署天氣資料庫模組
使用 SQLite 儲存天氣資料，提供資料持久化與快取功能
"""
import sqlite3
import os
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from contextlib import contextmanager


class WeatherDatabase:
    """天氣資料庫管理類別"""
    
    def __init__(self, db_path: str = "data.db"):
        """
        初始化資料庫連線
        
        Args:
            db_path: 資料庫檔案路徑，預設為 data.db
        """
        self.db_path = db_path
        self.create_tables()
    
    @contextmanager
    def get_connection(self):
        """
        取得資料庫連線的 context manager
        
        Yields:
            sqlite3.Connection: 資料庫連線物件
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 讓查詢結果可以用欄位名稱存取
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def create_tables(self):
        """建立資料庫表格"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 建立天氣資料表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    date TEXT NOT NULL,
                    max_temp REAL,
                    min_temp REAL,
                    weather TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(location, date)
                )
            """)
            
            # 建立索引以提升查詢效能
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_location 
                ON weather_data(location)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_date 
                ON weather_data(date)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_location_date 
                ON weather_data(location, date)
            """)
            
            print(f"✓ 資料庫初始化完成: {self.db_path}")
    
    def insert_weather_data(
        self,
        location: str,
        date: str,
        max_temp: Optional[float],
        min_temp: Optional[float],
        weather: str
    ) -> bool:
        """
        插入或更新天氣資料
        
        Args:
            location: 地點名稱
            date: 日期 (YYYY-MM-DD)
            max_temp: 最高溫度
            min_temp: 最低溫度
            weather: 天氣現象
        
        Returns:
            bool: 成功返回 True，失敗返回 False
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 使用 INSERT OR REPLACE 來處理重複資料
                cursor.execute("""
                    INSERT INTO weather_data 
                    (location, date, max_temp, min_temp, weather, updated_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(location, date) 
                    DO UPDATE SET
                        max_temp = excluded.max_temp,
                        min_temp = excluded.min_temp,
                        weather = excluded.weather,
                        updated_at = CURRENT_TIMESTAMP
                """, (location, date, max_temp, min_temp, weather))
                
                return True
                
        except Exception as e:
            print(f"✗ 插入資料時發生錯誤: {e}")
            return False
    
    def get_latest_data(self, location: str) -> Optional[Dict[str, Any]]:
        """
        取得特定地點的最新天氣資料
        
        Args:
            location: 地點名稱
        
        Returns:
            Dict: 天氣資料字典，若無資料則返回 None
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT location, date, max_temp, min_temp, weather, updated_at
                    FROM weather_data
                    WHERE location = ?
                    ORDER BY date DESC, updated_at DESC
                    LIMIT 1
                """, (location,))
                
                row = cursor.fetchone()
                
                if row:
                    return {
                        'location': row['location'],
                        'date': row['date'],
                        'max_temp': row['max_temp'],
                        'min_temp': row['min_temp'],
                        'weather': row['weather'],
                        'updated_at': row['updated_at']
                    }
                
                return None
                
        except Exception as e:
            print(f"✗ 查詢資料時發生錯誤: {e}")
            return None
    
    def get_all_latest_data(self) -> List[Dict[str, Any]]:
        """
        取得所有地點的最新天氣資料
        
        Returns:
            List[Dict]: 天氣資料列表
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 使用子查詢取得每個地點的最新記錄
                cursor.execute("""
                    SELECT location, date, max_temp, min_temp, weather, updated_at
                    FROM weather_data
                    WHERE (location, date, updated_at) IN (
                        SELECT location, date, MAX(updated_at)
                        FROM weather_data
                        GROUP BY location
                    )
                    ORDER BY location
                """)
                
                rows = cursor.fetchall()
                
                return [
                    {
                        'location': row['location'],
                        'date': row['date'],
                        'max_temp': row['max_temp'],
                        'min_temp': row['min_temp'],
                        'weather': row['weather'],
                        'updated_at': row['updated_at']
                    }
                    for row in rows
                ]
                
        except Exception as e:
            print(f"✗ 查詢所有資料時發生錯誤: {e}")
            return []
    
    def is_data_fresh(self, location: str, ttl_minutes: int = 10) -> bool:
        """
        檢查資料是否在有效期限內
        
        Args:
            location: 地點名稱
            ttl_minutes: 資料有效期限（分鐘）
        
        Returns:
            bool: 資料新鮮返回 True，過期或不存在返回 False
        """
        data = self.get_latest_data(location)
        
        if not data:
            return False
        
        try:
            # 解析 updated_at 時間戳記
            updated_at = datetime.strptime(data['updated_at'], '%Y-%m-%d %H:%M:%S')
            current_time = datetime.now()
            time_diff = current_time - updated_at
            
            return time_diff < timedelta(minutes=ttl_minutes)
            
        except Exception as e:
            print(f"✗ 檢查資料新鮮度時發生錯誤: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        取得資料庫統計資訊
        
        Returns:
            Dict: 統計資訊
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 總記錄數
                cursor.execute("SELECT COUNT(*) as total FROM weather_data")
                total = cursor.fetchone()['total']
                
                # 地點數
                cursor.execute("SELECT COUNT(DISTINCT location) as locations FROM weather_data")
                locations = cursor.fetchone()['locations']
                
                # 資料庫檔案大小
                db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                
                return {
                    'total_records': total,
                    'unique_locations': locations,
                    'db_size_bytes': db_size,
                    'db_size_kb': round(db_size / 1024, 2)
                }
                
        except Exception as e:
            print(f"✗ 取得統計資訊時發生錯誤: {e}")
            return {}


if __name__ == "__main__":
    # 測試資料庫功能
    print("=" * 50)
    print("測試 WeatherDatabase")
    print("=" * 50)
    
    db = WeatherDatabase()
    
    # 插入測試資料
    print("\n📝 插入測試資料...")
    test_data = [
        ("台北市", "2025-12-03", 25.0, 18.0, "多雲時晴"),
        ("台中市", "2025-12-03", 24.0, 16.0, "晴天"),
        ("高雄市", "2025-12-03", 28.0, 22.0, "晴天"),
    ]
    
    for location, date, max_temp, min_temp, weather in test_data:
        success = db.insert_weather_data(location, date, max_temp, min_temp, weather)
        if success:
            print(f"✓ 成功插入: {location}")
        else:
            print(f"✗ 插入失敗: {location}")
    
    # 查詢特定地點
    print("\n🔍 查詢台北市資料...")
    taipei_data = db.get_latest_data("台北市")
    if taipei_data:
        print(f"✓ 查詢成功:")
        print(f"  地點: {taipei_data['location']}")
        print(f"  日期: {taipei_data['date']}")
        print(f"  最高溫: {taipei_data['max_temp']}°C")
        print(f"  最低溫: {taipei_data['min_temp']}°C")
        print(f"  天氣: {taipei_data['weather']}")
    
    # 查詢所有資料
    print("\n📊 查詢所有地點資料...")
    all_data = db.get_all_latest_data()
    print(f"✓ 找到 {len(all_data)} 筆記錄")
    
    # 統計資訊
    print("\n📈 資料庫統計...")
    stats = db.get_statistics()
    print(f"  總記錄數: {stats.get('total_records', 0)}")
    print(f"  地點數: {stats.get('unique_locations', 0)}")
    print(f"  資料庫大小: {stats.get('db_size_kb', 0)} KB")
