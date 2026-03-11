import React from 'react'
import Modal from './Modal'
import './Modal.css'

function ConfirmDialog({
  isOpen,
  title = 'Are you sure?',
  description,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  onConfirm,
  onCancel,
  variant = 'danger',
}) {
  return (
    <Modal isOpen={isOpen} title={title} onClose={onCancel}>
      {description && <p>{description}</p>}
      <div className="modal__actions">
        <button
          type="button"
          className="btn btn-outline"
          onClick={onCancel}
        >
          {cancelLabel}
        </button>
        <button
          type="button"
          className={`btn ${variant === 'danger' ? 'btn-danger' : 'btn-primary'}`}
          onClick={onConfirm}
        >
          {confirmLabel}
        </button>
      </div>
    </Modal>
  )
}

export default ConfirmDialog

