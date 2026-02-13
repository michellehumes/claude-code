// ========================================
// ToolShed Tested - Main JavaScript
// ========================================

// Sample data for reviews and tools
const toolsData = [
    {
        id: 1,
        name: "DeWalt DCD771C2 Drill/Driver",
        category: "drills",
        brand: "dewalt",
        rating: 4.5,
        price: 129.99,
        image: "https://via.placeholder.com/400x300/ff6b00/ffffff?text=DeWalt+Drill",
        excerpt: "Powerful 20V MAX drill with 300 UWO for heavy-duty tasks. Excellent battery life and comfortable grip.",
        specs: {
            voltage: "20V MAX",
            torque: "300 UWO",
            speed: "0-450/1,500 RPM",
            weight: "3.6 lbs"
        }
    },
    {
        id: 2,
        name: "Milwaukee M18 FUEL Circular Saw",
        category: "saws",
        brand: "milwaukee",
        rating: 4.8,
        price: 199.99,
        image: "https://via.placeholder.com/400x300/ff6b00/ffffff?text=Milwaukee+Saw",
        excerpt: "Best-in-class cutting performance with POWERSTATE brushless motor. Cuts through materials like butter.",
        specs: {
            voltage: "18V",
            blade: "7-1/4 inch",
            speed: "5,800 RPM",
            weight: "9.1 lbs"
        }
    },
    {
        id: 3,
        name: "Makita XAG04Z Angle Grinder",
        category: "grinders",
        brand: "makita",
        rating: 4.6,
        price: 149.99,
        image: "https://via.placeholder.com/400x300/ff6b00/ffffff?text=Makita+Grinder",
        excerpt: "Brushless motor delivers 8,500 RPM for maximum performance. Automatic speed change technology optimizes performance.",
        specs: {
            voltage: "18V",
            disc: "4-1/2 inch",
            speed: "8,500 RPM",
            weight: "5.1 lbs"
        }
    },
    {
        id: 4,
        name: "Bosch ROS20VSC Random Orbit Sander",
        category: "sanders",
        brand: "bosch",
        rating: 4.7,
        price: 79.99,
        image: "https://via.placeholder.com/400x300/ff6b00/ffffff?text=Bosch+Sander",
        excerpt: "Variable speed control with microfilter dust canister. Produces smooth, swirl-free finishes.",
        specs: {
            voltage: "Corded",
            pad: "5 inch",
            speed: "7,500-12,000 OPM",
            weight: "4.4 lbs"
        }
    },
    {
        id: 5,
        name: "Ryobi P251 Impact Driver",
        category: "drills",
        brand: "ryobi",
        rating: 4.3,
        price: 89.99,
        image: "https://via.placeholder.com/400x300/ff6b00/ffffff?text=Ryobi+Impact",
        excerpt: "Budget-friendly option with impressive 1,600 in-lbs of torque. Great for DIY enthusiasts.",
        specs: {
            voltage: "18V ONE+",
            torque: "1,600 in-lbs",
            speed: "0-3,100 RPM",
            weight: "3.2 lbs"
        }
    },
    {
        id: 6,
        name: "DeWalt DWE7491RS Table Saw",
        category: "saws",
        brand: "dewalt",
        rating: 4.9,
        price: 599.99,
        image: "https://via.placeholder.com/400x300/ff6b00/ffffff?text=DeWalt+Table+Saw",
        excerpt: "Professional-grade table saw with 32-1/2 inch rip capacity. Rolling stand for easy mobility.",
        specs: {
            voltage: "Corded 15A",
            blade: "10 inch",
            speed: "4,800 RPM",
            weight: "110 lbs"
        }
    },
    {
        id: 7,
        name: "Milwaukee M12 Die Grinder",
        category: "grinders",
        brand: "milwaukee",
        rating: 4.4,
        price: 119.99,
        image: "https://via.placeholder.com/400x300/ff6b00/ffffff?text=Milwaukee+Die+Grinder",
        excerpt: "Compact and lightweight design perfect for tight spaces. Variable speed dial for maximum control.",
        specs: {
            voltage: "12V",
            collet: "1/4 inch",
            speed: "5,000-25,000 RPM",
            weight: "2.3 lbs"
        }
    },
    {
        id: 8,
        name: "Makita BO5041K Belt Sander",
        category: "sanders",
        brand: "makita",
        rating: 4.5,
        price: 159.99,
        image: "https://via.placeholder.com/400x300/ff6b00/ffffff?text=Makita+Belt+Sander",
        excerpt: "Powerful 7.8 amp motor with variable speed control. Large trigger switch for comfortable operation.",
        specs: {
            voltage: "Corded",
            belt: "3x21 inch",
            speed: "690-1,440 ft/min",
            weight: "8.6 lbs"
        }
    }
];

// ========================================
// Theme Management
// ========================================
class ThemeManager {
    constructor() {
        this.themeToggle = document.querySelector('.theme-toggle');
        this.currentTheme = localStorage.getItem('theme') || 'dark';
        this.init();
    }

    init() {
        this.setTheme(this.currentTheme);
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.currentTheme = theme;
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
}

// ========================================
// Mobile Menu
// ========================================
class MobileMenu {
    constructor() {
        this.toggle = document.querySelector('.mobile-menu-toggle');
        this.menu = document.querySelector('.nav-menu');
        this.init();
    }

    init() {
        if (!this.toggle || !this.menu) return;

        this.toggle.addEventListener('click', () => this.toggleMenu());

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.toggle.contains(e.target) && !this.menu.contains(e.target)) {
                this.closeMenu();
            }
        });

        // Close menu when clicking a link
        const menuLinks = this.menu.querySelectorAll('a');
        menuLinks.forEach(link => {
            link.addEventListener('click', () => this.closeMenu());
        });
    }

    toggleMenu() {
        const isExpanded = this.toggle.getAttribute('aria-expanded') === 'true';
        this.toggle.setAttribute('aria-expanded', !isExpanded);
        this.menu.classList.toggle('active');
    }

    closeMenu() {
        this.toggle.setAttribute('aria-expanded', 'false');
        this.menu.classList.remove('active');
    }
}

// ========================================
// Search Functionality
// ========================================
class SearchManager {
    constructor(data) {
        this.data = data;
        this.searchInput = document.getElementById('site-search');
        this.searchResults = document.getElementById('search-results');
        this.searchButton = document.querySelector('.search-button');
        this.debounceTimer = null;
        this.init();
    }

    init() {
        if (!this.searchInput) return;

        this.searchInput.addEventListener('input', (e) => {
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(() => this.performSearch(e.target.value), 300);
        });

        this.searchButton.addEventListener('click', () => {
            this.performSearch(this.searchInput.value);
        });

        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch(this.searchInput.value);
            }
        });

        // Close search results when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.searchInput.contains(e.target) && !this.searchResults.contains(e.target)) {
                this.hideResults();
            }
        });
    }

    performSearch(query) {
        if (!query || query.length < 2) {
            this.hideResults();
            return;
        }

        const results = this.data.filter(tool => {
            const searchText = query.toLowerCase();
            return (
                tool.name.toLowerCase().includes(searchText) ||
                tool.category.toLowerCase().includes(searchText) ||
                tool.brand.toLowerCase().includes(searchText) ||
                tool.excerpt.toLowerCase().includes(searchText)
            );
        });

        this.displayResults(results, query);
    }

    displayResults(results, query) {
        if (results.length === 0) {
            this.searchResults.innerHTML = `
                <div class="search-result-item">
                    <p style="text-align: center; color: var(--text-tertiary);">
                        No results found for "${query}"
                    </p>
                </div>
            `;
            this.searchResults.classList.add('active');
            return;
        }

        this.searchResults.innerHTML = results.map(tool => `
            <div class="search-result-item" role="option" tabindex="0">
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <img src="${tool.image}" alt="${tool.name}"
                         style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px;">
                    <div>
                        <strong>${tool.name}</strong>
                        <div style="display: flex; gap: 1rem; margin-top: 0.25rem; font-size: 0.875rem; color: var(--text-secondary);">
                            <span>${tool.category}</span>
                            <span>★ ${tool.rating}</span>
                            <span>$${tool.price}</span>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        this.searchResults.classList.add('active');

        // Add click handlers to results
        this.searchResults.querySelectorAll('.search-result-item').forEach((item, index) => {
            item.addEventListener('click', () => {
                this.selectResult(results[index]);
            });
        });
    }

    selectResult(tool) {
        // Scroll to the tool or open detail view
        console.log('Selected tool:', tool);
        this.hideResults();
        this.searchInput.value = '';
        // In a real application, this would navigate to the tool detail page
        alert(`You selected: ${tool.name}\nRating: ${tool.rating} stars\nPrice: $${tool.price}`);
    }

    hideResults() {
        this.searchResults.classList.remove('active');
    }
}

// ========================================
// Reviews Manager
// ========================================
class ReviewsManager {
    constructor(data) {
        this.data = data;
        this.reviewsGrid = document.getElementById('reviews-grid');
        this.loadMoreBtn = document.getElementById('load-more');
        this.displayedCount = 4;
        this.filteredData = [...data];
        this.init();
    }

    init() {
        if (!this.reviewsGrid) return;

        this.renderReviews();

        if (this.loadMoreBtn) {
            this.loadMoreBtn.addEventListener('click', () => this.loadMore());
        }

        // Set up filters
        this.setupFilters();
    }

    setupFilters() {
        const categoryFilter = document.getElementById('category-filter');
        const sortFilter = document.getElementById('sort-filter');
        const brandFilter = document.getElementById('brand-filter');

        [categoryFilter, sortFilter, brandFilter].forEach(filter => {
            if (filter) {
                filter.addEventListener('change', () => this.applyFilters());
            }
        });
    }

    applyFilters() {
        const category = document.getElementById('category-filter')?.value || 'all';
        const sort = document.getElementById('sort-filter')?.value || 'rating';
        const brand = document.getElementById('brand-filter')?.value || 'all';

        // Filter data
        this.filteredData = this.data.filter(tool => {
            const categoryMatch = category === 'all' || tool.category === category;
            const brandMatch = brand === 'all' || tool.brand === brand;
            return categoryMatch && brandMatch;
        });

        // Sort data
        switch (sort) {
            case 'rating':
                this.filteredData.sort((a, b) => b.rating - a.rating);
                break;
            case 'recent':
                // In real app, would sort by date
                this.filteredData.reverse();
                break;
            case 'popular':
                this.filteredData.sort((a, b) => b.rating - a.rating);
                break;
            case 'price-low':
                this.filteredData.sort((a, b) => a.price - b.price);
                break;
            case 'price-high':
                this.filteredData.sort((a, b) => b.price - a.price);
                break;
        }

        this.displayedCount = 4;
        this.renderReviews();
    }

    renderReviews() {
        const reviewsToShow = this.filteredData.slice(0, this.displayedCount);

        this.reviewsGrid.innerHTML = reviewsToShow.map(tool => `
            <article class="review-card" data-category="${tool.category}">
                <img src="${tool.image}" alt="${tool.name}" class="review-image" loading="lazy">
                <div class="review-content">
                    <span class="review-category">${tool.category}</span>
                    <h3 class="review-title">${tool.name}</h3>
                    <div class="review-rating">
                        <span class="stars">${this.generateStars(tool.rating)}</span>
                        <span class="rating-number">${tool.rating}/5</span>
                    </div>
                    <p class="review-excerpt">${tool.excerpt}</p>
                    <div class="review-specs">
                        ${Object.entries(tool.specs).map(([key, val]) => `<span class="review-spec"><strong>${key}:</strong> ${val}</span>`).join('')}
                    </div>
                    <div class="review-meta">
                        <span class="review-price">$${tool.price}</span>
                        <a href="#" class="review-link">Read Review &rarr;</a>
                    </div>
                    <a href="#" class="btn-check-price" rel="sponsored nofollow" aria-label="Check price for ${tool.name}">Check Today's Price &rarr;</a>
                </div>
            </article>
        `).join('');

        // Update load more button
        if (this.loadMoreBtn) {
            if (this.displayedCount >= this.filteredData.length) {
                this.loadMoreBtn.style.display = 'none';
            } else {
                this.loadMoreBtn.style.display = 'block';
            }
        }
    }

    generateStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let stars = '★'.repeat(fullStars);
        if (hasHalfStar) stars += '☆';
        const emptyStars = 5 - Math.ceil(rating);
        stars += '☆'.repeat(emptyStars);
        return stars;
    }

    loadMore() {
        this.displayedCount += 4;
        this.renderReviews();
    }
}

// ========================================
// Tool Comparison
// ========================================
class ComparisonManager {
    constructor(data) {
        this.data = data;
        this.compareSelects = document.querySelectorAll('.compare-select');
        this.comparisonResults = document.getElementById('comparison-results');
        this.selectedTools = [null, null, null];
        this.init();
    }

    init() {
        if (!this.comparisonResults) return;

        // Populate select options
        this.populateSelects();

        // Add change listeners
        this.compareSelects.forEach((select, index) => {
            select.addEventListener('change', (e) => {
                this.handleSelection(index, e.target.value);
            });
        });
    }

    populateSelects() {
        const options = this.data.map(tool =>
            `<option value="${tool.id}">${tool.name} - $${tool.price}</option>`
        ).join('');

        this.compareSelects.forEach(select => {
            const currentValue = select.value;
            select.innerHTML = '<option value="">Select a tool...</option>' + options;
            select.value = currentValue;
        });
    }

    handleSelection(index, toolId) {
        if (toolId) {
            this.selectedTools[index] = this.data.find(t => t.id == toolId);
        } else {
            this.selectedTools[index] = null;
        }
        this.renderComparison();
    }

    renderComparison() {
        const validTools = this.selectedTools.filter(t => t !== null);

        if (validTools.length === 0) {
            this.comparisonResults.innerHTML = '<p class="comparison-placeholder">Select tools above to begin comparing</p>';
            return;
        }

        const html = `
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Specification</th>
                        ${validTools.map(tool => `<th>${tool.name}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Category</strong></td>
                        ${validTools.map(tool => `<td>${tool.category}</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Brand</strong></td>
                        ${validTools.map(tool => `<td>${tool.brand}</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Rating</strong></td>
                        ${validTools.map(tool => `<td>${this.generateStars(tool.rating)} ${tool.rating}/5</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Price</strong></td>
                        ${validTools.map(tool => `<td style="color: var(--accent-primary); font-weight: 700;">$${tool.price}</td>`).join('')}
                    </tr>
                    ${this.renderSpecs(validTools)}
                </tbody>
            </table>
        `;

        this.comparisonResults.innerHTML = html;
    }

    renderSpecs(tools) {
        // Get all unique spec keys
        const allSpecs = new Set();
        tools.forEach(tool => {
            Object.keys(tool.specs).forEach(key => allSpecs.add(key));
        });

        return Array.from(allSpecs).map(spec => `
            <tr>
                <td><strong>${this.formatSpecName(spec)}</strong></td>
                ${tools.map(tool => `<td>${tool.specs[spec] || 'N/A'}</td>`).join('')}
            </tr>
        `).join('');
    }

    formatSpecName(spec) {
        return spec.charAt(0).toUpperCase() + spec.slice(1);
    }

    generateStars(rating) {
        const fullStars = Math.floor(rating);
        return '★'.repeat(fullStars) + '☆'.repeat(5 - fullStars);
    }
}

// ========================================
// FAQ Accordion
// ========================================
class FAQManager {
    constructor() {
        this.faqItems = document.querySelectorAll('.faq-item');
        this.init();
    }

    init() {
        this.faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            question.addEventListener('click', () => this.toggleFAQ(item));
        });
    }

    toggleFAQ(item) {
        const isActive = item.classList.contains('active');

        // Close all FAQs
        this.faqItems.forEach(faq => {
            faq.classList.remove('active');
            faq.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
        });

        // Open clicked FAQ if it wasn't active
        if (!isActive) {
            item.classList.add('active');
            item.querySelector('.faq-question').setAttribute('aria-expanded', 'true');
        }
    }
}

// ========================================
// Newsletter Forms
// ========================================
class NewsletterManager {
    constructor() {
        this.forms = document.querySelectorAll('[id*="newsletter-form"], .footer-newsletter-form, .sticky-newsletter-form');
        this.init();
    }

    init() {
        this.forms.forEach(form => {
            form.addEventListener('submit', (e) => this.handleSubmit(e));
        });
    }

    handleSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const email = form.querySelector('input[type="email"]').value;

        if (this.validateEmail(email)) {
            // In real application, send to server
            console.log('Newsletter signup:', email);
            alert('Thank you for subscribing! Check your email for confirmation.');
            form.reset();
        } else {
            alert('Please enter a valid email address.');
        }
    }

    validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
}

// ========================================
// Sticky Newsletter
// ========================================
class StickyNewsletter {
    constructor() {
        this.stickyBar = document.getElementById('sticky-newsletter');
        this.closeBtn = this.stickyBar?.querySelector('.sticky-newsletter-close');
        this.hasShown = localStorage.getItem('newsletter-shown') === 'true';
        this.init();
    }

    init() {
        if (!this.stickyBar) return;

        // Show after scrolling 50% of page
        window.addEventListener('scroll', () => this.handleScroll());

        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }
    }

    handleScroll() {
        if (this.hasShown) return;

        const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;

        if (scrollPercent > 50) {
            this.show();
        }
    }

    show() {
        this.stickyBar.classList.add('visible');
        this.hasShown = true;
        localStorage.setItem('newsletter-shown', 'true');
    }

    close() {
        this.stickyBar.classList.remove('visible');
    }
}

// ========================================
// Contact Form
// ========================================
class ContactForm {
    constructor() {
        this.form = document.getElementById('contact-form');
        this.init();
    }

    init() {
        if (!this.form) return;

        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    handleSubmit(e) {
        e.preventDefault();

        const formData = {
            name: this.form.querySelector('#contact-name').value,
            email: this.form.querySelector('#contact-email').value,
            subject: this.form.querySelector('#contact-subject').value,
            message: this.form.querySelector('#contact-message').value
        };

        // Validate
        if (!this.validateForm(formData)) {
            return;
        }

        // In real application, send to server
        console.log('Contact form submission:', formData);

        // Show loading state
        const submitBtn = this.form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;

        // Simulate API call
        setTimeout(() => {
            alert('Thank you for your message! We\'ll get back to you within 48 hours.');
            this.form.reset();
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 1000);
    }

    validateForm(data) {
        if (!data.name || !data.email || !data.subject || !data.message) {
            alert('Please fill in all fields.');
            return false;
        }

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
            alert('Please enter a valid email address.');
            return false;
        }

        return true;
    }
}

// ========================================
// Smooth Scrolling for Anchor Links
// ========================================
class SmoothScroll {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                const href = anchor.getAttribute('href');
                if (href === '#' || href === '') return;

                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    const offsetTop = target.offsetTop - 100; // Account for fixed header
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
}

// ========================================
// Lazy Loading Images
// ========================================
class LazyLoader {
    constructor() {
        this.init();
    }

    init() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }
}

// ========================================
// Breadcrumb Manager
// ========================================
class BreadcrumbManager {
    constructor() {
        this.breadcrumbs = document.querySelector('.breadcrumbs ol');
        this.init();
    }

    init() {
        // Listen for filter changes to update breadcrumbs
        const categoryFilter = document.getElementById('category-filter');
        if (categoryFilter) {
            categoryFilter.addEventListener('change', (e) => {
                this.updateBreadcrumbs(e.target.value);
            });
        }
    }

    updateBreadcrumbs(category) {
        if (!this.breadcrumbs) return;

        if (category === 'all') {
            this.breadcrumbs.innerHTML = '<li><a href="/">Home</a></li>';
        } else {
            this.breadcrumbs.innerHTML = `
                <li><a href="/">Home</a></li>
                <li><a href="#categories">Categories</a></li>
                <li>${category}</li>
            `;
        }
    }
}

// ========================================
// Initialize Everything
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all managers
    new ThemeManager();
    new MobileMenu();
    new SearchManager(toolsData);
    new ReviewsManager(toolsData);
    new ComparisonManager(toolsData);
    new FAQManager();
    new NewsletterManager();
    new StickyNewsletter();
    new ContactForm();
    new SmoothScroll();
    new LazyLoader();
    new BreadcrumbManager();

    console.log('ToolShed Tested initialized successfully!');
});

// ========================================
// Performance Monitoring
// ========================================
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page Load Time:', perfData.loadEventEnd - perfData.fetchStart, 'ms');
        }, 0);
    });
}

// ========================================
// Service Worker Registration (for PWA)
// ========================================
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment to enable service worker
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered:', registration))
        //     .catch(error => console.log('SW registration failed:', error));
    });
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ThemeManager,
        SearchManager,
        ReviewsManager,
        ComparisonManager,
        toolsData
    };
}
