import { useEffect } from "react";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";
// streamlit-component-lib@2.0.0 strips the generic from ComponentProps in its
// index.d.ts re-export; import from the inner module to keep the type arg.
import type { ComponentProps } from "streamlit-component-lib/dist/StreamlitReact";

interface Vessel {
  id: string;
  name: string;
}

interface Args {
  vessels: Vessel[];
  horizonDays: number;
}

function FleetTimelineInner({ args }: ComponentProps<Args>): JSX.Element {
  const { vessels, horizonDays } = args;

  useEffect(() => {
    Streamlit.setFrameHeight();
  });

  return (
    <div
      style={{
        fontFamily: "system-ui, -apple-system, sans-serif",
        padding: "16px",
        color: "#e5e7eb",
        background: "#0f172a",
        borderRadius: "8px",
      }}
    >
      <h2 style={{ margin: 0, fontSize: "18px" }}>fleet_timeline — PoC</h2>
      <p style={{ opacity: 0.8, marginTop: "8px" }}>
        React ↔ Streamlit bridge is alive. Horizon: {horizonDays} days.
      </p>
      <p style={{ opacity: 0.6, fontSize: "13px" }}>
        Received {vessels.length} vessel{vessels.length === 1 ? "" : "s"} from
        Streamlit.
      </p>
    </div>
  );
}

// Fallback render when loaded outside Streamlit (raw Vite dev server preview)
function StandalonePreview(): JSX.Element {
  const inStreamlit = window.parent !== window;
  if (inStreamlit) return <></>;
  return (
    <div
      style={{
        fontFamily: "system-ui, -apple-system, sans-serif",
        padding: "16px",
        color: "#e5e7eb",
        background: "#0f172a",
        minHeight: "100vh",
      }}
    >
      <h2 style={{ margin: 0 }}>fleet_timeline</h2>
      <p style={{ opacity: 0.7 }}>
        Standalone Vite preview. Mount inside Streamlit via
        <code style={{ marginLeft: "4px" }}>fleet_timeline(vessels=[])</code>.
      </p>
    </div>
  );
}

const Connected = withStreamlitConnection(FleetTimelineInner);

export default function FleetTimeline(): JSX.Element {
  const inStreamlit = window.parent !== window;
  return inStreamlit ? <Connected /> : <StandalonePreview />;
}
