import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import axios from 'axios';
import ClientDashboard from './ClientDashboard';
import EditorDashboard from './EditorDashboard';

function Dashboard() {
  const [userRole, setUserRole] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
          setIsLoading(false);
          return;
        }

        const response = await axios.get('http://localhost:5000/api/user-info', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        setUserRole(response.data.role);
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Error fetching user info:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUserInfo();
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="App">
      {userRole === 'client' ? (
        <ClientDashboard />
      ) : userRole === 'editor' ? (
        <EditorDashboard />
      ) : null}
    </div>
  );
}

export default Dashboard;