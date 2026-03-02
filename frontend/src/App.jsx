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
import Login from './components/Login';
import Register from './components/Register';
import { resumeAPI, authAPI } from './services/api';

function App() {
  const [currentResume, setCurrentResume] = useState(null);
  const [activeTab, setActiveTab] = useState('resumes');
  const [user, setUser] = useState(null);
  const [showRegister, setShowRegister] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    if (token && savedUser) {
      setUser(JSON.parse(savedUser));
      // Verify token is still valid
      authAPI.getCurrentUser().catch(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setUser(null);
      });
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setActiveTab('resumes');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setCurrentResume(null);
    setActiveTab('resumes');
  };

  const handleResumeUpload = async (resumeData) => {
    setCurrentResume(resumeData);
    setActiveTab('analysis');
  };

  const handleResumeSelect = (resume) => {
    setCurrentResume(resume);
    setActiveTab('analysis');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    return (
      <div className="app">
        <header className="app-header">
          <h1>ResumeForge</h1>
          <p>Analyze, optimize, and generate professional resumes</p>
        </header>
        <div className="app-container">
          {showRegister ? (
            <Register onRegister={handleLogin} />
          ) : (
            <div>
              <Login onLogin={handleLogin} />
              <div style={{ textAlign: 'center', marginTop: '20px' }}>
                <p>Don't have an account?{' '}
                  <button
                    onClick={() => setShowRegister(true)}
                    style={{ background: 'none', border: 'none', color: '#3498db', cursor: 'pointer', textDecoration: 'underline' }}
                  >
                    Register here
                  </button>
                </p>
              </div>
            </div>
          )}
          {showRegister && (
            <div style={{ textAlign: 'center', marginTop: '20px' }}>
              <p>Already have an account?{' '}
                <button
                  onClick={() => setShowRegister(false)}
                  style={{ background: 'none', border: 'none', color: '#3498db', cursor: 'pointer', textDecoration: 'underline' }}
                >
                  Login here
                </button>
              </p>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', maxWidth: '1200px', margin: '0 auto' }}>
          <div>
            <h1>ResumeForge</h1>
            <p>Analyze, optimize, and generate professional resumes</p>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <span style={{ color: 'white', fontSize: '14px' }}>Welcome, {user.username}</span>
            <button
              onClick={handleLogout}
              style={{
                background: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                border: '1px solid white',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Logout
            </button>
          </div>
        </div>
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
