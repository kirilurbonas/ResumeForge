import React from 'react'
import LoadingSpinner from './LoadingSpinner'
import './LoadingOverlay.css'

function LoadingOverlay({ label = 'Loading...' }) {
  return (
    <div className="loading-overlay">
      <div className="loading-overlay__backdrop" />
      <div className="loading-overlay__content">
        <LoadingSpinner label={label} size="lg" />
      </div>
    </div>
  )
}

export default LoadingOverlay

