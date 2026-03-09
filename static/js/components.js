/**
 * Tugon UI Components
 * Reusable component rendering functions
 */

const Components = {
  /**
   * Get heart image filename based on council
   * @param {string} council - Council name (CASSC, CBASC, etc.)
   * @returns {string} Heart image filename
   */
  getHeartImage(council) {
    const heartMap = {
      'CASSC': 'heart-cas.png',
      'CBASC': 'heart-cba.png',
      'CFADSC': 'heart-cfad.png',
      'CSC': 'heart-csc.png',
      'COESC': 'heart-coesc.png'
    };
    return heartMap[council] || 'heart-cas.png';
  },

  /**
   * Escape HTML to prevent XSS
   * @param {string} str - String to escape
   * @returns {string} Escaped string
   */
  escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  },

  /**
   * Render a candidate card
   * @param {Object} candidate - Candidate data
   * @param {number} index - Index for animation delay
   * @returns {string} HTML string
   */
  candidateCard(candidate, index = 0) {
    const delay = Math.min(index + 1, 8);
    const photoUrl = `/static/${candidate.photo || 'images/default-candidate.svg'}`;
    
    return `
      <div class="col-md-6 col-xl-3 reveal-up delay-${delay}">
        <article class="candidate-card candidate-card-full h-100">
          <img
            class="candidate-photo"
            loading="lazy"
            width="300"
            height="260"
            src="${this.escapeHtml(photoUrl)}"
            alt="${this.escapeHtml(candidate.name)}"
          >
          <div class="candidate-body d-flex flex-column">
            <span class="panel-kicker">${this.escapeHtml(candidate.council)}</span>
            <span class="candidate-position">${this.escapeHtml(candidate.position)}</span>
            <h2 class="candidate-name"><img class="council-heart" src="/static/images/${this.getHeartImage(candidate.council)}" alt=""> ${this.escapeHtml(candidate.name)}</h2>
            <a class="btn btn-campaign mt-auto" href="/candidate/${this.escapeHtml(candidate.id)}">View Profile</a>
          </div>
        </article>
      </div>
    `;
  },

  /**
   * Render multiple candidate cards
   * @param {Array} candidates - Array of candidate data
   * @returns {string} HTML string
   */
  candidateCards(candidates) {
    if (!candidates || candidates.length === 0) {
      return `
        <div class="col-12">
          <div class="text-center mt-5 reveal-up">
            <p class="candidate-plan mb-0">No candidates match your current search/filter.</p>
          </div>
        </div>
      `;
    }
    return candidates.map((c, i) => this.candidateCard(c, i)).join('');
  },

  /**
   * Render a council card for the home page
   * @param {Object} council - Council data
   * @param {number} index - Index for animation delay
   * @returns {string} HTML string
   */
  councilCard(council, index = 0) {
    const delay = Math.min(index + 1, 6);
    return `
      <div class="col-md-6 col-lg-4 reveal-up delay-${delay}">
        <a class="council-card h-100 d-block text-decoration-none" href="/council/${this.escapeHtml(council.slug)}">
          <h3 class="council-name">${this.escapeHtml(council.short_name)}</h3>
          <p class="council-description">${this.escapeHtml(council.description)}</p>
          <span class="council-count">${council.count} candidate${council.count !== 1 ? 's' : ''}</span>
        </a>
      </div>
    `;
  },

  /**
   * Render council cards grid
   * @param {Array} councils - Array of council data
   * @returns {string} HTML string
   */
  councilCards(councils) {
    return councils.map((c, i) => this.councilCard(c, i)).join('');
  },

  /**
   * Render spotlight candidate card
   * @param {Object} candidate - Candidate data
   * @param {number} index - Index for animation delay
   * @returns {string} HTML string
   */
  spotlightCard(candidate, index = 0) {
    const delay = Math.min(index + 1, 6);
    const photoUrl = `/static/${candidate.photo || 'images/default-candidate.svg'}`;
    
    return `
      <div class="col-md-6 col-lg-3 reveal-up delay-${delay}">
        <article class="candidate-card h-100">
          <img
            class="candidate-photo"
            loading="lazy"
            width="260"
            height="260"
            src="${this.escapeHtml(photoUrl)}"
            alt="${this.escapeHtml(candidate.name)}"
          >
          <div class="candidate-body">
            <span class="panel-kicker">${this.escapeHtml(candidate.council)}</span>
            <span class="candidate-position">${this.escapeHtml(candidate.position)}</span>
            <h3 class="candidate-name"><img class="council-heart" src="/static/images/${this.getHeartImage(candidate.council)}" alt=""> ${this.escapeHtml(candidate.name)}</h3>
            <a class="btn btn-campaign-outline btn-sm mt-2" href="/candidate/${this.escapeHtml(candidate.id)}">View Profile</a>
          </div>
        </article>
      </div>
    `;
  },

  /**
   * Render platform section card
   * @param {Object} section - Platform section data
   * @param {number} index - Index for animation delay
   * @returns {string} HTML string
   */
  platformSection(section, index = 0) {
    const delay = Math.min(index + 1, 6);
    return `
      <div class="col-md-6 col-lg-4 reveal-up delay-${delay}">
        <div class="platform-card h-100">
          <i class="bi ${this.escapeHtml(section.icon)} platform-icon"></i>
          <h3 class="platform-title">${this.escapeHtml(section.title)}</h3>
          <p class="platform-description">${this.escapeHtml(section.description)}</p>
        </div>
      </div>
    `;
  },

  /**
   * Render gallery item
   * @param {Object} item - Gallery item data
   * @param {number} index - Index for animation delay
   * @returns {string} HTML string
   */
  galleryItem(item, index = 0) {
    const delay = Math.min(index + 1, 8);
    const imageUrl = `/static/${item.file}`;
    
    return `
      <div class="col-md-6 col-lg-4 reveal-up delay-${delay}">
        <figure class="gallery-item">
          <img
            class="gallery-image"
            loading="lazy"
            src="${this.escapeHtml(imageUrl)}"
            alt="${this.escapeHtml(item.caption)}"
          >
          <figcaption class="gallery-caption">${this.escapeHtml(item.caption)}</figcaption>
        </figure>
      </div>
    `;
  },

  /**
   * Render credentials with proper hierarchy
   * @param {string} credentials - Raw credentials string
   * @returns {string} HTML string
   */
  credentials(credentials) {
    if (!credentials) return '<p class="text-muted">No credentials listed.</p>';
    
    const lines = credentials.split('\n');
    let html = '';
    
    const headerKeywords = [
      'ACADEMIC EXCELLENCE', 'EXTRA CURRICULARS', 'INTERNATIONAL LEVEL',
      'NATIONAL LEVEL', 'REGIONAL LEVEL', 'CITY-WIDE LEVEL', 'SCHOOL LEVEL'
    ];
    
    for (const rawLine of lines) {
      const line = rawLine.trim();
      if (!line) continue;
      
      const isHeader = headerKeywords.some(keyword => line.includes(keyword));
      
      if (isHeader) {
        let icon = 'bi-star-fill';
        if (line.includes('ACADEMIC')) icon = 'bi-mortarboard-fill';
        else if (line.includes('INTERNATIONAL')) icon = 'bi-globe';
        
        html += `
          <div class="credentials-header mt-3">
            <i class="bi ${icon}"></i>
            ${this.escapeHtml(line)}
          </div>
        `;
      } else {
        html += `<p class="credentials-item">${this.escapeHtml(line)}</p>`;
      }
    }
    
    return html;
  },

  /**
   * Render GPOA highlights
   * @param {Array} gpoa - GPOA array
   * @returns {string} HTML string
   */
  gpoaHighlights(gpoa) {
    if (!gpoa || gpoa.length === 0) return '';
    
    return gpoa.map((item, index) => `
      <div class="col-md-6 col-lg-4 reveal-up delay-${Math.min(index + 1, 6)}">
        <div class="gpoa-card h-100">
          <i class="bi ${this.escapeHtml(item.icon)} gpoa-icon"></i>
          <h4 class="gpoa-title">${this.escapeHtml(item.title)}</h4>
          <p class="gpoa-description">${this.escapeHtml(item.description)}</p>
        </div>
      </div>
    `).join('');
  },

  /**
   * Render loading spinner
   * @returns {string} HTML string
   */
  loading() {
    return `
      <div class="col-12 text-center py-5">
        <div class="spinner-border text-warning" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    `;
  },

  /**
   * Render error message
   * @param {string} message - Error message
   * @returns {string} HTML string
   */
  error(message = 'An error occurred. Please try again.') {
    return `
      <div class="col-12 text-center py-5">
        <div class="alert alert-warning" role="alert">
          <i class="bi bi-exclamation-triangle me-2"></i>
          ${this.escapeHtml(message)}
        </div>
      </div>
    `;
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Components;
}
