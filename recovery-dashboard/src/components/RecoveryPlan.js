// src/components/RecoveryPlan.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function RecoveryPlan() {
  const [recoveryPlan, setRecoveryPlan] = useState('');

  // Fetch the combined recovery plan from the wrapper agent
  useEffect(() => {
    axios.get('/api/patients/1/report/')  // Change the endpoint to your backend URL
      .then((response) => {
        setRecoveryPlan(response.data.report);
      })
      .catch((error) => {
        console.error('Error fetching recovery plan:', error);
      });
  }, []);

  return (
    <div>
      <h2>Combined Recovery Plan</h2>
      <p>{recoveryPlan}</p>
    </div>
  );
}

export default RecoveryPlan;
