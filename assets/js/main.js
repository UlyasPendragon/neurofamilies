/* NeuroFamilies.org — Main JavaScript */

document.addEventListener('DOMContentLoaded', function() {
  
  // Mobile menu toggle
  const menuToggle = document.querySelector('.mobile-menu-toggle');
  const mainNav = document.querySelector('.main-nav');
  
  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', function() {
      const isOpen = mainNav.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', isOpen);
    });
    
    // Close menu on Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && mainNav.classList.contains('open')) {
        mainNav.classList.remove('open');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.focus();
      }
    });
  }
  
  // Smooth scroll for anchor links (respects prefers-reduced-motion)
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
      anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          target.focus();
        }
      });
    });
  }
  
  // Print-friendly: expand all collapsed sections
  window.addEventListener('beforeprint', function() {
    document.querySelectorAll('[aria-expanded="false"]').forEach(function(el) {
      el.setAttribute('aria-expanded', 'true');
    });
  });
  
});
