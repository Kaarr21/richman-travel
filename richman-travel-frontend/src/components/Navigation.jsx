import React from 'react'

export default function Navigation({ currentView, setCurrentView, isAdmin, setIsAdmin }) {
  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-2">
            <i className="fas fa-mountain text-green-600 text-2xl"></i>
            <h1 className="text-2xl font-bold text-gray-800">Richman Travel & Tours</h1>
          </div>
          <div className="hidden md:flex space-x-8">
            {['home','destinations','booking','about'].map(view => (
              <button key={view} onClick={() => setCurrentView(view)} className={`font-medium ${currentView === view ? 'text-green-600' : 'text-gray-700 hover:text-green-600'}`}>
                {view.charAt(0).toUpperCase() + view.slice(1)}
              </button>
            ))}
          </div>
          <div className="flex items-center space-x-4">
            <button onClick={() => setIsAdmin(!isAdmin)} className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700">
              {isAdmin ? 'User View' : 'Admin'}
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
