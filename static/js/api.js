/**
 * Tugon API Client
 * Handles all API calls to the Flask backend
 */

const API = {
  baseUrl: '',

  /**
   * Make a GET request to the API
   * @param {string} endpoint - API endpoint path
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} Response data
   */
  async get(endpoint, params = {}) {
    const url = new URL(`${this.baseUrl}${endpoint}`, window.location.origin);
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.append(key, value);
      }
    });

    try {
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`API fetch error for ${endpoint}:`, error);
      throw error;
    }
  },

  // Candidate endpoints
  async getCandidates(query = '', council = 'ALL') {
    return this.get('/api/candidates', { q: query, council });
  },

  async getCandidate(candidateId) {
    return this.get(`/api/candidate/${candidateId}`);
  },

  // Council endpoints
  async getCouncils() {
    return this.get('/api/councils');
  },

  async getCouncil(slug) {
    return this.get(`/api/council/${slug}`);
  },

  // Gallery endpoint
  async getGallery() {
    return this.get('/api/gallery');
  },

  // Home page data
  async getHomeData() {
    return this.get('/api/home');
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = API;
}
