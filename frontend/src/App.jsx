import React, { useState, useEffect } from 'react';
import './App.css';
import ResumeUpload from './components/ResumeUpload';
import AnalysisDashboard from './components/AnalysisDashboard';
import TemplateSelector from './components/TemplateSelector';
import ResumeGenerator from './components/ResumeGenerator';
import { resumeAPI } from './services/api';

function App() {
  const [currentResume, setCurrentResume] = useState(null);
  const [activeTab, setActiveTab] = useState('upload');

  const handleResumeUpload = async (resumeData) => {
    setCurrentResume(resumeData);
    setActiveTab('analysis');
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>ResumeForge</h1>
        <p>Analyze, optimize, and generate professional resumes</p>
      </header>

      <div className="app-container">
        <nav className="tab-nav">
          <button
            className={activeTab === 'upload' ? 'active' : ''}
            onClick={() => setActiveTab('upload')}
          >
            Upload Resume
          </button>
          {currentResume && (
            <>
              <button
                className={activeTab === 'analysis' ? 'active' : ''}
                onClick={() => setActiveTab('analysis')}
              >
                Analysis
              </button>
              <button
                className={activeTab === 'templates' ? 'active' : ''}
                onClick={() => setActiveTab('templates')}
              >
                Templates & Generate
              </button>
            </>
          )}
        </nav>

        <main className="app-content">
          {activeTab === 'upload' && (
            <ResumeUpload onUpload={handleResumeUpload} />
          )}
          {activeTab === 'analysis' && currentResume && (
            <AnalysisDashboard resumeId={currentResume.id} />
          )}
          {activeTab === 'templates' && currentResume && (
            <div>
              <TemplateSelector resumeId={currentResume.id} />
              <ResumeGenerator resumeId={currentResume.id} />
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
