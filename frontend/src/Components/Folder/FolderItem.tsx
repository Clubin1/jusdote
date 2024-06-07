import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

interface File {
  _id: string;
  filename: string;
  folder_id: string;
  size: number;
  content_type: string;
}

const FolderItem: React.FC = () => {
  const { folderId } = useParams<{ folderId: string }>();
  const [files, setFiles] = useState<File[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const userId = localStorage.getItem('userId');
  useEffect(() => {
    fetchFiles();
  }, [folderId]);

  const fetchFiles = async () => {
    try {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken || !folderId) {
        return;
      }
      const response = await axios.get<File[]>(`http://localhost:5000/api/folders/${folderId}/files`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'User-Id': userId, 
        },
      });
      setFiles(response.data);
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && folderId) {
      const formData = new FormData();
      formData.append('file', file);
      try {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
          return;
        }
        const response = await axios.post(`http://localhost:5000/api/folders/${folderId}/files`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${accessToken}`,
          },
        });
        console.log('File uploaded:', response.data);
        fetchFiles();
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };

  return (
    <div>
      <h2>Folder: {folderId}</h2>
      <div>
        <h3>Upload File</h3>
        <input type="file" onChange={handleFileUpload} />
      </div>
      <div>
        <h3>Files</h3>
        <ul>
          {files.map((file) => (
            <li key={file._id}>{file.filename}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default FolderItem;
