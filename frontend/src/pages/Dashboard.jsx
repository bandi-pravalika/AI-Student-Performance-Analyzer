import React, { useState } from 'react'
import { Users, TrendingUp, AlertCircle, BookOpen } from 'lucide-react'
import { StatCard, Card } from '../components/Cards'
import { Alert } from '../components/Alert'
import { StudentCard } from '../components/StudentCards'
import {
  PerformanceLineChart,
  RiskDistributionChart,
  GradeDistributionChart,
} from '../components/Charts'

// Mock data
const mockStudents = [
  {
    id: 1,
    name: 'Sarah Johnson',
    email: 'sarah.j@school.edu',
    attendance: 92,
    studyHours: 6.5,
    avgScore: 82,
    predictedScore: 85,
    grade: 'A',
    riskLevel: 'Low',
    trend: 'up',
    trendValue: 5,
  },
  {
    id: 2,
    name: 'Mike Chen',
    email: 'mike.chen@school.edu',
    attendance: 65,
    studyHours: 3.2,
    avgScore: 68,
    predictedScore: 62,
    grade: 'C',
    riskLevel: 'High',
    trend: 'down',
    trendValue: 8,
  },
  {
    id: 3,
    name: 'Emma Davis',
    email: 'emma.d@school.edu',
    attendance: 78,
    studyHours: 4.5,
    avgScore: 74,
    predictedScore: 76,
    grade: 'B',
    riskLevel: 'Medium',
    trend: 'up',
    trendValue: 3,
  },
]

export function DashboardPage() {
  const [selectedStudent, setSelectedStudent] = useState(null)

  return (
    <div className="container-main py-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-dark-900 dark:text-white mb-2">
          Dashboard
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Welcome back! Here's your student performance overview.
        </p>
      </div>

      {/* Alerts */}
      <div className="space-y-3">
        <Alert type="warning" title="5 Students at Risk">
          Several students need immediate attention. Review their profiles and consider interventions.
        </Alert>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={Users}
          label="Total Students"
          value="324"
          change="+12"
          trend="up"
          color="primary"
        />
        <StatCard
          icon={TrendingUp}
          label="Avg Score"
          value="75.3"
          change="+2.1"
          trend="up"
          color="success"
        />
        <StatCard
          icon={AlertCircle}
          label="At Risk"
          value="28"
          change="+5"
          trend="down"
          color="danger"
        />
        <StatCard
          icon={BookOpen}
          label="Attendance"
          value="82%"
          change="+1.2"
          trend="up"
          color="warning"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PerformanceLineChart />
        <RiskDistributionChart />
      </div>

      <GradeDistributionChart />

      {/* Recent Students */}
      <div>
        <h2 className="text-2xl font-bold text-dark-900 dark:text-white mb-6">
          Recent Students
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockStudents.map((student) => (
            <StudentCard
              key={student.id}
              student={student}
              onClick={() => setSelectedStudent(student)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
