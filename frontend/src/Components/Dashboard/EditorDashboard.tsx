import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Application {
  _id: string;
  name: string;
  // Add other properties as needed
}

function EditorDashboard() {
  const [applications, setApplications] = useState<Application[]>([]);

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
          // Handle the case when the access token is missing
          return;
        }

        const response = await axios.get<Application[]>('http://localhost:5000/api/editor/applications', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (Array.isArray(response.data)) {
          setApplications(response.data);
        } else {
          console.error('Unexpected response format:', response.data);
        }
      } catch (error) {
        console.error('Error fetching applications:', error);
      }
    };

    fetchApplications();
  }, []);

  return (
    <div className="App">
      <h1>Editor Dashboard</h1>
      <h2>Applications</h2>
      {applications.length === 0 ? (
        <p>No applications found.</p>
      ) : (
        <ul>
          {applications.map((app) => (
            <li key={app._id}>{app.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default EditorDashboard;