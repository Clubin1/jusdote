import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FolderItem from './FolderItem';
import { Link } from 'react-router-dom';

interface Folder {
  _id: string;
  name: string;
  owner: string;
  files: string[];
  permissions: Permission[];
}

interface Permission {
  user_id: string;
  role: string;
}

function Folder() {
  const [folders, setFolders] = useState<Folder[]>([]);
  const [folderName, setFolderName] = useState('');
  const [selectedFolder, setSelectedFolder] = useState<Folder | null>(null);
  const [permissionsInput, setPermissionsInput] = useState<{
    [key: string]: { userToAdd: string; userRole: string };
  }>({});

  useEffect(() => {
    fetchFolders();
  }, []);

  const fetchFolders = async () => {
    try {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        return;
      }
      const response = await axios.get<Folder[]>('http://localhost:5000/api/folders', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setFolders(response.data);
    } catch (error) {
      console.error('Error fetching folders:', error);
    }
  };

  const createFolder = async () => {
    try {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        return;
      }

      const response = await axios.post(
        'http://localhost:5000/api/folders',
        { name: folderName },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      console.log('Folder created:', response.data);
      setFolderName('');
      fetchFolders();
    } catch (error) {
      console.error('Error creating folder:', error);
    }
  };

  const deleteFolder = async (folderId: string) => {
    try {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        return;
      }

      await axios.delete(`http://localhost:5000/api/folders/${folderId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      console.log('Folder deleted');
      fetchFolders();
    } catch (error) {
      console.error('Error deleting folder:', error);
    }
  };

  const addPermission = async (folderId: string) => {
    try {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        return;
      }

      const { userToAdd, userRole } = permissionsInput[folderId] || { userToAdd: '', userRole: '' };

      const response = await axios.post(
        `http://localhost:5000/api/folders/${folderId}/add_permission`,
        { user_id: userToAdd, role: userRole, folder_id: folderId},
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      console.log('Permission added:', response.data);
      setPermissionsInput((prev) => ({
        ...prev,
        [folderId]: { userToAdd: '', userRole: '' },
      }));
      fetchFolders();
    } catch (error) {
      console.error('Error adding permission:', error);
    }
  };

  const handleFolderClick = (folder: Folder) => {
    setSelectedFolder(folder);
  };

  const handleInputChange = (folderId: string, field: 'userToAdd' | 'userRole', value: string) => {
    setPermissionsInput((prev) => ({
      ...prev,
      [folderId]: {
        ...prev[folderId],
        [field]: value,
      },
    }));
  };

  return (
    <div>
      <h1>Folders</h1>
      <div>
        <input
          type="text"
          placeholder="Folder Name"
          value={folderName}
          onChange={(e) => setFolderName(e.target.value)}
        />
        <button onClick={createFolder}>Create Folder</button>
      </div>
      Owned
      <ul>
        {folders.map((folder) => (
          <li key={folder._id}>
            <Link to={`/folder/${folder._id}`}>{folder.name}</Link>
            <button onClick={() => deleteFolder(folder._id)}>Delete</button>
            <div>
              <input
                type="text"
                placeholder="User ID"
                value={permissionsInput[folder._id]?.userToAdd || ''}
                onChange={(e) => handleInputChange(folder._id, 'userToAdd', e.target.value)}
              />
              <input
                type="text"
                placeholder="Role"
                value={permissionsInput[folder._id]?.userRole || ''}
                onChange={(e) => handleInputChange(folder._id, 'userRole', e.target.value)}
              />
              <button onClick={() => addPermission(folder._id)}>Add Permission</button>
            </div>
          </li>
        ))}
      </ul>
      Shared with you
      {selectedFolder && <FolderItem />}
    </div>
  );
}

export default Folder;
