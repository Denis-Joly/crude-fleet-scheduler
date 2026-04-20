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
streamlit run app/streamlit_app.py
```

`__init__.py` has `_RELEASE = False`, so Streamlit loads the component from
the Vite dev server. Flip to `True` and run `npm run build` to use the bundled
`build/` output for deployment.
