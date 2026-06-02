import React from 'react'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { Card } from './Cards'

export function PerformanceLineChart({ data }) {
  const chartData = [
    { month: 'Jan', score: 72, target: 75 },
    { month: 'Feb', score: 75, target: 75 },
    { month: 'Mar', score: 73, target: 75 },
    { month: 'Apr', score: 78, target: 75 },
    { month: 'May', score: 81, target: 75 },
    { month: 'Jun', score: 84, target: 75 },
  ]

  return (
    <Card header={<h3 className="text-lg font-bold">Performance Trend</h3>}>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="currentColor" className="opacity-20" />
          <XAxis stroke="currentColor" className="opacity-60" />
          <YAxis stroke="currentColor" className="opacity-60" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: 'none',
              borderRadius: '8px',
              color: '#fff',
            }}
            wrapperStyle={{ outline: 'none' }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#0ea5e9"
            strokeWidth={2}
            dot={{ fill: '#0ea5e9', r: 4 }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="target"
            stroke="#22c55e"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ fill: '#22c55e', r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  )
}

export function RiskDistributionChart() {
  const data = [
    { name: 'Low Risk', value: 45, fill: '#22c55e' },
    { name: 'Medium Risk', value: 35, fill: '#eab308' },
    { name: 'High Risk', value: 20, fill: '#ef4444' },
  ]

  return (
    <Card header={<h3 className="text-lg font-bold">Risk Distribution</h3>}>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            paddingAngle={5}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.fill} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Card>
  )
}

export function GradeDistributionChart() {
  const data = [
    { grade: 'A', students: 25, fill: '#0ea5e9' },
    { grade: 'B', students: 40, fill: '#10b981' },
    { grade: 'C', students: 22, fill: '#f59e0b' },
    { grade: 'F', students: 13, fill: '#ef4444' },
  ]

  return (
    <Card header={<h3 className="text-lg font-bold">Grade Distribution</h3>}>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="currentColor" className="opacity-20" />
          <XAxis dataKey="grade" stroke="currentColor" className="opacity-60" />
          <YAxis stroke="currentColor" className="opacity-60" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: 'none',
              borderRadius: '8px',
              color: '#fff',
            }}
          />
          <Bar dataKey="students" fill="#0ea5e9">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.fill} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Card>
  )
}

export function FeatureImportanceChart({ data }) {
  const chartData = [
    { name: 'Study Hours', importance: 0.35 },
    { name: 'Attendance', importance: 0.28 },
    { name: 'Previous Score', importance: 0.22 },
    { name: 'Test Prep', importance: 0.15 },
  ]

  return (
    <Card header={<h3 className="text-lg font-bold">Feature Importance</h3>}>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 200, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="currentColor" className="opacity-20" />
          <XAxis type="number" stroke="currentColor" className="opacity-60" />
          <YAxis dataKey="name" type="category" stroke="currentColor" className="opacity-60" width={190} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: 'none',
              borderRadius: '8px',
              color: '#fff',
            }}
          />
          <Bar dataKey="importance" fill="#8b5cf6" />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  )
}

export function ScoreDistributionChart() {
  const data = [
    { range: '0-20', count: 5 },
    { range: '20-40', count: 8 },
    { range: '40-60', count: 15 },
    { range: '60-80', count: 35 },
    { range: '80-100', count: 37 },
  ]

  return (
    <Card header={<h3 className="text-lg font-bold">Score Distribution</h3>}>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="currentColor" className="opacity-20" />
          <XAxis dataKey="range" stroke="currentColor" className="opacity-60" />
          <YAxis stroke="currentColor" className="opacity-60" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: 'none',
              borderRadius: '8px',
              color: '#fff',
            }}
          />
          <Bar dataKey="count" fill="#06b6d4" />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  )
}
