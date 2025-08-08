import React from 'react'

export default function HeroSection({ setCurrentView }) {
  return (
    <section className="hero-bg min-h-screen flex items-center relative" style={{
      background: `linear-gradient(135deg, rgba(34, 197, 94, 0.9), rgba(16, 185, 129, 0.8)), url('https://images.unsplash.com/photo-1516426122078-c23e76319801?w=400')`,
      backgroundSize: 'cover', backgroundPosition: 'center'
    }}>
      <div className="absolute inset-0 bg-black opacity-20"></div>
      <div className="max-w-7xl mx-auto px-4 relative z-10 text-center text-white">
        <h1 className="text-6xl font-bold mb-6">Discover Kenya <span className="block text-4xl mt-2 text-green-300">with a Local Expert</span></h1>
        <p className="text-xl mb-8 max-w-3xl mx-auto">Join Richard on an unforgettable journey through Kenya's most spectacular landscapes...</p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button onClick={() => setCurrentView('booking')} className="bg-green-600 hover:bg-green-700 text-white px-8 py-4 rounded-lg">Book Your Adventure</button>
          <button onClick={() => setCurrentView('destinations')} className="border-2 border-white text-white hover:bg-white hover:text-green-600 px-8 py-4 rounded-lg">Explore Destinations</button>
        </div>
      </div>
    </section>
  )
}
