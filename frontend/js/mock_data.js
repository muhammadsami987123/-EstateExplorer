// High quality fallback dataset matching backend schemas
export const mockProperties = [
  {
    id: "prop-001",
    title: "Ultra-Modern Luxury Villa with Infinity Pool",
    description: "Architectural masterpiece in DHA Phase 8 featuring 6 en-suite bedrooms, imported Italian marble, high-tech smart home automation, private infinity pool, and lush landscaped garden.",
    property_type: "villa",
    listing_type: "sale",
    price: 185000000,
    currency: "PKR",
    bedrooms: 6,
    bathrooms: 7,
    area_sqft: 9000,
    parking_spaces: 4,
    furnished: "furnished",
    country: "Pakistan",
    city: "Karachi",
    area: "DHA Phase 8",
    address: "Street 14, Zone B, DHA Phase 8",
    latitude: 24.783,
    longitude: 67.065,
    features: ["Swimming Pool", "Smart Home Automation", "Private Garden", "Elevator", "Solar Power", "Servant Quarters", "Gated Security"],
    images: [
      "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=800&q=80"
    ],
    agent: {
      name: "Ahmed Raza",
      phone: "+92 300 1234567",
      email: "ahmed.raza@luxurypakistan.com"
    },
    created_at: "2024-09-01T10:00:00Z"
  },
  {
    id: "prop-002",
    title: "Panoramic Sea View Penthouse at Emaar Oceanfront",
    description: "Exclusive top-floor corner penthouse with 360-degree Arabian Sea views, wraparound balcony, floor-to-ceiling soundproof glass, and access to private residents' club.",
    property_type: "apartment",
    listing_type: "sale",
    price: 98000000,
    currency: "PKR",
    bedrooms: 4,
    bathrooms: 5,
    area_sqft: 4800,
    parking_spaces: 3,
    furnished: "semi-furnished",
    country: "Pakistan",
    city: "Karachi",
    area: "Clifton",
    address: "Emaar Coral Towers, Crescent Bay, Clifton",
    latitude: 24.795,
    longitude: 67.042,
    features: ["Sea View", "Concierge Service", "Gym & Spa", "Infinity Pool", "Private Elevators", "24/7 Surveillance"],
    images: [
      "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80"
    ],
    agent: {
      name: "Zainab Malik",
      phone: "+92 321 9876543",
      email: "zainab@emaarpartners.pk"
    },
    created_at: "2024-09-05T14:30:00Z"
  },
  {
    id: "prop-003",
    title: "Classic Colonial Style Bungalow in Gulberg III",
    description: "Prestigious 2-kanal residence in prime Gulberg III featuring double-height ceiling foyer, heritage woodwork, expansive lawn with century-old trees, and generator backup.",
    property_type: "house",
    listing_type: "sale",
    price: 145000000,
    currency: "PKR",
    bedrooms: 5,
    bathrooms: 6,
    area_sqft: 7500,
    parking_spaces: 5,
    furnished: "unfurnished",
    country: "Pakistan",
    city: "Lahore",
    area: "Gulberg III",
    address: "Block H, Gulberg III, Main Boulevard",
    latitude: 31.512,
    longitude: 74.345,
    features: ["Expansive Lawn", "Backup Generator", "High Ceilings", "Wine Cellar / Store", "Guard Room", "Prime Commercial Potential"],
    images: [
      "https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1600573472591-ee6c563aaec9?auto=format&fit=crop&w=800&q=80"
    ],
    agent: {
      name: "Tariq Mahmood",
      phone: "+92 333 4455667",
      email: "tariq@lahorerealtors.com"
    },
    created_at: "2024-09-08T09:15:00Z"
  },
  {
    id: "prop-004",
    title: "Executive Modern Mansion overlooking Margalla Hills",
    description: "Nestled directly beneath Margalla Hills in Sector F-6/2. Custom German fixtures, private movie theatre, rooftop barbecue terrace, and diplomat-grade security perimeter.",
    property_type: "house",
    listing_type: "sale",
    price: 260000000,
    currency: "PKR",
    bedrooms: 6,
    bathrooms: 8,
    area_sqft: 11000,
    parking_spaces: 6,
    furnished: "furnished",
    country: "Pakistan",
    city: "Islamabad",
    area: "Sector F-6",
    address: "Street 28, Sector F-6/2",
    latitude: 33.729,
    longitude: 73.075,
    features: ["Margalla View", "Home Cinema", "Rooftop Terrace", "CCTV & Security", "Solar Array", "Wine & Cigar Lounge"],
    images: [
      "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=800&q=80"
    ],
    agent: {
      name: "Bilal Farooq",
      phone: "+92 345 5566778",
      email: "bilal@islamabadestates.com"
    },
    created_at: "2024-09-10T11:20:00Z"
  },
  {
    id: "prop-005",
    title: "High-Floor Luxury Apartment in Downtown Dubai",
    description: "Stunning Burj Khalifa and Dubai Fountain views. Designer Scandinavian furnishings, 5-star hotel concierge, valeting, and private sky lounge access.",
    property_type: "apartment",
    listing_type: "rent",
    price: 280000,
    currency: "AED",
    bedrooms: 2,
    bathrooms: 3,
    area_sqft: 1650,
    parking_spaces: 2,
    furnished: "furnished",
    country: "UAE",
    city: "Dubai",
    area: "Downtown Dubai",
    address: "The Address Residence Sky View, Downtown Dubai",
    latitude: 25.197,
    longitude: 55.274,
    features: ["Burj Khalifa View", "Hotel Amenities", "Valet Parking", "Gym & Pool", "Direct Mall Access", "24/7 Security"],
    images: [
      "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80"
    ],
    agent: {
      name: "Hamza Al-Maktoum",
      phone: "+971 50 123 4567",
      email: "hamza@dubaipremier.ae"
    },
    created_at: "2024-09-12T16:00:00Z"
  },
  {
    id: "prop-006",
    title: "Elegant Georgian Townhouse in Kensington",
    description: "Restored Grade II listed townhouse spanning 5 floors with manicured private mews garden, wine cellar, passenger lift, and bespoke kitchen by Smallbone of Devizes.",
    property_type: "house",
    listing_type: "sale",
    price: 4750000,
    currency: "GBP",
    bedrooms: 5,
    bathrooms: 5,
    area_sqft: 4200,
    parking_spaces: 2,
    furnished: "unfurnished",
    country: "UK",
    city: "London",
    area: "Kensington",
    address: "18 Holland Park Gardens, Kensington, London W14",
    latitude: 51.501,
    longitude: -0.207,
    features: ["Private Garden", "Grade II Listed", "Passenger Lift", "Wine Cellar", "Period Fireplaces", "Underfloor Heating"],
    images: [
      "https://images.unsplash.com/photo-1576941089067-2de3c901e126?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80"
    ],
    agent: {
      name: "Victoria Sterling",
      phone: "+44 20 7946 0912",
      email: "victoria@sterlinglondon.co.uk"
    },
    created_at: "2024-09-15T12:00:00Z"
  }
];

export const mockLocations = [
  { id: "loc-pk", name: "Pakistan", type: "country", count: 35 },
  { id: "loc-ae", name: "UAE", type: "country", count: 18 },
  { id: "loc-uk", name: "United Kingdom", type: "country", count: 12 },
  { id: "loc-khi", name: "Karachi", parent_id: "loc-pk", type: "city", count: 20, avg_price: "PKR 65M", trend: "+8.4%" },
  { id: "loc-lhr", name: "Lahore", parent_id: "loc-pk", type: "city", count: 10, avg_price: "PKR 55M", trend: "+6.8%" },
  { id: "loc-isb", name: "Islamabad", parent_id: "loc-pk", type: "city", count: 5, avg_price: "PKR 85M", trend: "+11.2%" },
  { id: "loc-dxb", name: "Dubai", parent_id: "loc-ae", type: "city", count: 18, avg_price: "AED 3.8M", trend: "+14.5%" },
  { id: "loc-ldn", name: "London", parent_id: "loc-uk", type: "city", count: 12, avg_price: "GBP 1.9M", trend: "+3.2%" }
];
