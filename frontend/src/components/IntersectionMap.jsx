import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function IntersectionMap() {
  const emergencyRoute = [
    [13.0827, 80.2707], // RG Hospital
    [13.0821, 80.2750]  // Chennai Central
  ];

  return (
    <div className="map">
      <MapContainer center={[13.0827, 80.271]} zoom={15} style={{ height: "400px" }}>
        <TileLayer
          attribution="Mach-10 Smart Mobility"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <Polyline positions={emergencyRoute} color="red" />

        <Marker position={[13.0827, 80.2707]}>
          <Popup>🏥 Rajiv Gandhi Govt. General Hospital</Popup>
        </Marker>

        <Marker position={[13.0821, 80.2750]}>
          <Popup>🚉 Chennai Central</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}
