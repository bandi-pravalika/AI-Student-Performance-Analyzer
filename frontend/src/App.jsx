import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import { Navbar } from './components/Navbar'
import { Sidebar } from './components/Sidebar'
import { PredictionModal } from './components/PredictionModal'
import { DashboardPage } from './pages/Dashboard'
import { AnalyticsPage } from './pages/Analytics'
import { StudentsPage } from './pages/Students'
import { TrendsPage } from './pages/Trends'
import './index.css'

function AppContent() {
  const [isPredictionModalOpen, setIsPredictionModalOpen] = useState(false)

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <Sidebar onPredictClick={() => setIsPredictionModalOpen(true)} />

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Navbar */}
        <Navbar onPredictClick={() => setIsPredictionModalOpen(true)} />

        {/* Main content area */}
        <main className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/students" element={<StudentsPage />} />
            <Route path="/trends" element={<TrendsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>

      {/* Prediction Modal */}
      <PredictionModal
        isOpen={isPredictionModalOpen}
        onClose={() => setIsPredictionModalOpen(false)}
      />
    </div>
  )
}

export default function App() {
  return (
    <Router>
      <ThemeProvider>
        <AppContent />
      </ThemeProvider>
    </Router>
  )
}
