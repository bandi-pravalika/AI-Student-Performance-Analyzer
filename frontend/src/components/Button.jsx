import React from 'react'

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  className = '',
  ...props
}) {
  const baseStyles =
    'inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'

  const variants = {
    primary:
      'bg-primary-500 text-white hover:bg-primary-600 focus:ring-offset-white dark:focus:ring-offset-gray-900',
    secondary:
      'bg-gray-200 text-dark-900 hover:bg-gray-300 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600',
    ghost:
      'text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 dark:text-primary-400',
    danger:
      'bg-danger-500 text-white hover:bg-danger-600 focus:ring-danger-500',
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}
