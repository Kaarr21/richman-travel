// richman-travel-frontend/src/components/AdminDashboard.jsx - Fixed version with API integration
import React, { useState, useEffect } from 'react'
import { apiClient } from '../utils/api'

export default function AdminDashboard({ setIsAdmin }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [token, setToken] = useState(localStorage.getItem('adminToken'))
  const [loginForm, setLoginForm] = useState({ username: '', password: '' })
  const [loginError, setLoginError] = useState('')
  const [isLoggingIn, setIsLoggingIn] = useState(false)
  
  // Dashboard data
  const [bookings, setBookings] = useState([])
  const [stats, setStats] = useState(null)
  const [selectedBooking, setSelectedBooking] = useState(null)
  const [statusFilter, setStatusFilter] = useState('all')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  // Check authentication on component mount
  useEffect(() => {
    if (token) {
      setIsAuthenticated(true)
      fetchDashboardData()
    }
  }, [token])

  // Test backend connection
  useEffect(() => {
    const testConnection = async () => {
      try {
        const response = await apiClient.checkHealth()
        console.log('Backend connection successful:', response)
      } catch (error) {
        console.error('Backend connection failed:', error)
        setError('Cannot connect to backend server. Please ensure it is running.')
      }
    }
    testConnection()
  }, [])

  const handleLogin = async (e) => {
    e.preventDefault()
    setIsLoggingIn(true)
    setLoginError('')

    try {
      const response = await apiClient.adminLogin(loginForm)
      const authToken = response.token
      
      localStorage.setItem('adminToken', authToken)
      setToken(authToken)
      setIsAuthenticated(true)
      setLoginForm({ username: '', password: '' })
      
      // Fetch dashboard data after successful login
      await fetchDashboardData()
    } catch (error) {
      console.error('Login failed:', error)
      setLoginError(error.message || 'Login failed. Please check your credentials.')
    } finally {
      setIsLoggingIn(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('adminToken')
    setToken(null)
    setIsAuthenticated(false)
    setBookings([])
    setStats(null)
    setError('')
  }

  const fetchDashboardData = async () => {
    if (!token) return

    setLoading(true)
    setError('')

    try {
      // Fetch bookings and stats in parallel
      const [bookingsResponse, statsResponse] = await Promise.all([
        apiClient.getAdminBookings(token, currentPage, statusFilter === 'all' ? '' : statusFilter),
        apiClient.getDashboardStats(token).catch(err => {
          console.warn('Stats fetch failed:', err)
          return null
        })
      ])

      setBookings(bookingsResponse.data || [])
      if (bookingsResponse.pagination) {
        setTotalPages(bookingsResponse.pagination.pages)
      }

      if (statsResponse) {
        setStats(statsResponse.data)
      }

    } catch (error) {
      console.error('Error fetching dashboard data:', error)
      setError('Failed to load dashboard data: ' + error.message)
      
      // If unauthorized, logout
      if (error.status === 401) {
        handleLogout()
      }
    } finally {
      setLoading(false)
    }
  }

  const updateBookingStatus = async (bookingId, newStatus, estimatedCost = null) => {
    if (!token) return

    try {
      const updateData = { status: newStatus }
      if (estimatedCost) updateData.estimated_cost = estimatedCost

      await apiClient.updateBooking(token, bookingId, updateData)
      
      // Refresh bookings list
      await fetchDashboardData()
      setSelectedBooking(null)
      
    } catch (error) {
      console.error('Error updating booking:', error)
      setError('Failed to update booking: ' + error.message)
    }
  }

  // Trigger data refresh when filters change
  useEffect(() => {
    if (isAuthenticated && token) {
      fetchDashboardData()
    }
  }, [statusFilter, currentPage])

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed': return 'bg-green-100 text-green-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'cancelled': return 'bg-red-100 text-red-800'
      case 'completed': return 'bg-blue-100 text-blue-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'confirmed': return 'fa-check-circle'
      case 'pending': return 'fa-clock'
      case 'cancelled': return 'fa-times-circle'
      case 'completed': return 'fa-flag-checkered'
      default: return 'fa-question-circle'
    }
  }

  // Login form component
  if (!isAuthenticated) {
    return (
      <section className="py-16 bg-gray-50 min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full">
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="text-center mb-8">
              <i className="fas fa-user-shield text-4xl text-green-600 mb-4"></i>
              <h2 className="text-2xl font-bold text-gray-800">Admin Login</h2>
              <p className="text-gray-600">Access the admin dashboard</p>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-6">
                <i className="fas fa-exclamation-triangle mr-2"></i>
                {error}
              </div>
            )}

            {loginError && (
              <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-6">
                <i className="fas fa-exclamation-circle mr-2"></i>
                {loginError}
              </div>
            )}

            <form onSubmit={handleLogin}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Username
                </label>
                <input
                  type="text"
                  value={loginForm.username}
                  onChange={(e) => setLoginForm(prev => ({ ...prev, username: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  placeholder="Enter username"
                  required
                  disabled={isLoggingIn}
                />
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  value={loginForm.password}
                  onChange={(e) => setLoginForm(prev => ({ ...prev, password: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  placeholder="Enter password"
                  required
                  disabled={isLoggingIn}
                />
              </div>

              <button
                type="submit"
                disabled={isLoggingIn}
                className={`w-full py-3 px-4 rounded-lg font-medium transition-colors ${
                  isLoggingIn
                    ? 'bg-gray-400 cursor-not-allowed text-white'
                    : 'bg-green-600 hover:bg-green-700 text-white'
                }`}
              >
                {isLoggingIn ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                    </svg>
                    Signing In...
                  </span>
                ) : (
                  <span>
                    <i className="fas fa-sign-in-alt mr-2"></i>
                    Sign In
                  </span>
                )}
              </button>
            </form>

            <div className="mt-6 text-center">
              <button
                onClick={() => setIsAdmin(false)}
                className="text-gray-600 hover:text-gray-800"
              >
                ← Back to Website
              </button>
            </div>

            <div className="mt-4 p-3 bg-blue-50 rounded-lg text-xs text-blue-800">
              <strong>Default Credentials:</strong><br />
              Username: admin<br />
              Password: admin123<br />
              (Change these in production!)
            </div>
          </div>
        </div>
      </section>
    )
  }

  // Main dashboard
  return (
    <section className="py-16 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h2 className="text-4xl font-bold text-gray-800 mb-2">Admin Dashboard</h2>
            <p className="text-gray-600">Manage bookings and track your travel business</p>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => fetchDashboardData()}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <i className={`fas fa-sync-alt mr-2 ${loading ? 'animate-spin' : ''}`}></i>
              Refresh
            </button>
            <button
              onClick={() => setIsAdmin(false)}
              className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <i className="fas fa-eye mr-2"></i>
              User View
            </button>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <i className="fas fa-sign-out-alt mr-2"></i>
              Logout
            </button>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-6">
            <div className="flex items-center">
              <i className="fas fa-exclamation-triangle mr-2"></i>
              {error}
            </div>
          </div>
        )}

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Total Bookings</p>
                  <p className="text-2xl font-bold text-gray-800">{stats.bookings?.total || 0}</p>
                </div>
                <div className="p-3 rounded-full bg-blue-100">
                  <i className="fas fa-calendar-alt text-blue-600 text-xl"></i>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Confirmed</p>
                  <p className="text-2xl font-bold text-gray-800">{stats.bookings?.confirmed || 0}</p>
                </div>
                <div className="p-3 rounded-full bg-green-100">
                  <i className="fas fa-check-circle text-green-600 text-xl"></i>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Pending</p>
                  <p className="text-2xl font-bold text-gray-800">{stats.bookings?.pending || 0}</p>
                </div>
                <div className="p-3 rounded-full bg-yellow-100">
                  <i className="fas fa-clock text-yellow-600 text-xl"></i>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Daily Visits</p>
                  <p className="text-2xl font-bold text-gray-800">{stats.visits?.daily || 0}</p>
                </div>
                <div className="p-3 rounded-full bg-purple-100">
                  <i className="fas fa-eye text-purple-600 text-xl"></i>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Filters and Actions */}
        <div className="bg-white p-6 rounded-xl shadow-md mb-6">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-4">
              <h3 className="text-lg font-semibold text-gray-800">
                Bookings ({bookings.length})
              </h3>
              <select 
                value={statusFilter} 
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              >
                <option value="all">All Status</option>
                <option value="pending">Pending</option>
                <option value="confirmed">Confirmed</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="bg-white rounded-xl shadow-md p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading bookings...</p>
          </div>
        )}

        {/* Bookings Table */}
        {!loading && (
          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            {bookings.length === 0 ? (
              <div className="p-8 text-center">
                <i className="fas fa-calendar-times text-4xl text-gray-400 mb-4"></i>
                <p className="text-gray-600 text-lg">No bookings found</p>
                <p className="text-gray-500">
                  {statusFilter === 'all' 
                    ? 'No bookings have been submitted yet.' 
                    : `No ${statusFilter} bookings found.`
                  }
                </p>
              </div>
            ) : (
              <>
                <div className="overflow-x-auto">
                  <table className="min-w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Customer</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Destination</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Date</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Guests</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Status</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {bookings.map(booking => (
                        <tr key={booking.id} className="hover:bg-gray-50 transition-colors">
                          <td className="px-6 py-4">
                            <div>
                              <div className="font-medium text-gray-800">{booking.name}</div>
                              <div className="text-sm text-gray-500">{booking.email}</div>
                              {booking.phone && (
                                <div className="text-sm text-gray-500">{booking.phone}</div>
                              )}
                            </div>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-700">{booking.destination || 'Not specified'}</td>
                          <td className="px-6 py-4 text-sm text-gray-700">
                            {booking.preferred_date 
                              ? new Date(booking.preferred_date).toLocaleDateString()
                              : 'Flexible'
                            }
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-700">{booking.guests}</td>
                          <td className="px-6 py-4">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(booking.status)}`}>
                              <i className={`fas ${getStatusIcon(booking.status)} mr-1`}></i>
                              {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                            </span>
                          </td>
                          <td className="px-6 py-4">
                            <button 
                              onClick={() => setSelectedBooking(booking)}
                              className="text-green-600 hover:text-green-800 mr-3 transition-colors"
                              title="View Details"
                            >
                              <i className="fas fa-eye"></i>
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="px-6 py-4 border-t border-gray-200 flex justify-between items-center">
                    <span className="text-sm text-gray-600">
                      Page {currentPage} of {totalPages}
                    </span>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                        disabled={currentPage === 1}
                        className="px-3 py-1 border border-gray-300 rounded disabled:opacity-50"
                      >
                        Previous
                      </button>
                      <button
                        onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                        disabled={currentPage === totalPages}
                        className="px-3 py-1 border border-gray-300 rounded disabled:opacity-50"
                      >
                        Next
                      </button>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* Booking Detail Modal */}
        {selectedBooking && (
          <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h3 className="text-2xl font-bold text-gray-800">Booking Details</h3>
                  <button 
                    onClick={() => setSelectedBooking(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <i className="fas fa-times text-xl"></i>
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold text-gray-800 mb-2">Customer Information</h4>
                    <div className="space-y-2 text-sm">
                      <p><span className="font-medium">Reference:</span> {selectedBooking.booking_reference}</p>
                      <p><span className="font-medium">Name:</span> {selectedBooking.name}</p>
                      <p><span className="font-medium">Email:</span> {selectedBooking.email}</p>
                      {selectedBooking.phone && (
                        <p><span className="font-medium">Phone:</span> {selectedBooking.phone}</p>
                      )}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-800 mb-2">Trip Details</h4>
                    <div className="space-y-2 text-sm">
                      <p><span className="font-medium">Destination:</span> {selectedBooking.destination || 'Not specified'}</p>
                      <p><span className="font-medium">Date:</span> {
                        selectedBooking.preferred_date 
                          ? new Date(selectedBooking.preferred_date).toLocaleDateString()
                          : 'Flexible'
                      }</p>
                      <p><span className="font-medium">Guests:</span> {selectedBooking.guests}</p>
                      {selectedBooking.estimated_cost && (
                        <p><span className="font-medium">Estimated Cost:</span> ${selectedBooking.estimated_cost}</p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="mt-6">
                  <h4 className="font-semibold text-gray-800 mb-2">Status</h4>
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(selectedBooking.status)}`}>
                    <i className={`fas ${getStatusIcon(selectedBooking.status)} mr-2`}></i>
                    {selectedBooking.status.charAt(0).toUpperCase() + selectedBooking.status.slice(1)}
                  </span>
                </div>

                {selectedBooking.message && (
                  <div className="mt-6">
                    <h4 className="font-semibold text-gray-800 mb-2">Customer Message</h4>
                    <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg">{selectedBooking.message}</p>
                  </div>
                )}

                <div className="mt-6">
                  <h4 className="font-semibold text-gray-800 mb-2">Booking Timeline</h4>
                  <div className="text-sm text-gray-600">
                    <p>Created: {new Date(selectedBooking.created_at).toLocaleString()}</p>
                    <p>Updated: {new Date(selectedBooking.updated_at).toLocaleString()}</p>
                  </div>
                </div>

                <div className="flex gap-4 mt-8">
                  {selectedBooking.status === 'pending' && (
                    <button 
                      onClick={() => updateBookingStatus(selectedBooking.id, 'confirmed')}
                      className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg font-medium transition-colors"
                    >
                      <i className="fas fa-check mr-2"></i>
                      Confirm Booking
                    </button>
                  )}
                  
                  {selectedBooking.status === 'confirmed' && (
                    <button 
                      onClick={() => updateBookingStatus(selectedBooking.id, 'completed')}
                      className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors"
                    >
                      <i className="fas fa-flag-checkered mr-2"></i>
                      Mark Completed
                    </button>
                  )}

                  {(selectedBooking.status === 'pending' || selectedBooking.status === 'confirmed') && (
                    <button 
                      onClick={() => updateBookingStatus(selectedBooking.id, 'cancelled')}
                      className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg font-medium transition-colors"
                    >
                      <i className="fas fa-times mr-2"></i>
                      Cancel Booking
                    </button>
                  )}
                  
                  <button 
                    onClick={() => setSelectedBooking(null)}
                    className="flex-1 border border-gray-300 hover:bg-gray-50 text-gray-700 py-2 px-4 rounded-lg font-medium transition-colors"
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  )
}
