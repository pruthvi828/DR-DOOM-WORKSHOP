import type { CSSProperties } from "react";

type AmbientHudProps = { active: boolean; level: number };

const signalLines = Array.from({ length: 22 }, (_, index) => ({
  x: 28 + index * 26,
  height: 34 + ((index * 23) % 86),
  delay: `${(index % 6) * -0.12}s`,
}));

export function AmbientHud({ active, level }: AmbientHudProps) {
  return (
    <div className={`ambient-hud ${active ? "is-active" : ""}`} style={{ "--audio-level": level } as CSSProperties} aria-hidden="true">
      <svg className="signal-field" viewBox="0 0 620 190" preserveAspectRatio="none">
        {signalLines.map((line, index) => (
          <line
            className="signal-line"
            key={line.x}
            style={{ "--line-delay": line.delay } as CSSProperties}
            x1={line.x}
            x2={line.x}
            y1="176"
            y2={176 - line.height - (index % 3) * 8}
          />
        ))}
      </svg>
      <p className="hud-caption">AUDIO LINK / STANDBY</p>
    </div>
  );
}
