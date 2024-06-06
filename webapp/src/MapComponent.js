import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapComponent.css';
import L from 'leaflet';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Toggle from 'react-toggle'
import "react-toggle/style.css" // for ES6 modules

function MapComponent() {
  const [carData, setCarData] = useState([]);
  const [trafficLightData, setTrafficLightData] = useState([]);
  const [showAmbulance, setShowAmbulance] = useState(false); // Initialized to false
  const [ambulancePosition, setAmbulancePosition] = useState([40.641939, -8.651645]);


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
    { id: 'n1', position: [40.642558, -8.648344], number: '0' },
    { id: 'n2', position: [40.642502, -8.648184], number: '1' },
    { id: 'n3', position: [40.642536, -8.648020], number: '2' },
    { id: 'n4', position: [40.642671, -8.647877], number: '3' },
    { id: 'n5', position: [40.642835, -8.646730], number: '3' },
    { id: 'n6', position: [40.642810, -8.646621], number: '4' },
    { id: 'n7', position: [40.642833, -8.646517], number: '5' },
    { id: 'n8', position: [40.642938, -8.646439], number: '6' },
    { id: 'n9', position: [40.643159, -8.646472], number: '7' },
    { id: 'n10', position: [40.643280, -8.646697], number: '8' },
    { id: 'n11', position: [40.643301, -8.646769], number: '9' },
    { id: 'n12', position: [40.643076, -8.646816], number: '10' },
    { id: 'n13', position: [40.642846, -8.648004], number: '10' },
    { id: 'n14', position: [40.642960, -8.648177], number: '11' },
    { id: 'n15', position: [40.642927, -8.648340], number: '12' },
    { id: 'n16', position: [40.642773, -8.648412], number: '13' },
    //{ id: 'n2', latitude: 40.642850, longitude: -8.648600, number: '2' },
    // Additional numbers...
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/data');
        const data = await response.json();
        
        const carEntries = Object.keys(data).map(key => ({

          id: key*10,
          ...data[key]
        }));
        console.log(carEntries)
        setCarData(carEntries);

      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData(); // Fetch on mount
    const interval = setInterval(fetchData, 500);
    return () => clearInterval(interval);
  }, []);

useEffect(() => {
  const fetchData = async () => {
    try{
        const trafficResponse = await fetch('/dataRSU');
        const rsuData = await trafficResponse.json();
        const updatedTrafficLights = trafficLights.map((light, index) => {
          const state = rsuData[index]?.state || 3; // Default to '3' (red) if no state is found
          return {
            ...light,
            state
          };
        });
    setTrafficLightData(updatedTrafficLights);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
  };

        fetchData(); // Fetch on mount
        const interval = setInterval(fetchData, 500);
        return () => clearInterval(interval);
  
    }, []);



  const carIcon = new L.Icon({
    iconUrl: require('./icons/car.png'),
    iconSize: new L.Point(30, 30),
    className: 'car-icon'
  });

  const CarIcons = {
    20: new L.Icon({
      iconUrl: require('./icons/green.png'),
      iconSize: new L.Point(30, 30),
      className: 'traffic-light-icon'
    }),
    30: new L.Icon({
      iconUrl: require('./icons/red.png'),
      iconSize: new L.Point(30, 30),
      className: 'traffic-light-icon'
    }),
    40: new L.Icon({
      iconUrl: require('./icons/yellow.png'),
      iconSize: new L.Point(30, 30),
      className: 'traffic-light-icon'
    }),
    50: new L.Icon({
      iconUrl: require('./icons/car.png'),
      iconSize: new L.Point(30, 30),
      className: 'traffic-light-icon'
    }),
    60: new L.Icon({
      iconUrl: require('./icons/green.png'),
      iconSize: new L.Point(30, 30),
      className: 'traffic-light-icon'
    }),
    70: new L.Icon({
      iconUrl: require('./icons/green.png'),
      iconSize: new L.Point(30, 30),
      className: 'traffic-light-icon'
    })

  };


  const ambulanceIcon = new L.Icon({
    iconUrl: require('./icons/ambulance.png'),
    iconSize: new L.Point(30, 30),
    className: 'car-icon'
  });

  // Define icons for each state of t
// traffic light
  const trafficLightIcons = {
    3: new L.Icon({
      iconUrl: require('./icons/3.png'),
      iconSize: new L.Point(30, 30),
      className: 'traffic-light-icon'
    }),
    6: new L.Icon({
      iconUrl: require('./icons/2.png'),
      iconSize: new L.Point(30, 30),
      className: 'traffic-light-icon'
    }),
    4: new L.Icon({
      iconUrl: require('./icons/1.png'),
      iconSize: new L.Point(30, 30),
      className: 'traffic-light-icon'
    }),
    4: new L.Icon({
      iconUrl: require('./icons/1.png'),
      iconSize: new L.Point(30, 30),
      className: 'traffic-light-icon'
    })

  };

  const getTrafficLightIcon = (state) => {
    //console.log(`Selecting icon for state: ${state}`); // Debugging statement
    return trafficLightIcons[state] || trafficLightIcons[2]; // Default to red if undefined
  };


  //Function to change the car icon according to the id of the car
  const getCarIcon = (id) => {
    //debugging statement
    console.log(`Selecting icon for id: ${id}`);
    return CarIcons[id] || carIcon; // Default to red if undefine
  };


  const createNumberIcon = (number) => {
    return new L.divIcon({
      html: `<div style="background-color: rgba(255, 255, 255, 0.8); border-radius: 30%; border: 2px solid black; width: 12px; height: 12px; display: flex; align-items: center; justify-content: center; color: black; font-weight: bold;">${number}</div>`,
      className: '',  // No additional classes needed
      iconSize: [8, 1],
      iconAnchor: [4, 4]  // Centers the icon
    });
  };

  const toggleAmbulance = () => {
    setShowAmbulance(!showAmbulance);
  };

  return (
    <div className='container'>
      {/*<label className="toggle">*/}
      {/* <Toggle*/}
      {/*      checked={showAmbulance} // Ensure controlled component*/}
      {/*      onChange={toggleAmbulance} />*/}
      {/*    <span style={{marginLeft: '10px'}}>Emergency vehicle</span>*/}
      {/*</label>*/}
      <MapContainer center={[40.64264002592938, -8.648293544440508]} zoom={20} style={{ height: "100%", width: "100%"}} scrollWheelZoom={true}>
      <TileLayer url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png" maxZoom={19}/>

        {carData.map(car => (
          <Marker key={car.id} position={[car.latitude, car.longitude]} icon={getCarIcon(car.id)}>
            <Popup>
              Speed: {car.speed} km/h
              ID: {car.id}
            </Popup>
          </Marker>
        ))}
       {trafficLightData.map(light => (
          <Marker key={light.id} position={[light.latitude, light.longitude]} icon={getTrafficLightIcon(light.state)}>
            <Popup>
              Traffic Light ID: {light.id}
              State: {light.state}
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
        {showAmbulance && (
          <Marker position={ambulancePosition} icon={ambulanceIcon}>
            <Popup>Ambulance is here</Popup>
          </Marker>
        )}
      </MapContainer>
      <ToastContainer newestOnTop />
    </div>
  );
}

export default MapComponent;