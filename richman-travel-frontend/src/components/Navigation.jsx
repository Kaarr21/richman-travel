import React, { useState } from 'react'

export default function Navigation({ currentView, setCurrentView, isAdmin, setIsAdmin }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navigationItems = [
    { id: 'home', label: 'Home' },
    { id: 'destinations', label: 'Destinations' },
    { id: 'booking', label: 'Booking' },
    { id: 'about', label: 'About' }
  ]

  const handleNavClick = (view) => {
    setCurrentView(view)
    setMobileMenuOpen(false)
  }

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <div 
            className="flex items-center space-x-2 cursor-pointer" 
            onClick={() => handleNavClick('home')}
          >
            <i className="fas fa-mountain text-green-600 text-2xl"></i>
            <h1 className="text-2xl font-bold text-gray-800">Richman Travel & Tours</h1>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-8">
            {navigationItems.map(item => (
              <button 
                key={item.id} 
                onClick={() => handleNavClick(item.id)} 
                className={`font-medium transition-colors duration-200 ${
                  currentView === item.id 
                    ? 'text-green-600 border-b-2 border-green-600 pb-1' 
                    : 'text-gray-700 hover:text-green-600'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>

          {/* Admin Toggle & Mobile Menu Button */}
          <div className="flex items-center space-x-4">
            <button 
              onClick={() => setIsAdmin(!isAdmin)} 
              className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
                isAdmin 
                  ? 'bg-green-600 text-white hover:bg-green-700' 
                  : 'bg-gray-600 text-white hover:bg-gray-700'
              }`}
            >
              {isAdmin ? 'User View' : 'Admin'}
            </button>

            {/* Mobile Menu Button */}
            <button 
              className="md:hidden text-gray-700 hover:text-green-600"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <i className={`fas ${mobileMenuOpen ? 'fa-times' : 'fa-bars'} text-xl`}></i>
            </button>
          </div>
        </div>

        {/* Mobile Navigation Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t">
            {navigationItems.map(item => (
              <button 
                key={item.id} 
                onClick={() => handleNavClick(item.id)} 
                className={`block w-full text-left py-2 px-4 rounded-lg transition-colors duration-200 ${
                  currentView === item.id 
                    ? 'text-green-600 bg-green-50 font-medium' 
                    : 'text-gray-700 hover:text-green-600 hover:bg-gray-50'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>
        )}
      </div>
    </nav>
  )
}
