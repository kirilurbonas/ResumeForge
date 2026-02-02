import React, { useState, useEffect } from 'react';
import { resumeAPI } from '../services/api';
import ATSScore from './ATSScore';
import SuggestionsPanel from './SuggestionsPanel';
import './AnalysisDashboard.css';

function AnalysisDashboard({ resumeId }) {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAnalysis();
  }, [resumeId]);

  const loadAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await resumeAPI.analyze(resumeId);
      setAnalysis(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze resume');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Analyzing resume...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!analysis) {
    return null;
  }

  return (
    <div className="analysis-dashboard">
      <h2>Resume Analysis</h2>
      
      <ATSScore score={analysis.ats_score} />

      <div className="analysis-grid">
        <div className="analysis-section">
          <h3>Strengths</h3>
          <ul>
            {analysis.strengths.map((strength, idx) => (
              <li key={idx}>{strength}</li>
            ))}
          </ul>
        </div>

        <div className="analysis-section">
          <h3>Areas for Improvement</h3>
          <ul>
            {analysis.weaknesses.map((weakness, idx) => (
              <li key={idx}>{weakness}</li>
            ))}
          </ul>
        </div>
      </div>

      <SuggestionsPanel resumeId={resumeId} />
    </div>
  );
}

export default AnalysisDashboard;
