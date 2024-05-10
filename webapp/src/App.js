import React from 'react';
import './App.css';
import MapComponent from './MapComponent'; // Import the MapComponent

function App() {
    return ( <
        div className = "App" >
        <
        header className = "App-header" >
        Controlo Inteligente de trânsito com semáforos <
        /header> <
        MapComponent / > { /* Include the MapComponent */ } <
        /div>
    );
}

export default App;