import { useEffect, useState } from "react";
import { fetchEvents } from "../api";

export default function LiveEvents() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      fetchEvents().then(res => setEvents(res.data));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="widget">
      <h3>🚨 Live Events</h3>
      <ul>
        {events.map((e, idx) => (
          <li key={idx}>
            <pre>{JSON.stringify(e.payload)}</pre>
          </li>
        ))}
      </ul>
    </div>
  );
}
