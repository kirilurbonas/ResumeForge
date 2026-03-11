import React, { useState } from 'react';
import { resumeAPI } from '../services/api';
import { useToast } from '../hooks/useToast';
import './ResumeUpload.css';

function ResumeUpload({ onUpload }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(null);
  const { showSuccess, showError } = useToast();

  const validateAndSetFile = (selectedFile) => {
    if (!selectedFile) return;

    if (
      selectedFile.type === 'application/pdf' ||
      selectedFile.name.endsWith('.docx') ||
      selectedFile.name.endsWith('.doc')
    ) {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please upload a PDF or DOC/DOCX file');
      setFile(null);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    validateAndSetFile(selectedFile);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!uploading) {
      setIsDragging(true);
    }
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (uploading) return;
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files?.[0];
    validateAndSetFile(droppedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setUploadProgress(null);
    setError(null);

    try {
      // For now we show an indeterminate progress bar while uploading.
      // If needed, this can be wired to Axios onUploadProgress.
      const result = await resumeAPI.upload(file);
      setUploadProgress(100);
      onUpload(result);
      showSuccess('Resume uploaded successfully');
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to upload resume';
      setError(message);
      showError(message);
    } finally {
      setUploading(false);
      setTimeout(() => setUploadProgress(null), 400);
    }
  };

  return (
    <div className="resume-upload">
      <h2>Upload Your Resume</h2>
      <p>Upload your resume in PDF or DOCX format to get started</p>

      <div
        className={`upload-area upload-dropzone ${isDragging ? 'upload-dropzone--dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-upload"
          accept=".pdf,.docx,.doc"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <label htmlFor="file-upload" className="upload-label">
          {file ? file.name : 'Choose a file or drag it here'}
        </label>
        <p className="upload-hint">Supported formats: PDF, DOC, DOCX • Max size 10MB</p>
        {file && (
          <button onClick={handleUpload} disabled={uploading} className="upload-button">
            {uploading ? 'Uploading...' : 'Upload Resume'}
          </button>
        )}
        {uploading && (
          <div className="upload-progress">
            <div className="upload-progress-bar" />
          </div>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}
    </div>
  );
}

export default ResumeUpload;
