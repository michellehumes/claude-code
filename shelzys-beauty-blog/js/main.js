/* ============================================
   Shelzy's Beauty Blog - Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // --- Mobile Navigation Toggle ---
  const navToggle = document.querySelector('.nav-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navMenu.classList.toggle('open');
      navToggle.setAttribute('aria-expanded',
        navMenu.classList.contains('open'));
    });

    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // --- FAQ Accordion ---
  document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
      const item = question.parentElement;
      const isOpen = item.classList.contains('open');

      document.querySelectorAll('.faq-item').forEach(faq => {
        faq.classList.remove('open');
      });

      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const href = anchor.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // --- Affiliate link click tracking (analytics-ready) ---
  document.querySelectorAll('a[href*="amazon.com"]').forEach(link => {
    link.addEventListener('click', () => {
      if (typeof gtag === 'function') {
        gtag('event', 'affiliate_click', {
          event_category: 'affiliate',
          event_label: link.href,
          value: 1
        });
      }
    });
  });

  // --- Newsletter form handler ---
  const newsletterForm = document.querySelector('.newsletter-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = newsletterForm.querySelector('input[type="email"]').value;
      if (email) {
        alert('Thanks for subscribing! Check your inbox for beauty tips.');
        newsletterForm.reset();
      }
    });
  }

  // --- Lazy loading for images ---
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }
          imageObserver.unobserve(img);
        }
      });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
      imageObserver.observe(img);
    });
  }

  // ============================================
  //  NEW FEATURES
  // ============================================

  // --- Category Filtering (Homepage) ---
  const categoryBar = document.querySelector('.category-bar');
  const postsGrid = document.querySelector('.posts-grid');

  if (categoryBar && postsGrid) {
    const categoryLinks = categoryBar.querySelectorAll('a');
    const allCards = postsGrid.querySelectorAll('.post-card');

    categoryLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const cat = link.dataset.category || 'all';

        categoryLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');

        let visibleCount = 0;
        allCards.forEach(card => {
          if (cat === 'all' || card.dataset.category === cat) {
            card.classList.remove('hidden');
            visibleCount++;
          } else {
            card.classList.add('hidden');
          }
        });

        // Reset load-more when filtering
        if (typeof resetLoadMore === 'function') resetLoadMore();

        // Update count
        const countEl = document.querySelector('.posts-count');
        if (countEl) {
          countEl.textContent = visibleCount + ' post' + (visibleCount !== 1 ? 's' : '');
        }
      });
    });
  }

  // --- Search (Homepage) ---
  const searchInput = document.querySelector('.search-bar input');
  const noResults = document.querySelector('.search-no-results');

  if (searchInput && postsGrid) {
    const allCards = postsGrid.querySelectorAll('.post-card');
    const featuredPost = document.querySelector('.featured-post');

    searchInput.addEventListener('input', () => {
      const q = searchInput.value.toLowerCase().trim();

      // Reset category filter to "All"
      if (categoryBar) {
        categoryBar.querySelectorAll('a').forEach(l => l.classList.remove('active'));
        const allBtn = categoryBar.querySelector('a:first-child') || categoryBar.querySelector('a');
        if (allBtn) allBtn.classList.add('active');
      }

      let visibleCount = 0;
      allCards.forEach(card => {
        const title = (card.querySelector('.post-card-title')?.textContent || '').toLowerCase();
        const excerpt = (card.querySelector('.post-card-excerpt')?.textContent || '').toLowerCase();
        const category = (card.querySelector('.post-card-category')?.textContent || '').toLowerCase();

        if (!q || title.includes(q) || excerpt.includes(q) || category.includes(q)) {
          card.classList.remove('hidden');
          visibleCount++;
        } else {
          card.classList.add('hidden');
        }
      });

      // Show/hide featured post during search
      if (featuredPost) {
        featuredPost.style.display = q ? 'none' : '';
      }

      // No results message
      if (noResults) {
        noResults.style.display = (q && visibleCount === 0) ? 'block' : 'none';
      }

      // Update count
      const countEl = document.querySelector('.posts-count');
      if (countEl) {
        countEl.textContent = visibleCount + ' post' + (visibleCount !== 1 ? 's' : '');
      }

      if (typeof resetLoadMore === 'function') resetLoadMore();
    });
  }

  // --- Load More Pagination ---
  const POSTS_PER_PAGE = 12;
  let currentlyShown = POSTS_PER_PAGE;
  const loadMoreBtn = document.querySelector('.load-more-btn');

  function resetLoadMore() {
    if (!postsGrid || !loadMoreBtn) return;
    currentlyShown = POSTS_PER_PAGE;
    applyLoadMore();
  }

  function applyLoadMore() {
    if (!postsGrid || !loadMoreBtn) return;
    const visibleCards = postsGrid.querySelectorAll('.post-card:not(.hidden)');
    let shown = 0;

    visibleCards.forEach((card, i) => {
      if (i < currentlyShown) {
        card.style.display = '';
        shown++;
      } else {
        card.style.display = 'none';
      }
    });

    if (currentlyShown >= visibleCards.length) {
      loadMoreBtn.style.display = 'none';
    } else {
      loadMoreBtn.style.display = '';
      loadMoreBtn.textContent = 'Show More (' + (visibleCards.length - currentlyShown) + ' remaining)';
    }

    const countEl = document.querySelector('.posts-count');
    if (countEl) {
      countEl.textContent = 'Showing ' + Math.min(currentlyShown, visibleCards.length) + ' of ' + visibleCards.length + ' posts';
    }
  }

  // Make resetLoadMore available globally for filter/search
  window.resetLoadMore = resetLoadMore;

  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', () => {
      currentlyShown += POSTS_PER_PAGE;
      applyLoadMore();
    });

    // Initial apply
    applyLoadMore();
  }

  // --- Reading Progress Bar (Post pages) ---
  const progressBar = document.querySelector('.reading-progress');
  if (progressBar) {
    window.addEventListener('scroll', () => {
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled = window.scrollY;
      const pct = docHeight > 0 ? (scrolled / docHeight) * 100 : 0;
      progressBar.style.width = Math.min(pct, 100) + '%';
    });
  }

  // --- Scroll to Top Button ---
  const scrollTopBtn = document.querySelector('.scroll-to-top');
  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 400) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    });

    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --- Floating CTA (Post pages) ---
  const floatingCta = document.querySelector('.floating-cta');
  if (floatingCta) {
    const firstProduct = document.querySelector('.product-card');
    if (firstProduct) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (!entry.isIntersecting && window.scrollY > 300) {
            floatingCta.classList.add('visible');
          } else {
            floatingCta.classList.remove('visible');
          }
        });
      }, { threshold: 0.1 });

      observer.observe(firstProduct);
    }

    // Also hide near footer
    const footer = document.querySelector('.site-footer');
    if (footer) {
      const footerObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            floatingCta.classList.remove('visible');
          }
        });
      });
      footerObserver.observe(footer);
    }
  }

  // --- Auto-generate Table of Contents (Post pages) ---
  const postContent = document.querySelector('.post-content');
  const tocContainer = document.querySelector('.toc');

  if (tocContainer && postContent) {
    const headings = postContent.querySelectorAll('h2');
    const tocList = tocContainer.querySelector('.toc-list');

    if (headings.length > 2 && tocList) {
      headings.forEach((h, i) => {
        const id = 'section-' + i;
        h.id = id;
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = '#' + id;
        a.textContent = h.textContent;
        a.addEventListener('click', (e) => {
          e.preventDefault();
          h.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
        li.appendChild(a);
        tocList.appendChild(li);
      });
    } else if (tocContainer) {
      tocContainer.style.display = 'none';
    }

    // TOC collapse toggle
    const tocTitle = tocContainer?.querySelector('.toc-title');
    if (tocTitle) {
      tocTitle.addEventListener('click', () => {
        tocContainer.classList.toggle('collapsed');
      });
    }

    // Highlight active TOC item on scroll
    if (headings.length > 2) {
      const tocLinks = tocList?.querySelectorAll('a') || [];
      window.addEventListener('scroll', () => {
        let currentId = '';
        headings.forEach(h => {
          if (h.getBoundingClientRect().top < 100) {
            currentId = h.id;
          }
        });
        tocLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === '#' + currentId);
        });
      });
    }
  }

  // --- Share buttons (Post pages) ---
  document.querySelectorAll('.share-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const action = btn.dataset.share;
      const url = encodeURIComponent(window.location.href);
      const title = encodeURIComponent(document.title);

      let shareUrl = '';
      if (action === 'pinterest') {
        shareUrl = 'https://pinterest.com/pin/create/button/?url=' + url + '&description=' + title;
      } else if (action === 'facebook') {
        shareUrl = 'https://www.facebook.com/sharer/sharer.php?u=' + url;
      } else if (action === 'twitter') {
        shareUrl = 'https://twitter.com/intent/tweet?url=' + url + '&text=' + title;
      } else if (action === 'copy') {
        e.preventDefault();
        navigator.clipboard.writeText(window.location.href).then(() => {
          btn.textContent = '✓';
          setTimeout(() => { btn.textContent = 'Link'; }, 2000);
        });
        return;
      }

      if (shareUrl) {
        e.preventDefault();
        window.open(shareUrl, '_blank', 'width=600,height=400');
      }
    });
  });

});
