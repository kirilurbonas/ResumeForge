import React, { useState, useEffect } from 'react';
import { templateAPI } from '../services/api';
import './TemplateSelector.css';

function TemplateSelector({ resumeId, onTemplateSelect }) {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    setLoading(true);
    try {
      const result = await templateAPI.list();
      setTemplates(result);
      if (result.length > 0) {
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
      <div className="templates-grid">
        {templates.map((template) => (
          <div
            key={template.id}
            className={`template-card ${selectedTemplate === template.id ? 'selected' : ''}`}
            onClick={() => handleTemplateSelect(template.id)}
          >
            <div className="template-name">{template.name}</div>
            <div className="template-description">{template.description}</div>
            {template.ats_friendly && (
              <div className="ats-badge">ATS-Friendly</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default TemplateSelector;
