import { FormEvent, useState } from "react";
import { sendChatMessage } from "./api/chat";

type Message = { author: "user" | "jarvis"; text: string };

export function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [status, setStatus] = useState<"idle" | "thinking">("idle");
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const text = input.trim();
    if (!text || status === "thinking") return;
    setInput("");
    setError("");
    setMessages((current) => [...current, { author: "user", text }]);
    setStatus("thinking");

    try {
      const result = await sendChatMessage(crypto.randomUUID(), text);
      setMessages((current) => [...current, { author: "jarvis", text: result.reply }]);
      setStatus("idle");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Error receiving reply.");
      setStatus("idle");
    }
  }

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", padding: "20px", fontFamily: "system-ui, sans-serif" }}>
      <h1>Basic AI Chatbot (Mission 0)</h1>
      <p style={{ color: "#666" }}>Type a message below to test your connection to the FastAPI + Groq backend.</p>
      
      <div style={{ border: "1px solid #ccc", borderRadius: "8px", padding: "16px", minHeight: "250px", marginBottom: "16px", background: "#f9f9f9" }}>
        {messages.length === 0 && <p style={{ color: "#999" }}>No messages yet. Send a prompt to begin!</p>}
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: "12px", textAlign: msg.author === "user" ? "right" : "left" }}>
            <span style={{ display: "inline-block", padding: "8px 12px", borderRadius: "16px", background: msg.author === "user" ? "#0070f3" : "#e5e5ea", color: msg.author === "user" ? "#fff" : "#000" }}>
              <strong>{msg.author === "user" ? "You" : "AI"}:</strong> {msg.text}
            </span>
          </div>
        ))}
        {status === "thinking" && <p style={{ color: "#0070f3" }}>AI is thinking...</p>}
      </div>

      <form onSubmit={handleSubmit} style={{ display: "flex", gap: "8px" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          style={{ flex: 1, padding: "10px", borderRadius: "6px", border: "1px solid #ccc", fontSize: "16px" }}
          disabled={status === "thinking"}
        />
        <button type="submit" disabled={!input.trim() || status === "thinking"} style={{ padding: "10px 20px", borderRadius: "6px", border: "none", background: "#0070f3", color: "#fff", fontSize: "16px", cursor: "pointer" }}>
          Send
        </button>
      </form>
      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
    </div>
  );
}
