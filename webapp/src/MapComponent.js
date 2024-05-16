import React from 'react';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Import the car icon image, make sure the path is correct based on your project structure
import carIconUrl from './icons/car.png';
import trafficLightIconUrl from './icons/traffic-light.png';  // Adjust the path as necessary


// Create the custom Leaflet icon
const carIcon = new L.Icon({
    iconUrl: carIconUrl,
    iconSize: [40, 40], // Size of the icon in pixels
    iconAnchor: [20, 20], // Point of the icon which will correspond to marker's location
    popupAnchor: [0, -20] // Point from which the popup should open relative to the iconAnchor
});

const trafficLightIcon = new L.Icon({
    iconUrl: trafficLightIconUrl,
    iconSize: [30, 30], // Size of the icon in pixels, adjust as needed
    iconAnchor: [15, 30], // Point of the icon which will correspond to marker's location
    popupAnchor: [0, -30] // Point from which the popup should open relative to the iconAnchor
});

const MapComponent = () => {
    const markers = [
        { id: 1, position: [40.641754, -8.652605], icon: carIcon },
        { id: 2, position: [40.642678, -8.648147], icon: trafficLightIcon },  // Example position
    ];

    return (
        <MapContainer center={[40.642678, -8.648147]} zoom={30} style={{ height: '100vh', width: '100%' }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {markers.map(marker => (
                <Marker
                    key={marker.id}
                    position={marker.position}
                    icon={marker.icon}
                />
            ))}
        </MapContainer>
    );
};

export default MapComponent;
