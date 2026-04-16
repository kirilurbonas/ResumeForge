import React, { useEffect, useState } from 'react';
import {
  useNavigate,
  useParams,
  useSearchParams,
} from 'react-router-dom';
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
import LoadingOverlay from './components/LoadingOverlay';
import { resumeAPI, authAPI } from './services/api';

const RESUME_TABS = new Set([
  'analysis',
  'templates',
  'cover-letter',
  'interview',
  'versions',
]);

function App() {
  const { resumeId } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const tabParam = searchParams.get('tab');

  const [currentResume, setCurrentResume] = useState(null);
  const [activeTab, setActiveTab] = useState('resumes');
  const [user, setUser] = useState(null);
  const [showRegister, setShowRegister] = useState(false);
  const [loading, setLoading] = useState(true);
  const [isNavOpen, setIsNavOpen] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    if (token && savedUser) {
      setUser(JSON.parse(savedUser));
      authAPI.getCurrentUser().catch(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setUser(null);
      });
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    if (!user || !resumeId) {
      return undefined;
    }
    let cancelled = false;
    resumeAPI
      .get(resumeId)
      .then((data) => {
        if (cancelled) return;
        setCurrentResume(data);
      })
      .catch(() => {
        if (cancelled) return;
        navigate('/', { replace: true });
        setCurrentResume(null);
      });
    return () => {
      cancelled = true;
    };
  }, [user, resumeId, navigate]);

  useEffect(() => {
    if (!user || !resumeId || !currentResume || currentResume.id !== resumeId) {
      return;
    }
    const nextTab =
      tabParam && RESUME_TABS.has(tabParam) ? tabParam : 'analysis';
    setActiveTab(nextTab);
    if (!tabParam || !RESUME_TABS.has(tabParam)) {
      navigate(`/r/${resumeId}?tab=analysis`, { replace: true });
    }
  }, [user, resumeId, tabParam, currentResume, navigate]);

  const handleLogin = (userData) => {
    setUser(userData);
    setActiveTab('resumes');
    navigate('/', { replace: true });
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setCurrentResume(null);
    setActiveTab('resumes');
    navigate('/', { replace: true });
  };

  const handleResumeUpload = (resumeData) => {
    setCurrentResume(resumeData);
    setActiveTab('analysis');
    navigate(`/r/${resumeData.id}?tab=analysis`, { replace: true });
  };

  const handleResumeSelect = (resume) => {
    setCurrentResume(resume);
    setActiveTab('analysis');
    navigate(`/r/${resume.id}?tab=analysis`, { replace: true });
  };

  const goHomeResumes = () => {
    navigate('/');
    setCurrentResume(null);
    setActiveTab('resumes');
  };

  const goUpload = () => {
    navigate('/');
    setActiveTab('upload');
  };

  const goResumeTab = (tab) => {
    if (!currentResume) return;
    setActiveTab(tab);
    navigate(`/r/${currentResume.id}?tab=${tab}`, { replace: true });
  };

  const getTabLabel = () => {
    switch (activeTab) {
      case 'resumes':
        return 'My Resumes';
      case 'upload':
        return 'Upload Resume';
      case 'analysis':
        return 'Analysis';
      case 'templates':
        return 'Templates & Generate';
      case 'cover-letter':
        return 'Cover Letter';
      case 'interview':
        return 'Interview Prep';
      case 'versions':
        return 'Versions';
      default:
        return '';
    }
  };

  if (loading) {
    return <LoadingOverlay label="Loading your workspace..." />;
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
                <p>
                  Don&apos;t have an account?{' '}
                  <button
                    type="button"
                    onClick={() => setShowRegister(true)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#3498db',
                      cursor: 'pointer',
                      textDecoration: 'underline',
                    }}
                  >
                    Register here
                  </button>
                </p>
              </div>
            </div>
          )}
          {showRegister && (
            <div style={{ textAlign: 'center', marginTop: '20px' }}>
              <p>
                Already have an account?{' '}
                <button
                  type="button"
                  onClick={() => setShowRegister(false)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#3498db',
                    cursor: 'pointer',
                    textDecoration: 'underline',
                  }}
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
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <header className="app-header">
        <div className="app-header-inner">
          <div className="app-header-brand">
            <h1>ResumeForge</h1>
            <p>Analyze, optimize, and generate professional resumes</p>
          </div>
          <div className="app-header-actions">
            <button
              type="button"
              className="menu-toggle"
              aria-label="Toggle navigation"
              aria-expanded={isNavOpen}
              aria-controls="app-nav"
              onClick={() => setIsNavOpen((open) => !open)}
            >
              ☰
            </button>
            <span className="app-header-user">Welcome, {user.username}</span>
            <button
              type="button"
              onClick={handleLogout}
              className="btn btn-outline app-header-logout"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="app-container">
        <nav
          id="app-nav"
          className={`tab-nav ${isNavOpen ? '' : 'tab-nav--hidden'}`}
        >
          <button
            type="button"
            className={activeTab === 'resumes' ? 'active' : ''}
            onClick={goHomeResumes}
          >
            <span className="tab-icon" aria-hidden="true">
              📁
            </span>
            <span>My Resumes</span>
          </button>
          <button
            type="button"
            className={activeTab === 'upload' ? 'active' : ''}
            onClick={goUpload}
          >
            <span className="tab-icon" aria-hidden="true">
              ⬆️
            </span>
            <span>Upload Resume</span>
          </button>
          {currentResume && (
            <>
              <button
                type="button"
                className={activeTab === 'analysis' ? 'active' : ''}
                onClick={() => goResumeTab('analysis')}
              >
                <span className="tab-icon" aria-hidden="true">
                  📊
                </span>
                <span>Analysis</span>
              </button>
              <button
                type="button"
                className={activeTab === 'templates' ? 'active' : ''}
                onClick={() => goResumeTab('templates')}
              >
                <span className="tab-icon" aria-hidden="true">
                  📄
                </span>
                <span>Templates &amp; Generate</span>
              </button>
              <button
                type="button"
                className={activeTab === 'cover-letter' ? 'active' : ''}
                onClick={() => goResumeTab('cover-letter')}
              >
                <span className="tab-icon" aria-hidden="true">
                  ✉️
                </span>
                <span>Cover Letter</span>
              </button>
              <button
                type="button"
                className={activeTab === 'interview' ? 'active' : ''}
                onClick={() => goResumeTab('interview')}
              >
                <span className="tab-icon" aria-hidden="true">
                  💬
                </span>
                <span>Interview Prep</span>
              </button>
              <button
                type="button"
                className={activeTab === 'versions' ? 'active' : ''}
                onClick={() => goResumeTab('versions')}
              >
                <span className="tab-icon" aria-hidden="true">
                  🕒
                </span>
                <span>Versions</span>
              </button>
            </>
          )}
        </nav>

        <main id="main-content" className="app-content">
          <div className="breadcrumbs">
            <span className="breadcrumbs-root">Home</span>
            {getTabLabel() && (
              <>
                <span className="breadcrumbs-separator">/</span>
                <span className="breadcrumbs-current">{getTabLabel()}</span>
              </>
            )}
          </div>
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
