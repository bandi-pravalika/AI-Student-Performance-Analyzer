import React from 'react'
import { Card } from '../components/Cards'
import {
  PerformanceLineChart,
  RiskDistributionChart,
  GradeDistributionChart,
  FeatureImportanceChart,
  ScoreDistributionChart,
} from '../components/Charts'

export function AnalyticsPage() {
  return (
    <div className="container-main py-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-dark-900 dark:text-white mb-2">
          Analytics
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Comprehensive analytics and insights on student performance.
        </p>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PerformanceLineChart />
        <FeatureImportanceChart />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GradeDistributionChart />
        <ScoreDistributionChart />
      </div>

      <RiskDistributionChart />

      {/* Additional Insights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card header={<h3 className="text-lg font-bold">Top Performer</h3>}>
          <div className="text-center py-4">
            <p className="text-3xl font-bold text-primary-500 mb-2">97</p>
            <p className="font-medium text-dark-900 dark:text-white mb-1">Sarah Johnson</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Grade: A</p>
          </div>
        </Card>

        <Card header={<h3 className="text-lg font-bold">Average Performance</h3>}>
          <div className="text-center py-4">
            <p className="text-3xl font-bold text-warning-500 mb-2">75.3</p>
            <p className="font-medium text-dark-900 dark:text-white mb-1">Class Average</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Consistent growth</p>
          </div>
        </Card>

        <Card header={<h3 className="text-lg font-bold">Needs Support</h3>}>
          <div className="text-center py-4">
            <p className="text-3xl font-bold text-danger-500 mb-2">42</p>
            <p className="font-medium text-dark-900 dark:text-white mb-1">Mike Chen</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Grade: F</p>
          </div>
        </Card>
      </div>
    </div>
  )
}
