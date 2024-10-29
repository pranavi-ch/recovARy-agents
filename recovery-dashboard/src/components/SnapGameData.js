// src/components/SnapGameData.js
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

function SnapGameData() {
  const [gameData, setGameData] = useState([]);

  // Fetch the Snap AR game data from the backend
  useEffect(() => {
    axios.get('/api/patients/1/game-data/')  // Change the endpoint to your backend URL
      .then((response) => {
        const { speed_data, reaction_time_data } = response.data;
        // Combine speed and reaction time data for chart
        const combinedData = speed_data.map((speed, index) => ({
          name: `Time ${index + 1}`,
          speed,
          reactionTime: reaction_time_data[index],
        }));
        setGameData(combinedData);
      })
      .catch((error) => {
        console.error('Error fetching game data:', error);
      });
  }, []);

  return (
    <div>
      <h2>Snap AR Game Data</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={gameData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="speed" stroke="#8884d8" activeDot={{ r: 8 }} />
          <Line type="monotone" dataKey="reactionTime" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default SnapGameData;
