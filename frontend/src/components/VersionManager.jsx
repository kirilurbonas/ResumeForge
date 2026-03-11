import React, { useState, useEffect } from 'react';
import { resumeAPI } from '../services/api';
import EmptyState from './EmptyState';
import { useToast } from '../hooks/useToast';
import './VersionManager.css';

function VersionManager({ resumeId }) {
  const [versions, setVersions] = useState([]);
  const [selectedVersion, setSelectedVersion] = useState(null);
  const [changeDescription, setChangeDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState(null);
  const { showSuccess, showError } = useToast();

  useEffect(() => {
    loadVersions();
  }, [resumeId]);

  const loadVersions = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await resumeAPI.listVersions(resumeId);
      setVersions(result.versions || []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load versions');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateVersion = async () => {
    setCreating(true);
    setError(null);
    try {
      await resumeAPI.createVersion(resumeId, changeDescription || null);
      setChangeDescription('');
      await loadVersions();
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to create version';
      setError(message);
      showError(message);
    } finally {
      setCreating(false);
    }
    showSuccess('Version created successfully');
  };

  const handleViewVersion = async (version) => {
    setLoading(true);
    try {
      const versionData = await resumeAPI.getVersion(resumeId, version);
      setSelectedVersion(versionData);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load version');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="version-manager">
      <h3>Version Management</h3>

      <div className="create-version-section">
        <h4>Create New Version</h4>
        <div className="form-group">
          <label>Change Description (Optional)</label>
          <input
            type="text"
            value={changeDescription}
            onChange={(e) => setChangeDescription(e.target.value)}
            placeholder="e.g., Updated work experience, Added new skills"
            disabled={creating}
          />
        </div>
        <button
          onClick={handleCreateVersion}
          disabled={creating}
          className="create-button"
        >
          {creating ? 'Creating...' : 'Create Version'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="versions-list">
        <h4>Version History</h4>
        {loading && <div className="loading">Loading versions...</div>}
        {!loading && versions.length === 0 && (
          <EmptyState
            title="No versions yet"
            description="Create a new version to capture the current state of your resume."
          />
        )}
        {versions.length > 0 && (
          <div className="versions-grid">
            {versions.map((version) => (
              <div
                key={version.version}
                className={`version-card ${selectedVersion?.version === version.version ? 'selected' : ''}`}
                onClick={() => handleViewVersion(version.version)}
              >
                <div className="version-header">
                  <span className="version-number">Version {version.version}</span>
                  <span className="version-date">{formatDate(version.created_at)}</span>
                </div>
                {version.changes && (
                  <div className="version-changes">{version.changes}</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedVersion && (
        <div className="version-details">
          <h4>Version {selectedVersion.version} Details</h4>
          <div className="version-info">
            <div className="info-section">
              <strong>Filename:</strong> {selectedVersion.filename}
            </div>
            <div className="info-section">
              <strong>Uploaded:</strong> {formatDate(selectedVersion.uploaded_at)}
            </div>
            <div className="info-section">
              <strong>Experience:</strong> {selectedVersion.experience?.length || 0} positions
            </div>
            <div className="info-section">
              <strong>Education:</strong> {selectedVersion.education?.length || 0} entries
            </div>
            <div className="info-section">
              <strong>Skills:</strong> {selectedVersion.skills?.length || 0} skills
            </div>
          </div>
          <button
            onClick={() => setSelectedVersion(null)}
            className="close-button"
          >
            Close
          </button>
        </div>
      )}
    </div>
  );
}

export default VersionManager;
