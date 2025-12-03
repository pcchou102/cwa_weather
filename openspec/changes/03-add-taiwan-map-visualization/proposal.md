# Change 03: Add Taiwan Map Visualization

## Background
The user wants to visualize weather data on a map of Taiwan within the Streamlit app.
They specifically requested:
1.  A map of Taiwan.
2.  Displaying temperature information using different colors.
3.  Previewing the changes locally before deploying to GitHub.

## Proposed Changes
1.  **Update `weather_app.py`**:
    -   Define a mapping of Region Names (e.g., "北部地區") to Latitude/Longitude coordinates.
    -   Fetch weather data for all available regions on startup (or cache it).
    -   Create a Pandas DataFrame containing Location, Lat, Lon, and Temperature (Max Temp).
    -   Implement a `pydeck` chart (`st.pydeck_chart`) to display these points on a map.
    -   Configure the map layer to color points based on temperature (e.g., using a color scale).
    -   Add a tooltip to show details when hovering over a point.

## Technical Details
-   **Coordinates**:
    -   北部地區: 25.0330, 121.5654 (Taipei)
    -   中部地區: 24.1477, 120.6736 (Taichung)
    -   南部地區: 22.6273, 120.3014 (Kaohsiung)
    -   東北部地區: 24.7596, 121.7511 (Yilan)
    -   東南部地區: 22.7613, 121.1445 (Taitung)
    -   澎湖地區: 23.5711, 119.5793 (Penghu)
    -   (Add others if found in the list like 金門, 馬祖)
-   **Visualization**:
    -   Use `pdk.Layer` (ScatterplotLayer).
    -   `get_fill_color`: Function of temperature.
    -   `get_radius`: Fixed or function of something else.

## Verification Plan
-   Run `streamlit run weather_app.py`.
-   Verify the map appears.
-   Verify points are correctly positioned over Taiwan.
-   Verify colors change based on temperature.
