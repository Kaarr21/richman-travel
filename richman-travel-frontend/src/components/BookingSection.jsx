import React, { useState } from 'react'

export default function BookingSection() {
  const [formData, setFormData] = useState({ name:'', email:'', phone:'', destination:'', date:'', guests:1, message:'' })

  const handleChange = e => setFormData({ ...formData, [e.target.name]: e.target.value })
  const handleSubmit = e => {
    e.preventDefault()
    alert('Booking request submitted!')
    setFormData({ name:'', email:'', phone:'', destination:'', date:'', guests:1, message:'' })
  }

  return (
    <section className="py-16 bg-white">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Book Your Adventure</h2>
        </div>
        <form onSubmit={handleSubmit} className="space-y-6 bg-gray-50 rounded-xl p-8 shadow-lg">
          {/* Name & Email */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <input type="text" name="name" value={formData.name} onChange={handleChange} placeholder="Full Name" required className="px-4 py-3 border rounded-lg" />
            <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Email" required className="px-4 py-3 border rounded-lg" />
          </div>
          {/* Phone & Destination */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <input type="tel" name="phone" value={formData.phone} onChange={handleChange} placeholder="Phone" className="px-4 py-3 border rounded-lg" />
            <select name="destination" value={formData.destination} onChange={handleChange} className="px-4 py-3 border rounded-lg">
              <option value="">Select Destination</option>
              <option value="maasai-mara">Maasai Mara Safari</option>
              <option value="mount-kenya">Mount Kenya Expedition</option>
              <option value="diani-beach">Diani Beach</option>
              <option value="hells-gate">Hell's Gate</option>
            </select>
          </div>
          {/* Date & Guests */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <input type="date" name="date" value={formData.date} onChange={handleChange} className="px-4 py-3 border rounded-lg" />
            <input type="number" name="guests" value={formData.guests} onChange={handleChange} min="1" max="20" className="px-4 py-3 border rounded-lg" />
          </div>
          {/* Message */}
          <textarea name="message" value={formData.message} onChange={handleChange} rows="4" placeholder="Additional message..." className="px-4 py-3 border rounded-lg w-full"></textarea>
          <button type="submit" className="bg-green-600 hover:bg-green-700 text-white px-8 py-4 rounded-lg">Submit Booking Request</button>
        </form>
      </div>
    </section>
  )
}
