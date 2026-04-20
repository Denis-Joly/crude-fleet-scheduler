# fleet_timeline component

Custom Streamlit component — time-slider map of the optimized fleet schedule.
This directory is the **pre-start scaffold** that proves the toolchain; the
real D3 + Mapbox implementation lands in Week 12 per project plan §7.

## Local dev

```bash
cd app/components/fleet_timeline
npm install
npm run dev            # Vite dev server on :3001
```

In a second terminal from the repo root:

```bash
FLEET_TIMELINE_DEV=1 streamlit run app/streamlit_app.py
```

`FLEET_TIMELINE_DEV=1` flips the component to load from the Vite dev server
(hot reload). Unset it (or run `streamlit run …` normally) to serve the
committed `build/` bundle — that's what Streamlit Cloud uses.

## Before pushing

Rebuild and commit so the deployed version stays in sync:

```bash
npm run build
git add build/ && git commit -m "rebuild fleet_timeline bundle"
```
