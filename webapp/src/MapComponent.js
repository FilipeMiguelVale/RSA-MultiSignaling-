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

  // Static numbers positions
  const numberPositions = [
    { id: 'n1', position: [40.64246735129016, -8.6485201216305], number: '0' },
    { id: 'n1', position: [40.642399899557034, -8.648201329699718], number: '1' },
    { id: 'n1', position: [40.64244641800096, -8.647897864304072], number: '2' },
    { id: 'n1', position: [40.64264877285484, -8.647677162198146], number: '3' },
    { id: 'n1', position: [40.64280693484221, -8.646812745616604], number: '3' },
    { id: 'n1', position: [40.64268366156104, -8.646717720913703], number: '4' },
    { id: 'n1', position: [40.64273948345254, -8.646346818763465], number: '5' },
    { id: 'n1', position: [40.64295114103379, -8.646009634990524], number: '6' },
    { id: 'n1', position: [40.64326400557164, -8.646167127935588], number: '7' },
    { id: 'n1', position: [40.643261384867486, -8.646536688850805], number: '8' },
    { id: 'n1', position: [40.64316179803358, -8.64696151121129], number: '9' },
    { id: 'n1', position: [40.64307269389833, -8.647044403379189], number: '10' },
    { id: 'n1', position: [40.64289710598954, -8.64789404810016], number: '10' },
    { id: 'n1', position: [40.64298358963856, -8.64810818633413], number: '11' },
    { id: 'n1', position: [40.64284731231383, -8.648360316678158], number: '12' },
    { id: 'n1', position: [40.642703172532975, -8.648684977669097], number: '13' },
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
      html: <div style="background-color: rgba(255, 255, 255, 0.8); border-radius: 50%; border: 2px solid black; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; color: black; font-weight: bold;">${number}</div>,
      className: '',  // No additional classes needed
      iconSize: [15, 1],
      iconAnchor: [12, 12]  // Centers the icon
    });
  };

  return (
    <div className='container'>
      <MapContainer center={[40.64264002592938, -8.648293544440508]} zoom={17.5} style={{ height: "100%", width: "100%"}} scrollWheelZoom={false}>
        <TileLayer url="https://api.mapbox.com/styles/v1/jp-amaral/cl758vsmy000714o2rx0w0779/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoianAtYW1hcmFsIiwiYSI6ImNsNzU4c3g1MzExMHozbm1hdWlvbnRrbmoifQ.SpZQvOQyQCwhNZluPGPXQg" />
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