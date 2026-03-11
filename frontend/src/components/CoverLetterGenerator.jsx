import React, { useState } from 'react';
import { resumeAPI } from '../services/api';
import { useToast } from '../hooks/useToast';
import './CoverLetterGenerator.css';

function CoverLetterGenerator({ resumeId }) {
  const [jobDescription, setJobDescription] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [tone, setTone] = useState('professional');
  const [length, setLength] = useState('medium');
  const [coverLetter, setCoverLetter] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { showSuccess, showError } = useToast();

  const handleGenerate = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await resumeAPI.generateCoverLetter(
        resumeId,
        jobDescription,
        companyName || null,
        tone,
        length
      );
      setCoverLetter(result);
      showSuccess('Cover letter generated successfully');
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to generate cover letter';
      setError(message);
      showError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!coverLetter) return;
    
    const blob = new Blob([coverLetter.cover_letter], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cover_letter_${companyName || 'application'}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const handleCopy = () => {
    if (!coverLetter) return;
    navigator.clipboard.writeText(coverLetter.cover_letter);
    showSuccess('Cover letter copied to clipboard');
  };

  return (
    <div className="cover-letter-generator">
      <h3>Generate Cover Letter</h3>
      
      <div className="cover-letter-form">
        <div className="form-group">
          <label>Job Description *</label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here..."
            rows="6"
            className="textarea"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label>Company Name (Optional)</label>
          <input
            type="text"
            className="input"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="e.g., Google, Microsoft"
            disabled={loading}
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Tone</label>
            <select
              value={tone}
              onChange={(e) => setTone(e.target.value)}
              className="select"
              disabled={loading}
            >
              <option value="professional">Professional</option>
              <option value="friendly">Friendly</option>
              <option value="formal">Formal</option>
            </select>
          </div>

          <div className="form-group">
            <label>Length</label>
            <select
              value={length}
              onChange={(e) => setLength(e.target.value)}
              className="select"
              disabled={loading}
            >
              <option value="short">Short (200-250 words)</option>
              <option value="medium">Medium (300-400 words)</option>
              <option value="long">Long (500-600 words)</option>
            </select>
          </div>
        </div>

        <button
          onClick={handleGenerate}
          disabled={loading || !jobDescription.trim()}
          className="generate-button btn btn-primary"
        >
          {loading ? 'Generating...' : 'Generate Cover Letter'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {coverLetter && (
        <div className="cover-letter-result">
          <div className="result-header">
            <h4>Generated Cover Letter</h4>
            <div className="result-actions">
              <button onClick={handleCopy} className="action-button">Copy</button>
              <button onClick={handleDownload} className="action-button">Download</button>
            </div>
          </div>
          <div className="cover-letter-content">
            {coverLetter.cover_letter.split('\n').map((line, idx) => (
              <p key={idx}>{line}</p>
            ))}
          </div>
          <div className="cover-letter-meta">
            <span>Word Count: {coverLetter.word_count}</span>
            <span>Tone: {coverLetter.tone}</span>
            <span>Length: {coverLetter.length}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default CoverLetterGenerator;
