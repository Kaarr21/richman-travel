// richman-travel-frontend/src/components/BookingSection.jsx - Improved version
import React, { useState } from 'react';
import { apiClient } from '../utils/api';

export default function BookingSection() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    destination: '',
    date: '',
    guests: 1,
    message: ''
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [fieldErrors, setFieldErrors] = useState({});

  const destinations = [
    { value: 'maasai-mara-safari', label: 'Maasai Mara Safari' },
    { value: 'mount-kenya-expedition', label: 'Mount Kenya Expedition' },
    { value: 'diani-beach-coastal', label: 'Diani Beach' },
    { value: 'hells-gate-national-park', label: "Hell's Gate National Park" },
    { value: 'amboseli-national-park', label: 'Amboseli National Park' },
    { value: 'lake-nakuru', label: 'Lake Nakuru' }
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear field error when user starts typing
    if (fieldErrors[name]) {
      setFieldErrors(prev => ({ ...prev, [name]: '' }));
    }
    
    // Clear general message when user modifies form
    if (message.text) {
      setMessage({ type: '', text: '' });
    }
  };

  const validateForm = () => {
    const errors = {};
    
    if (!formData.name.trim() || formData.name.trim().length < 2) {
      errors.name = 'Name must be at least 2 characters long';
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!emailRegex.test(formData.email.trim())) {
      errors.email = 'Please enter a valid email address';
    }
    
    if (formData.phone.trim()) {
      const phoneDigits = formData.phone.replace(/\D/g, '');
      if (phoneDigits.length < 7 || phoneDigits.length > 15) {
        errors.phone = 'Phone number should be 7-15 digits';
      }
    }
    
    if (formData.date) {
      const selectedDate = new Date(formData.date);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      if (selectedDate < today) {
        errors.date = 'Please select a future date';
      }
    }
    
    const guests = parseInt(formData.guests);
    if (isNaN(guests) || guests < 1) {
      errors.guests = 'Number of guests must be at least 1';
    } else if (guests > 50) {
      errors.guests = 'Maximum 50 guests allowed';
    }
    
    if (formData.message.length > 1000) {
      errors.message = 'Message cannot exceed 1000 characters';
    }
    
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage({ type: '', text: '' });
    setFieldErrors({});

    // Client-side validation
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      setIsSubmitting(false);
      setMessage({
        type: 'error',
        text: 'Please fix the errors below and try again.'
      });
      return;
    }

    try {
      // Clean the data before sending
      const cleanData = {
        name: formData.name.trim(),
        email: formData.email.trim().toLowerCase(),
        phone: formData.phone.trim(),
        destination: formData.destination,
        date: formData.date || null,
        guests: parseInt(formData.guests) || 1,
        message: formData.message.trim()
      };

      console.log('Submitting booking data:', cleanData);
      
      const response = await apiClient.createBooking(cleanData);
      
      setMessage({
        type: 'success',
        text: `Booking request submitted successfully! Your reference: ${response.data.booking_reference}. We'll contact you within 24 hours.`
      });
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        destination: '',
        date: '',
        guests: 1,
        message: ''
      });
      
      // Scroll to success message
      setTimeout(() => {
        document.querySelector('.success-message')?.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'center' 
        });
      }, 100);
      
    } catch (error) {
      console.error('Booking submission error:', error);
      
      // Handle validation errors from server
      if (error.message.includes('Validation failed') && error.errors) {
        const serverErrors = {};
        error.errors.forEach(err => {
          if (err.includes('Name')) serverErrors.name = err;
          if (err.includes('Email') || err.includes('email')) serverErrors.email = err;
          if (err.includes('phone') || err.includes('Phone')) serverErrors.phone = err;
          if (err.includes('date') || err.includes('Date')) serverErrors.date = err;
          if (err.includes('guests') || err.includes('Guests')) serverErrors.guests = err;
          if (err.includes('message') || err.includes('Message')) serverErrors.message = err;
        });
        
        setFieldErrors(serverErrors);
        setMessage({
          type: 'error',
          text: 'Please check the form and fix any errors.'
        });
      } else {
        setMessage({
          type: 'error',
          text: error.message || 'Failed to submit booking. Please check your connection and try again.'
        });
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Get today's date for min attribute
  const today = new Date().toISOString().split('T')[0];

  return (
    <section className="py-16 bg-white">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Book Your Adventure</h2>
          <p className="text-lg text-gray-600">
            Ready to explore Kenya? Fill out the form below and we'll create a personalized experience just for you.
          </p>
        </div>

        {/* Success/Error Message */}
        {message.text && (
          <div className={`mb-6 p-4 rounded-lg border ${
            message.type === 'success' 
              ? 'bg-green-50 border-green-200 text-green-800 success-message'
              : 'bg-red-50 border-red-200 text-red-800'
          }`}>
            <div className="flex items-start">
              <i className={`fas ${message.type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle'} mt-0.5 mr-3`}></i>
              <div className="flex-1">
                {message.text}
              </div>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6 bg-gray-50 rounded-xl p-8 shadow-lg">
          {/* Personal Information */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Personal Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Enter your full name"
                  disabled={isSubmitting}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:opacity-50 disabled:cursor-not-allowed ${
                    fieldErrors.name ? 'border-red-500 bg-red-50' : 'border-gray-300'
                  }`}
                />
                {fieldErrors.name && (
                  <p className="mt-1 text-sm text-red-600 flex items-center">
                    <i className="fas fa-exclamation-circle mr-1"></i>
                    {fieldErrors.name}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address <span className="text-red-500">*</span>
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="your.email@example.com"
                  disabled={isSubmitting}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:opacity-50 disabled:cursor-not-allowed ${
                    fieldErrors.email ? 'border-red-500 bg-red-50' : 'border-gray-300'
                  }`}
                />
                {fieldErrors.email && (
                  <p className="mt-1 text-sm text-red-600 flex items-center">
                    <i className="fas fa-exclamation-circle mr-1"></i>
                    {fieldErrors.email}
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Trip Details */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Trip Details</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  placeholder="+254 700 123 456"
                  disabled={isSubmitting}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:opacity-50 disabled:cursor-not-allowed ${
                    fieldErrors.phone ? 'border-red-500 bg-red-50' : 'border-gray-300'
                  }`}
                />
                {fieldErrors.phone && (
                  <p className="mt-1 text-sm text-red-600 flex items-center">
                    <i className="fas fa-exclamation-circle mr-1"></i>
                    {fieldErrors.phone}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Preferred Destination
                </label>
                <select
                  name="destination"
                  value={formData.destination}
                  onChange={handleChange}
                  disabled={isSubmitting}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:opacity-50 disabled:cursor-not-allowed ${
                    fieldErrors.destination ? 'border-red-500 bg-red-50' : 'border-gray-300'
                  }`}
                >
                  <option value="">Select a destination</option>
                  {destinations.map(dest => (
                    <option key={dest.value} value={dest.value}>
                      {dest.label}
                    </option>
                  ))}
                </select>
                {fieldErrors.destination && (
                  <p className="mt-1 text-sm text-red-600 flex items-center">
                    <i className="fas fa-exclamation-circle mr-1"></i>
                    {fieldErrors.destination}
                  </p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Preferred Date
                </label>
                <input
                  type="date"
                  name="date"
                  value={formData.date}
                  onChange={handleChange}
                  min={today}
                  disabled={isSubmitting}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:opacity-50 disabled:cursor-not-allowed ${
                    fieldErrors.date ? 'border-red-500 bg-red-50' : 'border-gray-300'
                  }`}
                />
                {fieldErrors.date && (
                  <p className="mt-1 text-sm text-red-600 flex items-center">
                    <i className="fas fa-exclamation-circle mr-1"></i>
                    {fieldErrors.date}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Number of Guests <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  name="guests"
                  value={formData.guests}
                  onChange={handleChange}
                  min="1"
                  max="50"
                  disabled={isSubmitting}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:opacity-50 disabled:cursor-not-allowed ${
                    fieldErrors.guests ? 'border-red-500 bg-red-50' : 'border-gray-300'
                  }`}
                />
                {fieldErrors.guests && (
                  <p className="mt-1 text-sm text-red-600 flex items-center">
                    <i className="fas fa-exclamation-circle mr-1"></i>
                    {fieldErrors.guests}
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Additional Information */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Additional Message
            </label>
            <textarea
              name="message"
              value={formData.message}
              onChange={handleChange}
              rows="4"
              placeholder="Tell us about your interests, special requirements, or any questions you have..."
              disabled={isSubmitting}
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 resize-vertical disabled:opacity-50 disabled:cursor-not-allowed ${
                fieldErrors.message ? 'border-red-500 bg-red-50' : 'border-gray-300'
              }`}
              maxLength="1000"
            />
            <div className="flex justify-between mt-1">
              {fieldErrors.message ? (
                <p className="text-sm text-red-600 flex items-center">
                  <i className="fas fa-exclamation-circle mr-1"></i>
                  {fieldErrors.message}
                </p>
              ) : (
                <span></span>
              )}
              <span className="text-sm text-gray-500">
                {formData.message.length}/1000
              </span>
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-6">
            <button
              type="submit"
              disabled={isSubmitting}
              className={`w-full py-4 px-8 rounded-lg font-semibold text-lg transition-all duration-300 ${
                isSubmitting
                  ? 'bg-gray-400 cursor-not-allowed text-white'
                  : 'bg-green-600 hover:bg-green-700 active:bg-green-800 text-white transform hover:scale-105 shadow-lg hover:shadow-xl'
              }`}
            >
              {isSubmitting ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Submitting Your Request...
                </span>
              ) : (
                <span className="flex items-center justify-center">
                  <i className="fas fa-paper-plane mr-2"></i>
                  Submit Booking Request
                </span>
              )}
            </button>
            
            <p className="text-sm text-gray-600 text-center mt-4">
              <i className="fas fa-info-circle mr-1"></i>
              We'll review your request and contact you within 24 hours with a detailed itinerary and pricing.
            </p>
          </div>
        </form>

        {/* Contact Info */}
        <div className="mt-12 bg-green-50 rounded-xl p-6 text-center">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Need Help?</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center justify-center">
              <i className="fas fa-phone text-green-600 mr-2"></i>
              <span className="text-gray-700">+254 700 123 456</span>
            </div>
            <div className="flex items-center justify-center">
              <i className="fas fa-envelope text-green-600 mr-2"></i>
              <span className="text-gray-700">richard@richmantravel.co.ke</span>
            </div>
            <div className="flex items-center justify-center">
              <i className="fas fa-clock text-green-600 mr-2"></i>
              <span className="text-gray-700">Mon-Fri 8AM-6PM</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
