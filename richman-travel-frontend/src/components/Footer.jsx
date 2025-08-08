import React from 'react'

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-8">
      <div className="max-w-6xl mx-auto px-4 text-center">
        <p className="mb-4">&copy; {new Date().getFullYear()} Richman Travel & Tours. All rights reserved.</p>
        <div className="flex justify-center space-x-4">
          <a href="#" className="hover:text-green-400"><i className="fab fa-facebook-f"></i></a>
          <a href="#" className="hover:text-green-400"><i className="fab fa-instagram"></i></a>
          <a href="#" className="hover:text-green-400"><i className="fab fa-twitter"></i></a>
        </div>
      </div>
    </footer>
  )
}
