import React, { useState, useEffect } from 'react';
import { templateAPI } from '../services/api';
import './TemplateSelector.css';

function TemplateSelector({ resumeId, onTemplateSelect }) {
  const [templates, setTemplates] = useState([]);
  const [industries, setIndustries] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [selectedIndustry, setSelectedIndustry] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadTemplates();
    loadIndustries();
  }, []);

  useEffect(() => {
    loadTemplates();
  }, [selectedIndustry]);

  const loadTemplates = async () => {
    setLoading(true);
    try {
      const result = await templateAPI.list(selectedIndustry || null);
      setTemplates(result);
      if (result.length > 0 && !selectedTemplate) {
        setSelectedTemplate(result[0].id);
        if (onTemplateSelect) {
          onTemplateSelect(result[0].id);
        }
      }
    } catch (err) {
      console.error('Failed to load templates:', err);
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

  const handleTemplateSelect = (templateId) => {
    setSelectedTemplate(templateId);
    if (onTemplateSelect) {
      onTemplateSelect(templateId);
    }
  };

  if (loading) {
    return <div className="loading">Loading templates...</div>;
  }

  return (
    <div className="template-selector">
      <h3>Select a Template</h3>
      
      {industries.length > 0 && (
        <div className="industry-filter">
          <label>Filter by Industry:</label>
          <select
            value={selectedIndustry}
            onChange={(e) => setSelectedIndustry(e.target.value)}
          >
            <option value="">All Templates</option>
            {industries.map(industry => (
              <option key={industry} value={industry}>
                {industry.charAt(0).toUpperCase() + industry.slice(1)}
              </option>
            ))}
          </select>
        </div>
      )}

      {loading && <div className="loading">Loading templates...</div>}
      
      {!loading && templates.length === 0 && (
        <div className="no-templates">No templates found.</div>
      )}

      {!loading && templates.length > 0 && (
        <div className="templates-grid">
          {templates.map((template) => (
            <div
              key={template.id}
              className={`template-card ${selectedTemplate === template.id ? 'selected' : ''}`}
              onClick={() => handleTemplateSelect(template.id)}
            >
              <div className="template-name">{template.name}</div>
              <div className="template-description">{template.description}</div>
              <div className="template-badges">
                {template.ats_friendly && (
                  <div className="ats-badge">ATS-Friendly</div>
                )}
                {template.industry && (
                  <div className="industry-badge">{template.industry}</div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default TemplateSelector;
