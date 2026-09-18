const API_BASE = 'http://localhost:8000/api';

const api = {
  async request(method, endpoint, data = null, params = {}) {
    const url = new URL(API_BASE + endpoint);
    Object.entries(params).forEach(([k, v]) => v !== null && v !== undefined && url.searchParams.append(k, v));
    const opts = { method, headers: { 'Content-Type': 'application/json', 'X-Session-ID': getSessionId() } };
    if (data) opts.body = JSON.stringify(data);
    try {
      const res = await fetch(url.toString(), opts);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.error(`API Error [${method} ${endpoint}]:`, err);
      throw err;
    }
  },
  get: (endpoint, params) => api.request('GET', endpoint, null, params),
  post: (endpoint, data) => api.request('POST', endpoint, data),
  delete: (endpoint) => api.request('DELETE', endpoint),
  properties: {
    list: (filters = {}) => api.get('/properties', filters),
    get: (id) => api.get(`/properties/${id}`),
    featured: () => api.get('/properties/featured'),
  },
  locations: {
    all: () => api.get('/locations'),
    countries: () => api.get('/locations/countries'),
    children: (id) => api.get(`/locations/${id}/children`),
    search: (q) => api.get('/locations/search', { q }),
  },
  search: {
    run: (prefs) => api.post('/search', prefs),
    sessions: {
      list: () => api.get('/search/sessions'),
      save: (s) => api.post('/search/sessions', s),
      delete: (id) => api.delete(`/search/sessions/${id}`),
    },
  },
  recommendations: { get: (prefs) => api.post('/recommendations', prefs) },
  market: { all: () => api.get('/market'), get: (id) => api.get(`/market/${id}`) },
  saved: {
    list: () => api.get('/saved'),
    add: (propertyId) => api.post('/saved', { property_id: propertyId }),
    remove: (id) => api.delete(`/saved/${id}`),
  },
  collections: {
    list: () => api.get('/collections'),
    create: (data) => api.post('/collections', data),
    addProperty: (colId, propId) => api.post(`/collections/${colId}/properties`, { property_id: propId }),
  },
  reports: {
    generate: (prefs) => api.post('/reports/generate', prefs),
    get: (id) => api.get(`/reports/${id}`),
    downloadUrl: (id, format) => `${API_BASE}/reports/${id}/download?format=${format}`,
  },
  ai: {
    analyze: (d) => api.post('/ai/analyze', d),
    chat: (messages, context) => api.post('/ai/chat', { messages, context }),
    extract: (text) => api.post('/ai/extract', { text }),
    compare: (properties, prefs) => api.post('/ai/compare', { properties, preferences: prefs }),
    insight: (locationId) => api.post('/ai/insight', { location_id: locationId }),
  },
};

function getSessionId() {
  let id = localStorage.getItem('session_id');
  if (!id) { id = 'sess_' + Math.random().toString(36).substr(2, 9); localStorage.setItem('session_id', id); }
  return id;
}

export default api;
export { getSessionId, API_BASE };
