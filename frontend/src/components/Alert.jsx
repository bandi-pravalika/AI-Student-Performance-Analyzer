import React from 'react'
import { AlertCircle, CheckCircle, AlertTriangle, Info } from 'lucide-react'
import { cn } from '../utils/cn'

export function Alert({ type = 'info', title, children, onClose }) {
  const colors = {
    info: {
      bg: 'bg-primary-50 dark:bg-primary-500/10',
      border: 'border-primary-200 dark:border-primary-500/30',
      icon: 'text-primary-600 dark:text-primary-400',
      title: 'text-primary-900 dark:text-primary-200',
    },
    success: {
      bg: 'bg-success-50 dark:bg-success-500/10',
      border: 'border-success-200 dark:border-success-500/30',
      icon: 'text-success-600 dark:text-success-400',
      title: 'text-success-900 dark:text-success-200',
    },
    warning: {
      bg: 'bg-warning-50 dark:bg-warning-500/10',
      border: 'border-warning-200 dark:border-warning-500/30',
      icon: 'text-warning-600 dark:text-warning-400',
      title: 'text-warning-900 dark:text-warning-200',
    },
    error: {
      bg: 'bg-danger-50 dark:bg-danger-500/10',
      border: 'border-danger-200 dark:border-danger-500/30',
      icon: 'text-danger-600 dark:text-danger-400',
      title: 'text-danger-900 dark:text-danger-200',
    },
  }

  const color = colors[type]
  const icons = {
    info: Info,
    success: CheckCircle,
    warning: AlertTriangle,
    error: AlertCircle,
  }
  const Icon = icons[type]

  return (
    <div className={cn('card border p-4 flex gap-4', color.bg, color.border)}>
      <Icon size={20} className={cn('flex-shrink-0 mt-0.5', color.icon)} />
      <div className="flex-1">
        {title && <h4 className={cn('font-semibold mb-1', color.title)}>{title}</h4>}
        <p className="text-sm text-gray-700 dark:text-gray-300">{children}</p>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="flex-shrink-0 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        >
          ✕
        </button>
      )}
    </div>
  )
}

export function Badge({ variant = 'primary', size = 'md', children }) {
  const sizes = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-2 text-base',
  }

  const variants = {
    primary: 'bg-primary-100 dark:bg-primary-500/20 text-primary-700 dark:text-primary-300',
    success: 'bg-success-100 dark:bg-success-500/20 text-success-700 dark:text-success-300',
    warning: 'bg-warning-100 dark:bg-warning-500/20 text-warning-700 dark:text-warning-300',
    danger: 'bg-danger-100 dark:bg-danger-500/20 text-danger-700 dark:text-danger-300',
    gray: 'bg-gray-100 dark:bg-dark-700 text-gray-700 dark:text-gray-300',
  }

  return (
    <span className={cn('badge rounded-full font-medium', sizes[size], variants[variant])}>
      {children}
    </span>
  )
}

export function RiskBadge({ level }) {
  const config = {
    Low: { emoji: '🟢', variant: 'success' },
    Medium: { emoji: '🟡', variant: 'warning' },
    High: { emoji: '🔴', variant: 'danger' },
  }

  const { emoji, variant } = config[level] || { emoji: '⚪', variant: 'gray' }

  return (
    <Badge variant={variant}>
      {emoji} {level} Risk
    </Badge>
  )
}
