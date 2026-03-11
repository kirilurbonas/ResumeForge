import React from 'react'
import './SkeletonLoader.css'

function SkeletonLoader({
  width = '100%',
  height = '1rem',
  circle = false,
  className = '',
  style = {},
}) {
  const inlineStyle = {
    width,
    height,
    borderRadius: circle ? '50%' : 'var(--radius-md)',
    ...style,
  }

  return <div className={`skeleton-loader ${className}`} style={inlineStyle} />
}

export default SkeletonLoader

