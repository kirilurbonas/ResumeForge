import React from 'react';
import './ATSScore.css';

function ATSScore({ score }) {
  const getScoreColor = (score) => {
    if (score >= 80) return '#48bb78';
    if (score >= 60) return '#ed8936';
    return '#f56565';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Improvement';
  };

  return (
    <div className="ats-score">
      <h3>ATS Compatibility Score</h3>
      <div className="score-circle" style={{ borderColor: getScoreColor(score) }}>
        <div className="score-value" style={{ color: getScoreColor(score) }}>
          {score}
        </div>
        <div className="score-max">/ 100</div>
      </div>
      <div className="score-label" style={{ color: getScoreColor(score) }}>
        {getScoreLabel(score)}
      </div>
      <p className="score-description">
        This score indicates how well your resume is optimized for Applicant Tracking Systems (ATS).
      </p>
    </div>
  );
}

export default ATSScore;
