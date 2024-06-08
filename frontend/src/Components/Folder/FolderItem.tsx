import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

interface File {
  _id: string;
  filename: string;
  folder_id: string;
  size: number;
  content_type: string;
  download_url: string;
}

const FolderItem: React.FC = () => {
  const { folderId } = useParams<{ folderId: string }>();
  const [files, setFiles] = useState<File[]>([]);
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
      const filesWithUrls = await Promise.all(
        response.data.map(async (file) => {
          const fileResponse = await axios.get<{ metadata: File; download_url: string }>(
            `http://localhost:5000/api/files/${file._id}`,
            {
              params: { user_id: userId },
            }
          );
          return { ...fileResponse.data.metadata, download_url: fileResponse.data.download_url };
        })
      );
      setFiles(filesWithUrls);
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

  const renderFilePreview = (file: File) => {
    const fileExtension = file.filename.split('.').pop()?.toLowerCase();
    if (['jpg', 'jpeg', 'png', 'gif'].includes(fileExtension || '')) {
      return <img src={file.download_url} alt={file.filename} style={{ maxWidth: '100%' }} />;
    } else if (['mp4', 'webm'].includes(fileExtension || '')) {
      return (
        <video controls style={{ maxWidth: '100%' }}>
          <source src={file.download_url} type={file.content_type} />
        </video>
      );
    } else {
      return <a href={file.download_url}>{file.filename}</a>;
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
            <li key={file._id}>{renderFilePreview(file)}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default FolderItem;