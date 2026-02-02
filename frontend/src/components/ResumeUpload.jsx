import React, { useState } from 'react';
import { resumeAPI } from '../services/api';
import './ResumeUpload.css';

function ResumeUpload({ onUpload }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type === 'application/pdf' || 
          selectedFile.name.endsWith('.docx') || 
          selectedFile.name.endsWith('.doc')) {
        setFile(selectedFile);
        setError(null);
      } else {
        setError('Please upload a PDF or DOCX file');
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const result = await resumeAPI.upload(file);
      onUpload(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload resume');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="resume-upload">
      <h2>Upload Your Resume</h2>
      <p>Upload your resume in PDF or DOCX format to get started</p>

      <div className="upload-area">
        <input
          type="file"
          id="file-upload"
          accept=".pdf,.docx,.doc"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <label htmlFor="file-upload" className="upload-label">
          {file ? file.name : 'Choose File'}
        </label>
        {file && (
          <button onClick={handleUpload} disabled={uploading} className="upload-button">
            {uploading ? 'Uploading...' : 'Upload Resume'}
          </button>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}
    </div>
  );
}

export default ResumeUpload;
