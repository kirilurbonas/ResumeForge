import React, { useState, useEffect } from 'react';
import { resumeAPI } from '../services/api';
import './SuggestionsPanel.css';

function SuggestionsPanel({ resumeId }) {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadSuggestions();
  }, [resumeId]);

  const loadSuggestions = async () => {
    setLoading(true);
    try {
      const result = await resumeAPI.getSuggestions(resumeId);
      setSuggestions(result.suggestions || []);
    } catch (err) {
      console.error('Failed to load suggestions:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading suggestions...</div>;
  }

  return (
    <div className="suggestions-panel">
      <h3>Improvement Suggestions</h3>
      <div className="suggestions-list">
        {suggestions.length === 0 ? (
          <p>No suggestions available at this time.</p>
        ) : (
          suggestions.map((suggestion, idx) => (
            <div key={idx} className="suggestion-item">
              {typeof suggestion === 'string' ? (
                <p>{suggestion}</p>
              ) : (
                <p>{suggestion}</p>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default SuggestionsPanel;
