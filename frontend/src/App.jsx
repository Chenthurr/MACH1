import LiveEvents from "./components/LiveEvents";
import IntersectionMap from "./components/IntersectionMap";
import StatsPanel from "./components/StatsPanel";
import "./styles/main.css";

export default function App() {
  return (
    <div className="layout">
      <h1>🚦 MACH-10 Smart Traffic Dashboard</h1>
      <StatsPanel />
      <IntersectionMap />
      <LiveEvents />
    </div>
  );
}
