import React, { useState } from 'react'
import Navigation from './components/Navigation'
import HeroSection from './components/HeroSection'
import DestinationsSection from "./components/DestinationsSection";
import BookingSection from './components/BookingSection'
import AboutSection from './components/AboutSection'
import AdminDashboard from './components/AdminDashboard'
import Footer from './components/Footer'

export default function App() {
  const [currentView, setCurrentView] = useState('home')
  const [isAdmin, setIsAdmin] = useState(false)

  return (
    <div className="min-h-screen">
      <Navigation currentView={currentView} setCurrentView={setCurrentView} isAdmin={isAdmin} setIsAdmin={setIsAdmin} />
      {isAdmin ? (
        <AdminDashboard />
      ) : (
        <>
          {currentView === 'home' && <>
            <HeroSection setCurrentView={setCurrentView} />
            <DestinationsSection />
            <AboutSection />
          </>}
          {currentView === 'destinations' && <DestinationsSection />}
          {currentView === 'booking' && <BookingSection />}
          {currentView === 'about' && <AboutSection />}
        </>
      )}
      <Footer />
    </div>
  )
}
