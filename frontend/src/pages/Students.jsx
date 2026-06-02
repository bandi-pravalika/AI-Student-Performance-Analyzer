import React, { useState } from 'react'
import { Search, Plus, Filter, Download } from 'lucide-react'
import { Card } from '../components/Cards'
import { StudentDetailCard, StudentList } from '../components/StudentCards'
import { Button } from '../components/Button'

// Mock data
const allStudents = [
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
  {
    id: 4,
    name: 'James Wilson',
    email: 'james.w@school.edu',
    attendance: 95,
    studyHours: 7.2,
    avgScore: 88,
    predictedScore: 90,
    grade: 'A',
    riskLevel: 'Low',
    trend: 'up',
    trendValue: 4,
  },
  {
    id: 5,
    name: 'Lisa Martinez',
    email: 'lisa.m@school.edu',
    attendance: 72,
    studyHours: 4.0,
    avgScore: 70,
    predictedScore: 68,
    grade: 'C',
    riskLevel: 'Medium',
    trend: 'down',
    trendValue: 2,
  },
]

export function StudentsPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedStudent, setSelectedStudent] = useState(null)
  const [filterRisk, setFilterRisk] = useState('all')

  const filteredStudents = allStudents.filter((student) => {
    const matchesSearch =
      student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.email.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesRisk = filterRisk === 'all' || student.riskLevel === filterRisk
    return matchesSearch && matchesRisk
  })

  return (
    <div className="container-main py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-dark-900 dark:text-white mb-2">
            Students
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage and monitor all students in your class.
          </p>
        </div>
        <div className="flex gap-3 mt-4 md:mt-0">
          <button className="inline-flex items-center gap-2 px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors">
            <Plus size={20} />
            Add Student
          </button>
          <button className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 text-dark-900 dark:text-white rounded-lg hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors">
            <Download size={20} />
            Export
          </button>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search by name or email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-dark-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter size={20} className="text-gray-600 dark:text-gray-400" />
          <select
            value={filterRisk}
            onChange={(e) => setFilterRisk(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-dark-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="all">All Risk Levels</option>
            <option value="Low">Low Risk</option>
            <option value="Medium">Medium Risk</option>
            <option value="High">High Risk</option>
          </select>
        </div>
      </div>

      {/* Results Summary */}
      <div className="text-sm text-gray-600 dark:text-gray-400">
        Showing {filteredStudents.length} of {allStudents.length} students
      </div>

      {/* Student Detail or List */}
      {selectedStudent ? (
        <div className="space-y-4">
          <button
            onClick={() => setSelectedStudent(null)}
            className="text-primary-500 hover:text-primary-600 font-medium"
          >
            ← Back to List
          </button>
          <StudentDetailCard student={selectedStudent} />
        </div>
      ) : (
        <StudentList
          students={filteredStudents}
          onSelectStudent={setSelectedStudent}
        />
      )}
    </div>
  )
}
