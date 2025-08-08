import React from 'react'

export default function DestinationsSection() {
  const mockDestinations = [
    { id:1, name:"Maasai Mara Safari", image:"https://images.unsplash.com/photo-1516426122078-c23e76319801?w=400", description:"Experience the Great Migration...", duration:"3 days", highlights:["Big Five","Great Migration","Maasai Culture"] },
    { id:2, name:"Mount Kenya Expedition", image:"https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400", description:"Conquer Africa's second-highest peak...", duration:"5 days", highlights:["Mountain Climbing","Alpine Lakes","Rare Wildlife"] },
    { id:3, name:"Coastal Paradise - Diani Beach", image:"https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400", description:"Relax on pristine white sand beaches...", duration:"2 days", highlights:["White Sand Beaches","Water Sports","Coral Reefs"] },
    { id:4, name:"Hell's Gate National Park", image:"https://images.unsplash.com/photo-1571771019784-3ff35f4f4277?w=400", description:"Cycle through dramatic landscapes...", duration:"1 day", highlights:["Cycling Safari","Rock Climbing","Geothermal Springs"] }
  ]

  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Popular Destinations</h2>
          <p className="text-gray-600 text-lg">Explore Kenya's diverse landscapes and rich culture</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {mockDestinations.map(dest => (
            <div key={dest.id} className="bg-white rounded-xl shadow-lg card-hover overflow-hidden">
              <img src={dest.image} alt={dest.name} className="w-full h-48 object-cover" />
              <div className="p-6">
                <h3 className="text-xl font-semibold mb-2">{dest.name}</h3>
                <p className="text-gray-600 text-sm mb-3">{dest.description}</p>
                <span className="text-green-600 font-medium"><i className="fas fa-clock mr-1"></i>{dest.duration}</span>
                <div className="flex flex-wrap gap-1 mt-2">
                  {dest.highlights.map((h,i) => <span key={i} className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">{h}</span>)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
