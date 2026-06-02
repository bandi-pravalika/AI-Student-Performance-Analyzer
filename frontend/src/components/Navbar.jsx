import React from 'react'
import { Menu, X, Sun, Moon, LogOut, Settings } from 'lucide-react'
import { useTheme } from '../context/ThemeContext'

export function Navbar({ toggleSidebar, isSidebarOpen }) {
  const { isDark, toggleTheme } = useTheme()

  return (
    <nav className="sticky top-0 z-40 bg-white dark:bg-dark-800 border-b border-gray-200 dark:border-dark-700 shadow-soft">
      <div className="px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          {/* Left side - Logo and toggle */}
          <div className="flex items-center gap-4">
            <button
              onClick={toggleSidebar}
              className="p-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded-lg transition-colors lg:hidden"
            >
              {isSidebarOpen ? (
                <X size={24} />
              ) : (
                <Menu size={24} />
              )}
            </button>

            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-400 to-primary-600 rounded-lg flex items-center justify-center text-white font-bold text-lg">
                📊
              </div>
              <div className="hidden sm:block">
                <h1 className="text-lg font-bold text-dark-900 dark:text-white">
                  Student Performance
                </h1>
                <p className="text-xs text-gray-600 dark:text-gray-400">Analytics Platform</p>
              </div>
            </div>
          </div>

          {/* Right side - Actions */}
          <div className="flex items-center gap-3">
            <button
              onClick={toggleTheme}
              className="p-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded-lg transition-colors"
              title="Toggle theme"
            >
              {isDark ? (
                <Sun size={20} className="text-yellow-500" />
              ) : (
                <Moon size={20} className="text-gray-600" />
              )}
            </button>

            <button className="p-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded-lg transition-colors">
              <Settings size={20} />
            </button>

            <div className="hidden sm:flex items-center gap-3 pl-3 border-l border-gray-200 dark:border-dark-700">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-medium text-dark-900 dark:text-white">Admin User</p>
                <p className="text-xs text-gray-600 dark:text-gray-400">analyst@school.edu</p>
              </div>
              <img
                src="https://api.dicebear.com/7.x/avataaars/svg?seed=admin"
                alt="User"
                className="w-10 h-10 rounded-full"
              />
            </div>

            <button className="p-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded-lg transition-colors sm:hidden">
              <LogOut size={20} />
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
