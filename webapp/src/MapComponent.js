import React from 'react';
import { MapContainer, TileLayer, Circle, Rectangle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';


const MapComponent = () => {
    const circles = [
        { id: 1, position: [40.632696, -8.648598], radius: 5, color: "green" },
        { id: 2, position: [51.515, -0.1], radius: 200, color: "green" },
    ];

    const rectangles = [{
            id: 1,
            bounds: [
                [40.631902, -8.650508],
                [40.632696, -8.648598]
            ],
            color: "red"
        },
        {
            id: 2,
            bounds: [
                [40.631499, -8.651631],
                [40.6426918, -8.648598]
            ],
            color: "red"
        },
        // New rectangles added below
        // {
        //     id: 3,
        //     bounds: [
        //         [40.633, -8.649],
        //         [40.634, -8.647]
        //     ],
        //     color: "blue" // Change the color if needed
        // },
        // {
        //     id: 4,
        //     bounds: [
        //         [40.635, -8.646],
        //         [40.636, -8.644]
        //     ],
        //     color: "blue" // Change the color if needed
        // },
        // {
        //     id: 5,
        //     bounds: [
        //         [40.637, -8.643],
        //         [40.638, -8.641]
        //     ],
        //     color: "blue" // Change the color if needed
        // },
    ];

    const createSmallerBounds = (bounds, shrinkFactor = 0.0002) => {
        const [sw, ne] = bounds;
        const center = [(sw[0] + ne[0]) / 2, (sw[1] + ne[1]) / 2];
        return [
            [center[0] - shrinkFactor, center[1] - shrinkFactor],
            [center[0] + shrinkFactor, center[1] + shrinkFactor]
        ];
    };

    return ( <
        MapContainer center = {
            [40.632696, -8.648598]
        }
        zoom = { 70 }
        style = {
            { height: '100vh', width: '100%' }
        } >
        <
        TileLayer url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" / > {
            circles.map(circle => ( <
                Circle key = { circle.id }
                center = { circle.position }
                radius = { circle.radius }
                color = { circle.color }
                />
            ))
        } {
            rectangles.map(rectangle => ( <
                Rectangle key = { rectangle.id }
                bounds = { createSmallerBounds(rectangle.bounds) }
                color = { rectangle.color }
                />
            ))
        } <
        /MapContainer>
    );
};


export default MapComponent