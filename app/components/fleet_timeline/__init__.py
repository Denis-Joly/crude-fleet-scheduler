"""Python wrapper for the fleet_timeline React component.

Release mode is driven by the ``FLEET_TIMELINE_DEV`` env var:

* unset (production / Streamlit Cloud) → loads the bundled ``build/``
  output produced by ``npm run build``.
* ``FLEET_TIMELINE_DEV=1`` (local dev) → loads from the Vite dev server
  at ``http://localhost:3001`` for hot-reload.

Workflow: run ``npm run build`` in this directory before pushing any change
to the component so ``build/`` stays current in git.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import streamlit.components.v1 as components

_RELEASE = os.environ.get("FLEET_TIMELINE_DEV") != "1"

_COMPONENT_NAME = "fleet_timeline"

if _RELEASE:
    _build_dir = Path(__file__).parent / "build"
    _component_func = components.declare_component(_COMPONENT_NAME, path=str(_build_dir))
else:
    _component_func = components.declare_component(_COMPONENT_NAME, url="http://localhost:3001")


def fleet_timeline(
    vessels: list[dict[str, Any]] | None = None,
    horizon_days: int = 45,
    key: str | None = None,
) -> Any:
    """Render the fleet-timeline map.

    Parameters mirror what the solver's JSON output will supply once wired up.
    During pre-start this is a stub — it just echoes ``vessels`` back so we can
    confirm the Streamlit ↔ React bridge works.
    """
    return _component_func(
        vessels=vessels or [],
        horizonDays=horizon_days,
        key=key,
        default=None,
    )
