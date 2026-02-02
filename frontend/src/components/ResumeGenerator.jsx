import React, { useState } from 'react';
import { resumeAPI } from '../services/api';
import './ResumeGenerator.css';

function ResumeGenerator({ resumeId }) {
  const [selectedTemplate, setSelectedTemplate] = useState('modern');
  const [selectedFormat, setSelectedFormat] = useState('doc');
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setGenerating(true);
    setError(null);

    try {
      const blob = await resumeAPI.generate(resumeId, selectedTemplate, selectedFormat);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const extension = selectedFormat === 'doc' ? 'docx' : 'pdf';
      a.download = `resume.${extension}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate resume');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="resume-generator">
      <h3>Generate Resume</h3>
      
      <div className="generator-controls">
        <div className="control-group">
          <label>Template:</label>
          <select
            value={selectedTemplate}
            onChange={(e) => setSelectedTemplate(e.target.value)}
            disabled={generating}
          >
            <option value="modern">Modern</option>
            <option value="classic">Classic</option>
            <option value="ats_friendly">ATS-Friendly</option>
            <option value="minimalist">Minimalist</option>
          </select>
        </div>

        <div className="control-group">
          <label>Format:</label>
          <select
            value={selectedFormat}
            onChange={(e) => setSelectedFormat(e.target.value)}
            disabled={generating}
          >
            <option value="doc">DOCX (Word)</option>
            <option value="pdf">PDF</option>
          </select>
        </div>

        <button
          onClick={handleGenerate}
          disabled={generating}
          className="generate-button"
        >
          {generating ? 'Generating...' : 'Generate & Download'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}
    </div>
  );
}

export default ResumeGenerator;
