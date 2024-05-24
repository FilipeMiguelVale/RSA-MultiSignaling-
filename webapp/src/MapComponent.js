import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapComponent.css';
import L from 'leaflet';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Toggle from 'react-toggle';
import "react-toggle/style.css";

// const CustomToast = ({ content, description }) => (
//   <div>
//     <div>{content}</div>
//     <h5>{description}</h5>
//   </div>
// );

function MapComponent() {
  const [obuData, setObuData] = useState([]);
  const [rsuData, setRsuData] = useState([]);
  // const [showHighwayInfo, setShowHighwayInfo] = useState(true);

  useEffect(() => {
    const fetchAndUpdateData = async () => {
      try {
        const response = await fetch('/data');
        const data = await response.json();
        const obuEntries = [];
        const rsuEntries = [];

        Object.keys(data).forEach(key => {
          if (key.startsWith('OBU')) { // Assuming OBU data keys start with 'OBU'
            obuEntries.push({
              id: key,
              ...data[key]
            });
          } else { // Assuming RSU data keys do not start with 'OBU'
            rsuEntries.push({
              id: key,
              ...data[key]
            });
          }
        });

        setObuData(obuEntries);
        setRsuData(rsuEntries);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    const interval = setInterval(fetchAndUpdateData, 500);
    return () => clearInterval(interval);
  }, []);

  const carIcon = new L.Icon({
    iconUrl: require('./icons/car.png'),
    iconSize: new L.Point(50, 50),
    className: 'car-icon'
  });

  return (
    <div className='container'>
      {/* <Toggle defaultChecked={showHighwayInfo} onChange={() => setShowHighwayInfo(!showHighwayInfo)} /> */}
      <MapContainer center={[40.641754, -8.652605]} zoom={17.5} style={{ height: "100%", width: "100%"}} scrollWheelZoom={false}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {obuData.map((obu, index) => (
          <Marker key={index} position={[obu.latitude, obu.longitude]} icon={carIcon}>
            <Popup>
              Speed: {obu.speed} km/h
              ID: {obu.id}
            </Popup>
          </Marker>
        ))}
        {rsuData.map((rsu, index) => (
          <Marker key={index} position={[rsu.latitude, rsu.longitude]} icon={carIcon}>
            <Popup>
              Speed: {rsu.speed} km/h
              ID: {rsu.id}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      <ToastContainer newestOnTop />
    </div>
  );
}

export default MapComponent;
