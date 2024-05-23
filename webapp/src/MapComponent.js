import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Import the car icon image
import carIconUrl from './icons/car.png';

// Define the Leaflet icon for the car
const carIcon = new L.Icon({
    iconUrl: carIconUrl,
    iconSize: [40, 40], // Size of the icon in pixels
    iconAnchor: [20, 20], // Point of the icon which will correspond to marker's location
    popupAnchor: [0, -20]
});

const MapComponent = () => {
    const [carPositions, setCarPositions] = useState({});
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("/data");
                const data = await response.json();
                console.log(data)
                const positions = {};
                data.forEach((item) => {
                    const carId = Object.keys(item)[0];
                    positions[carId] = {
                        lat: item[carId].latitude,
                        lng: item[carId].longitude,
                        speed: item[carId].speed
                    };
                });
                setCarPositions(positions);
            } catch (error) {
                console.error('Failed to fetch data:', error);
            }
        };

        const intervalId = setInterval(fetchData, 5000); // Fetch data every 5 seconds

        return () => clearInterval(intervalId); // Cleanup interval on component unmount
    }, []);

    return (
        <MapContainer center={[40.641754, -8.652605]} zoom={73} style={{ height: '100vh', width: '100%' }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {Object.entries(carPositions).map(([id, position]) => (
                <Marker key={id} position={[position.lat, position.lng]} icon={carIcon} />
            ))}
        </MapContainer>
    );
};

export default MapComponent;
