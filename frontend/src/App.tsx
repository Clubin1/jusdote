import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Components/Login/Login';
import Signup from './Components/Signup/Signup';
import ClientApplication from './Components/ClientApplication/ClientApplication';
import EditorApplication from './Components/EditorApplication/EditorApplication';
import Messaging from './Components/Messaging/Messaging';
import Dashboard from './Components/Dashboard/Dashboard';
import Folder from './Components/Folder/Folder';
import FolderItem from './Components/Folder/FolderItem';
import Jobs from './Components/JobApplying/Jobs';

function App() {
  return (
    <Router>
      <main className="main">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/client-application" element={<ClientApplication />} />
          <Route path="/editor-application" element={<EditorApplication />} />
          <Route path="/messaging" element={<Messaging />} />
          <Route path="/folder" element={<Folder />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/folder/:folderId" element={<FolderItem />} />
          <Route path="/jobs" element={<Jobs />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
