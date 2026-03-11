import React, { useState, useEffect } from 'react';
import { resumeAPI, templateAPI } from '../services/api';
import LoadingSpinner from './LoadingSpinner';
import ConfirmDialog from './ConfirmDialog';
import EmptyState from './EmptyState';
import { useToast } from '../hooks/useToast';
import './ResumeList.css';

function ResumeList({ onResumeSelect }) {
  const [resumes, setResumes] = useState([]);
  const [industries, setIndustries] = useState([]);
  const [selectedIndustry, setSelectedIndustry] = useState('');
  const [selectedTag, setSelectedTag] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resumeToDelete, setResumeToDelete] = useState(null);
  const { showSuccess, showError } = useToast();

  useEffect(() => {
    loadResumes();
    loadIndustries();
  }, []);

  useEffect(() => {
    loadResumes();
  }, [selectedIndustry, selectedTag]);

  const loadResumes = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await resumeAPI.listResumes(
        selectedIndustry || null,
        selectedTag || null
      );
      setResumes(result.resumes || []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load resumes');
    } finally {
      setLoading(false);
    }
  };

  const loadIndustries = async () => {
    try {
      const result = await templateAPI.listIndustries();
      setIndustries(result.industries || []);
    } catch (err) {
      console.error('Failed to load industries:', err);
    }
  };

  const handleResumeClick = (resume) => {
    if (onResumeSelect) {
      onResumeSelect(resume);
    }
  };

  const openDeleteDialog = (resume, e) => {
    e.stopPropagation();
    setResumeToDelete(resume);
  };

  const handleConfirmDelete = async () => {
    if (!resumeToDelete) return;
    try {
      await resumeAPI.delete(resumeToDelete.id);
      setResumeToDelete(null);
      await loadResumes();
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to delete resume';
      setError(message);
      showError(message);
      setResumeToDelete(null);
      return;
    }
    showSuccess('Resume deleted successfully');
  };

  const handleCancelDelete = () => {
    setResumeToDelete(null);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="resume-list">
      <h3>My Resumes</h3>

      <div className="filters">
        <div className="filter-group">
          <label>Filter by Industry:</label>
          <select
            value={selectedIndustry}
            onChange={(e) => setSelectedIndustry(e.target.value)}
          >
            <option value="">All Industries</option>
            {industries.map(industry => (
              <option key={industry} value={industry}>
                {industry.charAt(0).toUpperCase() + industry.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Filter by Tag:</label>
          <input
            type="text"
            value={selectedTag}
            onChange={(e) => setSelectedTag(e.target.value)}
            placeholder="Enter tag..."
          />
        </div>

        <button onClick={loadResumes} className="refresh-button">
          Refresh
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading && (
        <div className="loading">
          <LoadingSpinner label="Loading resumes..." />
        </div>
      )}

      {!loading && resumes.length === 0 && (
        <EmptyState
          title="No resumes yet"
          description="Upload your first resume to start analyzing and optimizing it."
        />
      )}

      {!loading && resumes.length > 0 && (
        <div className="resumes-grid">
          {resumes.map((resume) => (
            <div
              key={resume.id}
              className="resume-card"
              onClick={() => handleResumeClick(resume)}
            >
              <div className="resume-header">
                <h4>{resume.filename}</h4>
                <button
                  onClick={(e) => openDeleteDialog(resume, e)}
                  className="delete-button"
                  title="Delete resume"
                >
                  ×
                </button>
              </div>
              <div className="resume-meta">
                <div className="meta-item">
                  <strong>Version:</strong> {resume.version}
                </div>
                <div className="meta-item">
                  <strong>Uploaded:</strong> {formatDate(resume.uploaded_at)}
                </div>
                {resume.industry && (
                  <div className="meta-item">
                    <strong>Industry:</strong> {resume.industry}
                  </div>
                )}
                {resume.tags && resume.tags.length > 0 && (
                  <div className="meta-item">
                    <strong>Tags:</strong>{' '}
                    {resume.tags.map((tag, idx) => (
                      <span key={idx} className="tag">{tag}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="resume-count">
        Showing {resumes.length} resume{resumes.length !== 1 ? 's' : ''}
      </div>

      <ConfirmDialog
        isOpen={!!resumeToDelete}
        title="Delete resume?"
        description={
          resumeToDelete
            ? `Are you sure you want to delete "${resumeToDelete.filename}"? This action cannot be undone.`
            : ''
        }
        confirmLabel="Delete"
        cancelLabel="Cancel"
        variant="danger"
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
      />
    </div>
  );
}

export default ResumeList;
