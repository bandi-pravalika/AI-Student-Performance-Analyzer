import React, { useState } from 'react'
import { Card } from '../components/Cards'
import { PerformanceLineChart } from '../components/Charts'

export function TrendsPage() {
  const [selectedStudent, setSelectedStudent] = useState(null)
  const [comparisonMode, setComparisonMode] = useState(false)

  const students = [
    { id: 1, name: 'Sarah Johnson' },
    { id: 2, name: 'Mike Chen' },
    { id: 3, name: 'Emma Davis' },
    { id: 4, name: 'James Wilson' },
  ]

  return (
    <div className="container-main py-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-dark-900 dark:text-white mb-2">
          Performance Trends
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Track student performance trends over time.
        </p>
      </div>

      {/* View Toggle */}
      <div className="flex gap-4">
        <button
          onClick={() => setComparisonMode(false)}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            !comparisonMode
              ? 'bg-primary-500 text-white'
              : 'bg-gray-200 dark:bg-gray-700 text-dark-900 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600'
          }`}
        >
          Individual View
        </button>
        <button
          onClick={() => setComparisonMode(true)}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            comparisonMode
              ? 'bg-primary-500 text-white'
              : 'bg-gray-200 dark:bg-gray-700 text-dark-900 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600'
          }`}
        >
          Comparison View
        </button>
      </div>

      {/* Student Selector */}
      <Card header={<h3 className="text-lg font-bold">Select Student(s)</h3>}>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {students.map((student) => (
            <button
              key={student.id}
              onClick={() => setSelectedStudent(student.id)}
              className={`p-3 rounded-lg border-2 transition-colors text-center ${
                selectedStudent === student.id
                  ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                  : 'border-gray-300 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-600'
              }`}
            >
              <p className="font-medium text-sm">{student.name}</p>
            </button>
          ))}
        </div>
      </Card>

      {/* Trends Chart */}
      <PerformanceLineChart />

      {/* Key Insights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card header={<h3 className="text-lg font-bold">Current Trend</h3>}>
          <div className="py-4">
            <p className="text-center text-3xl font-bold text-success-500 mb-2">
              ↑ +8.5%
            </p>
            <p className="text-center text-sm text-gray-600 dark:text-gray-400">
              Consistent improvement over 12 weeks
            </p>
          </div>
        </Card>

        <Card header={<h3 className="text-lg font-bold">Weekly Avg</h3>}>
          <div className="py-4">
            <p className="text-center text-3xl font-bold text-primary-500 mb-2">
              76.2
            </p>
            <p className="text-center text-sm text-gray-600 dark:text-gray-400">
              Last 4 weeks average
            </p>
          </div>
        </Card>

        <Card header={<h3 className="text-lg font-bold">Projected</h3>}>
          <div className="py-4">
            <p className="text-center text-3xl font-bold text-warning-500 mb-2">
              82
            </p>
            <p className="text-center text-sm text-gray-600 dark:text-gray-400">
              Expected score by end of term
            </p>
          </div>
        </Card>
      </div>

      {/* Milestones */}
      <Card header={<h3 className="text-lg font-bold">Milestones</h3>}>
        <div className="space-y-4">
          {[
            { date: 'Dec 15', event: 'Mid-term Exam', score: 72 },
            { date: 'Dec 22', event: 'Project Submission', score: 78 },
            { date: 'Jan 5', event: 'Study Intervention', score: 75 },
            { date: 'Jan 19', event: 'Final Review', score: 82 },
          ].map((milestone, idx) => (
            <div key={idx} className="flex items-center gap-4 pb-4 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
              <div className="flex-shrink-0 w-12 h-12 bg-primary-100 dark:bg-primary-900/30 rounded-lg flex items-center justify-center">
                <span className="text-primary-600 dark:text-primary-400 font-bold">
                  {milestone.score}
                </span>
              </div>
              <div className="flex-1">
                <p className="font-medium text-dark-900 dark:text-white">{milestone.event}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">{milestone.date}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
