import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  BarChart3,
  Users,
  TrendingUp,
  Settings,
  HelpCircle,
  X,
} from 'lucide-react'
import { cn } from '../utils/cn'

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/', color: 'text-primary-500' },
  { icon: BarChart3, label: 'Analytics', path: '/analytics', color: 'text-blue-500' },
  { icon: Users, label: 'Students', path: '/students', color: 'text-purple-500' },
  { icon: TrendingUp, label: 'Predictions', path: '/predictions', color: 'text-green-500' },
]

const bottomItems = [
  { icon: Settings, label: 'Settings', path: '/settings', color: 'text-gray-500' },
  { icon: HelpCircle, label: 'Help', path: '/help', color: 'text-gray-500' },
]

export function Sidebar({ isOpen, toggleSidebar }) {
  const location = useLocation()

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/20 dark:bg-black/40 z-30 lg:hidden"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed left-0 top-0 z-40 h-screen w-64 bg-white dark:bg-dark-800 border-r border-gray-200 dark:border-dark-700',
          'flex flex-col gap-6 p-6 transition-transform duration-300 ease-out',
          'lg:translate-x-0 lg:sticky lg:top-0',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {/* Close button mobile */}
        <button
          onClick={toggleSidebar}
          className="absolute top-4 right-4 p-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded-lg lg:hidden"
        >
          <X size={20} />
        </button>

        {/* Main navigation */}
        <nav className="flex-1 space-y-2">
          <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4 mt-8 lg:mt-0">
            Menu
          </p>
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => toggleSidebar()}
                className={cn(
                  'flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-all duration-200',
                  isActive
                    ? 'bg-primary-50 dark:bg-primary-500/10 text-primary-600 dark:text-primary-400'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-dark-700'
                )}
              >
                <Icon size={20} className={cn('transition-colors', isActive && item.color)} />
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>

        {/* Bottom navigation */}
        <nav className="space-y-2 border-t border-gray-200 dark:border-dark-700 pt-4">
          <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">
            Support
          </p>
          {bottomItems.map((item) => {
            const Icon = item.icon
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => toggleSidebar()}
                className="flex items-center gap-3 px-4 py-3 rounded-lg font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-dark-700 transition-all duration-200"
              >
                <Icon size={20} className={item.color} />
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>

        {/* Footer info */}
        <div className="bg-primary-50 dark:bg-primary-500/10 rounded-lg p-4 border border-primary-100 dark:border-primary-500/20">
          <p className="text-sm font-semibold text-primary-900 dark:text-primary-300 mb-2">
            💡 Pro Tip
          </p>
          <p className="text-xs text-primary-800 dark:text-primary-200">
            Use keyboard shortcuts to navigate faster. Press ? for help.
          </p>
        </div>
      </aside>
    </>
  )
}
