export type ComponentState = "ready" | "error" | "unknown" | "active";

type StatusItem = { label: string; state: ComponentState; detail?: string };

type SystemStatusProps = { items: StatusItem[] };

const stateLabel: Record<ComponentState, string> = {
  ready: "READY",
  active: "ACTIVE",
  error: "ERROR",
  unknown: "UNCHECKED",
};

export function SystemStatus({ items }: SystemStatusProps) {
  return (
    <aside className="system-status" aria-label="System status">
      <p className="status-title">SYSTEM STATUS</p>
      <div className="status-grid">
        {items.map((item) => (
          <div className="status-tile" key={item.label}>
            <span className={`status-light ${item.state}`} title={stateLabel[item.state]} />
            <span className="status-tile-label">{item.label}</span>
            <strong>{item.detail ?? stateLabel[item.state]}</strong>
          </div>
        ))}
      </div>
      <p className="status-key"><i className="status-light ready" /> ready <i className="status-light error" /> error</p>
    </aside>
  );
}
