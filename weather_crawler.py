import requests
import json
import sys

def fetch_weather_data():
    # The URL provided
    url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=CWA-EED186C4-DA85-4467-8C6F-F87B1111AA87&downloadType=WEB&format=JSON"
    
    print(f"Fetching data from: {url}...")
    
    try:
        # Send a GET request to the API
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse the JSON content
        data = response.json()
        
        # Define the output filename
        filename = "weather_data.json"
        
        # Save the data to a JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Success! Data has been saved to '{filename}'.")
        
        # Parse and display the table
        extract_and_display_table(data)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error: Failed to decode JSON response.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)

def extract_and_display_table(data):
    """
    Parses the specific structure of CWA F-A0010-001 (Agriculture Forecast)
    Structure: cwaopendata -> resources -> resource -> data -> agrWeatherForecasts -> weatherForecasts -> location
    """
    print("\n" + "="*80)
    # Define table columns: Location, Date, Max Temp, Min Temp, Weather
    print(f"{'地點 (Location)':<12} | {'日期 (Date)':<12} | {'最高溫 (MaxT)':<12} | {'最低溫 (MinT)':<12} | {'天氣現象 (Weather)'}")
    print("="*80)

    try:
        # Correct navigation based on the actual JSON structure
        root = data.get('cwaopendata', {})
        resources = root.get('resources', {})
        resource = resources.get('resource', {})
        data_node = resource.get('data', {})
        agr_forecasts = data_node.get('agrWeatherForecasts', {})
        weather_forecasts = agr_forecasts.get('weatherForecasts', {})
        locations = weather_forecasts.get('location', [])

        if not locations:
            print("❌ No location data found. The JSON structure might have changed.")
            # Debug: print available keys to help diagnose
            print(f"Debug - Keys found in 'data': {data_node.keys()}")
            return

        for loc in locations:
            name = loc.get('locationName', 'Unknown')
            
            # In this dataset, weatherElements is a dictionary, not a list
            elements = loc.get('weatherElements', {})
            
            # Extract Max Temperature (MaxT)
            # Structure: elements['MaxT']['daily'][0]
            max_t_data = elements.get('MaxT', {}).get('daily', [])
            first_day_max = max_t_data[0] if max_t_data else {}
            max_temp = first_day_max.get('temperature', '-')
            date = first_day_max.get('dataDate', '-') # Get date from the first element

            # Extract Min Temperature (MinT)
            min_t_data = elements.get('MinT', {}).get('daily', [])
            first_day_min = min_t_data[0] if min_t_data else {}
            min_temp = first_day_min.get('temperature', '-')

            # Extract Weather Description (Wx)
            wx_data = elements.get('Wx', {}).get('daily', [])
            first_day_wx = wx_data[0] if wx_data else {}
            weather = first_day_wx.get('weather', '-')

            # Print the row
            print(f"{name:<14} | {date:<12} | {max_temp:>5} °C      | {min_temp:>5} °C      | {weather}")

    except Exception as e:
        print(f"❌ Error parsing data for table: {e}")

if __name__ == "__main__":
    fetch_weather_data()