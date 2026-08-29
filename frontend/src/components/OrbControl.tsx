import type { CSSProperties } from "react";

type OrbState = "idle" | "listening" | "thinking" | "speaking" | "error";

type OrbControlProps = {
  disabled: boolean;
  onStart: () => void;
  onStop: () => void;
  state: OrbState;
};

// ====================================================================
// TODO: [MISSION 1] CUSTOMIZE YOUR ASSISTANT'S ORB LETTERMARK
// Add your assistant's codename letters to this array!
// Example: const letters = ["F", "R", "I", "D", "A", "Y"];
// ====================================================================
const letters: string[] = [];

export function OrbControl({ disabled, onStart, onStop, state }: OrbControlProps) {
  const label = state === "listening" ? "Release to send" : state === "thinking" ? "Processing request" : state === "speaking" ? "Jarvis is responding" : "Hold to talk with Jarvis";
  return (
    <button
      type="button"
      className={`orb-control state-${state}`}
      aria-label={label}
      disabled={disabled}
      onPointerDown={(event) => { event.currentTarget.setPointerCapture(event.pointerId); onStart(); }}
      onPointerUp={onStop}
      onPointerCancel={onStop}
    >
      <span className="orb-shell" aria-hidden="true" />
      <span className="orb-lettermark" aria-hidden="true">{letters.map((letter, index) => <span key={`${letter}-${index}`} style={{ "--letter-delay": `${index * .1}s` } as CSSProperties}>{letter}</span>)}</span>
      <span className="orb-status">{state === "listening" ? "LISTENING" : "HOLD TO TALK"}</span>
    </button>
  );
}
