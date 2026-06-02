import React from 'react'
import { ArrowUp, ArrowDown, TrendingUp } from 'lucide-react'
import { cn } from '../utils/cn'

export function StatCard({ icon: Icon, label, value, change, trend = 'up', color = 'primary' }) {
  const colors = {
    primary: 'bg-primary-50 dark:bg-primary-500/10 text-primary-600 dark:text-primary-400',
    success: 'bg-success-50 dark:bg-success-500/10 text-success-600 dark:text-success-400',
    warning: 'bg-warning-50 dark:bg-warning-500/10 text-warning-600 dark:text-warning-400',
    danger: 'bg-danger-50 dark:bg-danger-500/10 text-danger-600 dark:text-danger-400',
  }

  return (
    <div className="card p-6">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">{label}</p>
          <h3 className="text-3xl font-bold text-dark-900 dark:text-white mb-3">{value}</h3>
          {change && (
            <div className="flex items-center gap-2">
              <span
                className={cn(
                  'flex items-center gap-1 text-sm font-medium',
                  trend === 'up'
                    ? 'text-success-600 dark:text-success-400'
                    : 'text-danger-600 dark:text-danger-400'
                )}
              >
                {trend === 'up' ? <ArrowUp size={16} /> : <ArrowDown size={16} />}
                {change}
              </span>
              <span className="text-xs text-gray-500 dark:text-gray-400">vs last month</span>
            </div>
          )}
        </div>
        <div className={cn('p-3 rounded-lg', colors[color])}>
          <Icon size={24} />
        </div>
      </div>
    </div>
  )
}

export function Card({ children, className = '', header = null, footer = null }) {
  return (
    <div className={cn('card', className)}>
      {header && <div className="border-b border-gray-200 dark:border-dark-700 p-6">{header}</div>}
      <div className="p-6">{children}</div>
      {footer && <div className="border-t border-gray-200 dark:border-dark-700 p-6">{footer}</div>}
    </div>
  )
}

export function InfoCard({ title, description, icon: Icon, color = 'primary' }) {
  const bgColors = {
    primary: 'bg-primary-50 dark:bg-primary-500/10',
    success: 'bg-success-50 dark:bg-success-500/10',
    warning: 'bg-warning-50 dark:bg-warning-500/10',
    danger: 'bg-danger-50 dark:bg-danger-500/10',
  }

  const textColors = {
    primary: 'text-primary-700 dark:text-primary-300',
    success: 'text-success-700 dark:text-success-300',
    warning: 'text-warning-700 dark:text-warning-300',
    danger: 'text-danger-700 dark:text-danger-300',
  }

  return (
    <div className={cn('card p-6 flex gap-4', bgColors[color])}>
      <div className={cn('flex-shrink-0 mt-1', textColors[color])}>
        <Icon size={24} />
      </div>
      <div className="flex-1">
        <h4 className="font-semibold text-dark-900 dark:text-white mb-1">{title}</h4>
        <p className="text-sm text-gray-600 dark:text-gray-400">{description}</p>
      </div>
    </div>
  )
}

export function ScoreCard({ score, maxScore = 100, grade, status = 'neutral' }) {
  const percentage = (score / maxScore) * 100
  const statusColor = {
    excellent: 'text-success-600 dark:text-success-400',
    good: 'text-primary-600 dark:text-primary-400',
    neutral: 'text-warning-600 dark:text-warning-400',
    poor: 'text-danger-600 dark:text-danger-400',
  }[status]

  return (
    <div className="card p-6 text-center">
      <div className="relative w-24 h-24 mx-auto mb-4">
        <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90">
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke="currentColor"
            strokeWidth="6"
            className="text-gray-200 dark:text-dark-700"
          />
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke="currentColor"
            strokeWidth="6"
            strokeDasharray={`${(percentage / 100) * 283} 283`}
            className={cn('transition-all duration-500', statusColor)}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={cn('text-2xl font-bold', statusColor)}>{Math.round(score)}</span>
          <span className="text-xs text-gray-500 dark:text-gray-400">/ {maxScore}</span>
        </div>
      </div>
      <h4 className={cn('text-lg font-bold mb-1', statusColor)}>{grade}</h4>
      <p className="text-sm text-gray-600 dark:text-gray-400">Final Score</p>
    </div>
  )
}
