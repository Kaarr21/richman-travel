// richman-travel-frontend/src/utils/api.js
const API_BASE_URL = 'http://localhost:5000/api';

class ApiClient {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || `HTTP error! status: ${response.status}`);
      }
      
      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Public endpoints
  async getDestinations(featured = false) {
    const query = featured ? '?featured=true' : '';
    return this.request(`/destinations${query}`);
  }

  async getDestinationBySlug(slug) {
    return this.request(`/destinations/${slug}`);
  }

  async createBooking(bookingData) {
    return this.request('/bookings', {
      method: 'POST',
      body: bookingData,
    });
  }

  async sendContactMessage(messageData) {
    return this.request('/contact', {
      method: 'POST',
      body: messageData,
    });
  }

  async checkHealth() {
    return this.request('/health');
  }

  // Admin endpoints (require authentication)
  async adminLogin(credentials) {
    return this.request('/auth/login', {
      method: 'POST',
      body: credentials,
    });
  }

  async getAdminBookings(token, page = 1, status = '') {
    const query = new URLSearchParams({ page, per_page: 20 });
    if (status) query.append('status', status);
    
    return this.request(`/admin/bookings?${query}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
  }

  async updateBooking(token, bookingId, updateData) {
    return this.request(`/admin/bookings/${bookingId}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}` },
      body: updateData,
    });
  }

  async getDashboardStats(token) {
    return this.request('/admin/dashboard/stats', {
      headers: { Authorization: `Bearer ${token}` },
    });
  }
}

export const apiClient = new ApiClient();