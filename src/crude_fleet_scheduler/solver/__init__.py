"""Solver selection for the scheduling MILPs.

The project is solver-agnostic by design. Primary backend is SCIP (native
SOS2, Apache 2.0, open source) via ``pyscipopt``. HiGHS is used via Pyomo
for fast LP/MIP on non-SOS models. Gurobi is an optional perf backend.

This module deliberately stays *thin* until Week 3 when model code lands.
It captures the solver-capability metadata and dispatches by name; the
concrete factories get wired up alongside the first real MILP.

Usage once wired:

    from crude_fleet_scheduler.solver import resolve
    cfg = resolve()                  # default SCIP
    cfg = resolve("highs")           # env override with CFS_SOLVER=highs
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

SolverName = Literal["scip", "highs", "gurobi", "cbc"]

DEFAULT: SolverName = "scip"

_ALL: tuple[SolverName, ...] = ("scip", "highs", "gurobi", "cbc")


@dataclass(frozen=True, slots=True)
class SolverConfig:
    """Metadata describing a supported MIP backend."""

    name: SolverName
    pyomo_key: str  # Pyomo SolverFactory key, for non-SCIP backends
    native_sos2: bool  # True → use pyo.SOSConstraint(sos=2); False → manual encoding
    open_source: bool
    notes: str


_REGISTRY: dict[SolverName, SolverConfig] = {
    "scip": SolverConfig(
        name="scip",
        pyomo_key="scip",  # pyscipopt used directly for SCIP, not via Pyomo
        native_sos2=True,
        open_source=True,
        notes="primary backend; native SOS2; wheels bundle SCIP binary",
    ),
    "highs": SolverConfig(
        name="highs",
        pyomo_key="appsi_highs",
        native_sos2=False,  # confirmed missing as of HiGHS v1.14, April 2026
        open_source=True,
        notes="fast LP/MIP; no SOS constraints — manual encoding required",
    ),
    "gurobi": SolverConfig(
        name="gurobi",
        pyomo_key="gurobi",
        native_sos2=True,
        open_source=False,
        notes="optional perf benchmark; requires commercial or academic license",
    ),
    "cbc": SolverConfig(
        name="cbc",
        pyomo_key="cbc",
        native_sos2=True,
        open_source=True,
        notes="universal fallback; older and slower than SCIP/HiGHS",
    ),
}


def resolve(name: SolverName | None = None) -> SolverConfig:
    """Return config for the chosen solver.

    Resolution order: explicit ``name`` → ``CFS_SOLVER`` env var → DEFAULT.
    """
    chosen = name or os.environ.get("CFS_SOLVER") or DEFAULT
    if chosen not in _REGISTRY:
        raise ValueError(f"unknown solver {chosen!r}; expected one of {list(_ALL)}")
    return _REGISTRY[chosen]  # type: ignore[index]


def supports_sos2(name: SolverName | None = None) -> bool:
    """True if the chosen backend exposes native SOS2 constraints."""
    return resolve(name).native_sos2


__all__ = ["DEFAULT", "SolverConfig", "SolverName", "resolve", "supports_sos2"]
