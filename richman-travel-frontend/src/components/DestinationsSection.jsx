// richman-travel-frontend/src/components/DestinationsSection.jsx - Updated
import React, { useState, useEffect } from 'react';
import { apiClient } from '../utils/api';

export default function DestinationsSection() {
  const [destinations, setDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDestinations();
  }, []);

  const fetchDestinations = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getDestinations();
      setDestinations(response.data || []);
    } catch (error) {
      console.error('Error fetching destinations:', error);
      setError('Failed to load destinations. Please try again.');
      // Fallback to mock data
      setDestinations([
        { id: 1, name: "Maasai Mara Safari", image_url: "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=400", description: "Experience the Great Migration...", duration: "3 days", highlights: ["Big Five", "Great Migration", "Maasai Culture"] },
        { id: 2, name: "Mount Kenya Expedition", image_url: "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400", description: "Conquer Africa's second-highest peak...", duration: "5 days", highlights: ["Mountain Climbing", "Alpine Lakes", "Rare Wildlife"] }
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading destinations...</p>
        </div>
      </section>
    );
  }

  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Popular Destinations</h2>
          <p className="text-gray-600 text-lg">Explore Kenya's diverse landscapes and rich culture</p>
          {error && (
            <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mt-4">
              {error}
            </div>
          )}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {destinations.map(dest => (
            <div key={dest.id} className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow overflow-hidden">
              <img src={dest.image_url} alt={dest.name} className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="text-xl font-semibold mb-2">{dest.name}</h3>
                <p className="text-gray-600 text-sm mb-3">{dest.description}</p>
                <span className="text-green-600 font-medium">
                  <i className="fas fa-clock mr-1"></i>{dest.duration}
                </span>
                <div className="flex flex-wrap gap-1 mt-2">
                  {(dest.highlights || []).map((h, i) => (
                    <span key={i} className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">
                      {h}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
