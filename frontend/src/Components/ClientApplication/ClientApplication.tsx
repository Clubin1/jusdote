import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import axios from 'axios';

function ClientApplication() {
  const [userRole, setUserRole] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [name, setName] = useState('');
  const [address, setAddress] = useState('');
  const [userId, setUserId] = useState('');

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
        setUserId(response.data.userId);
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

  if (userRole === 'editor') {
    return <Navigate to="/editor-application" replace />;
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        return;
      }

      const response = await axios.post(
        'http://localhost:5000/api/client/applications',
        {
          name,
          address,
          userId,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      console.log('Application submitted:', response.data);
      setName('');
      setAddress('');
    } catch (error) {
      console.error('Error submitting application:', error);
    }
  };

  return (
    <div className="App">
      <h1>Client Application</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="address">Address:</label>
          <input
            type="text"
            id="address"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default ClientApplication;