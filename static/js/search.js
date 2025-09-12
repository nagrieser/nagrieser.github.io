class LocalSearch {
    constructor() {
        this.searchIndex = null;
        this.isSearchReady = false;
        this.searchInput = null;
        this.searchResults = null;
        this.currentResults = [];
        this.currentResultIndex = -1;
        
        this.initSearch();
    }

    async initSearch() {
        try {
            // Load the search index script
            const script = document.createElement('script');
            script.src = '/search_index.en.js';
            
            script.onload = () => {
                if (window.searchIndex) {
                    this.searchIndex = window.searchIndex.documentStore.docs;
                    this.isSearchReady = true;
                    console.log('Search index loaded successfully');
                } else {
                    console.error('Search index not found in loaded script');
                }
            };
            
            script.onerror = () => {
                console.error('Failed to load search index script');
            };
            
            document.head.appendChild(script);
        } catch (error) {
            console.error('Failed to load search index:', error);
        }
    }

    setupSearchUI() {
        this.searchInput = document.getElementById('search-input');
        this.searchResults = document.getElementById('search-results');
        
        if (!this.searchInput || !this.searchResults) {
            console.error('Search UI elements not found');
            return;
        }

        // Setup event listeners
        this.searchInput.addEventListener('input', this.debounce(this.handleSearch.bind(this), 300));
        this.searchInput.addEventListener('keydown', this.handleKeydown.bind(this));
        
        // Close search results when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-container')) {
                this.hideResults();
            }
        });

        // Show/hide search based on input focus
        this.searchInput.addEventListener('focus', () => {
            if (this.currentResults.length > 0) {
                this.showResults();
            }
        });
    }

    handleSearch(event) {
        const query = event.target.value.trim().toLowerCase();
        
        if (query.length < 2) {
            this.hideResults();
            return;
        }

        if (!this.isSearchReady) {
            console.warn('Search index not ready yet');
            return;
        }

        this.performSearch(query);
    }

    performSearch(query) {
        const results = [];
        const searchTerms = query.split(/\s+/).filter(term => term.length > 1);
        
        for (const [url, doc] of Object.entries(this.searchIndex)) {
            let score = 0;
            const titleLower = (doc.title || '').toLowerCase();
            const bodyLower = (doc.body || '').toLowerCase();
            
            // Title matches are weighted higher
            for (const term of searchTerms) {
                if (titleLower.includes(term)) {
                    score += titleLower.indexOf(term) === 0 ? 10 : 5; // Higher score for starting matches
                }
                if (bodyLower.includes(term)) {
                    score += 1;
                }
            }
            
            if (score > 0) {
                results.push({
                    title: doc.title || 'Untitled',
                    body: doc.body || '',
                    permalink: url,
                    score: score,
                    excerpt: this.getExcerpt(doc.body || '', searchTerms)
                });
            }
        }

        // Sort by score (descending) and limit results
        this.currentResults = results
            .sort((a, b) => b.score - a.score)
            .slice(0, 8);
        
        this.displayResults();
    }

    getExcerpt(text, searchTerms) {
        const maxLength = 150;
        let bestMatch = { index: -1, term: '' };
        
        // Find the first occurrence of any search term
        for (const term of searchTerms) {
            const index = text.toLowerCase().indexOf(term.toLowerCase());
            if (index !== -1 && (bestMatch.index === -1 || index < bestMatch.index)) {
                bestMatch = { index, term };
            }
        }
        
        if (bestMatch.index === -1) {
            return text.substring(0, maxLength) + (text.length > maxLength ? '...' : '');
        }
        
        // Extract excerpt around the match
        const start = Math.max(0, bestMatch.index - 50);
        const end = Math.min(text.length, bestMatch.index + maxLength - 50);
        let excerpt = text.substring(start, end);
        
        // Add ellipsis if truncated
        if (start > 0) excerpt = '...' + excerpt;
        if (end < text.length) excerpt = excerpt + '...';
        
        // Highlight search terms
        for (const term of searchTerms) {
            const regex = new RegExp(`(${this.escapeRegex(term)})`, 'gi');
            excerpt = excerpt.replace(regex, '<mark>$1</mark>');
        }
        
        return excerpt;
    }

    escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    displayResults() {
        if (this.currentResults.length === 0) {
            this.searchResults.innerHTML = '<div class="search-no-results">No results found</div>';
        } else {
            const resultsHTML = this.currentResults.map((result, index) => `
                <div class="search-result-item ${index === this.currentResultIndex ? 'highlighted' : ''}" 
                     data-index="${index}">
                    <a href="${result.permalink}" class="search-result-link">
                        <div class="search-result-title">${this.highlightSearchTerms(result.title)}</div>
                        <div class="search-result-excerpt">${result.excerpt}</div>
                        <div class="search-result-url">${result.permalink}</div>
                    </a>
                </div>
            `).join('');
            
            this.searchResults.innerHTML = resultsHTML;
            
            // Add click handlers to results
            this.searchResults.querySelectorAll('.search-result-item').forEach((item, index) => {
                item.addEventListener('click', () => {
                    const result = this.currentResults[index];
                    window.location.href = result.permalink;
                });
            });
        }
        
        this.showResults();
    }

    highlightSearchTerms(text) {
        if (!this.searchInput) return text;
        
        const query = this.searchInput.value.trim();
        const searchTerms = query.split(/\s+/).filter(term => term.length > 1);
        
        let highlightedText = text;
        for (const term of searchTerms) {
            const regex = new RegExp(`(${this.escapeRegex(term)})`, 'gi');
            highlightedText = highlightedText.replace(regex, '<mark>$1</mark>');
        }
        
        return highlightedText;
    }

    handleKeydown(event) {
        if (!this.currentResults.length) return;
        
        switch (event.key) {
            case 'ArrowDown':
                event.preventDefault();
                this.currentResultIndex = Math.min(this.currentResultIndex + 1, this.currentResults.length - 1);
                this.updateHighlight();
                break;
            case 'ArrowUp':
                event.preventDefault();
                this.currentResultIndex = Math.max(this.currentResultIndex - 1, -1);
                this.updateHighlight();
                break;
            case 'Enter':
                event.preventDefault();
                if (this.currentResultIndex >= 0) {
                    const result = this.currentResults[this.currentResultIndex];
                    window.location.href = result.permalink;
                }
                break;
            case 'Escape':
                this.hideResults();
                this.searchInput.blur();
                break;
        }
    }

    updateHighlight() {
        const items = this.searchResults.querySelectorAll('.search-result-item');
        items.forEach((item, index) => {
            if (index === this.currentResultIndex) {
                item.classList.add('highlighted');
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.classList.remove('highlighted');
            }
        });
    }

    showResults() {
        if (this.searchResults) {
            this.searchResults.style.display = 'block';
        }
    }

    hideResults() {
        if (this.searchResults) {
            this.searchResults.style.display = 'none';
            this.currentResultIndex = -1;
        }
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize search when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.localSearch = new LocalSearch();
    // Setup UI after a short delay to ensure DOM is fully ready
    setTimeout(() => {
        window.localSearch.setupSearchUI();
    }, 100);
});
