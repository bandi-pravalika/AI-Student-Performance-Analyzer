import React, { useState } from 'react'
import { X } from 'lucide-react'
import { Card } from './Cards'
import { Alert } from './Alert'

export function PredictionModal({ isOpen, onClose, onSubmit }) {
  const [formData, setFormData] = useState({
    studyHours: 5,
    attendance: 80,
    previousScore: 75,
    testPrepHours: 3,
  })

  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: parseFloat(value) || 0,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    // Simulate API call
    setTimeout(() => {
      const predictedScore = Math.min(
        100,
        (formData.studyHours * 5 +
          formData.attendance * 0.3 +
          formData.previousScore * 0.4 +
          formData.testPrepHours * 4) /
          2
      )

      setPrediction({
        score: Math.round(predictedScore),
        grade: predictedScore >= 90 ? 'A' : predictedScore >= 80 ? 'B' : predictedScore >= 70 ? 'C' : 'F',
        riskLevel: predictedScore >= 75 ? 'Low' : predictedScore >= 60 ? 'Medium' : 'High',
        confidence: 0.87,
      })
      setLoading(false)
    }, 1000)
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-2xl font-bold text-dark-900 dark:text-white">
            Predict Performance
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          {prediction ? (
            <div className="space-y-4">
              <Alert type="success" title="Prediction Complete">
                Based on the provided metrics, we've generated a prediction.
              </Alert>

              <div className="space-y-3">
                <div className="p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Predicted Score</p>
                  <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">
                    {prediction.score}
                  </p>
                </div>

                <div className="grid grid-cols-3 gap-3">
                  <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg text-center">
                    <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">Grade</p>
                    <p className="text-2xl font-bold text-dark-900 dark:text-white">
                      {prediction.grade}
                    </p>
                  </div>
                  <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg text-center">
                    <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">Risk Level</p>
                    <p className="text-sm font-bold text-danger-600 dark:text-danger-400">
                      {prediction.riskLevel}
                    </p>
                  </div>
                  <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg text-center">
                    <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">Confidence</p>
                    <p className="text-sm font-bold text-primary-600 dark:text-primary-400">
                      {(prediction.confidence * 100).toFixed(0)}%
                    </p>
                  </div>
                </div>

                <button
                  onClick={() => {
                    setPrediction(null)
                    setFormData({ studyHours: 5, attendance: 80, previousScore: 75, testPrepHours: 3 })
                  }}
                  className="w-full px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium"
                >
                  New Prediction
                </button>
                <button
                  onClick={onClose}
                  className="w-full px-4 py-2 bg-gray-200 dark:bg-gray-700 text-dark-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors font-medium"
                >
                  Close
                </button>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-dark-900 dark:text-white mb-1">
                  Study Hours (per week): {formData.studyHours}
                </label>
                <input
                  type="range"
                  name="studyHours"
                  min="0"
                  max="10"
                  step="0.5"
                  value={formData.studyHours}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-dark-900 dark:text-white mb-1">
                  Attendance (%): {formData.attendance}
                </label>
                <input
                  type="range"
                  name="attendance"
                  min="0"
                  max="100"
                  step="5"
                  value={formData.attendance}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-dark-900 dark:text-white mb-1">
                  Previous Score: {formData.previousScore}
                </label>
                <input
                  type="range"
                  name="previousScore"
                  min="0"
                  max="100"
                  step="1"
                  value={formData.previousScore}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-dark-900 dark:text-white mb-1">
                  Test Prep Hours: {formData.testPrepHours}
                </label>
                <input
                  type="range"
                  name="testPrepHours"
                  min="0"
                  max="10"
                  step="0.5"
                  value={formData.testPrepHours}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:bg-gray-400 transition-colors font-medium"
              >
                {loading ? 'Predicting...' : 'Get Prediction'}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}
