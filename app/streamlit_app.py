"""Streamlit shell — pre-start PoC.

Confirms the React component bridge works. Real scenario picker, solver
integration, and KPI dashboard arrive in Weeks 10–13 per project plan.
"""

from __future__ import annotations

import streamlit as st

from app.components.fleet_timeline import fleet_timeline

st.set_page_config(page_title="Crude Fleet Scheduler", layout="wide")

st.title("Crude Fleet Scheduler")
st.caption("Pre-start PoC — toolchain smoke test")

demo_vessels = [
    {"id": "V001", "name": "Nordic Dawn"},
    {"id": "V002", "name": "Atlantic Voyager"},
]

horizon = st.slider("Horizon (days)", min_value=7, max_value=90, value=45)

fleet_timeline(vessels=demo_vessels, horizon_days=horizon, key="pre_start_poc")
