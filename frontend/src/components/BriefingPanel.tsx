import { useEffect, useMemo, useState } from "react";

type Weather = { temperature: number; code: number };
type LocationState = "idle" | "loading" | "ready" | "error";

const weatherLabel = (code: number) => {
  if (code === 0) return "Clear";
  if ([1, 2, 3].includes(code)) return "Partly cloudy";
  if ([45, 48].includes(code)) return "Fog";
  if ([51, 53, 55, 56, 57].includes(code)) return "Drizzle";
  if ([61, 63, 65, 66, 67, 80, 81, 82].includes(code)) return "Rain";
  if ([71, 73, 75, 77, 85, 86].includes(code)) return "Snow";
  if ([95, 96, 99].includes(code)) return "Storm";
  return "Weather available";
};

function greetingFor(date: Date) {
  const hour = date.getHours();
  if (hour < 12) return "Good morning, sir.";
  if (hour < 18) return "Good afternoon, sir.";
  return "Good evening, sir.";
}

export function BriefingPanel() {
  const [now, setNow] = useState(() => new Date());
  const [locationState, setLocationState] = useState<LocationState>("idle");
  const [locationLabel, setLocationLabel] = useState("Location not shared");
  const [weather, setWeather] = useState<Weather | null>(null);
  const [weatherError, setWeatherError] = useState("");

  useEffect(() => {
    const timer = window.setInterval(() => setNow(new Date()), 30_000);
    return () => window.clearInterval(timer);
  }, []);

  const clock = useMemo(() => new Intl.DateTimeFormat("en-IN", { hour: "2-digit", minute: "2-digit", hour12: false }).format(now), [now]);
  const date = useMemo(() => new Intl.DateTimeFormat("en-IN", { weekday: "short", day: "2-digit", month: "short" }).format(now).toUpperCase(), [now]);

  function shareLocation() {
    if (!navigator.geolocation) {
      setLocationState("error");
      setLocationLabel("Location unavailable");
      return;
    }
    setLocationState("loading");
    setWeatherError("");
    navigator.geolocation.getCurrentPosition(
      async ({ coords }) => {
        const latitude = coords.latitude.toFixed(3);
        const longitude = coords.longitude.toFixed(3);
        setLocationLabel(`${latitude}°, ${longitude}°`);
        try {
          const response = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,weather_code&timezone=auto`);
          if (!response.ok) throw new Error("Weather service unavailable");
          const body = await response.json() as { current?: { temperature_2m?: number; weather_code?: number } };
          if (typeof body.current?.temperature_2m !== "number" || typeof body.current.weather_code !== "number") throw new Error("Weather data unavailable");
          setWeather({ temperature: body.current.temperature_2m, code: body.current.weather_code });
          setLocationState("ready");
        } catch {
          setLocationState("ready");
          setWeatherError("Weather unavailable");
        }
      },
      () => {
        setLocationState("error");
        setLocationLabel("Location permission denied");
      },
      { enableHighAccuracy: false, timeout: 10_000, maximumAge: 600_000 },
    );
  }

  return <aside className="briefing-panel" aria-label="Local system briefing">
    <p className="briefing-kicker">LOCAL SYSTEM BRIEFING</p>
    <h2>{greetingFor(now)}</h2>
    <div className="briefing-readings">
      <div><span>LOCAL TIME</span><strong>{clock}</strong><small>{date}</small></div>
      <div><span>WEATHER</span><strong>{weather ? `${Math.round(weather.temperature)}°C` : "—"}</strong><small>{weather ? weatherLabel(weather.code) : weatherError || "Share location to check"}</small></div>
    </div>
    <div className="briefing-location"><span>LOCATION</span><p>{locationLabel}</p><button type="button" onClick={shareLocation} disabled={locationState === "loading"}>{locationState === "loading" ? "Locating…" : locationState === "ready" ? "Refresh location" : "Share location"}</button></div>
  </aside>;
}
