import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Application {
  _id: string;
  name: string;
  address: string;
  interested_users: string[];
}

function Jobs() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [userId, setUserId] = useState('');

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const response = await axios.get<Application[]>('http://localhost:5000/api/client/query_applications');
        setApplications(response.data);
      } catch (error) {
        console.error('Error fetching applications:', error);
      }
    };
    fetchApplications();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.get<Application[]>('http://localhost:5000/api/client/query_applications', {
        params: {
          user_id: userId,
        },
      });
      setApplications(response.data);
    } catch (error) {
      console.error('Error fetching applications:', error);
    }
  };

  const handleInterest = async (applicationId: string) => {
    try {
      const token = localStorage.getItem('access_token');
      await axios.post(
        'http://localhost:5000/api/client/applications/interest',
        { applicationId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const response = await axios.get<Application[]>('http://localhost:5000/api/client/query_applications');
      setApplications(response.data);
    } catch (error) {
      console.error('Error expressing interest:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          User ID:
          <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} />
        </label>
        <button type="submit">Submit</button>
      </form>
      <h2>Applications:</h2>
      {applications.map((application) => (
        <div key={application._id}>
          <p>Name: {application.name}</p>
          <p>Address: {application.address}</p>
          <button onClick={() => handleInterest(application._id)}>Interested</button>
          <hr />
        </div>
      ))}
    </div>
  );
}

export default Jobs;