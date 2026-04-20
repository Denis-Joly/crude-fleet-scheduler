# Mathematical formulation

> **Status:** placeholder. Finalised in Week 7 per [project plan](../vessel_routing_project_plan_v3.md) §8. This file locks in design decisions made in pre-start so the Week-7 write-up doesn't drift.

## Decision variables

| Variable | Type | Meaning |
|---|---|---|
| `x[v, c]` | binary | vessel `v` assigned to cargo `c` |
| `y[v, c, t]` | binary | vessel `v` starts loading cargo `c` at time `t` |
| `s[v, c]` | continuous ∈ [s_min, s_max] | sailing speed on laden leg |
| `b[v, c]` | continuous ≥ 0 | ballast time before cargo `c` |
| `d[v, c]` | continuous ≥ 0 | demurrage slack |
| `f[v, c]` | continuous | fuel cost on voyage (PWL of speed) |

## Objective

minimise Σ(freight_cost · time_on_hire) + Σ fuel_cost + ρ · Σ demurrage

where ρ is the demurrage penalty multiplier (scenario-parameterised).

## SOS2 linearisation of the fuel–speed curve

Bunker consumption follows approximately F(s) ≈ α·s³ + β (Kontovas & Psaraftis, 2013; Stopford). The cubic term makes the problem nonlinear. We linearise via **piecewise-linear approximation with SOS2 constraints on breakpoint weights** — the same structural trick used in [pytfa](https://github.com/EPFL-LCSB/pytfa) for thermodynamic Gibbs-free-energy terms.

Given N breakpoints `{(s_k, F_k)}` on the speed axis:

    s[v, c] = Σ_k λ_k[v, c] · s_k
    f[v, c] = Σ_k λ_k[v, c] · F_k
    Σ_k λ_k[v, c] = 1
    λ_k[v, c] ≥ 0
    {λ_k[v, c]}_k  is an SOS2 set  (at most two adjacent λ_k are nonzero)

The SOS2 constraint is what makes the convex combination equivalent to a piecewise-linear function rather than a hull.

### Two implementations, one model

Because the project runs on multiple solvers (SCIP, HiGHS, CBC, Gurobi) and HiGHS in particular does not support SOS constraints natively, the formulation supports **both paths**:

1. **Native SOS2** — used when `solver.native_sos2 is True` (SCIP, CBC, Gurobi). Pyomo emits `SOSConstraint(sos=2)` and the solver's specialised branching handles the rest.
2. **Manual adjacency encoding** — used with HiGHS or as a solver-agnostic baseline. Introduce binary indicators `z_k ∈ {0, 1}` with:

        Σ_k z_k = 1              (exactly one "left" breakpoint of the active segment)
        λ_0       ≤ z_0
        λ_k       ≤ z_{k-1} + z_k       for 1 ≤ k < N
        λ_N       ≤ z_{N-1}

   Equivalent feasible region; no specialised branching, so performance drops on instances with many breakpoints and many PWL-constrained pairs.

The two encodings are benchmarked in `docs/architecture.md` (Week 8).

## Why solver-agnostic from day one

Commercial trading firms run Gurobi or CPLEX, but a portfolio piece lives in a world where anyone must be able to clone and run. SCIP was Apache 2.0 licensed from v9 (2024), ships via `pyscipopt` with bundled binaries, and exposes native SOS2 — making it the natural primary backend for this project. Gurobi remains useful as a benchmark: the README reports both solve times so the difference is visible without making Gurobi load-bearing.

## The pytfa parallel

In [pytfa](https://github.com/EPFL-LCSB/pytfa) the same SOS2 structure linearises the Gibbs free-energy change ΔG°' = -RT ln K — specifically the log-ratio term ln([S]/[P]) inside thermodynamic feasibility constraints. Variables change meaning; the linearisation does not.

| Domain | Nonlinear term | PWL target | Constraint structure |
|---|---|---|---|
| Thermodynamic FBA (pytfa) | ln(concentration ratio) inside ΔG°' | metabolite activity | SOS2 weights on log-spaced breakpoints |
| Tanker scheduling (here) | s³ in fuel burn rate F(s) | fuel cost per voyage | SOS2 weights on speed breakpoints |

Same toolkit, same trick, different label on the axis.
