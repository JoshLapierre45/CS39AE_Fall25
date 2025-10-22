lat, lon = 39.7392, -104.9903  # Denver
wurl = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
@st.cache_data(ttl=600)
def get_weather():
    r = requests.get(wurl, timeout=10); r.raise_for_status()
    j = r.json()["current"]
    return pd.DataFrame([{"time": pd.to_datetime(j["time"]),
                          "temperature": j["temperature_2m"],
                          "wind": j["wind_speed_10m"]}])
