// Roadmap.js - JavaScript functionality for the roadmap site

document.addEventListener('DOMContentLoaded', function() {
    // Topic toggle functionality in modals
    const topicHeaders = document.querySelectorAll('.topic-header');
    topicHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            const isOpen = content.classList.contains('active');
            
            // Toggle active class
            if (isOpen) {
                content.classList.remove('active');
                header.querySelector('i').className = 'fas fa-chevron-down';
            } else {
                content.classList.add('active');
                header.querySelector('i').className = 'fas fa-chevron-up';
            }
        });
    });
    
    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (currentLocation === href || 
            (href !== '/' && currentLocation.startsWith(href))) {
            link.classList.add('active');
        }
    });
    
    // Initialize Bootstrap tooltips
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Smooth scroll to section when clicking on timeline nodes
    const scrollLinks = document.querySelectorAll('a.timeline-node');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const offset = 100; // Offset to account for fixed header
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - offset;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Animation for domain cards on scroll
    const animateOnScroll = () => {
        const cards = document.querySelectorAll('.domain-card');
        
        cards.forEach(card => {
            const cardTop = card.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (cardTop < windowHeight - 100) {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Set initial state for animation
    const cards = document.querySelectorAll('.domain-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    // Run animation on load and scroll
    window.addEventListener('load', animateOnScroll);
    window.addEventListener('scroll', animateOnScroll);
});