import React, { useState, useEffect } from 'react';
import { resumeAPI } from '../services/api';
import LoadingSpinner from './LoadingSpinner';
import EmptyState from './EmptyState';
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
    return <LoadingSpinner label="Loading suggestions..." size="sm" />;
  }

  return (
    <div className="suggestions-panel">
      <h3>Improvement Suggestions</h3>
      <div className="suggestions-list">
        {suggestions.length === 0 ? (
          <EmptyState
            title="No suggestions yet"
            description="Run an analysis or provide more details to get personalized suggestions."
          />
        ) : (
          suggestions.map((suggestion, idx) => (
            <div key={idx} className="suggestion-item">
              <p>{suggestion}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default SuggestionsPanel;
