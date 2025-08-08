import React from 'react'

export default function AboutSection() {
  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">About Us</h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Richman Travel & Tours is your gateway to unforgettable experiences in Kenya.
            Led by Richard, a passionate local guide, we curate personalized adventures that
            showcase the beauty, culture, and wildlife of our incredible country.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-xl shadow-md text-center">
            <i className="fas fa-map-marked-alt text-green-600 text-3xl mb-4"></i>
            <h3 className="text-xl font-semibold mb-2">Local Expertise</h3>
            <p className="text-gray-600">Our deep knowledge of Kenya ensures you see the hidden gems alongside the famous sights.</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-md text-center">
            <i className="fas fa-users text-green-600 text-3xl mb-4"></i>
            <h3 className="text-xl font-semibold mb-2">Personalized Tours</h3>
            <p className="text-gray-600">We tailor each trip to match your interests, pace, and budget for a truly unique adventure.</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-md text-center">
            <i className="fas fa-globe-africa text-green-600 text-3xl mb-4"></i>
            <h3 className="text-xl font-semibold mb-2">Sustainable Travel</h3>
            <p className="text-gray-600">We support local communities and conservation efforts to keep Kenya’s treasures thriving.</p>
          </div>
        </div>
      </div>
    </section>
  )
}
