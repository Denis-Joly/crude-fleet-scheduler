# Crude Fleet Scheduler

MILP-based scheduler for crude oil tanker fleets (VLCC / Suezmax). Assigns cargoes to vessels over a 45-day horizon, minimizing charter cost, bunker fuel consumption, and demurrage exposure — with SOS2 linearization of the cubic fuel–speed relationship.

**Status:** pre-start scaffolding (Apr 20 – May 3, 2026). See [project plan](vessel_routing_project_plan_v3.md).

## Highlights
- **SOS2 speed-fuel linearization** — same technique used in [pytfa](https://github.com/EPFL-LCSB/pytfa) for thermodynamic Gibbs-free-energy constraints, applied here to bunker fuel.
- **Hybrid dashboard** — Streamlit shell with a custom React + D3 + Mapbox time-slider component showing the optimized fleet animating across the horizon.
- **Production-quality data layer** — Pydantic-validated ingestion of MarineCadastre AIS, Equasis vessel specs, World Port Index ports.

## Quick start

```bash
uv sync --all-extras   # or: pip install -e ".[dev]"
pre-commit install
pytest

# run the app (release mode — serves the committed React bundle)
streamlit run app/streamlit_app.py
```

### Working on the React component

```bash
cd app/components/fleet_timeline
npm install
npm run dev                     # Vite on :3001, hot reload

# in another terminal, from repo root:
FLEET_TIMELINE_DEV=1 streamlit run app/streamlit_app.py
```

Before pushing any change to the component, rebuild and commit the output:

```bash
cd app/components/fleet_timeline && npm run build
git add build/ && git commit -m "rebuild fleet_timeline bundle"
```

Streamlit Cloud has no Node runtime, so the committed `build/` directory is
what it serves.

## Out of scope
Real-time re-optimization, ML demand forecasting, FFA hedging, emissions compliance (CII/EU ETS), chartering strategy, product tankers / LNG / dry bulk.

## License
MIT
