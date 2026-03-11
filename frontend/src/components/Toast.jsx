import React from 'react'
import './Toast.css'

function Toast({ id, message, type = 'info', onClose }) {
  return (
    <div className={`toast toast--${type}`}>
      <div className="toast__content">
        <span className="toast__message">{message}</span>
      </div>
      <button
        type="button"
        className="toast__close"
        onClick={() => onClose(id)}
        aria-label="Dismiss notification"
      >
        ×
      </button>
    </div>
  )
}

export default Toast

