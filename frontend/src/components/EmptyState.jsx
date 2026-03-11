import React from 'react'
import './EmptyState.css'

function EmptyState({ title, description, actionLabel, onAction }) {
  return (
    <div className="empty-state">
      <div className="empty-state__icon" aria-hidden="true">
        📄
      </div>
      {title && <h4 className="empty-state__title">{title}</h4>}
      {description && <p className="empty-state__description">{description}</p>}
      {actionLabel && onAction && (
        <button
          type="button"
          className="btn btn-primary"
          onClick={onAction}
        >
          {actionLabel}
        </button>
      )}
    </div>
  )
}

export default EmptyState

