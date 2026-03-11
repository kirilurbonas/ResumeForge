import React, { useState } from 'react';
import { resumeAPI } from '../services/api';
import './InterviewPrep.css';

function InterviewPrep({ resumeId }) {
  const [jobDescription, setJobDescription] = useState('');
  const [questionTypes, setQuestionTypes] = useState(['behavioral', 'technical', 'situational']);
  const [questions, setQuestions] = useState(null);
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingAnswer, setLoadingAnswer] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateQuestions = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await resumeAPI.generateInterviewQuestions(
        resumeId,
        jobDescription,
        questionTypes
      );
      setQuestions(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate questions');
    } finally {
      setLoading(false);
    }
  };

  const handleGetAnswer = async (question) => {
    setSelectedQuestion(question);
    setLoadingAnswer(true);
    setAnswer(null);
    try {
      const result = await resumeAPI.generateAnswer(
        resumeId,
        question,
        jobDescription || null
      );
      setAnswer(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate answer');
    } finally {
      setLoadingAnswer(false);
    }
  };

  const toggleQuestionType = (type) => {
    if (questionTypes.includes(type)) {
      setQuestionTypes(questionTypes.filter(t => t !== type));
    } else {
      setQuestionTypes([...questionTypes, type]);
    }
  };

  return (
    <div className="interview-prep">
      <h3>Interview Preparation</h3>
      
      <div className="prep-form">
        <div className="form-group">
          <label>Job Description *</label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here..."
            rows="4"
            className="textarea"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label>Question Types</label>
          <div className="question-type-checkboxes">
            {['behavioral', 'technical', 'situational', 'general'].map(type => (
              <label key={type} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={questionTypes.includes(type)}
                  onChange={() => toggleQuestionType(type)}
                  disabled={loading}
                />
                <span>{type.charAt(0).toUpperCase() + type.slice(1)}</span>
              </label>
            ))}
          </div>
        </div>

        <button
          onClick={handleGenerateQuestions}
          disabled={loading || !jobDescription.trim() || questionTypes.length === 0}
          className="generate-button btn btn-primary"
        >
          {loading ? 'Generating Questions...' : 'Generate Interview Questions'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {questions && (
        <div className="questions-container">
          <h4>Interview Questions ({questions.total_questions} total)</h4>
          {Object.entries(questions.questions).map(([category, categoryQuestions]) => (
            <div key={category} className="question-category">
              <h5>{category.charAt(0).toUpperCase() + category.slice(1)} Questions</h5>
              <ul className="questions-list">
                {categoryQuestions.map((q, idx) => (
                  <li key={idx} className="question-item">
                    <div className="question-text">{q}</div>
                    <button
                      onClick={() => handleGetAnswer(q)}
                      className="get-answer-button"
                      disabled={loadingAnswer}
                    >
                      Get Suggested Answer
                    </button>
                    {selectedQuestion === q && answer && (
                      <div className="answer-panel">
                        <div className="answer-content">
                          <strong>Suggested Answer:</strong>
                          <p>{answer.suggested_answer}</p>
                        </div>
                        {answer.tips && answer.tips.length > 0 && (
                          <div className="answer-tips">
                            <strong>Tips:</strong>
                            <ul>
                              {answer.tips.map((tip, tipIdx) => (
                                <li key={tipIdx}>{tip}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {answer.key_points && answer.key_points.length > 0 && (
                          <div className="answer-key-points">
                            <strong>Key Points:</strong>
                            <ul>
                              {answer.key_points.map((point, pointIdx) => (
                                <li key={pointIdx}>{point}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                    {selectedQuestion === q && loadingAnswer && (
                      <div className="loading-answer">Generating answer...</div>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default InterviewPrep;
