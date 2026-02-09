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

    // Close menu when clicking a link
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

      // Close all other FAQ items
      document.querySelectorAll('.faq-item').forEach(faq => {
        faq.classList.remove('open');
      });

      // Toggle current item
      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // --- Active category highlight ---
  const categoryLinks = document.querySelectorAll('.category-bar a');
  const currentPage = window.location.pathname;

  categoryLinks.forEach(link => {
    if (link.getAttribute('href') === currentPage ||
        currentPage.includes(link.dataset.category)) {
      link.classList.add('active');
    }
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
        // Replace with actual newsletter service integration
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

});
