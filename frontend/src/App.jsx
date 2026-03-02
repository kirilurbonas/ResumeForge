import React, { useState, useEffect } from 'react';
import './App.css';
import ResumeUpload from './components/ResumeUpload';
import ResumeList from './components/ResumeList';
import AnalysisDashboard from './components/AnalysisDashboard';
import TemplateSelector from './components/TemplateSelector';
import ResumeGenerator from './components/ResumeGenerator';
import CoverLetterGenerator from './components/CoverLetterGenerator';
import InterviewPrep from './components/InterviewPrep';
import VersionManager from './components/VersionManager';
import { resumeAPI } from './services/api';

function App() {
  const [currentResume, setCurrentResume] = useState(null);
  const [activeTab, setActiveTab] = useState('resumes');

  const handleResumeUpload = async (resumeData) => {
    setCurrentResume(resumeData);
    setActiveTab('analysis');
  };

  const handleResumeSelect = (resume) => {
    setCurrentResume(resume);
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
            className={activeTab === 'resumes' ? 'active' : ''}
            onClick={() => setActiveTab('resumes')}
          >
            My Resumes
          </button>
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
              <button
                className={activeTab === 'cover-letter' ? 'active' : ''}
                onClick={() => setActiveTab('cover-letter')}
              >
                Cover Letter
              </button>
              <button
                className={activeTab === 'interview' ? 'active' : ''}
                onClick={() => setActiveTab('interview')}
              >
                Interview Prep
              </button>
              <button
                className={activeTab === 'versions' ? 'active' : ''}
                onClick={() => setActiveTab('versions')}
              >
                Versions
              </button>
            </>
          )}
        </nav>

        <main className="app-content">
          {activeTab === 'resumes' && (
            <ResumeList onResumeSelect={handleResumeSelect} />
          )}
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
          {activeTab === 'cover-letter' && currentResume && (
            <CoverLetterGenerator resumeId={currentResume.id} />
          )}
          {activeTab === 'interview' && currentResume && (
            <InterviewPrep resumeId={currentResume.id} />
          )}
          {activeTab === 'versions' && currentResume && (
            <VersionManager resumeId={currentResume.id} />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
