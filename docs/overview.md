# Overview

A mixed-integer linear programming (MILP) scheduler for crude oil tanker fleets (VLCC / Suezmax class). Given a 45-day horizon of cargo commitments and a vessel pool, the model assigns cargoes to vessels and optimises sailing speeds to minimise charter cost, bunker fuel consumption, and demurrage exposure, subject to the physical constraints of the trade (vessel DWT, port draft, laycan windows).

## Scope

**In scope**
- Crude oil tankers: VLCCs (~2M bbl) and Suezmaxes (~1M bbl)
- Loading: US Gulf primary (verified MarineCadastre AIS data)
- Discharge: Northwest Europe, Mediterranean, East Asia
- Deterministic optimisation with scenario sensitivity
- 45-day rolling horizon
- Interactive visualisation of the optimised schedule

**Out of scope**
- Real-time re-optimisation
- ML demand forecasting
- Freight derivatives hedging (FFAs)
- Emissions compliance (CII, EU ETS)
- Chartering strategy decisions
- Product tankers, LNG, dry bulk

## Mathematical approach

The core model is an MILP over binary vessel-cargo-time assignment variables plus continuous variables for sailing speed, ballast time, and demurrage slack.

The central technical move is **SOS2 linearisation of the cubic fuel–speed relationship**: bunker consumption F(s) ≈ α·s³ is approximated by piecewise-linear segments, with special-ordered-set-type-2 constraints enforcing that at most two *adjacent* breakpoint weights are nonzero. See [`formulation.md`](formulation.md) for the full formulation and a comparison of the native-SOS2 vs. manually-encoded paths.

## Model hierarchy

The codebase builds the model in three levels of increasing realism:

1. **Level 1 — Assignment MILP.** Vessel-cargo matching with cost, size, and draft compatibility. Solves in seconds.
2. **Level 2 — Time-aware MILP.** Adds laycan windows with demurrage slack, vessel continuity (ballast transit between cargoes), and no-overlap constraints.
3. **Level 3 — Speed-optimised MILP.** Adds continuous speed decisions with the SOS2-linearised fuel cost.

## Stack

- **Solvers:** SCIP via `pyscipopt` as the primary (native SOS2, Apache 2.0, bundled wheels). HiGHS for fast non-SOS models. Gurobi supported as an optional benchmark backend.
- **Modelling:** Pyomo — solver-agnostic.
- **Data:** Polars + Geopandas; Pydantic-validated ingestion.
- **Viz:** Streamlit shell with a custom React + D3 + Mapbox time-slider component. See [`visualization.md`](visualization.md) (WIP).

## Data sources

| Source | Purpose |
|---|---|
| MarineCadastre GeoParquet | US-waters AIS |
| Equasis | Vessel specs (~40 vessels) |
| World Port Index (NGA) | Port coordinates, drafts |
| `searoute` | Sea distance with canals |
| Baltic Exchange BDTI | Freight indices |
| Worldscale | Route baseline rates |
| Ship & Bunker | VLSFO prices |
| EIA petroleum exports | Trade-flow realism |

Real chartering fixtures are confidential. Cargoes are synthesised from EIA trade-flow data following industry parcel conventions; the model handles real fixtures identically. See [`data_sources.md`](data_sources.md) (WIP) for the synthesis methodology.

## Known limitations

- **Deterministic port service times.** Real congestion variance would require stochastic programming or robust optimisation.
- **No charter-party specifics.** Laytime clauses, off-hire provisions, and COA obligations are abstracted.
- **No weather routing.** Sailing times are nominal.
- **Synthetic cargoes.** Representative but not historical fixtures.
