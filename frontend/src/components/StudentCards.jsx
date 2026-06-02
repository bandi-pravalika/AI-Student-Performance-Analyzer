import React from 'react'
import { Card, ScoreCard } from './Cards'
import { RiskBadge, Badge } from './Alert'
import { TrendingUp, TrendingDown } from 'lucide-react'

export function StudentCard({ student, onClick }) {
  return (
    <Card className="cursor-pointer hover:shadow-medium transition-shadow" onClick={onClick}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <img
            src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${student.id}`}
            alt={student.name}
            className="w-12 h-12 rounded-lg"
          />
          <div>
            <h4 className="font-semibold text-dark-900 dark:text-white">{student.name}</h4>
            <p className="text-sm text-gray-500 dark:text-gray-400">{student.email}</p>
          </div>
        </div>
        <RiskBadge level={student.riskLevel} />
      </div>

      <div className="grid grid-cols-3 gap-4 mb-4 pb-4 border-b border-gray-100 dark:border-dark-700">
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Attendance</p>
          <p className="text-lg font-bold text-dark-900 dark:text-white">{student.attendance}%</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Study Hours</p>
          <p className="text-lg font-bold text-dark-900 dark:text-white">{student.studyHours}h</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Avg Score</p>
          <p className="text-lg font-bold text-dark-900 dark:text-white">{student.avgScore}</p>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Predicted Score</p>
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-primary-500">{student.predictedScore}</span>
            <Badge variant={student.trend === 'up' ? 'success' : 'danger'} size="sm">
              {student.trend === 'up' ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
              {student.trend === 'up' ? '+' : '-'}
              {student.trendValue}
            </Badge>
          </div>
        </div>
        <div className="text-right">
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Grade</p>
          <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">{student.grade}</p>
        </div>
      </div>
    </Card>
  )
}

export function StudentDetailCard({ prediction }) {
  if (!prediction) return null

  return (
    <Card header={<h3 className="text-lg font-bold">Prediction Details</h3>}>
      <div className="space-y-6">
        {/* Score and Grade */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Predicted Score</p>
            <p className="text-2xl font-bold text-primary-500">{prediction.predicted_score.toFixed(1)}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Grade</p>
            <p className="text-2xl font-bold text-dark-900 dark:text-white">{prediction.grade}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Risk Level</p>
            <RiskBadge level={prediction.risk_level} />
          </div>
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Risk Score</p>
            <p className="text-2xl font-bold text-warning-500">{prediction.risk_score.toFixed(1)}</p>
          </div>
        </div>

        {/* Confidence Interval */}
        <div className="bg-primary-50 dark:bg-primary-500/10 rounded-lg p-4 border border-primary-100 dark:border-primary-500/20">
          <p className="text-sm font-semibold text-primary-900 dark:text-primary-300 mb-3">
            95% Confidence Interval
          </p>
          <div className="space-y-2 text-sm text-primary-800 dark:text-primary-200">
            <p>Lower Bound: {prediction.confidence_interval.lower.toFixed(1)}</p>
            <p>Upper Bound: {prediction.confidence_interval.upper.toFixed(1)}</p>
            <p>Margin: ±{prediction.confidence_interval.margin.toFixed(1)}</p>
          </div>
        </div>

        {/* Feature Importance */}
        <div>
          <h4 className="font-semibold text-dark-900 dark:text-white mb-3">Feature Importance</h4>
          <div className="space-y-2">
            {Object.entries(prediction.feature_importance).map(([feature, importance]) => (
              <div key={feature}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-700 dark:text-gray-300">{feature}</span>
                  <span className="font-medium text-dark-900 dark:text-white">
                    {(importance * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-dark-700 rounded-full h-2">
                  <div
                    className="bg-primary-500 h-2 rounded-full transition-all"
                    style={{ width: `${importance * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  )
}

export function RecommendationCard({ recommendation }) {
  const priorityColors = {
    urgent: 'border-danger-200 dark:border-danger-500/30 bg-danger-50 dark:bg-danger-500/10',
    high: 'border-warning-200 dark:border-warning-500/30 bg-warning-50 dark:bg-warning-500/10',
    medium: 'border-primary-200 dark:border-primary-500/30 bg-primary-50 dark:bg-primary-500/10',
    low: 'border-success-200 dark:border-success-500/30 bg-success-50 dark:bg-success-500/10',
  }

  return (
    <div className={`card border p-4 ${priorityColors[recommendation.priority]}`}>
      <div className="flex gap-3">
        <div className="text-2xl">{recommendation.icon}</div>
        <div className="flex-1">
          <h4 className="font-semibold text-dark-900 dark:text-white mb-1">{recommendation.title}</h4>
          <p className="text-sm text-gray-700 dark:text-gray-300 mb-3">{recommendation.description}</p>
          <p className="text-sm font-medium text-primary-600 dark:text-primary-400 mb-3">
            💡 {recommendation.suggestion}
          </p>
          <div className="space-y-1 text-xs text-gray-600 dark:text-gray-400">
            <p className="font-medium">Action Items:</p>
            {recommendation.action_items.map((item, idx) => (
              <p key={idx}>✓ {item}</p>
            ))}
          </div>
        </div>
        <Badge variant={recommendation.priority === 'urgent' ? 'danger' : 'gray'} size="sm">
          {recommendation.priority.toUpperCase()}
        </Badge>
      </div>
    </div>
  )
}
