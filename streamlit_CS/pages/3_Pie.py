# pages/3_Pie.py
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Interactive Pie", page_icon="🥧", layout="centered")
st.title("Pie Chart of Different Space Objects")

# --- Resolve repo root even when this file lives in /pages
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "pie_demo.csv"

# --- Load CSV with strong guards
@st.cache_data(ttl=5)
def load_data(p: Path) -> pd.DataFrame:
    if not p.exists():
        # Fallback demo data so the chart still renders
        demo = pd.DataFrame({
            "Category": ["Satellite", "Launch Vehicle", "Ground Systems", "SDA", "R&D"],
            "Amount": [28, 22, 14, 19, 17]
        })
        return demo

    df = pd.read_csv(p)

    # Normalize common column-name mistakes
    cols = {c.strip().lower(): c for c in df.columns}
    # Map lower->original; we’ll reindex to canonical names
    # Accept a few aliases
    cat_col = None
    for cand in ["category", "name", "label"]:
        if cand in cols: cat_col = cols[cand]; break
    amt_col = None
    for cand in ["amount", "value", "count", "size"]:
        if cand in cols: amt_col = cols[cand]; break

    if cat_col is None or amt_col is None:
        raise ValueError(
            f"CSV needs columns like Category/Amount. Found: {list(df.columns)}"
        )

    df = df.rename(columns={cat_col: "Category", amt_col: "Amount"})

    # Coerce numeric, drop bad rows
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Category"] = df["Category"].astype(str).str.strip()
    df = df.dropna(subset=["Category", "Amount"])
    df = df[df["Category"] != ""]
    if df.empty:
        raise ValueError("After cleaning, no data rows remain. Check your CSV values.")

    return df

# --- Show path + quick diagnostics (helpful while you’re setting up)
with st.expander("🔍 Debug info"):
    st.write("Repo root:", ROOT)
    st.write("CSV path:", DATA_PATH)
    st.write("CSV exists:", DATA_PATH.exists())

try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

with st.expander("Preview data"):
    st.dataframe(df, use_container_width=True)

# --- Controls
st.sidebar.header("Controls")
chart_title = st.sidebar.text_input("Chart Title", value="Budget Allocation by Category")
selected = st.sidebar.multiselect(
    "Include categories",
    options=df["Category"].tolist(),
    default=df["Category"].tolist(),
)
norm = st.sidebar.checkbox("Normalize to 100%", value=True)
hole = st.sidebar.slider("Donut hole (0=pie, 0.6=donut)", 0.0, 0.6, 0.3, 0.05)
sort_slices = st.sidebar.checkbox("Sort by amount (desc)", value=True)

filtdf = df[df["Category"].isin(selected)].copy()
if sort_slices and not filtdf.empty:
    filtdf = filtdf.sort_values("Amount", ascending=False)

values_col = "Amount"
if norm and not filtdf.empty and filtdf["Amount"].sum() > 0:
    filtdf["Share"] = filtdf["Amount"] / filtdf["Amount"].sum() * 100
    values_col = "Share"

if filtdf.empty:
    st.warning("No categories selected or data is empty.")
else:
    fig = px.pie(filtdf, names="Category", values=values_col, hole=hole)
    # use width='stretch' (replacement for deprecated use_container_width)
    st.plotly_chart(fig, use_container_width=True)

st.caption("Tip: If edits aren’t showing, use the menu ▸ **Rerun** or Clear cache, or wait 5s (cache TTL).")
