import React from 'react'
import './LoadingSpinner.css'

function LoadingSpinner({ label = 'Loading...', size = 'md' }) {
  return (
    <div className={`loading-spinner loading-spinner--${size}`}>
      <div className="loading-spinner__dots">
        <span />
        <span />
        <span />
      </div>
      {label && <div className="loading-spinner__label">{label}</div>}
    </div>
  )
}

export default LoadingSpinner

