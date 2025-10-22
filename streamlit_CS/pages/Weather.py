# pages/6_Forecast_Precip.py
import streamlit as st
import pandas as pd
import requests
import time
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(page_title="14-Day Forecast: Precipitation (inches)", page_icon="🌧️", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1501691223387-dd0500403074?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=927");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: rgba(0,0,0,0);  /* make header transparent */
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
  [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
    transition: none !important;
    opacity: 1 !important;
  }
</style>
""", unsafe_allow_html=True)

st.title("🌧️ 14-Day Forecast — Precipitation (inches)")
st.caption("Daily precipitation (in) as area + precipitation probability (%) on a secondary axis. Default: Denver, CO.")

# --- City selector ---
PRESETS = {
    "Denver, CO": (39.7392, -104.9903),
    "Colorado Springs, CO": (38.8339, -104.8214),
    "Boulder, CO": (40.01499, -105.2705),
}
city = st.selectbox("Select City", list(PRESETS.keys()), index=0)
lat, lon = PRESETS[city]

# --- API setup (daily forecast) ---
api_url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}&longitude={lon}"
    "&daily=precipitation_sum,precipitation_probability_max,"
    "temperature_2m_max,temperature_2m_min"
    "&forecast_days=16&timezone=auto"
)
HEADERS = {"User-Agent": "msudenver-dataviz-class/1.0", "Accept": "application/json"}

@st.cache_data(ttl=600, show_spinner=False)
def get_daily_forecast(url: str):
    """Fetch 14-day forecast and convert precipitation to inches."""
    try:
        r = requests.get(url, timeout=12, headers=HEADERS)
        r.raise_for_status()
        j = r.json()
        d = j["daily"]

        df = pd.DataFrame({
            "date": pd.to_datetime(d["time"]),
            "precip_mm": d.get("precipitation_sum", [None] * len(d["time"])),
            "precip_prob": d.get("precipitation_probability_max", [None] * len(d["time"])),
            "tmax": d.get("temperature_2m_max", [None] * len(d["time"])),
            "tmin": d.get("temperature_2m_min", [None] * len(d["time"])),
        })
        df = df.iloc[:14].copy()                # limit to 14 days
        df["precip_in"] = df["precip_mm"] / 25.4   # convert mm → inches
        return df, None
    except Exception as e:
        # fallback demo data (inches)
        dates = pd.date_range(pd.Timestamp.today().normalize(), periods=14, freq="D")
        demo = pd.DataFrame({
            "date": dates,
            "precip_in": [0.0, 0.02, 0.08, 0.0, 0.04, 0.15, 0.03, 0.0, 0.12, 0.05, 0.0, 0.1, 0.01, 0.0],
            "precip_prob": [5, 20, 60, 10, 35, 80, 40, 15, 75, 45, 10, 70, 25, 5],
            "tmax": [65, 67, 63, 70, 72, 60, 66, 68, 58, 62, 71, 61, 66, 68],
            "tmin": [42, 44, 46, 48, 45, 40, 42, 43, 38, 40, 46, 41, 42, 44],
        })
        return demo, f"API error (showing demo data): {e}"

# --- Auto-refresh controls ---
st.subheader("🔁 Auto-Refresh Settings")
refresh_sec = st.slider("Refresh every (sec)", 30, 300, 120)
auto_refresh = st.toggle("Enable auto-refresh", value=False)
st.caption(f"Last refreshed at: {time.strftime('%H:%M:%S')}")

# --- Fetch + preview ---
df, err = get_daily_forecast(api_url)
if err:
    st.warning(err)

with st.expander("Preview data"):
    st.dataframe(df, use_container_width=True)

# --- Plot: Precipitation (area, inches) + Probability (line, %) ---
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(
        x=df["date"], y=df["precip_in"],
        mode="lines",
        fill="tozeroy",
        name="Precipitation (in)"
    ),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(
        x=df["date"], y=df["precip_prob"],
        mode="lines+markers",
        name="Precipitation Probability (%)"
    ),
    secondary_y=True
)

fig.update_layout(
    title=f"{city} — 14-Day Precipitation Forecast",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=60, b=20)
)
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Precipitation (in)", secondary_y=False)
fig.update_yaxes(title_text="Probability (%)", range=[0, 100], secondary_y=True)

st.plotly_chart(fig, use_container_width=True)

# --- Auto-refresh loop ---
if auto_refresh:
    time.sleep(refresh_sec)
    get_daily_forecast.clear()
    st.rerun()
