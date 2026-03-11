import { useContext } from 'react'
import { ToastContext } from '../context/ToastContext'

export function useToast() {
  const context = useContext(ToastContext)

  if (!context) {
    throw new Error('useToast must be used within a ToastProvider')
  }

  const { addToast, removeToast } = context

  return {
    addToast,
    removeToast,
    showSuccess: (message, duration) =>
      addToast({ message, type: 'success', duration }),
    showError: (message, duration) =>
      addToast({ message, type: 'error', duration }),
    showInfo: (message, duration) =>
      addToast({ message, type: 'info', duration }),
    showWarning: (message, duration) =>
      addToast({ message, type: 'warning', duration }),
  }
}

