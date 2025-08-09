import React, { useState } from 'react'

export default function AdminDashboard() {
  const [bookings] = useState([
    { 
      id: 1, 
      name: 'John Doe', 
      email: 'john@example.com',
      phone: '+254 700 123 456',
      destination: 'Maasai Mara Safari', 
      date: '2025-08-15', 
      guests: 2,
      status: 'confirmed',
      price: 900,
      message: 'Looking forward to seeing the Big Five!'
    },
    { 
      id: 2, 
      name: 'Jane Smith', 
      email: 'jane@example.com',
      phone: '+254 700 654 321',
      destination: 'Mount Kenya Expedition', 
      date: '2025-09-05', 
      guests: 4,
      status: 'pending',
      price: 1400,
      message: 'First time mountain climbing, need guidance'
    },
    { 
      id: 3, 
      name: 'Mike Johnson', 
      email: 'mike@example.com',
      phone: '+254 700 987 654',
      destination: 'Diani Beach', 
      date: '2025-08-28', 
      guests: 2,
      status: 'confirmed',
      price: 400,
      message: 'Honeymoon trip, need romantic setting'
    },
    { 
      id: 4, 
      name: 'Sarah Wilson', 
      email: 'sarah@example.com',
      phone: '+254 700 456 789',
      destination: "Hell's Gate National Park", 
      date: '2025-08-20', 
      guests: 1,
      status: 'cancelled',
      price: 150,
      message: 'Solo adventure, interested in cycling'
    }
  ])

  const [selectedBooking, setSelectedBooking] = useState(null)
  const [statusFilter, setStatusFilter] = useState('all')

  const filteredBookings = statusFilter === 'all' 
    ? bookings 
    : bookings.filter(booking => booking.status === statusFilter)

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed': return 'bg-green-100 text-green-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'cancelled': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'confirmed': return 'fa-check-circle'
      case 'pending': return 'fa-clock'
      case 'cancelled': return 'fa-times-circle'
      default: return 'fa-question-circle'
    }
  }

  const totalRevenue = bookings
    .filter(b => b.status === 'confirmed')
    .reduce((sum, b) => sum + b.price, 0)

  const stats = [
    { label: 'Total Bookings', value: bookings.length, icon: 'fa-calendar-alt', color: 'blue' },
    { label: 'Confirmed', value: bookings.filter(b => b.status === 'confirmed').length, icon: 'fa-check-circle', color: 'green' },
    { label: 'Pending', value: bookings.filter(b => b.status === 'pending').length, icon: 'fa-clock', color: 'yellow' },
    { label: 'Revenue', value: `$${totalRevenue.toLocaleString()}`, icon: 'fa-dollar-sign', color: 'green' }
  ]

  return (
    <section className="py-16 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h2 className="text-4xl font-bold text-gray-800 mb-2">Admin Dashboard</h2>
          <p className="text-gray-600">Manage bookings and track your travel business</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <div key={index} className="bg-white p-6 rounded-xl shadow-md">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">{stat.label}</p>
                  <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
                </div>
                <div className={`p-3 rounded-full bg-${stat.color}-100`}>
                  <i className={`fas ${stat.icon} text-${stat.color}-600 text-xl`}></i>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Filters and Actions */}
        <div className="bg-white p-6 rounded-xl shadow-md mb-6">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-4">
              <h3 className="text-lg font-semibold text-gray-800">Bookings</h3>
              <select 
                value={statusFilter} 
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              >
                <option value="all">All Status</option>
                <option value="confirmed">Confirmed</option>
                <option value="pending">Pending</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div className="flex gap-2">
              <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors">
                <i className="fas fa-plus mr-2"></i>
                Add Booking
              </button>
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                <i className="fas fa-download mr-2"></i>
                Export
              </button>
            </div>
          </div>
        </div>

        {/* Bookings Table */}
        <div className="bg-white rounded-xl shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Customer</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Destination</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Date</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Guests</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Price</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Status</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {filteredBookings.map(booking => (
                  <tr key={booking.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <div>
                        <div className="font-medium text-gray-800">{booking.name}</div>
                        <div className="text-sm text-gray-500">{booking.email}</div>
                        <div className="text-sm text-gray-500">{booking.phone}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-700">{booking.destination}</td>
                    <td className="px-6 py-4 text-sm text-gray-700">
                      {new Date(booking.date).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric'
                      })}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-700">{booking.guests}</td>
                    <td className="px-6 py-4 text-sm font-medium text-gray-800">${booking.price}</td>
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
                      <button 
                        className="text-blue-600 hover:text-blue-800 mr-3 transition-colors"
                        title="Edit"
                      >
                        <i className="fas fa-edit"></i>
                      </button>
                      <button 
                        className="text-red-600 hover:text-red-800 transition-colors"
                        title="Delete"
                      >
                        <i className="fas fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

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
                      <p><span className="font-medium">Name:</span> {selectedBooking.name}</p>
                      <p><span className="font-medium">Email:</span> {selectedBooking.email}</p>
                      <p><span className="font-medium">Phone:</span> {selectedBooking.phone}</p>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-800 mb-2">Trip Details</h4>
                    <div className="space-y-2 text-sm">
                      <p><span className="font-medium">Destination:</span> {selectedBooking.destination}</p>
                      <p><span className="font-medium">Date:</span> {new Date(selectedBooking.date).toLocaleDateString()}</p>
                      <p><span className="font-medium">Guests:</span> {selectedBooking.guests}</p>
                      <p><span className="font-medium">Price:</span> ${selectedBooking.price}</p>
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

                <div className="flex gap-4 mt-8">
                  <button className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                    Confirm Booking
                  </button>
                  <button className="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                    Send Message
                  </button>
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
