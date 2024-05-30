import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapComponent.css';
import L from 'leaflet';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function MapComponent() {
  const [carData, setCarData] = useState([]);

  // Static traffic light positions
  const trafficLights = [
    { id: 'tl1', latitude: 40.642808, longitude: -8.648206 }, 
    { id: 'tl2', latitude: 40.642643, longitude: -8.648292 },
    { id: 'tl3', latitude: 40.642554, longitude: -8.648119 },
    { id: 'tl4', latitude: 40.642714, longitude: -8.647976 },
    { id: 'tl5', latitude: 40.642955, longitude: -8.646786 },
    { id: 'tl6', latitude: 40.642865, longitude: -8.646602 },
    { id: 'tl7', latitude: 40.643022, longitude: -8.646451 },
    { id: 'tl8', latitude: 40.643103, longitude: -8.646651 }
  ];

  const numberPositions = [
    { id: 'n1', position: [40.642560, -8.648328], number: '0' },
    { id: 'n1', position: [40.642529, -8.648125], number: '1' },
    { id: 'n1', position: [40.642548, -8.648060], number: '2' },
    { id: 'n1', position: [40.642619, -8.647964], number: '3' },
    { id: 'n1', position: [40.642865, -8.646714], number: '3' },
    { id: 'n1', position: [40.642829, -8.646633], number: '4' },
    { id: 'n1', position: [40.642867, -8.646505], number: '5' },
    { id: 'n1', position: [40.642914, -8.646424], number: '6' },
    { id: 'n1', position: [40.643128, -8.646467], number: '7' },
    { id: 'n1', position: [40.643134, -8.646628], number: '8' },
    { id: 'n1', position: [40.643118, -8.646700], number: '9' },
    { id: 'n1', position: [40.643063, -8.646783], number: '10' },
    { id: 'n1', position: [40.642812, -8.647993], number: '10' },
    { id: 'n1', position: [40.642843, -8.648168], number: '11' },
    { id: 'n1', position: [40.642818, -8.648237], number: '12' },
    { id: 'n1', position: [40.642713, -8.648449], number: '13' },
    //{ id: 'n2', latitude: 40.642850, longitude: -8.648600, number: '2' },
    // Additional numbers...
  ];

  useEffect(() => {
    const fetchAndUpdateData = async () => {
      try {
        const response = await fetch('/data');
        const data = await response.json();
        const carEntries = Object.keys(data).map(key => ({
          id: key,
          ...data[key]
        }));
        setCarData(carEntries);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    const interval = setInterval(fetchAndUpdateData, 500);
    return () => clearInterval(interval);
  }, []);

  const carIcon = new L.Icon({
    iconUrl: require('./icons/car.png'),
    iconSize: new L.Point(20, 20),
    className: 'car-icon'
  });

  const trafficLightIcon = new L.Icon({
    iconUrl: require('./icons/traffic-light.png'),
    iconSize: new L.Point(20, 20),
    className: 'traffic-light-icon'
  });

  const createNumberIcon = (number) => {
    return new L.divIcon({
      html: `<div style="background-color: rgba(255, 255, 255, 0.8); border-radius: 50%; border: 2px solid black; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; color: black; font-weight: bold;">${number}</div>`,
      className: '',  // No additional classes needed
      iconSize: [8, 1],
      iconAnchor: [4, 4]  // Centers the icon
    });
  };

  return (
    <div className='container'>
      <MapContainer center={[40.64264002592938, -8.648293544440508]} zoom={70} style={{ height: "100%", width: "100%"}} scrollWheelZoom={true}>
        <TileLayer url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png" />
        {carData.map(car => (
          <Marker key={car.id} position={[car.latitude, car.longitude]} icon={carIcon}>
            <Popup>
              Speed: {car.speed} km/h
              ID: {car.id}
            </Popup>
          </Marker>
        ))}
        {trafficLights.map(light => (
          <Marker key={light.id} position={[light.latitude, light.longitude]} icon={trafficLightIcon}>
            <Popup>
              Traffic Light ID: {light.id}
            </Popup>
          </Marker>
        ))}
        {numberPositions.map(pos => (
         <Marker key={pos.id} position={pos.position} icon={createNumberIcon(pos.number)}>
            <Popup>
              Number: {pos.number}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      <ToastContainer newestOnTop />
    </div>
  );
}

export default MapComponent;