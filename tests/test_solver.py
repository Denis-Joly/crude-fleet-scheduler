"""Solver dispatch tests.

Only checks the config registry and capability flags. Solver-execution tests
arrive in Week 3 when the first real MILP lands.
"""

from __future__ import annotations

import pytest

from crude_fleet_scheduler.solver import DEFAULT, resolve, supports_sos2


def test_default_is_scip() -> None:
    assert DEFAULT == "scip"
    assert resolve().name == "scip"


def test_env_var_overrides_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CFS_SOLVER", "highs")
    assert resolve().name == "highs"


def test_explicit_name_overrides_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CFS_SOLVER", "highs")
    assert resolve("gurobi").name == "gurobi"


def test_sos2_capability_matches_research_findings() -> None:
    # HiGHS confirmed missing SOS2 as of v1.14 (April 2026) —
    # https://github.com/ERGO-Code/HiGHS/issues/2148
    assert supports_sos2("scip") is True
    assert supports_sos2("gurobi") is True
    assert supports_sos2("highs") is False
    assert supports_sos2("cbc") is True  # CBC supports SOS, albeit older


def test_unknown_solver_raises() -> None:
    with pytest.raises(ValueError, match="unknown solver"):
        resolve("xpress")  # type: ignore[arg-type]
