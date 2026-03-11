import React, { useEffect } from 'react'
import './Modal.css'

function Modal({ isOpen, title, children, onClose }) {
  useEffect(() => {
    if (!isOpen) return

    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        onClose?.()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  const handleBackdropClick = (event) => {
    if (event.target.getAttribute('data-modal-backdrop') === 'true') {
      onClose?.()
    }
  }

  return (
    <div
      className="modal-backdrop"
      data-modal-backdrop="true"
      onClick={handleBackdropClick}
      aria-modal="true"
      role="dialog"
    >
      <div className="modal">
        {title && <h3 className="modal__title">{title}</h3>}
        <div className="modal__body">{children}</div>
      </div>
    </div>
  )
}

export default Modal

