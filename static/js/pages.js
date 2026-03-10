/**
 * Tugon Page Controllers
 * Page-specific initialization and event handling
 */

const Pages = {
  /**
   * Initialize page based on current route
   */
  init() {
    const path = window.location.pathname;
    
    // Re-observe reveal animations after dynamic content loads
    this.initRevealAnimations();
    
    // Route-based initialization
    if (path === '/candidates') {
      this.initCandidatesPage();
    } else if (path.startsWith('/candidate/')) {
      this.initCandidateProfilePage();
    } else if (path.startsWith('/council/')) {
      this.initCouncilPage();
    } else if (path === '/gallery') {
      this.initGalleryPage();
    } else if (path === '/') {
      this.initHomePage();
    }
  },

  /**
   * Initialize reveal animations for dynamically loaded content
   */
  initRevealAnimations() {
    const revealElements = document.querySelectorAll('.reveal-up:not(.is-visible)');
    
    if (!revealElements.length) return;
    
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.15,
        rootMargin: '0px 0px -40px 0px',
      }
    );

    revealElements.forEach((element) => observer.observe(element));
  },

  /**
   * Initialize candidates listing page
   */
  async initCandidatesPage() {
    const container = document.getElementById('candidates-container');
    const searchInput = document.getElementById('candidateSearch');
    const councilSelect = document.getElementById('councilFilter');
    const form = document.querySelector('.candidate-filter-form');
    
    if (!container) return;

    // Prevent form submission, use JS instead
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        this.loadCandidates();
      });
    }

    // Live search with debounce
    let searchTimeout;
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => this.loadCandidates(), 300);
      });
    }

    // Council filter change
    if (councilSelect) {
      councilSelect.addEventListener('change', () => this.loadCandidates());
    }

    // Initial load
    await this.loadCandidates();

  },

  /**
   * Load and render candidates
   */
  async loadCandidates() {
    const container = document.getElementById('candidates-container');
    const searchInput = document.getElementById('candidateSearch');
    const councilSelect = document.getElementById('councilFilter');
    
    if (!container) return;

    const query = searchInput ? searchInput.value.trim() : '';
    const council = councilSelect ? councilSelect.value : 'ALL';

    // Show loading state
    container.innerHTML = Components.loading();

    try {
      const data = await API.getCandidates(query, council);
      container.innerHTML = Components.candidateCards(data.candidates);
      
      // Update URL without reload
      const url = new URL(window.location);
      if (query) url.searchParams.set('q', query);
      else url.searchParams.delete('q');
      if (council !== 'ALL') url.searchParams.set('council', council);
      else url.searchParams.delete('council');
      window.history.replaceState({}, '', url);
      
      // Re-init animations
      this.initRevealAnimations();
    } catch (error) {
      container.innerHTML = Components.error('Failed to load candidates. Please try again.');
    }
  },

  /**
   * Initialize candidate profile page
   */
  async initCandidateProfilePage() {
    const candidateId = window.location.pathname.split('/').pop();
    const credentialsContainer = document.getElementById('credentials-container');
    const gpoaContainer = document.getElementById('gpoa-container');
    
    if (!credentialsContainer) return;
    
    try {
      const data = await API.getCandidate(candidateId);
      
      if (data.candidate) {
        // Render credentials
        credentialsContainer.innerHTML = Components.credentials(data.candidate.credentials);
        
        // Render GPOA if container exists
        if (gpoaContainer && data.council && data.council.gpoa) {
          gpoaContainer.innerHTML = Components.gpoaHighlights(data.council.gpoa);
        }
        
        this.initRevealAnimations();
      }
    } catch (error) {
      credentialsContainer.innerHTML = Components.error('Failed to load candidate details.');
    }
  },

  /**
   * Initialize council page
   */
  async initCouncilPage() {
    const slug = window.location.pathname.split('/').pop();
    const candidatesContainer = document.getElementById('council-candidates-container');
    if (!candidatesContainer) return;
    candidatesContainer.innerHTML = Components.loading();
    try {
      const data = await API.getCouncil(slug);
      candidatesContainer.innerHTML = Components.candidateCards(data.candidates);
      this.initRevealAnimations();
    } catch (error) {
      candidatesContainer.innerHTML = Components.error('Failed to load council candidates.');
    }
  },

  /**
   * Initialize gallery page
   */
  async initGalleryPage() {
    const container = document.getElementById('gallery-container');
    
    if (!container) return;
    
    container.innerHTML = Components.loading();
    
    try {
      const data = await API.getGallery();
      container.innerHTML = data.items.map((item, i) => Components.galleryItem(item, i)).join('');
      this.initRevealAnimations();
    } catch (error) {
      container.innerHTML = Components.error('Failed to load gallery.');
    }
  },

  /**
   * Initialize home page
   */
  async initHomePage() {
    const spotlightContainer = document.getElementById('spotlight-container');
    const councilsContainer = document.getElementById('councils-container');
    const platformContainer = document.getElementById('platform-container');
    
    // These containers are optional - if static content is preferred, they won't exist
    if (!spotlightContainer && !councilsContainer && !platformContainer) return;
    
    try {
      const data = await API.getHomeData();
      
      if (spotlightContainer && data.spotlight_candidates) {
        spotlightContainer.innerHTML = data.spotlight_candidates
          .map((c, i) => Components.spotlightCard(c, i))
          .join('');
      }
      
      if (councilsContainer && data.council_cards) {
        councilsContainer.innerHTML = Components.councilCards(data.council_cards);
      }
      
      if (platformContainer && data.platform_sections) {
        platformContainer.innerHTML = data.platform_sections
          .map((s, i) => Components.platformSection(s, i))
          .join('');
      }
      
      this.initRevealAnimations();
    } catch (error) {
      console.error('Failed to load home page data:', error);
    }
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Pages;
}
