// richman-travel-frontend/src/utils/api.js - Improved error handling
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
      console.log(`Making ${config.method || 'GET'} request to ${url}`, config.body);
      
      const response = await fetch(url, config);
      const data = await response.json();
      
      console.log(`Response from ${url}:`, { status: response.status, data });
      
      if (!response.ok) {
        // Create a more detailed error object
        const error = new Error(data.message || `HTTP error! status: ${response.status}`);
        error.status = response.status;
        error.errors = data.errors || [];
        error.response = data;
        throw error;
      }
      
      return data;
    } catch (error) {
      console.error('API request failed:', error);
      
      // If it's a network error, provide a more user-friendly message
      if (error instanceof TypeError && error.message.includes('fetch')) {
        const networkError = new Error('Unable to connect to the server. Please check your internet connection.');
        networkError.isNetworkError = true;
        throw networkError;
      }
      
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
    // Validate required fields on client side
    const requiredFields = ['name', 'email'];
    const missingFields = requiredFields.filter(field => !bookingData[field]?.trim());
    
    if (missingFields.length > 0) {
      const error = new Error('Missing required fields');
      error.errors = missingFields.map(field => `${field} is required`);
      throw error;
    }

    // Clean the data before sending
    const cleanData = {
      name: bookingData.name?.trim() || '',
      email: bookingData.email?.trim().toLowerCase() || '',
      phone: bookingData.phone?.trim() || '',
      destination: bookingData.destination || '',
      date: bookingData.date || '',
      guests: parseInt(bookingData.guests) || 1,
      message: bookingData.message?.trim() || ''
    };

    return this.request('/bookings', {
      method: 'POST',
      body: cleanData,
    });
  }

  async sendContactMessage(messageData) {
    // Clean the data before sending
    const cleanData = {
      name: messageData.name?.trim() || '',
      email: messageData.email?.trim().toLowerCase() || '',
      subject: messageData.subject?.trim() || '',
      message: messageData.message?.trim() || ''
    };

    return this.request('/contact', {
      method: 'POST',
      body: cleanData,
    });
  }

  async checkHealth() {
    return this.request('/health');
  }

  // Admin endpoints (require authentication)
  async adminLogin(credentials) {
    const cleanData = {
      username: credentials.username?.trim() || '',
      password: credentials.password || ''
    };

    return this.request('/auth/login', {
      method: 'POST',
      body: cleanData,
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

  // Test connection method
  async testConnection() {
    try {
      const response = await this.checkHealth();
      return response.status === 'healthy';
    } catch (error) {
      console.error('Connection test failed:', error);
      return false;
    }
  }
}

export const apiClient = new ApiClient();
