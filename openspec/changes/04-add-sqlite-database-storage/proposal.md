# Change 04: Add SQLite Database Storage

## Background
The user wants to persist weather data downloaded from the CWA API into a local SQLite database (`data.db`).
This will enable:
1. Historical data tracking
2. Reduced API calls (cache previous results)
3. Data analysis capabilities
4. Offline access to recent weather data

## Proposed Changes

### 1. Create `database.py` module
- Implement `WeatherDatabase` class for SQLite operations
- Table schema: `weather_data`
  - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
  - `location`: TEXT NOT NULL
  - `date`: TEXT NOT NULL
  - `max_temp`: REAL
  - `min_temp`: REAL
  - `weather`: TEXT
  - `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  - `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- Methods:
  - `create_tables()`: Initialize database schema
  - `insert_weather_data(location, date, max_temp, min_temp, weather)`: Add new record
  - `get_latest_data(location)`: Retrieve most recent data for a location
  - `get_all_latest_data()`: Retrieve latest data for all locations
  - `update_weather_data(location, date, ...)`: Update existing record
  - `close()`: Close database connection

### 2. Update `weather_client.py`
- Add optional database integration
- Store fetched data automatically when database is enabled
- Check database first before making API calls (with TTL check)

### 3. Update `weather_app.py`
- Initialize database on startup
- Use database-backed data fetching

### 4. Add `.gitignore` entry
- Exclude `data.db` from version control

## Technical Details
- Database file: `data.db` (SQLite3)
- Use `sqlite3` standard library (no additional dependencies)
- Implement connection pooling for web app
- Add indexes on `location` and `date` for query performance
- Use context managers for safe connection handling

## Verification Plan
- Create database and verify schema
- Insert sample data and query it back
- Verify `data.db` is created in project root
- Test API → Database → App data flow
- Confirm data persists across app restarts
