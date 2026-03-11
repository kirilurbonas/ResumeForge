import React, { createContext, useCallback, useMemo, useState } from 'react'
import ToastContainer from '../components/ToastContainer'

export const ToastContext = createContext({
  addToast: () => {},
  removeToast: () => {},
})

let toastIdCounter = 0

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const removeToast = useCallback((id) => {
    setToasts((current) => current.filter((toast) => toast.id !== id))
  }, [])

  const addToast = useCallback(
    ({ message, type = 'info', duration = 4000 }) => {
      if (!message) return
      const id = ++toastIdCounter
      setToasts((current) => [...current, { id, message, type }])
      if (duration > 0) {
        setTimeout(() => removeToast(id), duration)
      }
    },
    [removeToast],
  )

  const value = useMemo(
    () => ({
      addToast,
      removeToast,
    }),
    [addToast, removeToast],
  )

  return (
    <ToastContext.Provider value={value}>
      {children}
      <ToastContainer toasts={toasts} onRemove={removeToast} />
    </ToastContext.Provider>
  )
}

