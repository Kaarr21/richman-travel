// richman-travel-frontend/src/components/BookingSection.jsx - Updated
import React, { useState } from 'react';
import { apiClient } from '../utils/api';

export default function BookingSection() {
  const [formData, setFormData] = useState({
    name: '', email: '', phone: '', destination: '', date: '', guests: 1, message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const handleChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage({ type: '', text: '' });

    try {
      const response = await apiClient.createBooking(formData);
      setMessage({
        type: 'success',
        text: `Booking request submitted successfully! Your reference: ${response.data.booking_reference}`
      });
      setFormData({ name: '', email: '', phone: '', destination: '', date: '', guests: 1, message: '' });
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.message || 'Failed to submit booking. Please try again.'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="py-16 bg-white">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Book Your Adventure</h2>
        </div>

        {message.text && (
          <div className={`mb-6 p-4 rounded-lg ${
            message.type === 'success' 
              ? 'bg-green-100 border border-green-400 text-green-700'
              : 'bg-red-100 border border-red-400 text-red-700'
          }`}>
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6 bg-gray-50 rounded-xl p-8 shadow-lg">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Full Name"
              required
              disabled={isSubmitting}
              className="px-4 py-3 border rounded-lg disabled:opacity-50"
            />
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Email"
              required
              disabled={isSubmitting}
              className="px-4 py-3 border rounded-lg disabled:opacity-50"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="Phone"
              disabled={isSubmitting}
              className="px-4 py-3 border rounded-lg disabled:opacity-50"
            />
            <select
              name="destination"
              value={formData.destination}
              onChange={handleChange}
              disabled={isSubmitting}
              className="px-4 py-3 border rounded-lg disabled:opacity-50"
            >
              <option value="">Select Destination</option>
              <option value="maasai-mara-safari">Maasai Mara Safari</option>
              <option value="mount-kenya-expedition">Mount Kenya Expedition</option>
              <option value="diani-beach-coastal">Diani Beach</option>
              <option value="hells-gate-national-park">Hell's Gate</option>
            </select>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <input
              type="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              disabled={isSubmitting}
              className="px-4 py-3 border rounded-lg disabled:opacity-50"
            />
            <input
              type="number"
              name="guests"
              value={formData.guests}
              onChange={handleChange}
              min="1"
              max="20"
              disabled={isSubmitting}
              className="px-4 py-3 border rounded-lg disabled:opacity-50"
            />
          </div>

          <textarea
            name="message"
            value={formData.message}
            onChange={handleChange}
            rows="4"
            placeholder="Additional message..."
            disabled={isSubmitting}
            className="px-4 py-3 border rounded-lg w-full disabled:opacity-50"
          ></textarea>

          <button
            type="submit"
            disabled={isSubmitting}
            className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-8 py-4 rounded-lg transition-colors"
          >
            {isSubmitting ? 'Submitting...' : 'Submit Booking Request'}
          </button>
        </form>
      </div>
    </section>
  );
}
