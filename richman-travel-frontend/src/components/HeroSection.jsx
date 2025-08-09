import React from 'react'

export default function HeroSection({ setCurrentView }) {
  return (
    <section 
      className="relative min-h-screen flex items-center bg-cover bg-center"
      style={{
        backgroundImage: `linear-gradient(135deg, rgba(34, 197, 94, 0.8), rgba(16, 185, 129, 0.7)), url('https://images.unsplash.com/photo-1516426122078-c23e76319801?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80')`
      }}
    >
      {/* Overlay for better text readability */}
      <div className="absolute inset-0 bg-black opacity-20"></div>
      
      <div className="relative z-10 max-w-7xl mx-auto px-4 text-center text-white">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
            Discover Kenya{' '}
            <span className="block text-3xl sm:text-4xl lg:text-5xl mt-2 text-green-300">
              with a Local Expert
            </span>
          </h1>
          
          <p className="text-lg sm:text-xl mb-8 max-w-3xl mx-auto leading-relaxed">
            Join Richard on an unforgettable journey through Kenya's most spectacular landscapes, 
            from the iconic Maasai Mara to pristine coastal beaches. Experience authentic culture, 
            incredible wildlife, and memories that will last a lifetime.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button 
              onClick={() => setCurrentView('booking')} 
              className="w-full sm:w-auto bg-green-600 hover:bg-green-700 text-white font-semibold px-8 py-4 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              <i className="fas fa-calendar-alt mr-2"></i>
              Book Your Adventure
            </button>
            
            <button 
              onClick={() => setCurrentView('destinations')} 
              className="w-full sm:w-auto border-2 border-white text-white hover:bg-white hover:text-green-600 font-semibold px-8 py-4 rounded-lg transition-all duration-300 transform hover:scale-105"
            >
              <i className="fas fa-map-marked-alt mr-2"></i>
              Explore Destinations
            </button>
          </div>
          
          {/* Quick stats */}
          <div className="grid grid-cols-3 gap-8 mt-16 max-w-md mx-auto">
            <div className="text-center">
              <div className="text-2xl sm:text-3xl font-bold text-green-300">5+</div>
              <div className="text-sm text-green-100">Years Experience</div>
            </div>
            <div className="text-center">
              <div className="text-2xl sm:text-3xl font-bold text-green-300">500+</div>
              <div className="text-sm text-green-100">Happy Clients</div>
            </div>
            <div className="text-center">
              <div className="text-2xl sm:text-3xl font-bold text-green-300">10+</div>
              <div className="text-sm text-green-100">Destinations</div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 text-white animate-bounce">
        <i className="fas fa-chevron-down text-2xl"></i>
      </div>
    </section>
  )
}
