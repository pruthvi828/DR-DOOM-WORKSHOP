type AssistantState = "idle" | "listening" | "thinking" | "speaking" | "error";

type ActivityMonitorProps = { state: AssistantState };

const activityDetails: Record<AssistantState, { label: string; entries: string[] }> = {
  idle: { label: "STANDING BY", entries: ["VOICE CHANNEL ARMED", "TEXT CHANNEL READY", "AWAITING REQUEST"] },
  listening: { label: "LISTENING", entries: ["MICROPHONE CAPTURE ACTIVE", "AUDIO LEVEL TRACKING", "RELEASE TO SEND"] },
  thinking: { label: "PROCESSING", entries: ["REQUEST SENT", "JARVIS IS THINKING", "KEEPING CONTEXT SHORT"] },
  speaking: { label: "RESPONDING", entries: ["VOICE OUTPUT ACTIVE", "TEXT RESPONSE AVAILABLE", "AUDIO LINK ACTIVE"] },
  error: { label: "ATTENTION", entries: ["LAST REQUEST NEEDS REVIEW", "TEXT CHANNEL REMAINS READY", "TRY AGAIN WHEN READY"] },
};

export function ActivityMonitor({ state }: ActivityMonitorProps) {
  const activity = activityDetails[state];
  return (
    <aside className={`activity-monitor state-${state}`} aria-label="Jarvis activity monitor">
      <div className="monitor-heading"><span>ACTIVITY MONITOR</span><i aria-hidden="true" /></div>
      <strong>{activity.label}</strong>
      <ol>
        {activity.entries.map((entry) => <li key={entry}>{entry}</li>)}
      </ol>
      <p>RIGHT-CLICK THIS PANEL TO MOVE</p>
    </aside>
  );
}
