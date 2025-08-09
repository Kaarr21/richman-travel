import React, { useState } from 'react'
import Navigation from './components/Navigation'
import HeroSection from './components/HeroSection'
import DestinationsSection from "./components/DestinationsSection"
import BookingSection from './components/BookingSection'
import AboutSection from './components/AboutSection'
import AdminDashboard from './components/AdminDashboard'
import Footer from './components/Footer'
import './App.css'

export default function App() {
  const [currentView, setCurrentView] = useState('home')
  const [isAdmin, setIsAdmin] = useState(false)

  const renderContent = () => {
    if (isAdmin) {
      return <AdminDashboard />
    }

    switch (currentView) {
      case 'home':
        return (
          <>
            <HeroSection setCurrentView={setCurrentView} />
            <DestinationsSection />
            <AboutSection />
          </>
        )
      case 'destinations':
        return <DestinationsSection />
      case 'booking':
        return <BookingSection />
      case 'about':
        return <AboutSection />
      default:
        return (
          <>
            <HeroSection setCurrentView={setCurrentView} />
            <DestinationsSection />
            <AboutSection />
          </>
        )
    }
  }

  return (
    <div className="min-h-screen bg-white">
      <Navigation 
        currentView={currentView} 
        setCurrentView={setCurrentView} 
        isAdmin={isAdmin} 
        setIsAdmin={setIsAdmin} 
      />
      <main>
        {renderContent()}
      </main>
      <Footer />
    </div>
  )
}
