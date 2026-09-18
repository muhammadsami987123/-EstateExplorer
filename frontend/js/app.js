import { getSessionId } from './api.js';

// Theme management
const theme = {
  init() {
    const saved = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    this.updateToggle(saved);
  },
  toggle() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    this.updateToggle(next);
  },
  updateToggle(themeName) {
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.innerHTML = themeName === 'dark' ? '☀️' : '🌙';
  }
};

// Price formatter
function formatPrice(amount, currency = 'PKR', short = false) {
  if (!amount && amount !== 0) return 'Price on Request';
  const n = parseFloat(amount);
  if (short) {
    if (n >= 1e9) return `${currency} ${(n/1e9).toFixed(1)}B`;
    if (n >= 1e7) return `${currency} ${(n/1e7).toFixed(1)}M`;
    if (n >= 1e5) return `${currency} ${(n/1e5).toFixed(1)}L`;
    if (n >= 1000) return `${currency} ${(n/1000).toFixed(0)}K`;
  }
  if (currency === 'PKR') {
    if (n >= 1e7) return `PKR ${(n/1e7).toFixed(2)}M`;
    if (n >= 1e5) return `PKR ${(n/1e5).toFixed(1)}L`;
  }
  return `${currency} ${n.toLocaleString()}`;
}

function formatArea(sqft) {
  if (!sqft) return '';
  return `${Number(sqft).toLocaleString()} sq ft`;
}

function capitalize(str) {
  return str ? str.charAt(0).toUpperCase() + str.slice(1) : '';
}

// Toast notifications
function showToast(message, type = 'info', duration = 3500) {
  const container = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${message}</span><button type="button" aria-label="Close" onclick="this.parentElement.remove()">×</button>`;
  container.appendChild(toast);
  setTimeout(() => {
    if (toast.parentElement) toast.remove();
  }, duration);
}

function createToastContainer() {
  const div = document.createElement('div');
  div.id = 'toast-container';
  div.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column;gap:8px;';
  document.body.appendChild(div);
  return div;
}

// Skeleton helpers
function showSkeletons(container, count = 6, type = 'card') {
  if (!container) return;
  container.innerHTML = Array(count).fill(`<div class="skeleton skeleton-${type}"></div>`).join('');
}

// Compare list management
const compareList = {
  get() { return JSON.parse(localStorage.getItem('compareList') || '[]'); },
  add(id) {
    const list = this.get();
    if (list.length >= 3) { showToast('Max 3 properties for comparison', 'warning'); return false; }
    if (!list.includes(id)) { 
      list.push(id); 
      localStorage.setItem('compareList', JSON.stringify(list)); 
      showToast('Added to comparison bar', 'success');
    }
    this.updateBar();
    return true;
  },
  remove(id) {
    const list = this.get().filter(i => i !== id);
    localStorage.setItem('compareList', JSON.stringify(list));
    this.updateBar();
    showToast('Removed from comparison', 'info');
  },
  clear() { 
    localStorage.removeItem('compareList'); 
    this.updateBar(); 
  },
  updateBar() {
    let bar = document.getElementById('compare-bar');
    const list = this.get();
    if (!bar && list.length > 0) {
      bar = document.createElement('div');
      bar.id = 'compare-bar';
      bar.className = 'compare-bar';
      bar.innerHTML = `
        <div style="font-weight:600;display:flex;align-items:center;gap:6px;">
          <span>⚖️ Comparison</span>
          <span class="badge badge-match compare-count">${list.length}</span>
        </div>
        <a href="compare.html" class="btn btn-sm btn-gold">Compare Now</a>
        <button type="button" class="btn btn-sm btn-ghost" id="clear-compare-btn">Clear</button>
      `;
      document.body.appendChild(bar);
      bar.querySelector('#clear-compare-btn')?.addEventListener('click', () => this.clear());
    }
    if (bar) {
      bar.style.display = list.length > 0 ? 'flex' : 'none';
      const count = bar.querySelector('.compare-count');
      if (count) count.textContent = list.length;
    }
  }
};

// Saved properties toggle
async function toggleSave(propertyId, btn) {
  const saved = JSON.parse(localStorage.getItem('savedIds') || '[]');
  if (saved.includes(propertyId)) {
    // Remove
    const savedItems = JSON.parse(localStorage.getItem('savedItems') || '[]');
    const item = savedItems.find(s => s.property_id === propertyId);
    if (item) {
      try { 
        const apiMod = await import('./api.js');
        await apiMod.default.saved.remove(item.id); 
      } catch (err) {
        console.warn('API remove failed, local update proceeding', err);
      }
    }
    const newSaved = saved.filter(id => id !== propertyId);
    localStorage.setItem('savedIds', JSON.stringify(newSaved));
    if (btn) {
      btn.classList.remove('saved');
      btn.innerHTML = '♡';
    }
    showToast('Removed from saved properties', 'info');
  } else {
    try {
      const apiMod = await import('./api.js');
      await apiMod.default.saved.add(propertyId);
    } catch (err) {
      console.warn('API add failed, saving locally', err);
    }
    saved.push(propertyId);
    localStorage.setItem('savedIds', JSON.stringify(saved));
    if (btn) {
      btn.classList.add('saved');
      btn.innerHTML = '❤️';
    }
    showToast('Property saved to wishlist! ❤️', 'success');
  }
}

// Fallback high-res luxury property photography (Unsplash)
const fallbackImages = [
  'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=800&q=80'
];

// Helper to render a property card element
function createPropertyCardHTML(property, index = 0) {
  const savedIds = JSON.parse(localStorage.getItem('savedIds') || '[]');
  const isSaved = savedIds.includes(property.id);
  const imgUrl = property.images && property.images.length > 0 
    ? property.images[0] 
    : fallbackImages[index % fallbackImages.length];

  const badgeType = property.listing_type === 'rent' ? 'badge-rent' : 'badge-sale';
  const typeText = property.listing_type === 'rent' ? 'For Rent' : 'For Sale';
  const matchBadge = property.match_score 
    ? `<span class="badge badge-match">${Math.round(property.match_score)}% Match</span>` 
    : '';

  const specs = [];
  if (property.bedrooms) specs.push(`<span>🛏️ ${property.bedrooms} Beds</span>`);
  if (property.bathrooms) specs.push(`<span>🛁 ${property.bathrooms} Baths</span>`);
  if (property.area_sqft) specs.push(`<span>📐 ${formatArea(property.area_sqft)}</span>`);

  return `
    <article class="property-card" data-id="${property.id}">
      <div class="property-card__image-wrap">
        <img src="${imgUrl}" alt="${property.title || 'Luxury Real Estate'}" class="property-card__image" loading="lazy">
        <div class="property-card__badges">
          <span class="badge ${badgeType}">${typeText}</span>
          ${matchBadge}
        </div>
        <button type="button" class="property-card__save ${isSaved ? 'saved' : ''}" data-id="${property.id}" aria-label="Save Property">
          ${isSaved ? '❤️' : '♡'}
        </button>
      </div>
      <div class="property-card__body">
        <div class="property-card__price-row">
          <div class="property-card__price">
            ${formatPrice(property.price, property.currency || 'PKR')}
            ${property.listing_type === 'rent' ? '<span class="property-card__period">/mo</span>' : ''}
          </div>
          <span class="tag" style="font-size:0.75rem;">${capitalize(property.property_type || 'Property')}</span>
        </div>
        <h3 class="property-card__title">
          <a href="property.html?id=${property.id}">${property.title || 'Exclusive Residence'}</a>
        </h3>
        <div class="property-card__location">
          📍 ${property.area || ''}${property.city ? ', ' + property.city : ''}${property.country ? ', ' + property.country : ''}
        </div>
        <div class="property-card__specs">
          ${specs.join('') || '<span>Prime Real Estate Asset</span>'}
        </div>
        <div class="property-card__actions">
          <a href="property.html?id=${property.id}" class="btn btn-sm btn-primary" style="flex:1;">View Details</a>
          <button type="button" class="btn btn-sm btn-secondary compare-toggle-btn" data-id="${property.id}" title="Add to Compare">⚖️</button>
        </div>
      </div>
    </article>
  `;
}

// Attach event listeners for card actions (save, compare)
function attachCardEventListeners(container) {
  if (!container) return;
  
  container.querySelectorAll('.property-card__save').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = btn.dataset.id;
      toggleSave(id, btn);
    });
  });

  container.querySelectorAll('.compare-toggle-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = btn.dataset.id;
      compareList.add(id);
    });
  });
}

// Lazy image loading
function initLazyImages() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const img = e.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
        }
        observer.unobserve(img);
      }
    });
  }, { rootMargin: '200px' });
  document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
}

// Mobile nav toggle
function initMobileNav() {
  const toggle = document.querySelector('.nav-mobile-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => links.classList.toggle('nav-links--open'));
  }
}

// Global initialization
document.addEventListener('DOMContentLoaded', () => {
  theme.init();
  initMobileNav();
  initLazyImages();
  document.querySelector('.theme-toggle')?.addEventListener('click', () => theme.toggle());
  compareList.updateBar();
});

export {
  formatPrice,
  formatArea,
  capitalize,
  showToast,
  showSkeletons,
  compareList,
  toggleSave,
  getSessionId,
  theme,
  createPropertyCardHTML,
  attachCardEventListeners,
  fallbackImages
};
