import React, { useState } from 'react'

export default function AdminDashboard() {
  const [bookings] = useState([
    { id: 1, name: 'John Doe', destination: 'Maasai Mara Safari', date: '2025-08-15', guests: 2 },
    { id: 2, name: 'Jane Smith', destination: 'Mount Kenya Expedition', date: '2025-09-05', guests: 4 }
  ])

  return (
    <section className="py-16 bg-white">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-gray-800 mb-8">Admin Dashboard</h2>
        <div className="overflow-x-auto bg-gray-50 rounded-xl shadow-md">
          <table className="min-w-full border-collapse">
            <thead>
              <tr className="bg-green-600 text-white">
                <th className="p-3 text-left">Name</th>
                <th className="p-3 text-left">Destination</th>
                <th className="p-3 text-left">Date</th>
                <th className="p-3 text-left">Guests</th>
              </tr>
            </thead>
            <tbody>
              {bookings.map(b => (
                <tr key={b.id} className="border-b hover:bg-gray-100">
                  <td className="p-3">{b.name}</td>
                  <td className="p-3">{b.destination}</td>
                  <td className="p-3">{b.date}</td>
                  <td className="p-3">{b.guests}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  )
}
